"""Independent strategy timing, return, covariance and output checks."""

import json

import numpy as np
import pandas as pd
import pytest

from rebal.demo import make_panel, make_signals
from rebal.exhibits.strategy import (
    FACTOR_MODELS,
    cumulative_gains,
    descriptive_table,
    factor_alphas,
    regime_means,
    run,
    strategy_data,
    weights,
)
from rebal.regress import TABLE_COLUMNS


@pytest.fixture(scope="module")
def inputs():
    panel = make_panel()
    return make_signals(panel), panel


@pytest.fixture(scope="module")
def frame(inputs):
    return strategy_data(*inputs, demo=True)


def test_planted_positive_sharpe_and_zero_effect(inputs, frame):
    _, panel = inputs
    planted = descriptive_table(frame).set_index("asset")
    zero = strategy_data(make_signals(panel, 0, 0), panel, demo=True)
    null = descriptive_table(zero).set_index("asset")
    assert planted.loc["strategy", "sharpe"] > 0
    assert abs(null.loc["strategy", "sharpe"]) < 0.3


def test_weight_support_and_previous_month_reference(inputs):
    signals, _ = inputs
    s = signals.copy()
    s["threshold"] = 0.0
    w = weights(s)
    dates = pd.DatetimeIndex(s.date)
    months = dates.to_period("M")
    first = np.r_[True, months[1:] != months[:-1]]
    outside = (s.week4.to_numpy() == 0) & ~first
    np.testing.assert_array_equal(w.weight.to_numpy()[outside], 0.0)
    # Independent scalar oracle: previous month's FIRST week4 day, not its last.
    for i in np.flatnonzero(first)[1:]:
        previous = s.loc[(months == months[i] - 1) & (s.week4 == 1), "calendar"]
        assert w.calendar_weight.iloc[i] == np.sign(previous.iloc[0])
    week4 = (s.week4.to_numpy() == 1) & ~first
    np.testing.assert_array_equal(
        w.weight.to_numpy()[week4], -np.sign(s.calendar.to_numpy()[week4]) / 2
    )


def test_alternative_reversal_and_no_future_dependency(inputs):
    signals, _ = inputs
    w = weights(signals, "lag4")
    dates = pd.DatetimeIndex(signals.date)
    first = np.flatnonzero(dates.to_period("M")[1:] != dates.to_period("M")[:-1]) + 1
    np.testing.assert_array_equal(
        w.calendar_weight.iloc[first], np.sign(signals.calendar.iloc[first - 4])
    )
    cut = 400
    for reversal in ("previous-week4", "lag4"):
        pd.testing.assert_frame_equal(
            weights(signals.iloc[:cut], reversal), weights(signals, reversal).iloc[:cut]
        )


def test_actual_panel_return_timing_and_demo_isolation(inputs, frame):
    signals, panel = inputs
    original = panel.copy(deep=True)
    real = strategy_data(signals, panel)
    dates = panel.set_index("date")
    sig = signals.set_index("date")
    for data, demo in ((real, False), (frame, True)):
        for row in data.iloc[[0, 1, 22, -1]].itertuples():
            spread = (
                sig.loc[row.Index, "ret"]
                if demo
                else (dates.loc[row.Index, "r_es"] - dates.loc[row.Index, "r_ty"])
            )
            assert row.strategy == pytest.approx(spread * row.weight)
            assert row.vix == dates.loc[row.signal_date, "vix"]
            assert row.mkt_rf == dates.loc[row.Index, "mkt_rf"]
    pd.testing.assert_frame_equal(panel, original)
    assert frame.index.max() == pd.Timestamp("2023-03-17")
    assert frame.signal_date.min() == pd.Timestamp("1997-09-10")


def test_missing_signal_never_skips_to_next_available_return(inputs):
    signals, panel = inputs
    missing = pd.Timestamp("2012-06-12")
    data = strategy_data(signals.loc[signals.date != missing], panel)
    assert missing in data.index  # the preceding day's signal still earns this return
    assert pd.Timestamp("2012-06-13") not in data.index
    row = data.loc["2012-06-14"]
    assert row.signal_date == pd.Timestamp("2012-06-13")
    assert np.isnan(row.strategy_net_costs)  # do not invent a free trade across a gap


@pytest.mark.parametrize("se", ["hc0", "hc1"])
def test_factor_alpha_matches_hand_ols_and_hc_covariance(frame, se):
    data = frame.copy()
    data.loc[data.index[100], "mom"] = np.nan
    actual = factor_alphas(data, se).set_index("column")
    for model, factors in FACTOR_MODELS.items():
        complete = data[["strategy", *factors]].dropna()
        x = np.column_stack([np.ones(len(complete)), complete[factors]])
        y = complete.strategy.to_numpy()
        beta = np.linalg.lstsq(x, y, rcond=None)[0]
        residual = y - x @ beta
        bread = np.linalg.inv(x.T @ x)
        meat = x.T @ (x * residual[:, None] ** 2)
        covariance = bread @ meat @ bread
        if se == "hc1":
            covariance *= len(x) / (len(x) - x.shape[1])
        row = actual.loc[model]
        assert row.coef == pytest.approx(beta[0] * 25200)
        assert row.se == pytest.approx(np.sqrt(covariance[0, 0]) * 25200)
        assert row.t == pytest.approx(beta[0] / np.sqrt(covariance[0, 0]))
        assert row.nobs == len(complete)
    assert list(actual.reset_index()[TABLE_COLUMNS].columns) == TABLE_COLUMNS


def test_costs_charge_both_legs_and_keep_presample_position(inputs, frame):
    signals, _ = inputs
    w = weights(signals)
    t = frame.signal_date.iloc[0]
    i = w.index.get_loc(t)
    delta = abs(w.weight.iloc[i] - w.weight.iloc[i - 1])
    assert frame.turnover.iloc[0] == pytest.approx(2 * delta)
    assert frame.strategy_net_costs.iloc[0] == pytest.approx(
        frame.strategy.iloc[0] - delta * 1.5 / 10000
    )
    zero_cost = strategy_data(*inputs, demo=True, equity_cost_bps=0, bond_cost_bps=0)
    np.testing.assert_array_equal(zero_cost.strategy, zero_cost.strategy_net_costs)


def test_crisis_dates_and_standalone_component_volatility(frame):
    summary = descriptive_table(frame).set_index("asset")
    allowed = ~(
        ((frame.index >= "2008-09-01") & (frame.index <= "2009-03-31"))
        | ((frame.index >= "2020-03-01") & (frame.index <= "2020-03-31"))
    )
    assert summary.loc["strategy_ex_crises", "nobs"] == allowed.sum()
    returns = frame.strategy.to_numpy()[allowed]
    expected = np.mean(returns) / np.std(returns, ddof=1) * np.sqrt(252)
    assert summary.loc["strategy_ex_crises", "sharpe"] == pytest.approx(expected)
    for name in ("threshold_piece", "calendar_piece"):
        expected_vol = np.std(frame[name], ddof=1) * np.sqrt(252) * 100
        assert summary.loc[name, "volatility_pct_pa"] == pytest.approx(expected_vol)
    np.testing.assert_allclose(
        frame.strategy, (frame.threshold_piece + frame.calendar_piece) / 2
    )


def test_regimes_use_single_full_sample_median_with_missing_values_and_ties(frame):
    data = frame.copy()
    data["ivol"] = np.resize([0.0, 1.0, 1.0, 2.0, np.nan], len(data))
    table, medians = regime_means(data)
    assert medians["ivol"] == 1
    assert list(table.columns) == TABLE_COLUMNS
    rows = table.set_index("column")
    for label, mask in (("H", data.ivol > 1), ("L", data.ivol <= 1)):
        values = data.loc[mask, "strategy"].to_numpy()
        row = rows.loc[f"ivol:{label}"]
        assert row.nobs == len(values)
        assert row.coef == pytest.approx(values.mean() * 25200)
        assert row.se == pytest.approx(
            values.std(ddof=1) / np.sqrt(len(values)) * 25200
        )


def test_figure_scaling_before_log_compounding(frame):
    plotted, scale = cumulative_gains(frame)
    expected_scale = np.std(frame.r_es, ddof=1) / np.std(frame.strategy, ddof=1)
    assert scale == pytest.approx(expected_scale)
    np.testing.assert_allclose(
        plotted.strategy_log_gain, np.cumsum(np.log1p(frame.strategy * scale))
    )
    np.testing.assert_allclose(plotted.r_ty_log_gain, np.cumsum(np.log1p(frame.r_ty)))
    invalid = frame.copy()
    invalid.iloc[0, invalid.columns.get_loc("r_ty")] = -1.0
    with pytest.raises(ValueError, match="log gains"):
        cumulative_gains(invalid)


def test_input_validation(inputs):
    signals, _ = inputs
    with pytest.raises(ValueError, match="cal_reversal"):
        weights(signals, "unknown")
    with pytest.raises(ValueError, match="sorted, unique"):
        weights(pd.concat([signals.iloc[:3], signals.iloc[:3]]))
    with pytest.raises(ValueError, match="costs"):
        strategy_data(*inputs, equity_cost_bps=-1)
    with pytest.raises(ValueError, match="costs"):
        strategy_data(*inputs, bond_cost_bps=float("nan"))


def test_run_writes_contract_outputs(tmp_path, monkeypatch):
    monkeypatch.setattr("rebal.exhibits.strategy.output_dir", lambda kind: tmp_path)
    outputs = run(demo=True)
    assert {p.name for p in outputs} == {
        "table_6a.csv",
        "table_6b.csv",
        "table_6c.csv",
        "figure_6.csv",
        "figure_6.pdf",
        "strategy.metadata.json",
    }
    assert (tmp_path / "figure_6.pdf").read_bytes().startswith(b"%PDF")
    for name in ("table_6b", "table_6c"):
        table = pd.read_csv(tmp_path / f"{name}.csv")
        assert list(table.columns) == TABLE_COLUMNS
        assert not table.isna().any().any()
    metadata = json.loads((tmp_path / "strategy.metadata.json").read_text())
    assert metadata["demo"] is True
    assert metadata["parameters"]["bond_cost_bps"] == 0.5
    assert metadata["nobs"] == len(pd.read_csv(tmp_path / "figure_6.csv"))
