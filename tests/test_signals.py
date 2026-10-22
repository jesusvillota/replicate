"""Simulation identities, paper timing, exact contract, and exhibit integration."""

import json
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from rebal import paths
from rebal.demo import make_panel
from rebal.exhibits import signals_descriptive as descriptive
from rebal.signals import (
    DEFAULT_DELTAS,
    build,
    simulate_calendar,
    simulate_dates,
    simulate_threshold,
)


@pytest.fixture(scope="module")
def panel():
    return make_panel().set_index("date")


@pytest.fixture(scope="module")
def signals(panel):
    return build(panel.r_es, panel.r_ty, r_sp500tr=panel.r_sp500tr)


def test_exact_contract_columns_and_dtypes(signals):
    rows = (paths.REPO_ROOT / "docs/contracts/signals.md").read_text().splitlines()
    schema = {
        cells[0]: cells[1]
        for row in rows
        if row.startswith("| ") and not row.startswith("| Column ")
        for cells in [[cell.strip() for cell in row.split("|")[1:-1]]]
    }
    assert list(signals.columns) == list(schema)
    assert {name: str(signals[name].dtype) for name in signals} == schema
    assert signals.date.is_unique and signals.date.is_monotonic_increasing
    assert signals.date.dt.tz is None


def test_zero_threshold_one_day_drift(panel, signals):
    result = simulate_threshold(panel.r_es, panel.r_ty, 0)
    expected = 0.6 * (1 + panel.r_es) / (1 + 0.6 * panel.r_es + 0.4 * panel.r_ty)
    np.testing.assert_allclose(result.w_pre, expected)
    np.testing.assert_allclose(signals.thr_000, expected - 0.6)
    np.testing.assert_allclose(result.w_post, 0.6)
    assert result.trade.ne(0).all()
    assert list(result.columns) == ["w_pre", "w_post", "trade"]
    pd.testing.assert_index_equal(result.index, panel.index)
    np.testing.assert_allclose(result.trade, result.w_post - result.w_pre)


def test_unreachable_threshold_buy_and_hold(panel):
    result = simulate_threshold(panel.r_es, panel.r_ty, 1)
    equity = 0.6 * (1 + panel.r_es).cumprod()
    bonds = 0.4 * (1 + panel.r_ty).cumprod()
    np.testing.assert_allclose(result.w_pre, equity / (equity + bonds))
    np.testing.assert_allclose(result.w_post, result.w_pre)
    assert result.trade.eq(0).all()


def test_calendar_and_explicit_dates(panel):
    # Independent grouping oracle, including a truncated final month.
    sample = panel.loc[:"1997-06-17"].drop(pd.Timestamp("1997-05-30"))
    dates = sample.groupby(sample.index.to_period("M")).tail(1).index
    result = simulate_calendar(sample.r_es, sample.r_ty)
    pd.testing.assert_index_equal(result.index[result.trade.ne(0)], dates)
    assert result.trade.ne(0).groupby(result.index.to_period("M")).sum().eq(1).all()
    pd.testing.assert_frame_equal(
        result, simulate_dates(sample.r_es, sample.r_ty, dates)
    )
    np.testing.assert_allclose(result.loc[dates, "w_post"], 0.6)
    with pytest.raises(ValueError, match="input trading index"):
        simulate_dates(sample.r_es, sample.r_ty, [pd.Timestamp("1997-06-18")])


def test_point24_rule(panel):
    sample = panel / 10
    result = simulate_calendar(sample.r_es, sample.r_ty)
    spread = sample.r_es - sample.r_ty
    approximate = 0.24 * (
        (1 + spread).groupby(sample.index.to_period("M")).cumprod() - 1
    )
    np.testing.assert_allclose(result.w_pre - 0.6, approximate, rtol=0.05, atol=2e-5)


def test_trade_counts_nonincreasing_on_controlled_path():
    # First-passage counts need not be ordered on arbitrary oscillating paths.
    index = pd.bdate_range("2000-01-03", periods=2000)
    equity, bonds = pd.Series(0.002, index=index), pd.Series(0.0, index=index)
    counts = [
        simulate_threshold(equity, bonds, d).trade.ne(0).sum() for d in DEFAULT_DELTAS
    ]
    assert counts[0] == len(index)
    assert np.all(np.diff(counts) <= 0)
    assert counts[-1] < counts[1]


@pytest.mark.parametrize(
    "name,first",
    [
        ("mom_fast", 9),
        ("mom_medium", 19),
        ("mom_slow", 251),
        ("momentum", 251),
        ("rev_st", 4),
        ("rev_lt", 1259),
    ],
)
def test_burn_in(signals, name, first):
    assert signals[name].iloc[:first].isna().all()
    assert signals[name].iloc[first:].notna().all()


def test_momentum_and_reversals(panel, signals):
    ret = panel.r_es - panel.r_ty
    oracle = lambda k: np.sign((1 + ret).rolling(k).apply(np.prod, raw=True) - 1)
    for column, windows in (
        ("mom_fast", range(1, 11)),
        ("mom_medium", range(11, 21)),
        ("mom_slow", (21, 42, 63, 126, 252)),
    ):
        expected = np.mean([oracle(k).to_numpy() for k in windows], axis=0)
        np.testing.assert_allclose(signals[column], expected, equal_nan=True)
        assert signals[column].dropna().between(-1, 1).all()
    np.testing.assert_allclose(
        signals.momentum, (signals.mom_medium + signals.mom_slow) / 2, equal_nan=True
    )
    np.testing.assert_allclose(
        signals.rev_st,
        (1 + ret).rolling(5).apply(np.prod, raw=True) - 1,
        equal_nan=True,
    )
    expected_lt = (1 + ret.shift(252)).rolling(1008).apply(np.prod, raw=True) - 1
    np.testing.assert_allclose(signals.rev_lt, expected_lt, equal_nan=True)
    alternate = build(panel.r_es, panel.r_ty, momentum="all15")
    expected_all = (10 * signals.mom_medium + 5 * signals.mom_slow) / 15
    np.testing.assert_allclose(alternate.momentum, expected_all, equal_nan=True)
    assert not alternate.momentum.equals(signals.momentum)


def test_zero_returns_and_short_history():
    index = pd.bdate_range("2020-01-01", periods=260)
    zero = pd.Series(0.0, index=index)
    frame = build(zero, zero, r_sp500tr=zero)
    assert (
        frame[["mom_fast", "mom_medium", "mom_slow", "momentum"]]
        .iloc[251:]
        .eq(0)
        .all()
        .all()
    )
    assert frame.rev_lt.isna().all()
    assert frame.eom_rev.eq(0).all()
    assert build(zero.iloc[:1], zero.iloc[:1]).shape == (1, 63)


def test_calendar_dummies_use_supplied_calendar(panel):
    sample = panel.loc["2001-09-04":"2001-10-12"].drop(
        pd.date_range("2001-09-11", "2001-09-14")
    )
    frame = build(sample.r_es, sample.r_ty)
    days = (
        sample.groupby(sample.index.to_period("M")).cumcount(ascending=False).to_numpy()
        + 1
    )
    np.testing.assert_array_equal(frame.days_to_month_end, days)
    for number, expected in (
        (1, days > 15),
        (2, (days >= 11) & (days <= 15)),
        (3, (days >= 6) & (days <= 10)),
        (4, days <= 5),
    ):
        np.testing.assert_array_equal(frame[f"week{number}"], expected)
    assert frame[[f"week{i}" for i in range(1, 5)]].sum(axis=1).eq(1).all()


def test_literal_threshold_appendix_b_recursion():
    index = pd.bdate_range("2020-01-27", periods=8)
    eq = pd.Series([0.08, 0.02, -0.03, 0.01, 0.05, -0.01, 0.04, -0.02], index=index)
    bd = eq * 0
    clean = simulate_threshold(eq, bd, 0.01)
    literal = simulate_threshold(eq, bd, 0.01, timing="literal")
    assert clean.trade.iloc[0] != 0 and literal.trade.iloc[0] == 0
    previous = 0.6
    for t, ret in enumerate(eq):
        pre = previous * (1 + ret) / (1 + previous * ret)
        post = 0.6 if abs(previous - 0.6) >= 0.01 else pre
        np.testing.assert_allclose(literal.iloc[t], [pre, post, post - pre])
        previous = post
    pd.testing.assert_frame_equal(
        simulate_threshold(eq, bd, 0), simulate_threshold(eq, bd, 0, timing="literal")
    )


def test_literal_calendar_delays_month_end():
    index = pd.bdate_range("2020-01-27", "2020-02-07")
    eq, bd = pd.Series(0.01, index=index), pd.Series(0.0, index=index)
    clean = simulate_calendar(eq, bd)
    literal = simulate_calendar(eq, bd, timing="literal")
    assert clean.index[clean.trade.ne(0)].tolist() == [
        pd.Timestamp("2020-01-31"),
        pd.Timestamp("2020-02-07"),
    ]
    assert literal.index[literal.trade.ne(0)].tolist() == [pd.Timestamp("2020-02-03")]
    frame = build(eq, bd, timing="literal")
    np.testing.assert_allclose(frame.calendar, literal.w_pre - 0.6)
    np.testing.assert_allclose(
        frame.thr_010, simulate_threshold(eq, bd, 0.01, timing="literal").w_pre - 0.6
    )


def test_aggregate_and_target_variants(panel, signals):
    np.testing.assert_allclose(
        signals.threshold, signals[[f"thr_{i:03d}" for i in range(26)]].mean(axis=1)
    )
    np.testing.assert_allclose(signals.ret, panel.r_es - panel.r_ty)
    for suffix, weight in (("t86", 0.86), ("t50", 0.50), ("t70", 0.70)):
        expected = np.mean(
            [
                simulate_threshold(
                    panel.r_es, panel.r_ty, d, target=weight
                ).w_pre.to_numpy()
                - weight
                for d in DEFAULT_DELTAS[:26]
            ],
            axis=0,
        )
        np.testing.assert_allclose(signals[f"threshold_{suffix}"], expected)
        np.testing.assert_allclose(
            signals[f"calendar_{suffix}"],
            simulate_calendar(panel.r_es, panel.r_ty, target=weight).w_pre - weight,
        )


def test_eom_reversal_no_lookahead_and_holiday_anchor():
    # March 29 is a fifth Friday. March 22 is the fourth, removed as a holiday.
    index = pd.bdate_range("2024-03-01", "2024-04-05").difference(
        pd.DatetimeIndex(["2024-03-22"])
    )
    eq, bd = pd.Series(0.01, index=index), pd.Series(0.0, index=index)
    sp = pd.Series(0.02, index=index)
    frame = build(eq, bd, r_sp500tr=sp).set_index("date")
    assert frame.loc[:"2024-03-21", "eom_rev"].eq(0).all()
    assert frame.loc["2024-03-25", "eom_rev"] == pytest.approx(0.02)
    assert frame.loc["2024-03-29", "eom_rev"] == pytest.approx(1.02**5 - 1)
    assert frame.loc["2024-04-01":, "eom_rev"].eq(0).all()
    changed = sp.copy()
    changed.loc["2024-03-29"] = 0.5
    modified = build(eq, bd, r_sp500tr=changed).set_index("date")
    pd.testing.assert_series_equal(
        frame.loc[:"2024-03-28", "eom_rev"], modified.loc[:"2024-03-28", "eom_rev"]
    )
    truncated = build(
        eq.loc["2024-03-25":], bd.loc["2024-03-25":], r_sp500tr=sp.loc["2024-03-25":]
    )
    assert truncated.eom_rev.iloc[:5].isna().all()
    assert build(eq, bd).eom_rev.isna().all()


@pytest.mark.parametrize(
    "case",
    [
        "mismatch",
        "unsorted",
        "duplicate",
        "timezone",
        "intraday",
        "missing",
        "infinite",
        "minus_one",
        "empty",
    ],
)
def test_invalid_returns(case):
    index = pd.bdate_range("2020-01-01", periods=3)
    eq, bd = pd.Series(0.01, index=index), pd.Series(0.0, index=index)
    if case == "mismatch":
        bd.index = index + pd.Timedelta(days=1)
    if case == "unsorted":
        eq, bd = eq.iloc[::-1], bd.iloc[::-1]
    if case == "duplicate":
        eq.index = bd.index = pd.DatetimeIndex([index[0]] * 3)
    if case == "timezone":
        eq.index = bd.index = index.tz_localize("UTC")
    if case == "intraday":
        eq.index = bd.index = index + pd.Timedelta(hours=1)
    if case == "missing":
        eq.iloc[1] = np.nan
    if case == "infinite":
        bd.iloc[1] = np.inf
    if case == "minus_one":
        eq.iloc[1] = -1
    if case == "empty":
        eq, bd = eq.iloc[:0], bd.iloc[:0]
    with pytest.raises(ValueError):
        build(eq, bd)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"target": 1},
        {"target": np.nan},
        {"timing": "bad"},
        {"momentum": "bad"},
        {"deltas": [0]},
        {"deltas": [*DEFAULT_DELTAS, 0.001]},
        {"deltas": [*DEFAULT_DELTAS, 0.0001]},
    ],
)
def test_invalid_parameters(panel, kwargs):
    with pytest.raises(ValueError):
        build(panel.r_es, panel.r_ty, **kwargs)


def test_descriptive_statistics_and_correlation_oracles(panel, signals):
    table = descriptive.describe(signals).set_index("signal")
    for name in ("threshold", "calendar"):
        series = signals[name]
        assert table.loc[name, "mean"] == pytest.approx(series.mean() * 252)
        assert table.loc[name, "sd"] == pytest.approx(series.std() * np.sqrt(252))
        assert table.loc[name, "ar1"] == pytest.approx(series.autocorr())
        assert table.loc[name, "skewness"] == pytest.approx(series.skew())
        assert table.loc[name, "excess_kurtosis"] == pytest.approx(series.kurt())
    frame = signals.set_index("date").join(
        panel[["vix", "move", "epu", "ads", "sentiment"]]
    )
    frame["vix"] = frame.threshold * 2
    frame["move"] = -frame.calendar
    actual = descriptive.correlations(frame).set_index("predictor")
    expected = frame[list(descriptive.PREDICTORS)].dropna().corr()
    np.testing.assert_allclose(actual, expected)
    assert actual.loc["threshold", "vix"] == pytest.approx(1)
    assert actual.loc["calendar", "move"] == pytest.approx(-1)
    # Independent noise has no planted correlation.
    frame["vix"] = np.random.default_rng(42).normal(size=len(frame))
    assert (
        abs(
            descriptive.correlations(frame)
            .set_index("predictor")
            .loc["threshold", "vix"]
        )
        < 0.05
    )


def test_exhibits_write_demo_outputs(monkeypatch, tmp_path):
    monkeypatch.setattr(paths, "REPO_ROOT", tmp_path)
    written = descriptive.run(demo=True)
    assert {p.name for p in written} == {
        "table_C1.csv",
        "table_C2.csv",
        "figure_C1.csv",
        "figure_C1.pdf",
        "signals_descriptive.json",
    }
    assert all(
        p.parent == tmp_path / "output/demo" and p.stat().st_size > 0 for p in written
    )
    assert (tmp_path / "output/demo/figure_C1.pdf").read_bytes().startswith(b"%PDF")
    c1 = pd.read_csv(tmp_path / "output/demo/table_C1.csv")
    assert list(c1.columns) == [
        "exhibit", "column", "nobs", "term", "value", "sample_start", "sample_end"
    ]
    c1_keys = c1.set_index(["exhibit", "column", "term"])
    assert c1_keys.index.is_unique
    assert set(c1_keys.index) == {
        ("table_C1", signal, term)
        for signal in ("threshold", "calendar")
        for term in (
            "mean_annualized", "sd_annualized", "ar1", "skewness", "excess_kurtosis"
        )
    }
    plotted = pd.read_csv(tmp_path / "output/demo/figure_C1.csv")
    assert list(plotted.columns) == ["date", "threshold", "calendar"]
    for signal in ("threshold", "calendar"):
        assert c1_keys.loc[("table_C1", signal, "mean_annualized"), "value"] == (
            pytest.approx(plotted[signal].mean() * 252)
        )
        assert c1_keys.loc[("table_C1", signal, "sd_annualized"), "value"] == (
            pytest.approx(plotted[signal].std() * np.sqrt(252))
        )
    c2 = pd.read_csv(tmp_path / "output/demo/table_C2.csv")
    assert list(c2.columns) == ["exhibit", "column", "term", "value"]
    c2_keys = c2.set_index(["exhibit", "column", "term"])
    assert c2_keys.index.is_unique
    assert set(c2_keys.index) == {
        ("table_C2", row, column)
        for row in descriptive.PREDICTORS
        for column in descriptive.PREDICTORS
    }
    assert np.isfinite(c1.value).all() and np.isfinite(c2.value).all()
    metadata = json.loads(
        (tmp_path / "output/demo/signals_descriptive.json").read_text()
    )
    assert metadata["sample_start"].startswith("1997-09-10")
    assert metadata["sample_end"].startswith("2023-03-17")
    descriptive.run(demo=True, end="latest")
    metadata = json.loads(
        (tmp_path / "output/demo/signals_descriptive.json").read_text()
    )
    assert metadata["sample_end"].startswith("2023-12-29")


def test_real_build_cli_writes_external_contract(monkeypatch, tmp_path, panel, signals):
    monkeypatch.setenv("REPLICATE_DATA_DIR", str(tmp_path))
    processed = paths.processed_dir()
    panel.reset_index().to_parquet(processed / "daily_panel.parquet", index=False)
    result = subprocess.run(
        [sys.executable, "-m", "rebal.signals", "--build"],
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    pd.testing.assert_frame_equal(
        pd.read_parquet(processed / "signals_clean.parquet"), signals
    )
    metadata = json.loads((processed / "signals_clean.json").read_text())
    assert metadata["parameters"]["timing"] == "clean"
