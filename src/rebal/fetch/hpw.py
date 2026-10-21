"""Run: uv run python3 -m rebal.fetch.hpw

CLI arguments: --help shows usage. REPLICATE_DATA_DIR controls external storage.

Save Jun Pan's unchanged workbook and tidy daily Treasury noise in basis points.
No redistribution grant was found; both files stay in licensed_dir('hpw').
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import licensed_dir

URL = "https://en.saif.sjtu.edu.cn/junpan/Noise_Measure_2025.xlsx"


def read_noise(path: Path) -> pd.DataFrame:
    # pandas: small Excel source; columns beyond B contain publisher notes, not data.
    frame = pd.read_excel(path, sheet_name="Noise Measure", usecols="A:B")
    frame = frame.rename(columns={"Date": "date"})
    return validate(frame, ["Noise_bp"], {"Noise_bp": ("1987-01-02", "2023-03-17")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = licensed_dir("hpw")
    raw = download(URL, directory / "Noise_Measure_2025.xlsx")
    frame = read_noise(raw)
    check_size(raw)
    summarize(raw, "Date", sheet_name="Noise Measure", usecols="A:B")
    store(frame, directory / "noise.csv")


if __name__ == "__main__":
    main()
