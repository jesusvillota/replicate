"""Run: uv run python3 -m rebal.fetch.fred

CLI arguments: --help shows usage. No API key is required.

Read three FRED CSVs; save unchanged raw downloads and tidy original-unit CSVs.
Try recorded Wayback snapshots when the live endpoint is unavailable.
"""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import requests
from rich.console import Console

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

SNAPSHOTS = {
    "DTB3": "20260708052657",
    "DGS10": "20261014114807",
    "VIXCLS": "20261012093245",
}


def read_series(path: Path, series: str) -> pd.DataFrame:
    # pandas: small CSV parsing; FRED uses both empty fields and '.' for missing data.
    frame = pd.read_csv(path, na_values=["."])
    if list(frame.columns) != ["observation_date", series]:
        raise ValueError(f"{series}: expected FRED CSV, received a different schema")
    return validate(
        frame.rename(columns={"observation_date": "date"}),
        [series],
        {series: ("1997-09-10", "2023-03-17")},
    )


def fetch(series: str, directory: Path) -> None:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    raw = directory / f"{series}.raw.csv"
    with TemporaryDirectory(dir=directory) as temporary:
        candidate = Path(temporary) / "download.csv"
        try:
            download(url, candidate)
            frame = read_series(candidate, series)
        except (requests.RequestException, ValueError) as exc:
            archive = f"https://web.archive.org/web/{SNAPSHOTS[series]}id_/{url}"
            Console().print(
                f"FRED {series}: live source unavailable ({exc}); using {archive}",
                markup=False,
                highlight=False,
                soft_wrap=True,
            )
            download(archive, candidate)
            frame = read_series(candidate, series)
        check_size(candidate)
        candidate.replace(raw)
    summarize(raw, "observation_date")
    store(frame, directory / f"{series}.csv")


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    for series in SNAPSHOTS:
        fetch(series, public_dir("fred"))


if __name__ == "__main__":
    main()
