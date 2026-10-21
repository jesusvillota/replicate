"""Run: uv run python3 -m rebal.fetch.gsw

CLI arguments: --help shows usage.

Save the published Fed GSW CSV with its notes, and a tidy yield/parameter CSV.
Keep original units; drop par maturities above ten years only if size requires it.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import MAX_BYTES, check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

URL = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
COLUMNS = (
    [f"SVENY{i:02}" for i in range(1, 31)]
    + [f"SVENPY{i:02}" for i in range(1, 31)]
    + [f"BETA{i}" for i in range(4)]
    + ["TAU1", "TAU2"]
)


def read_curve(path: Path) -> tuple[pd.DataFrame, int]:
    lines = path.read_text().splitlines()
    skip = next((i for i, line in enumerate(lines) if line.startswith("Date,")), None)
    if skip is None:
        raise ValueError("GSW date header not found")
    # pandas: small published CSV, schema selection and missing-marker normalization.
    frame = pd.read_csv(path, skiprows=skip, na_values=["NA", -999.99])
    frame = frame.rename(columns={"Date": "date"})[["date", *COLUMNS]]
    return validate(frame, COLUMNS, {"SVENY10": ("1971-08-16", "2023-03-17")}), skip


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("gsw")
    raw = download(URL, directory / "feds200628.raw.csv")
    frame, skip = read_curve(raw)
    check_size(raw)
    summarize(raw, "Date", skiprows=skip)
    if len(frame.to_csv(index=False).encode()) >= MAX_BYTES:
        frame = frame.drop(columns=[f"SVENPY{i:02}" for i in range(11, 31)])
    store(frame, directory / "feds200628.csv")


if __name__ == "__main__":
    main()
