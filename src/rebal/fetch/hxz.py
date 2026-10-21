"""Run: uv run python3 -m rebal.fetch.hxz

CLI arguments: --help shows usage.

Read the newest q5 daily CSV linked on the official factors page. Save its
unchanged bytes, a tidy CSV (date + published series, percent), and source
metadata under data/public/hxz. Processing only; no return conversion.
"""

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urljoin, urlparse

import pandas as pd

from rebal.fetch._rates import check_size, store, validate
from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

PAGE_URL = "https://global-q.org/factors.html"
COLUMNS = ["R_F", "R_MKT", "R_ME", "R_IA", "R_ROE", "R_EG"]


class FactorLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        url = urlparse(urljoin(PAGE_URL, href))
        match = re.fullmatch(r"q5_factors_daily_(\d{4})\.csv", Path(url.path).name)
        if match and url.hostname in {"global-q.org", "www.global-q.org"}:
            self.links.append((int(match[1]), url._replace(scheme="https").geturl()))


def latest_daily_url(html: str) -> str:
    parser = FactorLinks()
    parser.feed(html)
    if not parser.links:
        raise ValueError("Official factors page has no q5 daily CSV link")
    return max(parser.links)[1]


def read_factors(path: Path) -> pd.DataFrame:
    # pandas: small published CSV parsing and validation, no analytical computation.
    frame = pd.read_csv(path)
    coverage = {column: ("1997-09-10", "2023-03-17") for column in COLUMNS}
    return validate(frame, COLUMNS, coverage)


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    directory = public_dir("hxz")
    with TemporaryDirectory(prefix="rebal-hxz-") as temporary:
        page = download(PAGE_URL, Path(temporary) / "factors.html")
        url = latest_daily_url(page.read_text(encoding="utf-8"))
    raw = download(url, directory / "q5_factors_daily.raw.csv")
    frame = read_factors(raw)
    check_size(raw)
    summarize(raw, "date")
    store(frame, directory / "q5_factors_daily.csv")
    metadata = {
        "data_url": url,
        "sha256": hashlib.sha256(raw.read_bytes()).hexdigest(),
    }
    (directory / "source.json").write_text(json.dumps(metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
