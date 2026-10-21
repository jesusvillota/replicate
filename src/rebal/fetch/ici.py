"""Run: uv run python3 -m rebal.fetch.ici

CLI arguments: --help shows usage.

Fetch ICI's original Excel workbook, using archived official bytes if blocked.
Write weekly flows in USD millions outside git. Processing only.
"""

import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd
import requests
from rich.console import Console

from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

LIVE_URL = "https://www.ici.org/flows_data_2026.xls"
ARCHIVES = [
    ("20251126095130", 2025),
    ("20260115002828", 2026),
    ("20260227055331", 2026),
    ("20260412002219", 2026),
]
COLUMNS = [
    "total_equity",
    "domestic_equity",
    "world_equity",
    "hybrid",
    "taxable_bond",
    "municipal_bond",
    "total",
]
# Published workbook uses empty spacer columns between the numeric columns.
POSITIONS = [3, 5, 17, 23, 27, 39, 1]


def read_weekly(path: Path) -> pd.DataFrame:
    # pandas: Excel layout parsing; no resampling or analytical computation.
    raw = pd.read_excel(path, sheet_name="Weekly MF Flow Estimates", header=None)
    if raw.shape[1] != 40 or raw.iat[2, 0] != "Millions, U.S. dollars":
        raise ValueError("Unexpected ICI workbook layout or units")
    headers = {
        (4, 1): "Total     long-term",
        (5, 3): "Total equity",
        (6, 5): "Total domestic",
        (6, 17): "Total world",
        (4, 23): "Hybrid",
        (6, 27): "Total taxable",
        (5, 39): "Municipal",
    }
    for (row, column), expected in headers.items():
        if raw.iat[row, column] != expected:
            raise ValueError(f"ICI column changed: expected {expected}")
    markers = raw.index[raw[0].eq("Estimated Weekly Net New Cash Flow")]
    if len(markers) != 1:
        raise ValueError("Expected one weekly section; never use monthly actuals")
    rows = raw.iloc[markers[0] + 1 :]
    dates = pd.to_datetime(rows[0], format="mixed", errors="coerce")
    rows = rows.loc[dates.notna()]
    result = rows[POSITIONS].copy()
    result.columns = COLUMNS
    result.insert(0, "date", dates.loc[rows.index])
    result[COLUMNS] = result[COLUMNS].apply(pd.to_numeric, errors="raise")
    if (
        result.empty
        or result.date.duplicated().any()
        or result[COLUMNS].isna().any().any()
    ):
        raise ValueError("Empty, duplicate or missing weekly observations")
    if (
        not result[COLUMNS]
        .map(lambda value: float("-inf") < value < float("inf"))
        .all()
        .all()
    ):
        raise ValueError("Nonfinite weekly flows")
    return result.sort_values("date").reset_index(drop=True)


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = licensed_dir("ici")
    frames = []
    sources = []
    files = []
    for snapshot, year in ARCHIVES:
        url = f"https://web.archive.org/web/{snapshot}id_/https://www.ici.org/flows_data_{year}.xls"
        raw = download(url, directory / f"flows_data_{year}.{snapshot}.raw.xls")
        frames.append(read_weekly(raw))
        sources.append(url)
        files.append(raw.name)
    raw = directory / "flows_data_2026.raw.xls"
    try:
        download(LIVE_URL, raw, retries=0)
    except requests.RequestException as exc:
        Console().print(
            f"ICI live download unavailable: {exc}; using archived originals."
        )
    else:
        frames.append(read_weekly(raw))
        sources.append(LIVE_URL)
        files.append(raw.name)
    # pandas: tiny source-vintage reconciliation, keeping the latest publication.
    frame = pd.concat(frames).drop_duplicates("date", keep="last").sort_values("date")
    output = directory / "ici_weekly_flows.csv"
    frame.to_csv(output, index=False, date_format="%Y-%m-%d")
    summarize(output, "date")
    metadata = {
        "downloaded": str(date.today()),
        "sources": sources,
        "live_url": LIVE_URL,
        "files": [*files, output.name],
        "units": "USD millions",
        "first": str(frame.date.min().date()),
        "last": str(frame.date.max().date()),
        "rows": len(frame),
    }
    (directory / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
