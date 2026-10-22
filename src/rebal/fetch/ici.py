"""Run: uv run python3 -m rebal.fetch.ici

CLI arguments: --refresh-archives downloads immutable snapshots again.

Fetch ICI's original Excel/PDF tables, using archived official bytes if blocked.
Write weekly flows in USD millions outside git. Processing only.
"""

import argparse
import base64
import csv
import hashlib
import json
import re
from datetime import date
from itertools import pairwise
from pathlib import Path
from urllib.parse import unquote, urlparse

import pandas as pd
import requests
from pypdf import PdfReader
from rich.console import Console

from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

LIVE_URL = "https://www.ici.org/flows_data_2026.xls"
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


def read_pdf_rows(text: str) -> pd.DataFrame:
    """Parse the published nine-column PDF table after its weekly marker only."""
    marker = "Estimated Weekly Net New Cash Flow"
    if text.count(marker) != 1 or "(Dollar Figures in Millions)" not in text:
        raise ValueError("Unexpected ICI PDF section or units")
    header = text.split("Monthly Net New Cash Flow")[0]
    labels = re.sub(r"\s+", " ", header)
    if not re.search(
        r"Total Domestic (Foreign|World).*Total Taxable Municipal", labels
    ):
        raise ValueError("Unexpected ICI PDF category headers")
    if "Date Equity Equity Equity Hybrid Bond Bond Bond Total" not in labels:
        raise ValueError("Unexpected ICI PDF column headers")
    rows = []
    for line in text.split(marker)[1].splitlines():
        fields = line.split()
        if not fields or not re.fullmatch(
            r"\d{1,2}/\d{1,2}/(?:\d{4}|\d{2})", fields[0]
        ):
            continue
        if len(fields) != 9:
            raise ValueError(f"Unexpected ICI PDF weekly row: {line}")
        values = [int(value.replace(",", "")) for value in fields[1:]]
        rows.append(
            [
                pd.to_datetime(
                    fields[0],
                    format=(
                        "%m/%d/%Y" if len(fields[0].split("/")[-1]) == 4 else "%m/%d/%y"
                    ),
                ),
                *[values[index] for index in (0, 1, 2, 3, 5, 6, 7)],
            ]
        )
    return pd.DataFrame(rows, columns=["date", *COLUMNS])


def read_weekly(path: Path) -> pd.DataFrame:
    # pandas: Excel layout parsing; no resampling or analytical computation.
    if path.suffix == ".pdf":
        text = "\n".join(
            page.extract_text(
                extraction_mode="layout", layout_mode_space_vertically=False
            )
            for page in PdfReader(path).pages
        )
        return validate_weekly(read_pdf_rows(text))
    book = pd.ExcelFile(path)
    sheet = "Weekly MF Flow Estimates"
    if sheet not in book.sheet_names:
        if len(book.sheet_names) != 1:
            raise ValueError("Unexpected ICI workbook sheets")
        sheet = book.sheet_names[0]
    raw = pd.read_excel(book, sheet_name=sheet, header=None)
    if raw.shape[1] == 9:
        units = "(Dollar Figures in Millions)"
        positions = [1, 2, 3, 4, 6, 7, 8]
        headers = {
            (4, 1): "Total",
            (4, 2): "Domestic",
            (4, 3): ("Foreign", "World"),
            (4, 5): "Total",
            (4, 6): "Taxable",
            (4, 7): "Municipal",
            (5, 0): "Date",
            (5, 1): "Equity",
            (5, 2): "Equity",
            (5, 3): "Equity",
            (5, 4): "Hybrid",
            (5, 5): "Bond",
            (5, 6): "Bond",
            (5, 7): "Bond",
            (5, 8): "Total",
        }
    elif raw.shape[1] == 40:
        units = ("Millions, U.S. dollars", "Millions, U.S. dolllars")
        positions = POSITIONS
        headers = {
            (4, 1): "Total     long-term",
            (5, 3): "Total equity",
            (6, 5): "Total domestic",
            (6, 17): "Total world",
            (4, 23): "Hybrid",
            (6, 27): "Total taxable",
            (5, 39): "Municipal",
        }
    else:
        raise ValueError("Unexpected ICI workbook layout")
    accepted_units = units if isinstance(units, tuple) else (units,)
    if raw.iat[2, 0] not in accepted_units:
        raise ValueError("Unexpected ICI workbook units")
    for (row, column), expected in headers.items():
        accepted = expected if isinstance(expected, tuple) else (expected,)
        if raw.iat[row, column] not in accepted:
            raise ValueError(f"ICI column changed: expected {expected}")
    markers = raw.index[raw[0].eq("Estimated Weekly Net New Cash Flow")]
    if len(markers) != 1:
        raise ValueError("Expected one weekly section; never use monthly actuals")
    rows = raw.iloc[markers[0] + 1 :]
    dates = pd.to_datetime(rows[0], format="mixed", errors="coerce")
    rows = rows.loc[dates.notna()]
    result = rows[positions].copy()
    result.columns = COLUMNS
    result.insert(0, "date", dates.loc[rows.index])
    result[COLUMNS] = result[COLUMNS].apply(pd.to_numeric, errors="raise")
    return validate_weekly(result)


def validate_weekly(result: pd.DataFrame) -> pd.DataFrame:
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


def archive_path(directory: Path, snapshot: str, original_url: str) -> Path:
    name = unquote(urlparse(original_url).path.split("/")[-1]).split(":")[-1]
    return directory / f"{Path(name).stem}.{snapshot}.raw{Path(name).suffix}"


def fetch_archive(
    directory: Path, source: dict, *, refresh: bool = False
) -> tuple[Path, str]:
    """Keep verified immutable published bytes; try alternate archive replay routes."""
    snapshot, original = source["snapshot"], source["original_url"]
    path = archive_path(directory, snapshot, original)
    canonical = f"https://web.archive.org/web/{snapshot}id_/{original}"

    def validate() -> None:
        digest = base64.b32encode(hashlib.sha1(path.read_bytes()).digest()).decode()
        if digest != source["sha1_base32"]:
            raise ValueError(f"ICI archive bytes differ from CDX digest: {path}")

    if path.exists() and not refresh:
        validate()
        return path, canonical
    normalized = original.replace("https://", "http://").replace(":80/", "/")
    urls = [
        canonical,
        f"http://web.archive.org/web/{snapshot}id_/{original}",
        f"https://web.archive.org/web/{snapshot}if_/{normalized}",
    ]
    for index, url in enumerate(urls):
        try:
            download(url, path, retries=0)
        except requests.RequestException:
            if index == len(urls) - 1:
                raise
        else:
            validate()
            return path, url
    raise AssertionError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh-archives",
        action="store_true",
        help="Redownload immutable archived originals instead of using verified files",
    )
    args = parser.parse_args()
    directory = licensed_dir("ici")
    frames = []
    sources = []
    files = []
    with Path(__file__).with_name("ici_archives.csv").open() as handle:
        archives = list(csv.DictReader(handle))
    # The manifest is ordered by archive publication time, across all ICI paths.
    for source in archives:
        raw, url = fetch_archive(directory, source, refresh=args.refresh_archives)
        frame = read_weekly(raw)
        frames.append(frame)
        sources.append(
            {
                **source,
                "url": url,
                "file": raw.name,
                "rows": len(frame),
                "first": str(frame.date.min().date()),
                "last": str(frame.date.max().date()),
            }
        )
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
        sources.append({"url": LIVE_URL, "file": raw.name})
        files.append(raw.name)
    # pandas: tiny source-vintage reconciliation, keeping the latest publication.
    frame = pd.concat(frames).drop_duplicates("date", keep="last").sort_values("date")
    output = directory / "ici_weekly_flows.csv"
    frame.to_csv(output, index=False, date_format="%Y-%m-%d")
    summarize(output, "date")
    # pandas: source-coverage metadata only; preserve holiday week-ending dates.
    blocks = []
    for reported in frame.date:
        if not blocks or (reported - pd.Timestamp(blocks[-1]["last"])).days > 8:
            blocks.append(
                {"first": str(reported.date()), "last": str(reported.date()), "rows": 1}
            )
        else:
            blocks[-1]["last"] = str(reported.date())
            blocks[-1]["rows"] += 1
    missing = [
        {
            "first": "2007-01-01",
            "last": str((frame.date.min() - pd.Timedelta(days=1)).date()),
        }
    ]
    for left, right in pairwise(blocks):
        missing.append(
            {
                "first": str(
                    (pd.Timestamp(left["last"]) + pd.Timedelta(days=1)).date()
                ),
                "last": str(
                    (pd.Timestamp(right["first"]) - pd.Timedelta(days=1)).date()
                ),
            }
        )
    metadata = {
        "downloaded": str(date.today()),
        "sources": sources,
        "live_url": LIVE_URL,
        "files": [*files, output.name],
        "units": "USD millions",
        "first": str(frame.date.min().date()),
        "last": str(frame.date.max().date()),
        "rows": len(frame),
        "coverage_blocks": blocks,
        "missing_intervals": missing,
    }
    (directory / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
