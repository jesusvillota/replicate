"""Fetch CFTC futures-only positioning history.

uv run python3 -m rebal.fetch.cftc
uv run python3 -m rebal.fetch.cftc --end-year 2023 --refresh

CLI arguments:
--end-year: last archive year (default: current year).
--refresh: download again, including cached completed years.

Reads official ZIP archives, preserves them unchanged, and writes cot_legacy.csv,
tff.csv and manifest.json under data/public/cftc. CSVs contain date, market_code,
and every original column for the selected markets, in original units.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from rebal.fetch.common import download, summarize
from rebal.paths import public_dir

BASE_URL = "https://www.cftc.gov/files/dea/history/"
LTPOS_URL = "https://www.cftc.gov/idc/groups/public/@marketreports/documents/file/lgtraderpos-csv.csv"
MARKETS = {"043602": "Treasury", "138741": "S&P 500", "13874A": "S&P 500"}
MAX_BYTES = 20_000_000


def archives(end_year: int) -> dict[str, list[str]]:
    """Annual legacy archives avoid the oversized 1986–2016 ZIP."""
    return {
        "cot_legacy": [f"deacot{year}.zip" for year in range(1997, end_year + 1)],
        "tff": ["fin_fut_txt_2006_2016.zip"]
        + [f"fut_fin_txt_{year}.zip" for year in range(2017, end_year + 1)],
    }


def fetch_archive(name: str, directory: Path, refresh: bool) -> dict:
    path = directory / name
    # The current-year archive changes each week. Completed years are cached.
    if refresh or not path.exists() or str(date.today().year) in name:
        download(BASE_URL + name, path)
    if path.stat().st_size >= MAX_BYTES:
        raise ValueError(f"{path}: must be under 20 MB")
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError(f"{path}: corrupt ZIP")
    return {
        "url": BASE_URL + name,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def read_markets(path: Path, report: str) -> pd.DataFrame:
    """Parse ZIP streams as strings so market codes and published values survive."""
    if report == "cot_legacy":
        code_col = "CFTC Contract Market Code"
        date_col = "As of Date in Form YYYY-MM-DD"
        name_col = "Market and Exchange Names"
    else:
        code_col = "CFTC_Contract_Market_Code"
        date_col = "Report_Date_as_YYYY-MM-DD"
        name_col = "Market_and_Exchange_Names"
    pieces = []
    with ZipFile(path) as archive:
        members = [name for name in archive.namelist() if name.lower().endswith(".txt")]
        if len(members) != 1:
            raise ValueError(f"{path}: expected exactly one TXT member")
        with archive.open(members[0]) as stream:
            # pandas: bounded CSV parsing from ZIP streams, preserving every source
            # field as text; only a few thousand selected rows survive per archive.
            for chunk in pd.read_csv(
                stream, dtype=str, keep_default_na=False, chunksize=5000
            ):
                chunk.columns = chunk.columns.str.strip()
                if not {code_col, date_col, name_col}.issubset(chunk.columns):
                    raise ValueError(f"{path}: unexpected {report} schema")
                codes = chunk[code_col].str.strip()
                selected = chunk.loc[codes.isin(MARKETS)].copy()
                if selected.empty:
                    continue
                selected.insert(0, "market_code", codes.loc[selected.index])
                selected.insert(
                    0,
                    "date",
                    pd.to_datetime(
                        selected[date_col].str.strip(), format="mixed"
                    ).dt.strftime("%Y-%m-%d"),
                )
                for code, expected in MARKETS.items():
                    names = selected.loc[selected.market_code == code, name_col]
                    pattern = (
                        r"(?:TREASURY|UST 10Y)"
                        if expected == "Treasury"
                        else r"S&P.*500"
                    )
                    if not names.str.contains(pattern, case=False, regex=True).all():
                        raise ValueError(f"{path}: unexpected market name for {code}")
                pieces.append(selected)
    if not pieces:
        raise ValueError(f"{path}: none of the requested market codes found")
    return pd.concat(pieces, ignore_index=True)


def write_report(
    report: str, files: list[Path], directory: Path, end_year: int
) -> dict:
    # pandas: concatenate small filtered frames without changing source values;
    # this is data ingestion, with no analytical aggregation or unit conversion.
    frames = [read_markets(path, report) for path in files]
    columns = list(frames[0].columns)
    if any(list(frame.columns) != columns for frame in frames):
        raise ValueError(f"{report}: archive schemas differ")
    frame = pd.concat(frames, ignore_index=True)
    frame = frame.loc[frame.date.between("1997-01-01", f"{end_year}-12-31")]
    frame = frame.sort_values(["date", "market_code"]).reset_index(drop=True)
    validate_report(frame, report, end_year)
    path = directory / f"{report}.csv"
    frame.to_csv(path, index=False)
    if path.stat().st_size >= MAX_BYTES:
        raise ValueError(f"{path}: must be under 20 MB")
    summarize(path, "date", key_cols=("market_code",), dtype=str)
    return {
        "rows": len(frame),
        "first": frame.date.min(),
        "last": frame.date.max(),
        "columns": len(frame.columns),
        "markets": {
            code: {
                "first": frame.loc[frame.market_code == code, "date"].min(),
                "last": frame.loc[frame.market_code == code, "date"].max(),
                "rows": int((frame.market_code == code).sum()),
            }
            for code in MARKETS
        },
    }


def validate_report(frame: pd.DataFrame, report: str, end_year: int) -> None:
    if frame.empty or frame.duplicated(["date", "market_code"]).any():
        raise ValueError(f"{report}: empty data or duplicate market/date keys")
    if set(frame.market_code) != set(MARKETS):
        raise ValueError(f"{report}: missing or unexpected market codes")
    start = "1997-01" if report == "cot_legacy" else "2006-06"
    if not frame.date.min().startswith(start):
        raise ValueError(f"{report}: missing start of history ({start})")
    # Both continuing contracts must cover every year, including 2023.
    # The full-size S&P contract disappears from the publisher's later reports.
    for code in ("043602", "13874A"):
        dates = pd.to_datetime(frame.loc[frame.market_code == code, "date"])
        first_year = int(start[:4])
        if set(dates.dt.year) != set(range(first_year, end_year + 1)):
            raise ValueError(f"{report}: incomplete years for {code}")
        if end_year < date.today().year and dates.max().month != 12:
            raise ValueError(f"{report}: incomplete final year for {code}")


def write_ltpos(source: Path, directory: Path) -> dict:
    """Read the published three-level, 35-market header without guessing units."""
    with source.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.reader(stream))
    selected = {
        "CBT 2 Year Treasury (TU)",
        "CBT 5 Year Treasury (FB)",
        "CBT 10 Year Treasury (TY)",
        "CBT T-Bond (US)",
        "CME S&P 500 (SP)",
        "CME S&P 500 E Mini (ES)",
    }
    records = []
    found = set()
    for offset in range(0, len(rows[0]), 12):
        market = rows[0][offset].strip()
        if market not in selected:
            continue
        found.add(market)
        if [value.strip() for value in rows[2][offset : offset + 2]] != [
            "Week Starting",
            "Week Ending",
        ]:
            raise ValueError(f"LTPos: unexpected date headers for {market}")
        for row in rows[3:]:
            values = row[offset : offset + 12]
            record = {
                "date": pd.to_datetime(values[1]).strftime("%Y-%m-%d"),
                "market": market,
                "period_start": pd.to_datetime(values[0]).strftime("%Y-%m-%d"),
            }
            for group, col in zip(
                ("dealers", "asset_managers", "leveraged_funds", "other_reportables"),
                (2, 4, 6, 8),
                strict=True,
            ):
                if [
                    value.strip().strip('"')
                    for value in rows[2][offset + col : offset + col + 2]
                ] != ["Buys", "Sells"]:
                    raise ValueError(f"LTPos: unexpected buy/sell headers for {market}")
                buys, sells = (
                    float(value.replace(",", "")) for value in values[col : col + 2]
                )
                if buys < 0 or sells < 0:
                    raise ValueError("LTPos: expected nonnegative buy/sell magnitudes")
                record[f"{group}_buys"] = buys
                record[f"{group}_sells"] = sells
                record[f"{group}_net_change"] = buys - sells
            record["daily_average_large_trader_net_position_changes"] = float(
                values[10].replace(",", "")
            )
            record["daily_average_trade_volume"] = float(values[11].replace(",", ""))
            records.append(record)
    if found != selected:
        raise ValueError("LTPos: missing equity-index or Treasury market")
    # pandas: small, already parsed records; sort and validate without resampling.
    frame = pd.DataFrame(records).sort_values(["date", "market"])
    if (
        len(frame) != 750
        or frame.date.min() != "2009-01-09"
        or frame.date.max() != "2011-05-27"
    ):
        raise ValueError("LTPos: incomplete 2009–2011 history")
    if frame.isna().any().any():
        raise ValueError("LTPos: missing observations")
    path = directory / "ltpos.csv"
    frame.to_csv(path, index=False)
    summarize(path, "date", key_cols=("market",))
    return {
        "rows": len(frame),
        "first": frame.date.min(),
        "last": frame.date.max(),
        "markets": sorted(found),
        "url": LTPOS_URL,
        "raw_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--end-year",
        type=int,
        default=date.today().year,
        help="Last year, from 2023 through the current year (default: current year).",
    )
    parser.add_argument(
        "--refresh", action="store_true", help="Redownload cached completed years."
    )
    args = parser.parse_args()
    if not 2023 <= args.end_year <= date.today().year:
        parser.error("--end-year must be from 2023 through the current year")
    return args


def main() -> None:
    args = parse_args()
    directory = public_dir("cftc")
    sources = archives(args.end_year)
    names = [name for group in sources.values() for name in group]
    with ThreadPoolExecutor(max_workers=6) as pool:
        metadata = dict(
            zip(
                names,
                pool.map(
                    lambda name: fetch_archive(name, directory, args.refresh), names
                ),
                strict=True,
            )
        )
    reports = {
        report: write_report(
            report, [directory / name for name in files], directory, args.end_year
        )
        for report, files in sources.items()
    }
    ltpos = directory / "lgtraderpos-csv.csv"
    if args.refresh or not ltpos.exists():
        download(LTPOS_URL, ltpos)
    reports["ltpos"] = write_ltpos(ltpos, directory)
    manifest = {
        "script": "rebal.fetch.cftc",
        "retrieved_on": date.today().isoformat(),
        "end_year": args.end_year,
        "archives": metadata,
        "reports": reports,
    }
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for path in directory.iterdir():
        if path.is_file() and path.stat().st_size >= MAX_BYTES:
            raise ValueError(f"{path}: must be under 20 MB")


if __name__ == "__main__":
    main()
