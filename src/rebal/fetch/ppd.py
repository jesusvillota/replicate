"""Run: uv run python3 -m rebal.fetch.ppd

CLI arguments: --help shows usage.

Fetch CRR's full PPD CSV and detailed investment workbook unchanged. Write a
plan-year CSV in original units and an annual coverage CSV. Processing only.
"""

import argparse
import json
import re
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlencode

import numpy as np
import pandas as pd
from rich.console import Console

from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

SCRIPT_URL = "https://publicplansdata.org/wp-content/themes/publicplans2024/js/ppd.js"
DETAIL_URL = "https://publicplansdata.org/wp-content/uploads/2024/09/PensionInvestmentPerformanceDetailed.xlsx"
CODEBOOK_URL = "https://publicplansdata.org/api/?q=gettemplate&template=data-codebook&format=csv&filename=ppd-codebook.csv&includeheader=1"
DETAIL_CODEBOOK_URL = (
    "https://publicplansdata.org/wp-content/uploads/2013/12/Investment-Codebook.xlsx"
)
TOTALS = [
    f"{asset}_{kind}"
    for asset in ("EQTotal", "FITotal", "CashTotal")
    for kind in ("Actl", "Trgt")
]
GEOGRAPHY = [
    f"{asset}_{kind}"
    for asset in (
        "EQDomesticMisc",
        "EQDomesticLarge",
        "EQDomesticMid",
        "EQDomesticSmall",
        "EQIntlMisc",
        "EQIntlDev",
        "EQIntlEmerg",
        "EQIntlPass",
        "EQIntlActv",
        "EQGlobal",
        "EQGlobalGrowth",
    )
    for kind in ("Actl", "Trgt")
]
BASE = ["ppd_id", "PlanName", "fy", "MktAssets_net", *TOTALS]


def read_allocations(raw: Path, detailed: Path) -> pd.DataFrame:
    # pandas: small CSV/Excel parsing, projection and key validation; no analysis.
    frame = pd.read_csv(raw, encoding="cp1252", usecols=BASE)
    detail = pd.read_excel(detailed, usecols=["ppd_id", "fy", *GEOGRAPHY])
    for source in (frame, detail):
        source["fy"] = pd.to_numeric(source.fy, errors="raise")
        source.drop(source.index[~source.fy.between(2003, 2022)], inplace=True)
        if source[["ppd_id", "fy"]].isna().any().any():
            raise ValueError("Missing plan-year key")
        if source.duplicated(["ppd_id", "fy"]).any():
            raise ValueError("Duplicate plan-year key")
        if not source.fy.eq(source.fy.astype(int)).all():
            raise ValueError("Fiscal years must be integers")
    frame = frame.merge(detail, on=["ppd_id", "fy"], how="left", validate="one_to_one")
    frame = frame[[*BASE, *GEOGRAPHY]].sort_values(["fy", "ppd_id"])
    if set(frame.fy) != set(range(2003, 2023)):
        raise ValueError("Expected every fiscal year 2003–2022")
    if frame.PlanName.isna().any():
        raise ValueError("Missing plan name")
    frame[["ppd_id", "fy"]] = frame[["ppd_id", "fy"]].astype(int)
    numeric = ["MktAssets_net", *TOTALS, *GEOGRAPHY]
    frame[numeric] = frame[numeric].apply(pd.to_numeric, errors="raise")
    if np.isinf(frame[numeric].to_numpy(dtype=float)).any():
        raise ValueError("Infinite assets or allocations")
    if frame[["MktAssets_net", *TOTALS]].isna().all().any():
        raise ValueError("An entire required main-dataset series is unavailable")
    for column in TOTALS:
        observed = set(frame.loc[frame[column].notna(), "fy"])
        if observed != set(range(2003, 2023)):
            raise ValueError(f"{column}: missing a required fiscal year")
    frame.insert(0, "date", pd.to_datetime(frame.fy.astype(str) + "-12-31"))
    return frame


def fetch() -> None:
    directory = public_dir("ppd")
    # The site's own full-download variable list includes all current fields.
    with TemporaryDirectory(prefix="ppd-download-") as temporary:
        script = download(SCRIPT_URL, Path(temporary) / "ppd.js")
        match = re.search(
            r'postargs\["variables"\]\s*=\s*"([^"]+)"', script.read_text()
        )
    if match is None:
        raise ValueError("Cannot locate CRR's full-dataset variable list")
    query = urlencode(
        {
            "a": "data-download",
            "q": "QVariables",
            "variables": match[1],
            "filtereegroupid": 0,
            "filtertierid": 0,
            "filename": "ppd-data-latest",
            "format": "csv",
        }
    )
    url = "https://publicplansdata.org/api/?" + query
    raw = download(url, directory / "ppd_full.raw.csv")
    detail = download(DETAIL_URL, directory / "investment_detail.raw.xlsx")
    codebook = download(CODEBOOK_URL, directory / "codebook.raw.csv")
    detail_codebook = download(
        DETAIL_CODEBOOK_URL, directory / "investment_codebook.raw.xlsx"
    )
    frame = read_allocations(raw, detail)
    output = directory / "ppd_allocations.csv"
    frame.to_csv(output, index=False, date_format="%Y-%m-%d")
    # Re-read the written panel; dates repeat across plans, but keys must not.
    stored = pd.read_csv(output)
    if stored.duplicated(["ppd_id", "fy"]).any() or len(stored) != len(frame):
        raise ValueError("Written panel failed plan-year validation")
    # summarize requires unique dates: use the annual coverage companion file.
    coverage = frame.groupby("date").size().rename("plan_count").reset_index()
    coverage_path = directory / "ppd_coverage.csv"
    coverage.to_csv(coverage_path, index=False, date_format="%Y-%m-%d")
    summarize(coverage_path, "date")
    paths = [raw, detail, codebook, detail_codebook, output, coverage_path]
    for path in paths:
        if path.stat().st_size >= 20_000_000:
            raise ValueError(f"{path}: exceeds 20 MB; retain only required columns")
    metadata = {
        "downloaded": str(date.today()),
        "sources": [url, DETAIL_URL, CODEBOOK_URL, DETAIL_CODEBOOK_URL, SCRIPT_URL],
        "files": [p.name for p in paths],
        "rows": len(frame),
        "fiscal_years": [2003, 2022],
        "allocation_variables": [*TOTALS, *GEOGRAPHY],
    }
    (directory / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    Console().print(
        f"OK {output} rows={len(frame)} fiscal_years=2003–2022",
        markup=False,
        highlight=False,
        soft_wrap=True,
    )


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    fetch()


if __name__ == "__main__":
    main()
