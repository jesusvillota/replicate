"""Fetch daily Yahoo histories: ``uv run python3 -m rebal.fetch.yahoo``.

CLI arguments: --tickers (default: all ten task tickers), --retries (default: 3),
--skip-existing, --shard i/N (default: 1/1), --list-remaining.

Writes original chart JSON, unadjusted OHLC/Adj Close CSVs and download metadata
under licensed_dir("yahoo"). Processing only; no returns or roll correction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from time import sleep

import pandas as pd
import yfinance as yf
from curl_cffi.requests import Session
from curl_cffi.requests.exceptions import RequestException
from rich.console import Console
from yfinance.exceptions import YFRateLimitError

from rebal.fetch.common import summarize
from rebal.paths import licensed_dir

TICKERS = (
    "ES=F",
    "ZN=F",
    "^GSPC",
    "^SP500TR",
    "^MOVE",
    "^VIX",
    "^RUI",
    "^RUT",
    "^RLV",
    "^RLG",
)
PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Adj Close", "Volume")
console = Console(highlight=False)


class ChartSession(Session):
    """Keep the longest daily chart response verbatim, without cookies/crumbs."""

    def __init__(self) -> None:
        super().__init__(impersonate="chrome")
        self.raw: bytes | None = None
        self.rows = 0

    def get(self, url: str, **kwargs):
        response = super().get(url, **kwargs)
        if "/finance/chart/" in url and response.status_code == 200:
            results = response.json().get("chart", {}).get("result") or []
            if results:
                result = results[0]
                rows = len(result.get("timestamp") or [])
                if (
                    result.get("meta", {}).get("dataGranularity") == "1d"
                    and rows > self.rows
                ):
                    self.raw, self.rows = response.content, rows
        return response


def validate_history(frame: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Validate quoted sessions and required sample boundaries before writing."""
    # pandas: small yfinance input; schema/date validation and CSV serialization only.
    missing = set(PRICE_COLUMNS) - set(frame.columns)
    if frame.empty or missing:
        raise ValueError(
            f"{ticker}: empty history or missing columns: {sorted(missing)}"
        )
    frame = frame.copy()
    frame.index = pd.to_datetime(frame.index).tz_localize(None).normalize()
    frame.index.name = "date"
    if (
        frame.index.hasnans
        or frame.index.has_duplicates
        or not frame.index.is_monotonic_increasing
    ):
        raise ValueError(f"{ticker}: missing, duplicate or unsorted dates")
    if frame["Close"].isna().any() or frame["Adj Close"].isna().any():
        raise ValueError(f"{ticker}: missing Close or Adj Close")
    if ticker == "^SP500TR":
        for boundary in ("1997-09-10", "2023-03-17"):
            if pd.Timestamp(boundary) not in frame.index:
                raise ValueError(
                    f"{ticker}: missing required sample boundary {boundary}"
                )
    if ticker in ("ES=F", "ZN=F") and frame.index.min() > pd.Timestamp("2001-01-01"):
        raise ValueError(f"{ticker}: futures history must start no later than 2001")
    return frame


def fetch_ticker(ticker: str, directory: Path, retries: int = 3) -> Path:
    """Download full history, backing off on rate limits and transport errors."""
    yf.config.debug.hide_exceptions = False
    with ChartSession() as session:
        for attempt in range(retries + 1):
            try:
                frame = yf.Ticker(ticker, session=session).history(
                    period="max",
                    interval="1d",
                    auto_adjust=False,
                    back_adjust=False,
                    repair=False,
                    rounding=False,
                )
                break
            except (YFRateLimitError, RequestException):
                if attempt == retries:
                    raise
                delay = min(2**attempt, 60)
                console.log(f"Retry {ticker} in {delay}s", markup=False)
                sleep(delay)
        frame = validate_history(frame, ticker)
        if session.raw is None:
            raise ValueError(
                f"{ticker}: original daily chart response was not captured"
            )
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{ticker}.csv"
        raw_path = path.with_suffix(".json")
        raw_path.write_bytes(session.raw)
        frame.to_csv(path, date_format="%Y-%m-%d")
        metadata = {
            "script": __name__,
            "ticker": ticker,
            "downloaded_utc": datetime.now(UTC).isoformat(),
            "source": f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}",
            "yfinance_version": yf.__version__,
            "period": "max",
            "interval": "1d",
            "auto_adjust": False,
            "repair": False,
            "raw_sha256": hashlib.sha256(session.raw).hexdigest(),
            "rows": len(frame),
            "first": str(frame.index.min().date()),
            "last": str(frame.index.max().date()),
            "files": [raw_path.name, path.name],
        }
        path.with_suffix(".metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n"
        )
    summarize(path, "date")
    return path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--tickers",
        nargs="+",
        choices=TICKERS,
        default=list(TICKERS),
        help="Tickers to fetch (default: all ten).",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retries after rate/transport failures (default: 3).",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Validate and skip complete ticker artifacts.",
    )
    parser.add_argument(
        "--shard", default="1/1", help="Round-robin shard i/N (default: 1/1)."
    )
    parser.add_argument(
        "--list-remaining", action="store_true", help="List work without downloading."
    )
    args = parser.parse_args(argv)
    try:
        args.shard_index, args.shard_count = map(int, args.shard.split("/"))
        if not 1 <= args.shard_index <= args.shard_count or args.retries < 0:
            raise ValueError
    except ValueError:
        parser.error("require shard 1 <= i <= N and retries >= 0")
    return args


def main() -> None:
    args = parse_args()
    directory = licensed_dir("yahoo")
    console.log(f"Output: {directory}", markup=False)
    tickers = sorted(set(args.tickers))[args.shard_index - 1 :: args.shard_count]
    for ticker in tickers:
        path = directory / f"{ticker}.csv"
        complete = all(
            path.with_suffix(suffix).is_file()
            for suffix in (".csv", ".json", ".metadata.json")
        )
        if args.skip_existing and complete:
            validate_history(
                pd.read_csv(path, index_col="date", parse_dates=True), ticker
            )
            if not args.list_remaining:
                summarize(path, "date")
        elif args.list_remaining:
            console.print(ticker, markup=False)
        else:
            fetch_ticker(ticker, directory, args.retries)


if __name__ == "__main__":
    main()
