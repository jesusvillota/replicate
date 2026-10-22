"""Run: uv run python3 -m rebal.fetch.french

CLI arguments: --help shows usage.

Read five official French daily ZIPs. Save unchanged archives and tidy CSVs
under data/public/french, with ISO dates and original percent units.
Processing only; keep the full published history.
"""

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

BASE_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FILES = {
    "F-F_Research_Data_Factors_daily": ["Mkt-RF", "SMB", "HML", "RF"],
    "F-F_Research_Data_5_Factors_2x3_daily": [
        "Mkt-RF",
        "SMB",
        "HML",
        "RMW",
        "CMA",
        "RF",
    ],
    "F-F_Momentum_Factor_daily": ["Mom"],
    "F-F_ST_Reversal_Factor_daily": ["ST_Rev"],
    "F-F_LT_Reversal_Factor_daily": ["LT_Rev"],
}


def daily_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y%m%d")


def read_factors(path: Path, columns: list[str]) -> tuple[pd.DataFrame, int]:
    """Read only the first daily block, rejecting changed schemas and bad rows."""
    with ZipFile(path) as archive:
        members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if len(members) != 1:
            raise ValueError(f"{path}: expected exactly one CSV in the archive")
        lines = archive.read(members[0]).decode("utf-8-sig").splitlines()
    rows = list(csv.reader(lines))
    header = next(
        (
            i
            for i, row in enumerate(rows)
            if row and not row[0].strip() and [v.strip() for v in row[1:]] == columns
        ),
        None,
    )
    if header is None:
        raise ValueError(f"{path}: missing daily header {columns}")
    records = []
    for row in rows[header + 1 :]:
        if not row or not row[0].strip():
            break
        day = row[0].strip()
        if not re.fullmatch(r"\d{8}", day):
            # Annual/monthly blocks and publisher footers are not daily returns.
            if re.fullmatch(r"\d{4}|\d{6}", day) or not day[0].isdigit():
                break
            raise ValueError(f"{path}: invalid daily date {day!r}")
        if len(row) != len(columns) + 1:
            raise ValueError(f"{path}: wrong number of daily values on {day}")
        values = [float(value.strip()) for value in row[1:]]
        records.append(
            [
                daily_date(day),
                *[None if value in {-99.99, -999.0} else value for value in values],
            ]
        )
    # pandas: small source-file parsing and validation, no analytical computation.
    frame = pd.DataFrame(records, columns=["date", *columns])
    first = (
        "1961-06-16"
        if columns == FILES["F-F_Research_Data_Factors_daily"]
        else "1997-09-10"
    )
    coverage = {column: (first, "2023-03-17") for column in columns}
    return validate(frame, columns, coverage), header


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("french")
    for name, columns in FILES.items():
        raw = download(f"{BASE_URL}{name}_CSV.zip", directory / f"{name}_CSV.zip")
        frame, header = read_factors(raw, columns)
        check_size(raw)
        summarize(
            raw,
            "date",
            skiprows=header,
            header=0,
            names=["date", *columns],
            nrows=len(frame),
            converters={"date": daily_date},
        )
        store(frame, directory / f"{name}.csv")


if __name__ == "__main__":
    main()
