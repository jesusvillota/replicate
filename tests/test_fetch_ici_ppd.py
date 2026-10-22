"""Source-format regressions: no monthly flows or lost plan-year keys."""

import base64
import hashlib

import numpy as np
import pandas as pd
import pytest

from rebal.fetch.ici import (
    archive_path,
    fetch_archive,
    read_pdf_rows,
    read_weekly,
    validate_weekly,
)
from rebal.fetch.ppd import BASE, GEOGRAPHY, read_allocations


def workbook(tmp_path):
    rows = [[None] * 40 for _ in range(13)]
    rows[2][0] = "Millions, U.S. dollars"
    rows[4][1] = "Total     long-term"
    rows[5][3] = "Total equity"
    rows[6][5] = "Total domestic"
    rows[6][17] = "Total world"
    rows[4][23] = "Hybrid"
    rows[6][27] = "Total taxable"
    rows[5][39] = "Municipal"
    rows[8] = ["12/31/2025", *([999999] * 39)]
    rows[9][0] = "Estimated Weekly Net New Cash Flow"
    # Holiday weeks can end on Tuesdays. Values distinguish every column.
    rows[10] = ["12/23/2025", *range(1, 40)]
    rows[11] = ["12/30/2025", *range(-1, -40, -1)]
    rows[12][0] = "Note: weekly estimates, monthly actuals."
    path = tmp_path / "ici.xlsx"
    pd.DataFrame(rows).to_excel(
        path, sheet_name="Weekly MF Flow Estimates", header=False, index=False
    )
    return path


@pytest.mark.parametrize("units", ["Millions, U.S. dollars", "Millions, U.S. dolllars"])
def test_ici_excludes_monthly_and_maps_categories(tmp_path, units):
    path = workbook(tmp_path)
    frame = pd.read_excel(path, header=None)
    frame.iat[2, 0] = units
    frame.to_excel(
        path, sheet_name="Weekly MF Flow Estimates", header=False, index=False
    )
    result = read_weekly(path)
    assert result.date.dt.strftime("%Y-%m-%d").tolist() == ["2025-12-23", "2025-12-30"]
    assert result.iloc[0, 1:].tolist() == [3, 5, 17, 23, 27, 39, 1]
    assert result.iloc[1, 1:].tolist() == [-3, -5, -17, -23, -27, -39, -1]


def test_ici_rejects_changed_schema(tmp_path):
    path = workbook(tmp_path)
    frame = pd.read_excel(path, header=None)
    frame.iloc[2, 0] = "Billions, U.S. dollars"
    frame.to_excel(
        path, sheet_name="Weekly MF Flow Estimates", header=False, index=False
    )
    with pytest.raises(ValueError, match="units"):
        read_weekly(path)


@pytest.mark.parametrize("world_header", ["Foreign", "World"])
def test_ici_legacy_layout_excludes_monthly_and_maps_bond_columns(
    tmp_path, world_header
):
    rows = [[None] * 9 for _ in range(13)]
    rows[2][0] = "(Dollar Figures in Millions)"
    rows[4] = [
        None,
        "Total",
        "Domestic",
        world_header,
        None,
        "Total",
        "Taxable",
        "Municipal",
        None,
    ]
    rows[5] = [
        "Date",
        "Equity",
        "Equity",
        "Equity",
        "Hybrid",
        "Bond",
        "Bond",
        "Bond",
        "Total",
    ]
    rows[7] = ["2015-01-31", *([999999] * 8)]
    rows[8][0] = "Estimated Weekly Net New Cash Flow"
    rows[9] = ["2015-02-04", 10, 4, 6, -3, 20, 18, 2, 27]
    rows[10] = ["2015-02-11", -10, -4, -6, 3, -20, -18, -2, -27]
    rows[12][0] = "Weekly cash flows are estimates"
    path = tmp_path / "legacy.xlsx"
    pd.DataFrame(rows).to_excel(
        path, sheet_name="aggregate_summary012109", header=False, index=False
    )
    result = read_weekly(path)
    assert result.date.dt.strftime("%Y-%m-%d").tolist() == ["2015-02-04", "2015-02-11"]
    assert result.iloc[0, 1:].tolist() == [10, 4, 6, -3, 18, 2, 27]
    assert result.iloc[1, 1:].tolist() == [-10, -4, -6, 3, -18, -2, -27]
    frame = pd.read_excel(path, header=None)
    frame.iat[5, 6] = "Equity"
    frame.to_excel(
        path, sheet_name="aggregate_summary012109", header=False, index=False
    )
    with pytest.raises(ValueError, match="column changed"):
        read_weekly(path)


def ppd_inputs(tmp_path):
    frame = pd.DataFrame({name: [0.25] * 20 for name in BASE})
    frame["ppd_id"] = 1
    frame["fy"] = list(range(2003, 2023))
    frame["PlanName"] = "Test plan"
    frame["MktAssets_net"] = 123456
    detail = pd.DataFrame({name: [np.nan] * 20 for name in GEOGRAPHY})
    detail["ppd_id"] = 1
    detail["fy"] = frame.fy
    detail["EQDomesticMisc_Actl"] = 0.123
    raw = tmp_path / "full.csv"
    detailed = tmp_path / "detail.xlsx"
    frame.to_csv(raw, index=False)
    detail.to_excel(detailed, index=False)
    return raw, detailed


def test_ppd_preserves_units_missing_targets_and_fiscal_years(tmp_path):
    result = read_allocations(*ppd_inputs(tmp_path))
    assert result.fy.tolist() == list(range(2003, 2023))
    assert result.MktAssets_net.eq(123456).all()
    assert result.EQTotal_Actl.eq(0.25).all()
    assert result.EQDomesticMisc_Actl.eq(0.123).all()
    assert result.EQIntlActv_Trgt.isna().all()
    assert not result.duplicated(["ppd_id", "fy"]).any()


@pytest.mark.parametrize("problem", ["duplicate", "missing_year", "missing_allocation"])
def test_ppd_rejects_invalid_panel(tmp_path, problem):
    raw, detailed = ppd_inputs(tmp_path)
    frame = pd.read_csv(raw)
    if problem == "duplicate":
        frame = pd.concat([frame, frame.iloc[:1]])
    elif problem == "missing_year":
        frame = frame.iloc[1:]
    else:
        frame.loc[frame.fy.eq(2003), "EQTotal_Actl"] = np.nan
    frame.to_csv(raw, index=False)
    with pytest.raises(ValueError):
        read_allocations(raw, detailed)


@pytest.mark.parametrize("day", ["12/23/08", "12/23/2008"])
def test_ici_pdf_preserves_old_dates_and_excludes_monthly(day):
    text = f"""Investment Company Institute
(Dollar Figures in Millions)
Total Domestic Foreign Total Taxable Municipal
Date Equity Equity Equity Hybrid Bond Bond Bond Total
Monthly Net New Cash Flow
1/31/2007 999 999 999 999 999 999 999 999
Estimated Weekly Net New Cash Flow
{day} -10 -4 -6 3 -20 -18 -2 -27
Weekly cash flows are estimates.
"""
    result = validate_weekly(read_pdf_rows(text))
    assert result.date.dt.strftime("%Y-%m-%d").tolist() == ["2008-12-23"]
    assert result.iloc[0, 1:].tolist() == [-10, -4, -6, 3, -18, -2, -27]
    with pytest.raises(ValueError, match="weekly row"):
        read_pdf_rows(text.replace(" -27", ""))
    with pytest.raises(ValueError, match="units"):
        read_pdf_rows(text.replace("Millions", "Billions"))


def test_ici_immutable_cache_validates_published_digest(tmp_path, monkeypatch):
    payload = b"published workbook bytes"
    source = {
        "snapshot": "20150405035035",
        "original_url": "http://www.ici.org/info/flows_data_2015.xls",
        "sha1_base32": base64.b32encode(hashlib.sha1(payload).digest()).decode(),
    }
    path = archive_path(tmp_path, source["snapshot"], source["original_url"])
    path.write_bytes(payload)

    def unexpected_download(*args, **kwargs):
        pytest.fail("Verified immutable archives should not need network access")

    monkeypatch.setattr("rebal.fetch.ici.download", unexpected_download)
    assert fetch_archive(tmp_path, source)[0] == path
    path.write_bytes(b"different archive capture")
    with pytest.raises(ValueError, match="CDX digest"):
        fetch_archive(tmp_path, source)
