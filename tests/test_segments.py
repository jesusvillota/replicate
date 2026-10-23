"""Causal planted returns, independent OLS, and segment input isolation."""

import json

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from rebal.exhibits import segments
from rebal.regress import TABLE_COLUMNS
from rebal.signals import build


@pytest.fixture(scope="module")
def panel():
    return segments.make_demo_panel()


@pytest.fixture(scope="module")
def table(panel):
    return segments.build_table(panel)


def test_planted_segment_effects(table):
    coef = table.query("column == '1'").set_index("term").coef
    assert coef.threshold == pytest.approx(-0.4, abs=0.05)
    assert coef["calendar:week4"] == pytest.approx(-0.3, abs=0.1)


def test_zero_effect_and_value_growth_insignificant(table):
    zero = segments.build_table(
        segments.make_demo_panel(beta_threshold=0, beta_calweek4=0)
    )
    for column in ["1", "2"]:
        effects = (
            zero.query("column == @column")
            .set_index("term")
            .loc[["threshold", "calendar:week4"]]
        )
        assert effects.coef.abs().lt(0.05).all()
        assert effects.p.gt(0.05).all()
    value = table.query("column == '2'").set_index("term")
    assert value.loc[["threshold", "calendar:week4"], "p"].gt(0.05).all()


def test_segment_signals_and_futures_isolation(panel, table):
    large, small = segments.PAIRS["1"]
    history = panel.set_index("date")
    expected = build(
        history[large] - history.rf_3m, history[small] - history.rf_3m, target=0.9
    )
    actual = segments.segment_signals(panel, large, small)
    pd.testing.assert_frame_equal(actual, expected)
    np.testing.assert_allclose(actual.ret, history[large] - history[small], atol=1e-16)
    changed = panel.copy()
    changed[["r_es", "r_ty", "r_sp500tr"]] = np.nan
    pd.testing.assert_frame_equal(segments.build_table(changed), table)
    changed[large] = panel[small]  # changing the segment must change its signals
    altered = segments.segment_signals(changed, large, small)
    assert not np.allclose(altered.threshold, actual.threshold)
    assert not np.allclose(altered.momentum, actual.momentum, equal_nan=True)


def test_independent_next_day_ols_and_sample(panel, table):
    signals = segments.segment_signals(panel, *segments.PAIRS["1"]).set_index("date")
    x = signals[["threshold", "calendar", "week4", "momentum", "ret"]].copy()
    x["calendar:week4"] = x.calendar * x.week4
    y = signals.ret.shift(-1)
    outcome_date = pd.Series(signals.index, index=signals.index).shift(-1)
    selected = (
        (signals.index >= segments.SAMPLE[0])
        & (signals.index <= segments.SAMPLE[1])
        & outcome_date.between(*segments.SAMPLE)
    )
    expected = sm.OLS(y[selected], sm.add_constant(x[selected])).fit(cov_type="HC1")
    actual = table.query("column == '1'").set_index("term").loc[expected.params.index]
    np.testing.assert_allclose(actual.coef, expected.params, atol=1e-12)
    np.testing.assert_allclose(actual.se, expected.bse, atol=1e-12)
    assert actual.nobs.eq(selected.sum()).all()
    assert actual.sample_start.eq("2006-08-18").all()
    assert actual.sample_end.eq("2023-03-17").all()


def test_contract_and_options(panel, table):
    assert list(table) == TABLE_COLUMNS
    assert set(table.column) == {"1", "2"}
    assert table.exhibit.eq("table_5").all()
    assert not table.duplicated(["column", "term"]).any()
    assert np.isfinite(table[["coef", "se", "t", "p", "nobs", "adj_r2"]]).all().all()
    alternate = segments.build_table(
        panel, value_weight=0.5, controls="all", end="latest", se="hac", hac_lags=3
    )
    assert set(segments.EXTERNAL) <= set(alternate.term)
    assert alternate.se_type.eq("hac").all()
    assert alternate.nobs.min() > table.nobs.max()
    assert alternate.sample_end.eq("2023-12-29").all()
    baseline = segments.build_table(panel, value_weight=0.5)
    pd.testing.assert_frame_equal(
        baseline.query("column == '1'"), table.query("column == '1'")
    )
    assert not np.allclose(
        baseline.query("column == '2'").coef, table.query("column == '2'").coef
    )


def test_missing_history_does_not_bridge_days(panel):
    changed = panel.copy()
    changed.loc[:9, "r_r1k"] = np.nan
    signals = segments.segment_signals(changed, *segments.PAIRS["1"])
    assert signals.date.iloc[0] == panel.date.iloc[10]
    changed.loc[100, "r_r1k"] = np.nan
    with pytest.raises(ValueError, match="interior missing"):
        segments.segment_signals(changed, *segments.PAIRS["1"])
    changed["r_r1k"] = np.nan
    with pytest.raises(ValueError, match="no complete history"):
        segments.segment_signals(changed, *segments.PAIRS["1"])


def test_run_writes_only_owned_artifacts(panel, table, tmp_path, monkeypatch):
    monkeypatch.setattr(segments, "make_demo_panel", lambda: panel)
    monkeypatch.setattr(segments, "output_dir", lambda kind: tmp_path)
    paths = segments.run(demo=True)
    assert {p.name for p in paths} == {"table_5.csv", "segments.metadata.json"}
    saved = pd.read_csv(paths[0], dtype={"column": str})
    pd.testing.assert_frame_equal(saved, table, check_exact=False, atol=1e-12)
    metadata = json.loads(paths[1].read_text())
    assert metadata["demo"] is True
    assert metadata["weights"] == {"1": 0.9, "2": 0.9}
    assert metadata["terms"] == segments.BASE
    assert len(metadata["estimation"]) == 2


@pytest.mark.parametrize(
    "options, message",
    [
        ({"value_weight": 0.6}, "value_weight"),
        ({"controls": "unknown"}, "controls"),
    ],
)
def test_invalid_options(panel, options, message):
    with pytest.raises(ValueError, match=message):
        segments.build_table(panel, **options)
