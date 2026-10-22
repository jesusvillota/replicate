"""Run: uv run python3 -m rebal.fetch.ads

CLI arguments: --help shows usage. No API key is required.

Save the Philadelphia Fed's latest ADS vintage and a tidy original-unit CSV.
This is a revised historical series, not a real-time vintage.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

URL = (
    "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/ads/"
    "ADS_Index_Most_Current_Vintage.xlsx"
)


def parse_date(value: str) -> pd.Timestamp:
    return pd.to_datetime(value, format="%Y:%m:%d", errors="raise")


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small workbook parsing; RECBARS is preserved in the raw workbook.
    raw = pd.read_excel(path, sheet_name="Sheet1")
    if list(raw.columns) != ["Date", "ADS_Index", "RECBARS"]:
        raise ValueError("Expected ADS latest-vintage columns")
    frame = raw[["Date", "ADS_Index"]].rename(
        columns={"Date": "date", "ADS_Index": "ads"}
    )
    frame["date"] = pd.to_datetime(frame.date, format="%Y:%m:%d", errors="raise")
    return validate(frame, ["ads"], {"ads": ("1997-09-10", "2023-03-17")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("ads")
    raw = download(URL, directory / "ADS_Index_Most_Current_Vintage.xlsx")
    frame = read_index(raw)
    check_size(raw)
    summarize(raw, "Date", sheet_name="Sheet1", converters={"Date": parse_date})
    store(frame, directory / "ads.csv")


if __name__ == "__main__":
    main()
