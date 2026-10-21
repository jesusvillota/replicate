"""Run: uv run python3 -m rebal.fetch.fears

CLI arguments: --help shows usage. REPLICATE_DATA_DIR controls external storage.

Save the archived public FEARS vintage, 2004–2011, in original units outside git.
This file does not supply the paper's longer, privately obtained FEARS series.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

URL = (
    "https://web.archive.org/web/20230627055206id_/"
    "https://www3.nd.edu/~zda/fears_post_20140512.csv"
)
COLUMNS = ["fears25", "fears30", "fears35"]


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small archived source-file parsing and validation only.
    frame = pd.read_csv(path)
    if list(frame.columns) != ["date", *COLUMNS]:
        raise ValueError("Expected archived public FEARS columns")
    frame["date"] = pd.to_datetime(frame.date, format="%m/%d/%Y", errors="raise")
    return validate(
        frame,
        COLUMNS,
        {column: ("2004-07-01", "2011-12-30") for column in COLUMNS},
    )


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = licensed_dir("fears")
    raw = download(URL, directory / "fears_post_20140512.raw.csv")
    frame = read_index(raw)
    check_size(raw)
    summarize(raw, "date")
    store(frame, directory / "fears.csv")


if __name__ == "__main__":
    main()
