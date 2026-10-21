"""Source-format regressions: no monthly flows or lost plan-year keys."""

import numpy as np
import pandas as pd
import pytest

from rebal.fetch.ici import read_weekly
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


def test_ici_excludes_monthly_and_maps_categories(tmp_path):
    result = read_weekly(workbook(tmp_path))
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
