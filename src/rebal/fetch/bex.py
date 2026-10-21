"""Run: uv run python3 -m rebal.fetch.bex

CLI arguments: --help shows usage. REPLICATE_DATA_DIR controls external storage.

Resolve Nancy Xu's current BEX workbook; save daily risk aversion and uncertainty
in original units. Both raw and tidy files stay outside git in licensed_dir('bex').
"""

import argparse
import html
import re
from pathlib import Path

import pandas as pd
import requests

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import USER_AGENT, download, summarize
from rebal.paths import licensed_dir

PAGE_URL = "https://www.nancyxu.net/risk-aversion-index"
SHEET = "DATA_PLOT_daily"


def workbook_url() -> str:
    """Follow the current official link instead of pinning an outdated vintage."""
    response = requests.get(PAGE_URL, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    links = {
        html.unescape(link)
        for link in re.findall(r'href="([^"]+\.xlsx(?:\?[^"]*)?)"', response.text)
        if "BEX_Indices_" in link
    }
    if len(links) != 1:
        raise ValueError("Expected one current BEX workbook link on Nancy Xu's page")
    return links.pop()


def parse_date(value: int) -> pd.Timestamp:
    return pd.to_datetime(str(value), format="%Y%m%d", errors="raise")


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small workbook parsing; columns D onward remain in the raw file.
    frame = pd.read_excel(path, sheet_name=SHEET, usecols="A:C")
    if list(frame.columns) != ["yyyymmdd", "ra_bex_PAPER", "unc_bex_PAPER"]:
        raise ValueError("Expected BEX daily risk aversion and uncertainty columns")
    frame = frame.rename(
        columns={"yyyymmdd": "date", "ra_bex_PAPER": "ra", "unc_bex_PAPER": "unc"}
    )
    frame["date"] = pd.to_datetime(
        frame.date.astype(str), format="%Y%m%d", errors="raise"
    )
    return validate(
        frame,
        ["ra", "unc"],
        {column: ("1997-09-10", "2023-03-17") for column in ["ra", "unc"]},
    )


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = licensed_dir("bex")
    raw = download(workbook_url(), directory / "bex.raw.xlsx")
    frame = read_index(raw)
    check_size(raw)
    summarize(
        raw,
        "yyyymmdd",
        sheet_name=SHEET,
        usecols="A:C",
        converters={"yyyymmdd": parse_date},
    )
    store(frame, directory / "bex.csv")


if __name__ == "__main__":
    main()
