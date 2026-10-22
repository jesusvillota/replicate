"""Fetch MSCI ACWI ex USA: ``uv run python3 -m rebal.fetch.msci``.

CLI arguments: --start-date (default: 1997-01-01), --end-date (default: latest
published world date). Dates use YYYY-MM-DD.

Reads MSCI's public end-of-day Excel download. Writes the original workbook,
date/index-level CSV and metadata under licensed_dir("msci"). No return scaling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, date, datetime
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests
from rich.console import Console
from xlrd import XLRDError

from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

BASE_URL = "https://app2.msci.com/products/service/index/indexmaster/"
INDEX_CODE = "899901"
INDEX_NAME = "ACWI ex USA Standard (Large+Mid Cap)"
STEM = "acwi_ex_usa_net_usd"


def parse_workbook(path: Path, start: date, end: date) -> pd.DataFrame:
    """Reject a wrong index, return variant, currency or malformed observation."""
    # pandas: small published Excel input; schema validation and format conversion only.
    sheet = pd.read_excel(path, sheet_name="History Index", header=None, engine="xlrd")
    if sheet.shape[1] != 2:
        raise ValueError("MSCI: expected one date column and one index column")
    for label, expected in (
        ("Index Level :", "Net"),
        ("Currency :", "USD"),
        ("Date", INDEX_NAME),
    ):
        matches = sheet.loc[sheet[0].eq(label), 1]
        if len(matches) != 1 or matches.iloc[0] != expected:
            raise ValueError(
                f"MSCI: expected {label} {expected!r}; got {matches.tolist()}"
            )
    header = sheet.index[sheet[0].eq("Date")][0]
    table = sheet.iloc[header + 1 :].copy()
    # Published observations end at a blank row, followed by the license text.
    blanks = table.index[table.isna().all(axis=1)]
    if len(blanks):
        table = table.loc[: blanks[0] - 1]
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(table[0], format="%b %d, %Y", errors="raise"),
            STEM: pd.to_numeric(table[1], errors="raise"),
        }
    )
    if frame.empty or frame.isna().any().any() or (frame[STEM] <= 0).any():
        raise ValueError("MSCI: empty history, missing values or nonpositive levels")
    dates = frame["date"]
    if dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError("MSCI: duplicate or unsorted dates")
    if dates.min().date() < start or dates.max().date() > end:
        raise ValueError("MSCI: dates outside the requested range")
    return frame


def fetch(start: date, end: date | None, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    if end is None:
        latest = download(
            BASE_URL + "getLatestWorldDate", directory / "latest_world_date.txt"
        )
        end = datetime.strptime(latest.read_text().strip(), "%Y%m%d").date()
    if start > end:
        raise ValueError("MSCI: start date is after end date")
    params = {
        "output": "INDEX_LEVELS",
        "currency_symbol": "USD",
        "index_variant": "NETR",
        "start_date": start.strftime("%Y%m%d"),
        "end_date": end.strftime("%Y%m%d"),
        "data_frequency": "daily",
        "index_codes": INDEX_CODE,
    }
    url = BASE_URL + "downloadLevelData?" + urlencode(params)
    raw = download(url, directory / f"{STEM}.xls")
    frame = parse_workbook(raw, start, end)
    path = directory / f"{STEM}.csv"
    frame.to_csv(path, index=False, date_format="%Y-%m-%d")
    metadata = {
        "script": __name__,
        "downloaded_utc": datetime.now(UTC).isoformat(),
        "source": url,
        "index_code": INDEX_CODE,
        "index_name": INDEX_NAME,
        "variant": "NETR",
        "currency": "USD",
        "frequency": "daily",
        "requested_start": start.isoformat(),
        "requested_end": end.isoformat(),
        "rows": len(frame),
        "first": str(frame["date"].min().date()),
        "last": str(frame["date"].max().date()),
        "raw_sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
        "files": [raw.name, path.name],
    }
    path.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    summarize(path, "date")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--start-date",
        type=date.fromisoformat,
        default=date(1997, 1, 1),
        help="First requested date (default: 1997-01-01).",
    )
    parser.add_argument(
        "--end-date",
        type=date.fromisoformat,
        help="Last requested date (default: latest published world date).",
    )
    args = parser.parse_args()
    if args.end_date and args.start_date > args.end_date:
        parser.error("start date must not be after end date")
    directory = licensed_dir("msci")
    console = Console(highlight=False)
    console.log(f"Output: {directory}", markup=False)
    try:
        fetch(args.start_date, args.end_date, directory)
    except (requests.RequestException, ValueError, OSError, XLRDError):
        console.print_exception(show_locals=False)
        console.print("MSCI unavailable; see docs/data/cards/msci.md", markup=False)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
