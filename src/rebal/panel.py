"""uv run python3 -m rebal.panel --build
uv run python3 -m rebal.panel --check

CLI Arguments:
--build: assemble the main and robustness panels from stored source files.
--check: validate both stored panels, print coverage, and fail on violations.

Reads the source-card inputs without downloading or changing them. Writes
processed_dir()/daily_panel.parquet, daily_panel_alt.parquet and panel.metadata.json.
Both parquets follow docs/contracts/daily_panel.md. Processing only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from rich.console import Console

from rebal import proxies
from rebal.paths import REPO_ROOT, licensed_dir, processed_dir

START, END = proxies.START, proxies.END
CONTROLS = (
    "vix",
    "move",
    "epu",
    "ads",
    "sentiment",
    "ra_bex",
    "unc_bex",
    "ara",
    "liquidity",
    "ivol",
)
FACTORS = (
    "mkt_rf",
    "smb",
    "hml",
    "rmw",
    "cma",
    "mom",
    "q_mkt",
    "q_me",
    "q_ia",
    "q_roe",
    "q_eg",
)
INDICES = (
    "r_sp500tr",
    "r_agg",
    "r_acwxus",
    "r_r1k",
    "r_r2k",
    "r_r1kv",
    "r_r1kg",
    "r_mkt_french",
    "r_10y_gsw",
)
COLUMNS = ("date", "r_es", "r_ty", "rf", "rf_3m", *CONTROLS, *FACTORS, *INDICES)
REQUIRED_STUDY = ("r_es", "r_ty", "rf", "vix", "epu", "ads", "sentiment", *FACTORS)

# pandas: the accepted rebal.proxies API requires date-indexed Series/frames.
# Vectorized alignment also preserves its missing-quote holding-return semantics.
# DuckDB projects source files; the final small frames use pandas for parquet I/O.


def align_series(
    series: pd.Series, calendar: pd.DatetimeIndex, *, control: bool = False
) -> pd.Series:
    """Align on equity sessions; only controls can carry five sessions forward."""
    aligned = series.reindex(calendar)
    return aligned.ffill(limit=5) if control else aligned


def trading_calendar(r_es: pd.Series, r_ty: pd.Series) -> pd.DatetimeIndex:
    """Use the common observed returns, excluding the four September closures."""
    pair = pd.concat([r_es, r_ty], axis=1).sort_index()
    finite = np.isfinite(pair).all(axis=1)
    closed = pair.index.to_series().between("2001-09-11", "2001-09-14")
    return pd.DatetimeIndex(pair.index[finite & ~closed])


def bill_return(quote_percent: pd.Series, calendar: pd.DatetimeIndex) -> pd.Series:
    """DTB3 discount quote × actual days until next retained session / 360."""
    days = calendar.to_series().shift(-1).sub(calendar.to_series()).dt.days
    return (quote_percent.reindex(calendar) / 100 * days / 360).rename("rf_3m")


def read_source(
    con: duckdb.DuckDBPyConnection,
    path: Path,
    columns: tuple[str, ...],
    paths: list[Path],
    *,
    etfs: bool = False,
) -> pd.DataFrame:
    """Project one source and reject ambiguous dates before any alignment."""
    if not path.is_file():
        raise FileNotFoundError(f"Missing panel input: {path}; see docs/data/cards/")
    reader = "read_parquet" if path.suffix == ".parquet" else "read_csv_auto"
    projection = ", ".join(f'"{name}"' for name in ("date", *columns))
    frame = con.execute(
        f"SELECT {projection} FROM {reader}(?) ORDER BY date", [str(path)]
    ).df()
    frame["date"] = pd.to_datetime(frame.date).astype("datetime64[ns]")
    keys = ["date", "ticker"] if etfs else ["date"]
    if frame.date.isna().any() or frame.duplicated(keys).any():
        raise ValueError(f"Invalid or duplicate source dates: {path}")
    paths.append(path)
    return frame.set_index("date")


def assemble_panels() -> tuple[pd.DataFrame, pd.DataFrame, list[Path], dict]:
    """Build E1/T3 and E2/T2 on the main pair's calendar, retaining burn-in."""
    paths: list[Path] = []
    public = REPO_ROOT / "data/public"
    # rebal has no shared DuckDB manager. One scoped connection closes all scans.
    with duckdb.connect() as con:

        def read(path: Path, *columns: str, etfs: bool = False) -> pd.DataFrame:
            return read_source(con, path, columns, paths, etfs=etfs)

        french = read(
            public / "french/F-F_Research_Data_Factors_daily.csv",
            "Mkt-RF",
            "SMB",
            "HML",
            "RF",
        )
        calendar = pd.DatetimeIndex(french.index)
        rf = french.RF / 100
        curve = read(
            public / "gsw/feds200628.csv",
            "SVENY06",
            "SVENY07",
            "SVENY09",
            "SVENY10",
            "SVENPY10",
            "BETA0",
            "BETA1",
            "BETA2",
            "BETA3",
            "TAU1",
            "TAU2",
        ).reindex(calendar)
        etfs = read(
            licensed_dir("crsp") / "etf_daily.parquet", "ticker", "ret", etfs=True
        )
        etfs = etfs.reset_index().pivot(index="date", columns="ticker", values="ret")
        tr = read(licensed_dir("yahoo") / "^SP500TR.csv", "Close").Close.reindex(
            calendar
        )
        main_es = proxies.es_spy(etfs.SPY.reindex(calendar), rf)
        main_ty = proxies.ty_zero_65(curve, rf)
        alt_es = proxies.es_total_return(tr, rf)
        alt_ty = proxies.ty_par_10(curve, rf)
        retained = trading_calendar(main_es, main_ty)
        data = pd.DataFrame(index=calendar)
        data["rf"] = rf
        data["vix"] = read(public / "fred/VIXCLS.csv", "VIXCLS").VIXCLS / 100
        data["move"] = read(licensed_dir("yahoo") / "^MOVE.csv", "Close").Close / 100
        for name in ("epu", "ads", "sentiment"):
            data[name] = read(public / name / f"{name}.csv", name)[name]
        bex = read(licensed_dir("bex") / "bex.csv", "ra", "unc")
        data["ra_bex"], data["unc_bex"] = bex.ra, bex.unc
        data["ara"] = read(licensed_dir("ara") / "ara.csv", "ara").ara
        noise_path = licensed_dir("hpw") / "noise.csv"
        noise = (
            read(noise_path, "Noise_bp").Noise_bp
            if noise_path.is_file()
            else pd.Series(dtype=float)
        )
        valid_noise = noise.dropna()
        if (
            not valid_noise.empty
            and valid_noise.index.min() <= START
            and valid_noise.index.max() >= END
        ):
            data["liquidity"] = noise
            liquidity = "HPW Noise_bp (basis points)"
        else:
            data["liquidity"] = read(public / "ofr/fsi.csv", "Funding").Funding
            liquidity = "OFR FSI Funding (index points); HPW lacks study coverage"
        data["ivol"] = read(
            licensed_dir("crsp") / "dispersion_daily.parquet", "ivol"
        ).ivol
        for name in CONTROLS:
            data[name] = align_series(data[name], calendar, control=True)
        for name, source in [("mkt_rf", "Mkt-RF"), ("smb", "SMB"), ("hml", "HML")]:
            data[name] = french[source] / 100
        ff5 = read(
            public / "french/F-F_Research_Data_5_Factors_2x3_daily.csv", "RMW", "CMA"
        )
        data["rmw"], data["cma"] = ff5.RMW / 100, ff5.CMA / 100
        data["mom"] = (
            read(public / "french/F-F_Momentum_Factor_daily.csv", "Mom").Mom / 100
        )
        q = read(
            public / "hxz/q5_factors_daily.csv",
            "R_MKT",
            "R_ME",
            "R_IA",
            "R_ROE",
            "R_EG",
        )
        for name, source in zip(FACTORS[6:], q.columns, strict=True):
            data[name] = q[source] / 100
        data["r_sp500tr"] = tr.pct_change(fill_method=None)
        # DEC-002: prefer the verified full-study public fund over the WRDS sample.
        data["r_agg"] = read(
            licensed_dir("yahoo_bond_funds") / "VBMFX_daily.parquet", "ret"
        ).ret
        msci = read(
            licensed_dir("msci") / "acwi_ex_usa_net_usd.csv", "acwi_ex_usa_net_usd"
        )
        # Compute on MSCI's own weekday grid before projecting onto US sessions.
        data["r_acwxus"] = msci.acwi_ex_usa_net_usd.pct_change(fill_method=None)
        for name, ticker in zip(
            INDICES[3:7], ("IWB", "IWM", "IWD", "IWF"), strict=True
        ):
            data[name] = etfs[ticker]
        data["r_mkt_french"] = (french["Mkt-RF"] + french.RF) / 100
        data["r_10y_gsw"] = proxies.ty_zero_10(curve, rf) + rf
        quote = read(public / "fred/DTB3.csv", "DTB3").DTB3
        data["rf_3m"] = bill_return(
            align_series(quote, calendar, control=True), retained
        )
    panels = []
    for es, ty in [(main_es, main_ty), (alt_es, alt_ty)]:
        panel = data.reindex(retained).copy()
        panel["r_es"], panel["r_ty"] = es.reindex(retained), ty.reindex(retained)
        panel = panel.rename_axis("date").reset_index().loc[:, COLUMNS]
        panel["date"] = panel.date.astype("datetime64[ns]")
        panel[list(COLUMNS[1:])] = panel[list(COLUMNS[1:])].astype("float64")
        panels.append(panel)
    choices = {
        "main": "E1/T3",
        "alternative": "E2/T2",
        "liquidity": liquidity,
        "r_agg": "Yahoo distribution-adjusted VBMFX; no splice",
        "r_acwxus": "MSCI 899901 USD NETR; no splice",
        "control_ffill_limit": 5,
        "ffill_calendar": "French equity sessions before main-pair filtering",
    }
    return panels[0], panels[1], paths, choices


def validate_panel(panel: pd.DataFrame) -> None:
    """Enforce the contract plus complete required study coverage."""
    if tuple(panel.columns) != COLUMNS:
        raise ValueError(
            "Panel columns/order differ from docs/contracts/daily_panel.md"
        )
    for name in COLUMNS:
        expected = "datetime64[ns]" if name == "date" else "float64"
        if str(panel[name].dtype) != expected:
            raise ValueError(f"{name}: expected {expected}, got {panel[name].dtype}")
    dates = panel.date
    if (
        panel.empty
        or dates.isna().any()
        or not dates.is_unique
        or not dates.is_monotonic_increasing
        or not dates.eq(dates.dt.normalize()).all()
    ):
        raise ValueError(
            "Panel dates must be nonempty, sorted, unique, naive midnights"
        )
    if dates.between("2001-09-11", "2001-09-14").any():
        raise ValueError("September 11–14, 2001 must be excluded")
    if panel[["r_es", "r_ty"]].isna().any().any():
        raise ValueError("Core returns cannot be missing")
    if np.isinf(panel[list(COLUMNS[1:])].to_numpy()).any():
        raise ValueError("Infinite panel values")
    study = panel.loc[dates.between(START, END)]
    if study.empty or study.date.iloc[0] != START or study.date.iloc[-1] != END:
        raise ValueError("Missing study endpoints")
    if study[list(REQUIRED_STUDY)].isna().any().any():
        raise ValueError("Required study controls/factors contain gaps")
    if not np.allclose(panel.r_mkt_french, panel.mkt_rf + panel.rf, equal_nan=True):
        raise ValueError("r_mkt_french must equal mkt_rf + rf")


def coverage_lines(panel: pd.DataFrame) -> list[str]:
    """Report full history and the study window separately for every column."""
    lines = []
    for name in COLUMNS:
        valid = panel.loc[panel[name].notna(), "date"]
        first = valid.min().strftime("%Y-%m-%d") if not valid.empty else "none"
        last = valid.max().strftime("%Y-%m-%d") if not valid.empty else "none"
        study = panel.loc[panel.date.between(START, END)]
        observed = study.loc[study[name].notna(), "date"]
        study_first = (
            observed.min().strftime("%Y-%m-%d") if not observed.empty else "none"
        )
        study_last = (
            observed.max().strftime("%Y-%m-%d") if not observed.empty else "none"
        )
        lines.append(
            f"{name}: {first} to {last}; NaN={panel[name].isna().mean():.2%}; "
            f"study={study_first} to {study_last}; NaN={study[name].isna().mean():.2%}"
        )
    return lines


def build(console: Console) -> None:
    main, alt, paths, choices = assemble_panels()
    for panel in (main, alt):
        validate_panel(panel)
    pd.testing.assert_frame_equal(
        main.drop(columns=["r_es", "r_ty"]), alt.drop(columns=["r_es", "r_ty"])
    )
    directory = processed_dir()
    for name, panel in [("daily_panel", main), ("daily_panel_alt", alt)]:
        destination = directory / f"{name}.parquet"
        panel.to_parquet(destination, index=False)
        console.log(f"Wrote {destination} rows={len(panel)}")
    metadata = {
        "generator": "rebal.panel",
        "built_utc": datetime.now(UTC).isoformat(),
        "contract": "docs/contracts/daily_panel.md",
        "choices": choices,
        "sources": [
            {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in paths
        ],
        "outputs": ["daily_panel.parquet", "daily_panel_alt.parquet"],
        "rows": len(main),
        "first": str(main.date.min().date()),
        "last": str(main.date.max().date()),
        "study_rows": int(main.date.between(START, END).sum()),
    }
    (directory / "panel.metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )


def check(console: Console) -> None:
    panels = []
    for name in ("daily_panel", "daily_panel_alt"):
        path = processed_dir() / f"{name}.parquet"
        panel = pd.read_parquet(path)
        validate_panel(panel)
        console.print(
            f"{name}: schema/dtypes OK (date=datetime64[ns], {len(COLUMNS) - 1} float64); "
            "dates sorted, unique, midnight; core returns complete",
            markup=False,
        )
        for line in coverage_lines(panel):
            console.print(line, soft_wrap=True)
        n = int(panel.date.between(START, END).sum())
        console.print(f"{name}: 1997-09-10 to 2023-03-17 rows={n}")
        console.print(
            f"Paper: regression N=6226 (difference {n - 6226:+d}); "
            f"about 6473 total days (difference {n - 6473:+d})"
        )
        panels.append(panel)
    pd.testing.assert_frame_equal(
        panels[0].drop(columns=["r_es", "r_ty"]),
        panels[1].drop(columns=["r_es", "r_ty"]),
    )
    console.print("PANEL OK")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build and validate both daily panels."
    )
    parser.add_argument(
        "--build", action="store_true", help="Build from stored source-card files."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate stored panels and print coverage.",
    )
    args = parser.parse_args()
    if not (args.build or args.check):
        parser.error("specify --build and/or --check")
    return args


def main() -> None:
    args = parse_args()
    console = Console()
    if args.build:
        build(console)
    if args.check:
        check(console)


if __name__ == "__main__":
    main()
