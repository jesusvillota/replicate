"""Run: uv run python3 -m rebal.fetch.ara

CLI arguments: --help shows usage. REPLICATE_DATA_DIR controls external storage.

Save the authors' public ARA ZIP (including its README) and original-unit CSV
outside git. No scaling or extension beyond its published 2004–2019 history.
"""

import argparse
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

URL = (
    "https://www.dropbox.com/scl/fo/xpi0irqtlnxq6rbre06k5/"
    "AH-eVcrOnGbSKMSBdSG0nEA?rlkey=y61un7nk0j45bny0z0yb8b4np&raw=1"
)


def read_index(path: Path) -> pd.DataFrame:
    # pandas: parse the small published CSV; retain the ZIP and its README intact.
    with ZipFile(path) as archive, archive.open("ARA.csv") as member:
        frame = pd.read_csv(member)
    if list(frame.columns) != ["date", "ara"]:
        raise ValueError("Expected published ARA date and attention columns")
    frame["date"] = pd.to_datetime(frame.date, format="%d%b%Y", errors="raise")
    return validate(frame, ["ara"], {"ara": ("2004-07-01", "2019-12-31")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = licensed_dir("ara")
    raw = download(URL, directory / "ara.raw.zip")
    frame = read_index(raw)
    check_size(raw)
    summarize(
        raw,
        "date",
        archive_member="ARA.csv",
        parse_dates=["date"],
        date_format="%d%b%Y",
    )
    store(frame, directory / "ara.csv")


if __name__ == "__main__":
    main()
