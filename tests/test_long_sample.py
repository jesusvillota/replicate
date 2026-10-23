"""Table 4 planted-effect, source-conversion and sample-boundary checks."""

import json

import numpy as np
import pandas as pd
import pytest

from rebal import proxies
from rebal.exhibits import long_sample
from rebal.regress import TABLE_COLUMNS, predictive_data


@pytest.fixture(scope="module")
def planted():
    panel, frame = long_sample.demo_inputs()
    return panel, frame, long_sample.build_table(frame, panel)


def test_recovers_planted_split(planted):
    _, _, table = planted
    coefficients = table.pivot(index="term", columns="column", values="coef")
    assert coefficients.loc["threshold", "2"] == pytest.approx(0, abs=0.05)
    assert coefficients.loc["threshold", "3"] == pytest.approx(-0.4, abs=0.05)
    assert coefficients.loc["calendar:week4", "2"] == pytest.approx(0, abs=0.05)
    assert coefficients.loc["calendar:week4", "3"] == pytest.approx(-0.3, abs=0.05)
    assert -0.4 < coefficients.loc["threshold", "1"] < -0.05


def test_zero_effect():
    panel, frame = long_sample.demo_inputs(beta_post=0, beta_calendar_post=0)
    table = long_sample.build_table(frame, panel)
    assert (
        table.loc[table.term.isin(["threshold", "calendar:week4"]), "coef"].abs() < 0.05
    ).all()


def test_contract_and_outcome_windows(planted):
    _, _, table = planted
    assert list(table.columns) == TABLE_COLUMNS
    assert set(table.column) == {"1", "2", "3"}
    assert set(table.exhibit) == {"table_4"}
    assert set(table.term) == {"const", *long_sample.TERMS}
    assert set(table.se_type) == {"hc1"}
    samples = table.drop_duplicates("column").set_index("column")
    assert samples.loc["2", "sample_end"] == "1997-09-09"
    # Both predictor and outcome must fall inside the late window.
    assert samples.loc["3", "sample_start"] == "1997-09-11"
    assert samples.loc["1", "sample_end"] == "2023-03-17"


def test_no_split_crossing_or_signal_restart(planted):
    panel, frame, _ = planted
    y, X, dates = predictive_data(
        frame,
        panel,
        long_sample.TERMS,
        sample=(long_sample.SPLIT, long_sample.END),
    )
    assert X.index.min() == pd.Timestamp("1997-09-10")
    assert dates.min() == pd.Timestamp("1997-09-11")
    original = frame.set_index("date").loc[X.index]
    np.testing.assert_allclose(X.threshold, original.threshold)
    np.testing.assert_allclose(y, frame.set_index("date").ret.reindex(dates).to_numpy())


def source_fixture(start="1961-06-16", end="1964-01-31"):
    dates = pd.bdate_range(start, end)
    rng = np.random.default_rng(8)
    french = pd.DataFrame(
        {"Mkt-RF": rng.normal(0, 1, len(dates)), "RF": 0.01}, index=dates
    )
    curve = pd.DataFrame({"SVENY09": np.nan, "SVENY10": np.nan}, index=dates)
    dgs10 = pd.Series(4.0, index=dates).where(dates >= "1962-01-02")
    return french, curve, dgs10


def test_honest_1961_start_and_252_day_warmup():
    french, curve, dgs10 = source_fixture()
    panel = long_sample.long_returns(french, curve, dgs10)
    assert panel.date.min() == pd.Timestamp("1962-01-03")
    frame = long_sample.build_signals(panel)
    assert frame.momentum.iloc[:251].isna().all()
    assert np.isfinite(frame.momentum.iloc[251:]).all()
    _, X, dates = predictive_data(
        frame,
        panel,
        long_sample.TERMS,
        sample=(long_sample.START, "1964-01-31"),
    )
    assert X.index.min() == panel.date.iloc[251]
    assert dates.min() == panel.date.iloc[252]
    assert dates.min() > pd.Timestamp("1962-01-03")


def test_french_units_and_identical_cash_legs():
    french, curve, dgs10 = source_fixture()
    panel = long_sample.long_returns(french, curve, dgs10).set_index("date")
    np.testing.assert_allclose(
        panel.r_mkt_french, (french["Mkt-RF"] + french.RF).reindex(panel.index) / 100
    )
    np.testing.assert_allclose(panel.r_es, french["Mkt-RF"].reindex(panel.index) / 100)
    np.testing.assert_allclose(
        panel.r_es - panel.r_ty, panel.r_mkt_french - panel.r_10y_gsw
    )
    # Independent constant-yield oracle includes actual-day carry, including weekends.
    date = pd.Timestamp("1962-01-08")
    assert panel.loc[date, "r_ty"] == pytest.approx(
        np.expm1(0.04 * 3 / 365.25) - 0.0001
    )


def test_seam_has_no_cross_source_yield_jump():
    french, curve, dgs10 = source_fixture("1971-08-09", "1971-08-31")
    curve.loc["1971-08-16":, ["SVENY09", "SVENY10"]] = [7.5, 8.0]
    panel = long_sample.long_returns(french, curve, dgs10).set_index("date")
    assert pd.Timestamp("1971-08-16") not in panel.index
    expected = proxies.ty_zero_10(curve, french.RF / 100)
    np.testing.assert_allclose(
        panel.loc["1971-08-17":, "r_ty"], expected.loc["1971-08-17":]
    )
    assert abs(panel.loc["1971-08-17", "r_ty"]) < 0.001
    omitted = long_sample.long_returns(french, curve, dgs10, pre_1971="omit")
    assert omitted.date.min() == pd.Timestamp("1971-08-17")


def test_missing_quote_is_not_filled():
    french, curve, dgs10 = source_fixture()
    dgs10.loc["1962-01-08"] = np.nan
    panel = long_sample.long_returns(french, curve, dgs10)
    assert not panel.date.isin(pd.to_datetime(["1962-01-08", "1962-01-09"])).any()
    with pytest.raises(ValueError, match="pre_1971"):
        long_sample.long_returns(french, curve, dgs10, pre_1971="invent")


def test_demo_runner_writes_contract_and_lineage(tmp_path, monkeypatch, planted):
    panel, frame, _ = planted
    monkeypatch.setattr(long_sample, "output_dir", lambda kind: tmp_path)
    monkeypatch.setattr(long_sample, "demo_inputs", lambda **kwargs: (panel, frame))
    csv, metadata = long_sample.run(demo=True)
    table = pd.read_csv(csv, dtype={"column": str})
    assert list(table.columns) == TABLE_COLUMNS
    assert set(table.column) == {"1", "2", "3"}
    lineage = json.loads(metadata.read_text())
    assert lineage["demo"] is True
    assert lineage["terms"] == long_sample.TERMS
    assert len(lineage["samples"]) == 3


def test_latest_endpoint(planted):
    panel, frame, _ = planted
    table = long_sample.build_table(frame, panel, end="latest")
    assert table.loc[table.column == "1", "sample_end"].eq("2023-12-29").all()
