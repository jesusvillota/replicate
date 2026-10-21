"""Independent numerical oracles for predictive-regression timing and tables."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from rebal.demo import make_panel, make_signals
from rebal.exhibits.predictive_tables import (
    BASE,
    CONTROL_SETS,
    EXHIBITS,
    HORIZONS,
    build_tables,
)
from rebal.regress import (
    DEFAULT_SAMPLE,
    TABLE_COLUMNS,
    ols,
    predictive,
    predictive_data,
)


@pytest.fixture(scope="module")
def inputs():
    panel = make_panel()
    return make_signals(panel), panel


@pytest.fixture(scope="module")
def tables(inputs):
    return build_tables(*inputs)


def test_planted_table_1(tables):
    table = tables[0]["table_1"]
    coefficients = table[table.column == "1"].set_index("term").coef
    assert coefficients.threshold == pytest.approx(-0.4, abs=0.05)
    assert coefficients["calendar:week4"] == pytest.approx(-0.3, abs=0.05)


def test_zero_effect(inputs):
    _, panel = inputs
    signals = make_signals(panel, beta_threshold=0, beta_calweek4=0)
    table = build_tables(signals, panel)[0]["table_1"]
    coefficients = table[table.column == "1"].set_index("term").coef
    assert abs(coefficients.threshold) < 0.05
    assert abs(coefficients["calendar:week4"]) < 0.05


@pytest.mark.parametrize("covariance", ["hc0", "hc1", "hac"])
@pytest.mark.parametrize("lags", [None, 3])
def test_covariance_matches_statsmodels(covariance, lags):
    rng = np.random.default_rng(14)
    X = pd.DataFrame(rng.normal(size=(180, 2)), columns=["a", "b"])
    y = X.a * 0.3 + rng.normal(size=len(X)) * (1 + X.b.abs())
    actual = ols(y, X, se=covariance, hac_lags=lags)
    options = {}
    if covariance == "hac":
        options = {
            "maxlags": lags if lags is not None else int(4 * (180 / 100) ** (2 / 9)),
            "kernel": "bartlett",
            "use_correction": False,
        }
    expected = sm.OLS(y, sm.add_constant(X)).fit(
        cov_type=covariance.upper(),
        cov_kwds=options,
        use_t=False,
    )
    for actual_values, expected_values in [
        (actual.coef, expected.params),
        (actual.se, expected.bse),
        (actual.t, expected.tvalues),
        (actual.p, expected.pvalues),
    ]:
        np.testing.assert_allclose(actual_values, expected_values, rtol=1e-12)


def test_timing_before_subset_and_missing_dates():
    dates = pd.bdate_range("2020-01-01", periods=12)
    panel = pd.DataFrame({"date": dates, "r_es": np.arange(12.0)})
    signals = pd.DataFrame(
        {"date": dates, "ret": np.arange(12.0) ** 2, "threshold": np.arange(12.0) + 100}
    )
    subset = pd.Series(np.arange(12) % 2 == 0, index=dates)
    y, x, outcomes = predictive_data(
        signals,
        panel,
        ["threshold"],
        y="r_es",
        sample=("2020-01-01", "latest"),
        subset=subset,
    )
    np.testing.assert_array_equal(y, [1, 3, 5, 7, 9, 11])
    np.testing.assert_array_equal(x.threshold, [100, 102, 104, 106, 108, 110])
    assert list(outcomes) == list(dates[1::2])
    # Removing a signal must not turn a one-day lead into a two-day lead.
    signals = signals.drop(index=3)
    y, x, _ = predictive_data(
        signals, panel, ["threshold"], sample=("2020-01-01", "latest")
    )
    assert dates[2] not in x.index  # ret at the actual next day is unavailable.
    assert y.loc[dates[4]] == 25
    assert not y.isna().any()
    y_subset, _, _ = predictive_data(
        signals,
        panel,
        ["threshold"],
        sample=("2020-01-01", "latest"),
        subset=np.ones(len(signals), dtype=bool),
    )
    pd.testing.assert_series_equal(y_subset, y)


def test_sample_boundaries_and_recorded_dates(inputs):
    signals, panel = inputs
    result = predictive(signals, panel, BASE)
    assert result.design.index.min() >= pd.Timestamp(DEFAULT_SAMPLE[0])
    assert result.tidy.sample_start.iloc[0] == "1997-09-11"
    assert result.tidy.sample_end.iloc[0] == DEFAULT_SAMPLE[1]
    latest = predictive(signals, panel, BASE, sample=(DEFAULT_SAMPLE[0], "latest"))
    assert latest.nobs > result.nobs
    assert latest.tidy.sample_end.iloc[0] == "2023-12-29"


def test_fwl_on_each_complete_sample(inputs, tables):
    signals, panel = inputs
    panel = panel.copy()
    panel.loc[panel.index[::11], "vix"] = np.nan
    signals = signals.copy()
    signals.loc[signals.index[::17], "threshold"] = np.nan
    changed, _ = build_tables(signals, panel)
    for source in [tables[0], changed]:
        for controls, col in [(False, "3"), (True, "4")]:
            base_col = "5" if controls else "1"
            baseline_table = source["table_1"]
            baseline = baseline_table[
                (baseline_table.column == base_col)
                & (baseline_table.term == "threshold")
            ].coef.item()
            residual = (
                source["table_D8"]
                .query("column == @col and term == 'threshold_perp'")
                .coef.item()
            )
            assert residual == pytest.approx(baseline, abs=1e-10)


def test_all_contracts_and_layouts(tables):
    frames, magnitudes = tables
    assert list(frames) == EXHIBITS
    counts = [5, 3, 3, 4, 2, 5, 5, 4, 4, 3, 4, 5, 5, 6, 10]
    for (name, frame), columns in zip(frames.items(), counts, strict=True):
        assert list(frame) == TABLE_COLUMNS
        assert frame.column.nunique() == columns, name
        assert frame.exhibit.eq(name).all()
        assert frame.nobs.gt(0).all()
        assert not frame.duplicated(["column", "term"]).any()
        assert np.isfinite(frame[["coef", "se", "t", "p", "adj_r2"]]).all().all()
        assert frame.sample_start.le(frame.sample_end).all()
    assert frames["table_D1"].se_type.eq("hac").all()
    assert frames["table_D2"].se_type.eq("hac").all()
    assert frames["table_D1"].term.eq("coefficient_sum").sum() == 2
    assert "ret" not in set(frames["table_D10"].term)
    assert {"calendar", "calendar:week4"} <= set(magnitudes.term)
    np.testing.assert_allclose(magnitudes.magnitude, magnitudes.coef * magnitudes.sd)


def test_d1_joint_trailing_sums_and_sum_se(inputs, tables):
    signals, _ = inputs
    history = signals.set_index("date")
    x = pd.DataFrame({f"ret_{h}": history.ret.rolling(h).sum() for h in HORIZONS})
    x = x.loc[DEFAULT_SAMPLE[0] : DEFAULT_SAMPLE[1]].dropna()
    expected = sm.OLS(history.threshold.loc[x.index], sm.add_constant(x)).fit(
        cov_type="HAC",
        cov_kwds={"maxlags": int(4 * (len(x) / 100) ** (2 / 9))},
    )
    actual = tables[0]["table_D1"].query("column == '1'").set_index("term")
    np.testing.assert_allclose(actual.loc[x.columns, "coef"], expected.params.iloc[1:])
    weights = np.r_[0, np.ones(len(HORIZONS))]
    assert actual.loc["coefficient_sum", "coef"] == pytest.approx(
        weights @ expected.params
    )
    assert actual.loc["coefficient_sum", "se"] == pytest.approx(
        np.sqrt(weights @ expected.cov_params() @ weights)
    )


def test_column_definitions_and_magnitudes(inputs, tables):
    signals, panel = inputs
    for column, controls in enumerate(CONTROL_SETS, 1):
        result = predictive(signals, panel, BASE + controls)
        magnitude = tables[1]
        magnitude = magnitude[
            (magnitude.exhibit == "table_1") & (magnitude.column == str(column))
        ].set_index("term")
        for term in BASE + controls:
            assert magnitude.loc[term, "sd"] == pytest.approx(
                result.design[term].std(ddof=1)
            )


def test_validation_and_nonfinite_rows():
    X = pd.DataFrame({"x": [0, 1, 2, np.inf, 4, 5.0]})
    y = pd.Series([0, 1, np.nan, 3, 3, 6.0])
    assert ols(y, X).nobs == 4
    with pytest.raises(ValueError, match="se must"):
        ols(y, X, se="bad")
    with pytest.raises(ValueError, match="nonnegative"):
        ols(y, X, hac_lags=-1)
    with pytest.raises(ValueError, match="rank deficient"):
        ols(y, X.assign(duplicate=X.x))
