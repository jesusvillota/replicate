"""Effect recovery, independent timing oracles and output-contract checks."""

import json

import numpy as np
import pandas as pd
import pytest

from rebal.demo import make_panel, make_signals
from rebal.exhibits import robustness_extra as extra
from rebal.regress import TABLE_COLUMNS, dated
from rebal.signals import build


def coefficients(table, column="1"):
    return table.loc[table.column == column].set_index("term").coef


@pytest.fixture(scope="module")
def inputs():
    p = make_panel()
    return make_signals(p), p


@pytest.mark.parametrize("betas", [(-0.4, -0.3), (0.0, 0.0)])
def test_demo_planted_and_zero_each_table(inputs, betas):
    tables = extra.build_tables(*inputs, demo_betas=betas)
    for table in tables.values():
        assert list(table) == TABLE_COLUMNS
        for column in table.column.unique():
            c = coefficients(table, column)
            assert c.threshold == pytest.approx(betas[0], abs=0.02)
            assert c["calendar:week4"] == pytest.approx(betas[1], abs=0.02)


@pytest.mark.parametrize("beta", [-0.4, 0.0])
def test_external_planted_index_outcome_and_d9_control(inputs, beta):
    s, p = (frame.copy() for frame in inputs)
    # Independent response, outside the module's demo response generator.
    rng = np.random.default_rng(8)
    index_response = (
        beta * s.threshold - 0.3 * s.calendar * s.week4 + rng.normal(0, 0.0001, len(s))
    ).shift(1)
    p.r_agg = p.r_sp500tr - index_response
    s.ret = index_response + (0.002 * (p.ra_bex - 3)).shift(1)
    tables = extra.build_tables(s, p, d4_signals="futures")
    c4 = coefficients(tables["table_D4"])
    assert c4.threshold == pytest.approx(beta, abs=0.02)
    assert c4["calendar:week4"] == pytest.approx(-0.3, abs=0.02)
    c9 = coefficients(tables["table_D9"])
    assert c9.threshold == pytest.approx(beta, abs=0.01)
    assert c9.ra_bex == pytest.approx(0.002, abs=0.00002)


def test_default_d4_matches_independent_rebuilt_design(inputs):
    s, p = inputs
    pair = p.set_index("date")
    rebuilt = build(pair.r_sp500tr, pair.r_agg, r_sp500tr=pair.r_sp500tr)
    x = pd.DataFrame(
        {
            "const": 1.0,
            "threshold": rebuilt.threshold,
            "calendar": rebuilt.calendar,
            "week4": rebuilt.week4,
            "calendar:week4": rebuilt.calendar * rebuilt.week4,
            "momentum": rebuilt.momentum,
            "ret": pair.r_sp500tr.to_numpy() - pair.r_agg.to_numpy(),
        }
    )
    y = rebuilt.ret.shift(-1)
    dates = rebuilt.date
    next_dates = dates.shift(-1)
    mask = (dates >= "1997-09-10") & (next_dates <= "2023-03-17")
    mask &= np.isfinite(x).all(axis=1) & y.notna()
    expected = np.linalg.lstsq(x.loc[mask], y.loc[mask], rcond=None)[0]
    table = extra.build_tables(s, p)["table_D4"]
    np.testing.assert_allclose(coefficients(table).loc[x.columns], expected, atol=1e-11)
    assert table.nobs.unique().tolist() == [int(mask.sum())]
    assert not np.allclose(
        coefficients(table),
        coefficients(extra.build_tables(s, p, d4_signals="futures")["table_D4"]),
    )


def test_d14_extra_lag_independent_response_and_control(inputs):
    s, p = (frame.copy() for frame in inputs)
    rng = np.random.default_rng(19)
    # White signals distinguish t-1 from t; ordinary AR signals could hide a bug.
    s.threshold = rng.normal(0, 0.005, len(s))
    s.calendar = rng.normal(0, 0.01, len(s))
    control = (1 + p.r_sp500tr) * (1 + p.r_sp500tr.shift(1)) - 1
    response = (
        -0.4 * s.threshold.shift(1)
        - 0.3 * s.calendar.shift(1) * s.week4
        + 0.07 * control
        + rng.normal(0, 0.0001, len(s))
    ).shift(1)
    p.r_acwxus = p.rf_3m + response
    p.loc[p.date < "2000-12-29", "r_acwxus"] = np.nan
    # A gap must remove a response, not compress the calendar before lagging.
    p.loc[4000, "r_acwxus"] = np.nan
    lagged = extra.build_tables(s, p)["table_D14"]
    c = coefficients(lagged)
    assert c.threshold == pytest.approx(-0.4, abs=0.002)
    assert c["calendar:week4"] == pytest.approx(-0.3, abs=0.002)
    assert c.sp500_trailing_2d == pytest.approx(0.07, abs=0.001)
    unlagged = coefficients(extra.build_tables(s, p, d14_lag=0)["table_D14"])
    assert abs(unlagged.threshold) < 0.02
    assert abs(unlagged["calendar:week4"]) < 0.02
    assert lagged.sample_start.min() >= "2000-12-29"


def test_missing_controls_column_samples_and_no_fears(inputs):
    s, p = (frame.copy() for frame in inputs)
    p.loc[p.date < "2006-01-01", "ra_bex"] = np.nan
    p.loc[p.date > "2018-12-31", "unc_bex"] = np.nan
    table = extra.build_tables(s, p)["table_D9"]
    assert set(table.column) == {"1", "2", "4"}
    assert not table.term.str.contains("fears", case=False).any()
    samples = table.groupby("column").first()
    assert samples.loc["1", "sample_start"] >= "2006-01-02"
    assert samples.loc["2", "sample_end"] <= "2019-01-01"
    assert samples.loc["4", "sample_start"] >= "2004-07-02"
    assert samples.loc["4", "sample_end"] <= "2020-01-01"
    assert samples.nobs.nunique() == 3


def test_d4_missing_returns_are_never_filled(inputs):
    _, p = inputs
    p = p.copy()
    p.loc[1000, "r_agg"] = np.nan
    with pytest.raises(ValueError, match="internal gaps"):
        extra.index_signals(p)
    p.loc[:1000, "r_agg"] = np.nan
    result = extra.index_signals(p)
    assert result.date.min() == p.date.iloc[1001]


def test_designs_do_not_mutate_inputs_and_d14_calendar(inputs):
    s, p = inputs
    before_s, before_p = s.copy(deep=True), p.copy(deep=True)
    ds, dp, _, _ = extra.prepare_designs(s, p)["table_D14"]
    pd.testing.assert_series_equal(ds.calendar, dated(s).calendar.shift(1))
    pd.testing.assert_series_equal(ds.week4, dated(s).week4)
    expected = ((1 + p.r_sp500tr) * (1 + p.r_sp500tr.shift(1)) - 1).to_numpy()
    np.testing.assert_allclose(dp.sp500_trailing_2d, expected, equal_nan=True)
    assert dp.loc[dp.index < "2000-12-29", "international_excess"].isna().all()
    pd.testing.assert_frame_equal(s, before_s)
    pd.testing.assert_frame_equal(p, before_p)


def test_run_contract_and_metadata(inputs, tmp_path, monkeypatch):
    monkeypatch.setattr(extra, "output_dir", lambda kind: tmp_path)
    paths = extra.run(demo=True)
    assert {path.name for path in paths} == {
        "table_D4.csv",
        "table_D9.csv",
        "table_D14.csv",
        "robustness_extra.metadata.json",
    }
    metadata = json.loads(paths[-1].read_text())
    assert "FEARS" in metadata["skipped"]["table_D9"]["3"]
    assert set(metadata["samples"]["table_D9"]) == {"1", "2", "4"}
    for path in paths[:-1]:
        table = pd.read_csv(path, dtype={"column": str})
        assert list(table) == TABLE_COLUMNS
        assert table.se_type.eq("hc1").all()
        assert table.nobs.gt(0).all()
        assert np.isfinite(table[["coef", "se", "t", "p"]]).all().all()
