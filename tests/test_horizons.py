"""Independent timing, covariance, Monte Carlo size and plotted-data checks."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from rich.console import Console
from scipy.signal import lfilter
from scipy.stats import norm

from rebal.demo import make_panel, make_signals
from rebal.exhibits import calibration_figures, horizon_figures
from rebal.exhibits._figure_output import plot_data
from rebal.regress_hodrick import hodrick


@pytest.fixture(scope="module")
def inputs():
    panel = make_panel()
    return make_signals(panel), panel


@pytest.fixture(scope="module")
def calibration(inputs):
    return calibration_figures.build_figures(*inputs)


@pytest.fixture(scope="module")
def horizons(inputs):
    return horizon_figures.build_figures(*inputs)


def test_hodrick_size():
    """A fixed, reproducible null experiment; no seed search or fitted tuning."""
    rng = np.random.default_rng(2026)
    draws, n, horizon = 200, 1000, 5
    rejects_hodrick, rejects_naive = 0, 0
    for _ in range(draws):
        x = lfilter([1], [1, -0.9], rng.normal(size=n + 500))[500:]
        returns = pd.Series(rng.normal(size=n))
        y = pd.Series(np.convolve(returns.to_numpy()[1:], np.ones(horizon), "valid"))
        design = pd.DataFrame({"x": x[: len(y)]})
        result = hodrick(y, design, returns, horizon)
        naive = sm.OLS(y, sm.add_constant(design)).fit()
        rejects_hodrick += abs(result.t["x"]) > norm.ppf(0.975)
        rejects_naive += abs(naive.tvalues["x"]) > norm.ppf(0.975)
    rate, naive_rate = rejects_hodrick / draws, rejects_naive / draws
    Console().print(
        f"Hodrick 1B rejection rate: {rate:.1%} ({rejects_hodrick}/{draws}); "
        f"naive overlapping OLS: {naive_rate:.1%} ({rejects_naive}/{draws})."
    )
    assert 0.02 <= rate <= 0.10
    assert naive_rate > rate


@pytest.mark.parametrize("horizon", [1, 3, 5])
def test_hodrick_reverse_scores_with_missing_origins(horizon):
    """Independent nested-loop covariance oracle includes both sample edges."""
    rng = np.random.default_rng(42)
    dates = pd.bdate_range("2020-01-01", periods=90)
    returns = pd.Series(rng.normal(size=len(dates)), index=dates)
    origins = np.arange(4, 80)
    origins = origins[origins % 7 != 0]
    x = pd.DataFrame(
        rng.normal(size=(len(origins), 2)), index=dates[origins], columns=["x", "z"]
    )
    y = pd.Series(
        [returns.iloc[t + 1 : t + horizon + 1].sum() for t in origins], index=x.index
    )
    result = hodrick(y, x, returns, horizon)
    design = sm.add_constant(x).to_numpy()
    used = sorted({t + j for t in origins for j in range(1, horizon + 1)})
    mean = returns.iloc[used].mean()
    meat = np.zeros((3, 3))
    for day in used:
        score = np.zeros(3)
        for i, origin in enumerate(origins):
            if origin < day <= origin + horizon:
                score += design[i] * (returns.iloc[day] - mean)
        meat += np.outer(score, score)
    bread = np.linalg.inv(design.T @ design)
    expected = bread @ meat @ bread
    np.testing.assert_allclose(result.covariance, expected, rtol=1e-12, atol=1e-14)
    np.testing.assert_allclose(result.coef, np.linalg.lstsq(design, y, rcond=None)[0])
    assert result.tidy.se_type.eq("hodrick_1b").all()


def test_planted_and_zero_effect(inputs, calibration):
    row = calibration["figure_2"].query("delta_pct == 0").iloc[0]
    assert row.t < -3
    _signals, panel = inputs
    zero = make_signals(panel, beta_threshold=0, beta_calweek4=0)
    x, y = zero.thr_000.to_numpy()[:-1], zero.ret.to_numpy()[1:]
    dates = zero.date.to_numpy()
    keep = (dates[:-1] >= np.datetime64("1997-09-10")) & (
        dates[1:] <= np.datetime64("2023-03-17")
    )
    oracle = sm.OLS(y[keep], sm.add_constant(x[keep])).fit(cov_type="HC1")
    actual = (
        calibration_figures.build_figures(zero, panel)["figure_2"]
        .query("delta_pct == 0")
        .iloc[0]
    )
    assert actual.coef == pytest.approx(oracle.params[1])
    assert actual.t == pytest.approx(oracle.tvalues[1])
    # thr_000 is half the demo threshold; compare in aggregate signal units.
    assert abs(actual.coef * 0.5) < 0.05


def test_calibration_definitions_and_subsets(inputs, calibration):
    signals, _ = inputs
    s = signals.set_index("date")
    target = s.ret.shift(-1)
    dates = pd.Series(s.index, index=s.index).shift(-1)
    sample = (s.index >= "1997-09-10") & dates.le("2023-03-17")
    for name, covariance in (("figure_2", "HC1"), ("figure_D1", "HAC")):
        data = calibration[name]
        assert len(data) == 42
        np.testing.assert_array_equal(data.delta_pct.iloc[:41], np.arange(41) / 10)
        for term, series, delta in (
            ("thr_000", "all", 0),
            ("threshold", "aggregate", None),
        ):
            mask = data.series.eq(series) if delta is None else data.delta_pct.eq(delta)
            x = sm.add_constant(s.loc[sample, [term]])
            options = (
                {"maxlags": int(4 * (len(x) / 100) ** (2 / 9))}
                if covariance == "HAC"
                else {}
            )
            oracle = sm.OLS(target.loc[sample], x).fit(
                cov_type=covariance, cov_kwds=options
            )
            assert data.loc[mask, "t"].item() == pytest.approx(oracle.tvalues[term])
    for name in ("figure_3", "figure_D2"):
        np.testing.assert_array_equal(calibration[name].window_days, np.arange(1, 11))
    dummy = (s.days_to_month_end <= 5).astype(float)
    x = pd.DataFrame(
        {"calendar": s.calendar, "interaction": s.calendar * dummy, "dummy": dummy}
    )
    oracle = sm.OLS(target.loc[sample], sm.add_constant(x.loc[sample])).fit(
        cov_type="HC1"
    )
    assert calibration["figure_3"].query("window_days == 5").t.item() == pytest.approx(
        oracle.tvalues.interaction
    )
    split = calibration["figure_D3"]
    empty = split.query("delta_pct == 0 and series == 'other'").iloc[0]
    assert empty.status == "not_estimable" and empty.nobs == 0 and np.isnan(empty.t)
    for series, selection in (
        ("rebalancing", s.thr_010.abs() >= 0.01),
        ("other", s.thr_010.abs() < 0.01),
    ):
        keep = sample & selection
        oracle = sm.OLS(
            target.loc[keep], sm.add_constant(s.loc[keep, ["thr_010"]])
        ).fit(cov_type="HC1")
        row = split[(split.delta_pct == 1) & (split.series == series)].iloc[0]
        assert row.nobs == keep.sum()
        assert row.t == pytest.approx(oracle.tvalues.thr_010)


def test_future_outcomes_and_sample_end(inputs, horizons):
    signals, _ = inputs
    s = signals.set_index("date")
    values = s.ret.to_numpy()
    x = np.column_stack(
        [
            np.ones(len(s)),
            s.threshold,
            s.calendar,
            s.week4,
            s.calendar * s.week4,
            s.momentum,
            s.ret,
        ]
    )
    for horizon in (1, 5, 15):
        origins = np.arange(len(s) - horizon)
        keep = (s.index[origins] >= "1997-09-10") & (
            s.index[origins + horizon] <= "2023-03-17"
        )
        origins = origins[keep]
        cumulative = np.array(
            [np.log1p(values[t + 1 : t + horizon + 1]).sum() for t in origins]
        )
        for name, y in (
            ("figure_4", cumulative),
            ("figure_D4", values[origins + horizon]),
        ):
            oracle = sm.OLS(y, x[origins]).fit(cov_type="HC1")
            actual = horizons[name].query("horizon_days == @horizon").set_index("term")
            np.testing.assert_allclose(
                actual.loc[["threshold", "calendar:week4"], "coef"],
                oracle.params[[1, 4]],
                rtol=1e-11,
            )
            assert actual.nobs.eq(len(origins)).all()
            assert actual.sample_end.eq("2023-03-17").all()
            np.testing.assert_allclose(
                actual.ci_high - actual.coef, norm.ppf(0.975) * actual.se
            )
            if name == "figure_D4":
                np.testing.assert_allclose(actual.se, oracle.bse[[1, 4]])
    assert horizons["figure_4"].se_type.eq("hodrick_1b").all()
    assert horizons["figure_D4"].se_type.eq("hc1").all()


def test_csvs_are_the_plotted_values(
    tmp_path, monkeypatch, inputs, calibration, horizons
):
    from rebal.exhibits import _figure_output

    monkeypatch.setattr(_figure_output, "output_dir", lambda kind: tmp_path)
    signals, panel = inputs
    paths = []
    for module in (calibration_figures, horizon_figures):
        monkeypatch.setattr(module, "load_panel", lambda **kwargs: panel)
        monkeypatch.setattr(module, "load_signals", lambda **kwargs: signals)
        paths.extend(module.run(demo=True))
    assert sum(path.suffix == ".pdf" for path in paths) == 7
    assert sum(path.suffix == ".csv" for path in paths) == 14
    for name, expected in (calibration | horizons).items():
        data = pd.read_csv(tmp_path / f"{name}.csv")
        pd.testing.assert_frame_equal(data, expected, check_dtype=False)
        assert (tmp_path / f"{name}.pdf").read_bytes().startswith(b"%PDF-")
        figure = plot_data(data, name, True)
        if "horizon_days" in data:
            for axis, term in zip(
                figure.axes, horizon_figures.PLOTTED_TERMS, strict=True
            ):
                part = data[data.term == term]
                np.testing.assert_allclose(axis.lines[0].get_xdata(), part.horizon_days)
                np.testing.assert_allclose(axis.lines[0].get_ydata(), part.coef)
                vertices = axis.collections[0].get_paths()[0].vertices
                for h, lo, hi in zip(
                    part.horizon_days, part.ci_low, part.ci_high, strict=True
                ):
                    limits = vertices[vertices[:, 0] == h, 1]
                    assert limits.min() == pytest.approx(lo)
                    assert limits.max() == pytest.approx(hi)
        else:
            x = "delta_pct" if "delta_pct" in data else "window_days"
            groups = data[data.series != "aggregate"].groupby("series", sort=False)
            axis = figure.axes[0]
            for line, (_, part) in zip(axis.lines, groups):
                np.testing.assert_allclose(line.get_xdata(), part[x])
                np.testing.assert_allclose(line.get_ydata(), part.t)
            assert axis.lines[-1].get_ydata() == [-2.58, -2.58]
            if data.series.eq("aggregate").any():
                np.testing.assert_allclose(
                    axis.lines[-2].get_ydata(),
                    data.loc[data.series == "aggregate", "t"].item(),
                )
        figure.clear()


def test_invalid_hodrick_inputs():
    returns = pd.Series(np.arange(30.0))
    x = pd.DataFrame({"x": np.arange(27.0)})
    y = pd.Series(np.arange(27.0) ** 2)
    with pytest.raises(ValueError, match="positive integer"):
        hodrick(y, x, returns, 0)
    with pytest.raises(ValueError, match="full future horizon"):
        hodrick(y, x, returns, 5)
    returns.iloc[10] = np.nan
    with pytest.raises(ValueError, match="must be finite"):
        hodrick(y, x, returns, 2)
