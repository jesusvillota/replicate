"""Run: uv run python3 -m rebal.fetch.ofr

CLI arguments: --help shows usage.

Save the OFR Financial Stress Index CSV unchanged, plus a tidy CSV with all
categories and regions. Retain the published contribution units.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

URL = "https://www.financialresearch.gov/financial-stress-index/data/fsi.csv"
COLUMNS = [
    "OFR FSI",
    "Credit",
    "Equity valuation",
    "Safe assets",
    "Funding",
    "Volatility",
    "United States",
    "Other advanced economies",
    "Emerging markets",
]


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small source-file parsing and validation only.
    frame = pd.read_csv(path).rename(columns={"Date": "date"})
    return validate(frame, COLUMNS, {"Funding": ("2000-01-03", "2023-03-17")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("ofr")
    raw = download(URL, directory / "fsi.raw.csv")
    frame = read_index(raw)
    check_size(raw)
    summarize(raw, "Date")
    store(frame, directory / "fsi.csv")


if __name__ == "__main__":
    main()
