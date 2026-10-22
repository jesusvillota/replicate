"""Synthetic calendar, rate, missing-value and contract checks for TASK-012."""

import io

import numpy as np
import pandas as pd
import pytest
from rich.console import Console

from rebal import panel
from rebal.demo import make_panel
from rebal.paths import REPO_ROOT


def test_bill_actual_days_and_percent_conversion():
    dates = pd.to_datetime(["2023-03-10", "2023-03-13", "2023-03-14"])
    quote = pd.Series([3.6, 7.2, 9.0], index=dates)
    result = panel.bill_return(quote, dates)
    np.testing.assert_allclose(result.iloc[:2], [0.0003, 0.0002])
    assert pd.isna(result.iloc[-1])  # No invented next trading day.


def test_controls_fill_at_most_five_trading_days():
    dates = pd.bdate_range("2023-03-03", periods=10)
    raw = pd.Series([np.nan, 8, *([np.nan] * 7), 9], index=dates)
    result = panel.align_series(raw, dates, control=True)
    assert pd.isna(result.iloc[0])  # No backfill.
    assert result.iloc[1:7].eq(8).all()  # Five fills, including a weekend.
    assert result.iloc[7:9].isna().all()
    assert result.iloc[9] == 9


def test_returns_and_factors_never_fill():
    dates = pd.bdate_range("2023-03-06", periods=4)
    source = pd.Series([0.01, -0.02], index=dates[[0, 3]])
    result = panel.align_series(source, dates)
    assert result.iloc[1:3].isna().all()
    pd.testing.assert_series_equal(result.dropna(), source)


def test_calendar_drops_all_september_closures_and_missing_core_returns():
    dates = pd.bdate_range("2001-09-07", "2001-09-19")
    es = pd.Series(0.01, index=dates)
    ty = pd.Series(0.02, index=dates)
    ty.loc["2001-09-18"] = np.nan
    expected = pd.to_datetime(["2001-09-07", "2001-09-10", "2001-09-17", "2001-09-19"])
    pd.testing.assert_index_equal(panel.trading_calendar(es, ty), expected)
    assert pd.isna(ty.loc["2001-09-18"])


def test_contract_columns_match_document():
    rows = (REPO_ROOT / "docs/contracts/daily_panel.md").read_text().splitlines()
    schema = {
        cells[0]: cells[1]
        for row in rows
        if row.startswith("| ") and not row.startswith("| Column ")
        for cells in [[c.strip() for c in row.split("|")[1:-1]]]
    }
    assert tuple(schema) == panel.COLUMNS
    assert schema["date"] == "datetime64[ns]"
    assert set(list(schema.values())[1:]) == {"float64"}


@pytest.fixture
def valid_panel():
    frame = make_panel(start="1997-09-09", end="2023-03-20")
    return frame.loc[~frame.date.between("2001-09-11", "2001-09-14")].reset_index(
        drop=True
    )


def test_validation_allows_optional_gaps(valid_panel):
    valid_panel["move"] = np.nan
    panel.validate_panel(valid_panel)
    lines = panel.coverage_lines(valid_panel)
    assert any("move: none to none; NaN=100.00%" in line for line in lines)
    assert any(
        "r_es:" in line and "study=1997-09-10 to 2023-03-17" in line for line in lines
    )


@pytest.mark.parametrize(
    "problem",
    [
        "missing_core",
        "factor_gap",
        "endpoint",
        "duplicate",
        "unsorted",
        "time",
        "dtype",
        "extra",
        "infinite",
        "market",
    ],
)
def test_validation_rejects_broken_panels(valid_panel, problem):
    frame = valid_panel.copy()
    if problem == "missing_core":
        frame.loc[0, "r_ty"] = np.nan
    elif problem == "factor_gap":
        frame.loc[2, "q_eg"] = np.nan
    elif problem == "endpoint":
        frame = frame.loc[frame.date.ne(panel.START)]
    elif problem == "duplicate":
        frame.loc[1, "date"] = frame.loc[0, "date"]
    elif problem == "unsorted":
        frame = frame.iloc[::-1]
    elif problem == "time":
        frame.loc[0, "date"] += pd.Timedelta(hours=1)
    elif problem == "dtype":
        frame["rf"] = frame.rf.astype("float32")
    elif problem == "extra":
        frame["extra"] = 0.0
    elif problem == "infinite":
        frame.loc[0, "ara"] = np.inf
    else:
        frame.loc[0, "r_mkt_french"] += 0.1
    with pytest.raises(ValueError):
        panel.validate_panel(frame)


def test_check_reopens_both_parquets_and_rejects_alternative_changes(
    tmp_path, monkeypatch, valid_panel
):
    monkeypatch.setattr(panel, "processed_dir", lambda: tmp_path)
    for name in ("daily_panel", "daily_panel_alt"):
        valid_panel.to_parquet(tmp_path / f"{name}.parquet", index=False)
    output = io.StringIO()
    panel.check(Console(file=output, width=160))
    assert output.getvalue().rstrip().endswith("PANEL OK")
    assert "rows=" in output.getvalue() and "regression N=6226" in output.getvalue()
    other = valid_panel.copy()
    other.loc[0, "epu"] += 1
    other.to_parquet(tmp_path / "daily_panel_alt.parquet", index=False)
    with pytest.raises(AssertionError):
        panel.check(Console(file=io.StringIO()))
