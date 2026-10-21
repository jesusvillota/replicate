"""Run: uv run python3 -m rebal.fetch.epu

CLI arguments: --help shows usage. No API key is required.

Save the published US daily news EPU CSV and a tidy, original-unit CSV.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

URL = "https://www.policyuncertainty.com/media/All_Daily_Policy_Data.csv"


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small published file parsing and validation only.
    raw = pd.read_csv(path)
    if list(raw.columns) != ["day", "month", "year", "daily_policy_index"]:
        raise ValueError("Expected US daily news EPU columns")
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(raw[["year", "month", "day"]]),
            "epu": raw.daily_policy_index,
        }
    )
    return validate(frame, ["epu"], {"epu": ("1997-09-10", "2023-03-17")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("epu")
    raw = download(URL, directory / "All_Daily_Policy_Data.raw.csv")
    frame = read_index(raw)
    check_size(raw)
    summarize(raw, ["year", "month", "day"])
    store(frame, directory / "epu.csv")


if __name__ == "__main__":
    main()
