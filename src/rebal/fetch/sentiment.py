"""Run: uv run python3 -m rebal.fetch.sentiment

CLI arguments: --help shows usage. No API key is required.

Save the SF Fed Daily News Sentiment workbook and a tidy original-unit CSV.
"""

import argparse
from pathlib import Path

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

URL = "https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx"


def read_index(path: Path) -> pd.DataFrame:
    # pandas: small workbook parsing; methodology remains in the raw workbook.
    frame = pd.read_excel(path, sheet_name="Data")
    if list(frame.columns) != ["date", "News Sentiment"]:
        raise ValueError("Expected SF Fed daily news sentiment columns")
    frame = frame.rename(columns={"News Sentiment": "sentiment"})
    return validate(frame, ["sentiment"], {"sentiment": ("1997-09-10", "2023-03-17")})


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("sentiment")
    raw = download(URL, directory / "news_sentiment_data.xlsx")
    frame = read_index(raw)
    check_size(raw)
    summarize(raw, "date", sheet_name="Data")
    store(frame, directory / "sentiment.csv")


if __name__ == "__main__":
    main()
