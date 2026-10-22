"""uv run python3 -m rebal.fetch.yahoo_bond_funds

CLI arguments: --tickers VBMFX VBTLX (default: both); --retries (default: 3);
--skip-existing; --shard i/N (default: 1/1); --list-remaining.

Reads Yahoo daily NAV, adjusted prices and distribution events. Preserves original
responses via yahoo.fetch_ticker and writes decimal total returns and metadata to
licensed_dir("yahoo_bond_funds"). Publicly accessible, terms-restricted data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from rich.console import Console

from rebal.fetch.common import summarize
from rebal.fetch.yahoo import fetch_ticker
from rebal.paths import licensed_dir

TICKERS = ("VBMFX", "VBTLX")
START = pd.Timestamp("1997-09-10")
END = pd.Timestamp("2023-03-17")
ADJUSTMENT_TOLERANCE = 1e-5
console = Console(highlight=False)


def total_returns(frame: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Reject raw-NAV substitutes and validate Yahoo's distribution adjustment."""
    if ticker not in TICKERS:
        raise ValueError("Expected VBMFX or VBTLX")
    # pandas: small CSV input validation; return calculations use DuckDB windows.
    frame = frame.copy()
    required = [
        "date",
        "Close",
        "Adj Close",
        "Dividends",
        "Capital Gains",
        "Stock Splits",
    ]
    if frame.empty or not set(required) <= set(frame.columns):
        raise ValueError("Missing daily prices or distribution columns")
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    dates = frame.date
    if (
        dates.isna().any()
        or dates.duplicated().any()
        or not dates.is_monotonic_increasing
        or dates.dt.tz is not None
    ):
        raise ValueError("Missing, duplicate, unsorted or timezone-aware dates")
    values = frame[required[1:]].to_numpy(dtype=float)
    if not np.isfinite(values).all() or (values[:, :2] <= 0).any():
        raise ValueError("Missing/nonfinite prices or events; nonpositive prices")
    if (values[:, 2:4] < 0).any() or (values[:, 4] != 0).any():
        raise ValueError("Negative distributions or splits require source review")
    if END not in set(dates) or (ticker == "VBMFX" and START not in set(dates)):
        raise ValueError("Missing required study boundary")
    with duckdb.connect() as con:
        con.register("history", frame)
        output = con.execute(
            """
            WITH prices AS (
                SELECT date, "Close" AS nav, "Adj Close" AS adjusted_close,
                       "Dividends" + "Capital Gains" AS distribution,
                       lag("Close") OVER (ORDER BY date) AS previous_nav,
                       lag("Adj Close") OVER (ORDER BY date) AS previous_adjusted
                FROM history
            )
            SELECT date, ? AS ticker, nav, adjusted_close, distribution,
                   adjusted_close / previous_adjusted - 1 AS ret,
                   nav / previous_nav - 1 AS nav_return,
                   nav / (previous_nav - distribution) - 1 AS event_adjusted_return
            FROM prices ORDER BY date
        """,
            [ticker],
        ).fetchdf()
    window = output.date.between(START, END)
    if not (output.loc[window, "distribution"] > 0).any():
        raise ValueError(
            "No study distributions: cannot verify total-return adjustment"
        )
    residual = (output.ret - output.event_adjusted_return).abs()
    if not np.isfinite(output.ret.iloc[1:]).all() or (output.ret.iloc[1:] < -1).any():
        raise ValueError("Invalid adjusted return")
    if not np.isfinite(output.event_adjusted_return.iloc[1:]).all():
        raise ValueError("Invalid distribution-adjusted return")
    if residual.max() > ADJUSTMENT_TOLERANCE:
        raise ValueError("Adjusted prices disagree with distribution events")
    if ticker == "VBMFX" and pd.isna(output.loc[output.date.eq(START), "ret"].iloc[0]):
        raise ValueError("Need a prior price for first study return")
    return output


def fetch(ticker: str, directory: Path, retries: int) -> Path:
    csv = fetch_ticker(ticker, directory, retries)
    output = total_returns(pd.read_csv(csv), ticker)
    path = directory / f"{ticker}_daily.parquet"
    output.to_parquet(path, index=False)
    summarize(path, "date")
    window = output.date.between(START, END)
    metadata = json.loads(csv.with_suffix(".metadata.json").read_text())
    metadata.update(
        {
            "script": __name__,
            "return_definition": "Adj Close_t / Adj Close_(t-1) - 1",
            "adjustment_reference": "https://help.yahoo.com/kb/SLN28256.html",
            "distribution_check": "Close_t / (Close_(t-1) - Dividends_t - Capital Gains_t) - 1",
            "study_max_adjustment_error": float(
                (output.ret - output.event_adjusted_return).abs().loc[window].max()
            ),
            "study_distribution_days": int(
                (output.loc[window, "distribution"] > 0).sum()
            ),
            "study_rows": int(window.sum()),
            "first_return": str(output.loc[output.ret.notna(), "date"].min().date()),
            "last_return": str(output.loc[output.ret.notna(), "date"].max().date()),
            "first_return_missing": True,
            "files": [
                csv.name,
                csv.with_suffix(".json").name,
                csv.with_suffix(".metadata.json").name,
                path.name,
            ],
            "caveat": "Vendor back-adjusted convention, not exactly (NAV_t + cash_t) / NAV_(t-1) - 1.",
        }
    )
    meta_path = path.with_suffix(".metadata.json")
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")
    console.print(f"OK {meta_path}", markup=False, soft_wrap=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--tickers", nargs="+", choices=TICKERS, default=list(TICKERS))
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--shard", default="1/1", help="Round-robin shard i/N.")
    parser.add_argument("--list-remaining", action="store_true")
    args = parser.parse_args()
    try:
        shard_index, shard_count = map(int, args.shard.split("/"))
        if args.retries < 0 or not 1 <= shard_index <= shard_count:
            raise ValueError
    except ValueError:
        parser.error("require retries >= 0 and shard 1 <= i <= N")
    directory = licensed_dir("yahoo_bond_funds")
    for ticker in sorted(set(args.tickers))[shard_index - 1 :: shard_count]:
        complete = all(
            (directory / f"{ticker}{suffix}").is_file()
            for suffix in (
                ".csv",
                ".json",
                ".metadata.json",
                "_daily.parquet",
                "_daily.metadata.json",
            )
        )
        if args.skip_existing and complete:
            expected = total_returns(pd.read_csv(directory / f"{ticker}.csv"), ticker)
            actual = pd.read_parquet(directory / f"{ticker}_daily.parquet")
            pd.testing.assert_frame_equal(actual, expected)
            if not args.list_remaining:
                summarize(directory / f"{ticker}_daily.parquet", "date")
        elif args.list_remaining:
            console.print(ticker, markup=False)
        else:
            fetch(ticker, directory, args.retries)


if __name__ == "__main__":
    main()
