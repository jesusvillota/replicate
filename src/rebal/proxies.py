"""uv run python3 -m rebal.proxies --report docs/data/proxy_comparison.md
uv run python3 -m rebal.proxies --demo --report output/demo/proxy_comparison.md

CLI Arguments:
--report FILE: Markdown destination (default: docs/data/proxy_comparison.md).
--demo: use reproducible synthetic inputs instead of stored source data.

Reads TASK-003/005/006/009/010 inputs, without downloading or changing them.
Writes candidate/pair metrics and input SHA-256 lineage in a Markdown report.
Processing only; reusable candidate functions return decimal daily excess returns.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from rich.console import Console

from rebal.paths import REPO_ROOT, licensed_dir

START = pd.Timestamp("1997-09-10")
END = pd.Timestamp("2023-03-17")
BENCH_START = pd.Timestamp("2000-09-01")
NAMES = {
    "E1": "CRSP SPY total return − RF",
    "E2": "Yahoo ^SP500TR return − RF",
    "E3": "Yahoo ES=F, repaired",
    "T1": "GSW 10-year zero − RF",
    "T2": "GSW 10-year par bond − RF",
    "T3": "GSW 6.5-year zero − RF",
    "T5": "CRSP IEF total return − RF",
    "T6": "Yahoo ZN=F, repaired",
}
UNAVAILABLE = {
    "E4": "WRDS ES futures: TASK-010 found no usable series.",
    "T4": "CRSP fixed-term Treasury index: TASK-010 access probe denied (42501).",
    "T7": "WRDS TY futures: TASK-010 found no usable series.",
}

# pandas: pure date-indexed Series are the downstream API required by TASK-012.
# NumPy prices the fitted curve; DuckDB scans files and aggregates all metrics.


def excess_return(
    total: pd.Series, rf: pd.Series, *, futures: bool = False
) -> pd.Series:
    """Subtract aligned decimal RF only for cash assets; never fill missing RF."""
    return total.copy() if futures else total - rf.reindex(total.index)


def es_spy(ret: pd.Series, rf: pd.Series) -> pd.Series:
    """E1: CRSP distribution-inclusive SPY simple return less daily RF."""
    return excess_return(ret, rf).rename("E1")


def es_total_return(close: pd.Series, rf: pd.Series) -> pd.Series:
    """E2: S&P 500 total-return index percentage change less daily RF."""
    return excess_return(close.pct_change(fill_method=None), rf).rename("E2")


def _elapsed(index: pd.DatetimeIndex) -> np.ndarray:
    return index.to_series().diff().dt.days.to_numpy() / 365.25


def zero_coupon_return(
    yield_percent: pd.Series,
    maturity: float,
    rf: pd.Series,
    *,
    remaining_yield_percent: pd.Series | None = None,
) -> pd.Series:
    """Hold an n-year zero for actual elapsed days, then reset maturity.

    P_previous=exp(-n*y_previous); P_today=exp(-(n-delta)*y_today).
    Yields enter in continuous percent/year. With no remaining-tenor yield,
    the local curve is assumed flat. Missing yields/RF remain missing.
    """
    if maturity <= 0:
        raise ValueError("maturity must be positive")
    delta = _elapsed(yield_percent.index)
    current = (
        yield_percent if remaining_yield_percent is None else remaining_yield_percent
    )
    log_ratio = (
        maturity * yield_percent.shift(1) / 100 - (maturity - delta) * current / 100
    )
    total = np.expm1(log_ratio).where((delta > 0) & (delta < maturity))
    return excess_return(total, rf)


def ty_zero_10(curve: pd.DataFrame, rf: pd.Series) -> pd.Series:
    """T1: 10-year zero; linearly interpolate SVENY09/10 as the bond ages."""
    delta = _elapsed(curve.index)
    remaining = curve.SVENY10 - delta * (curve.SVENY10 - curve.SVENY09)
    return zero_coupon_return(
        curve.SVENY10, 10, rf, remaining_yield_percent=remaining
    ).rename("T1")


def ty_zero_65(curve: pd.DataFrame, rf: pd.Series) -> pd.Series:
    """T3: 6.5-year zero, interpolating SVENY06/07; duration about 6.5 years."""
    slope = curve.SVENY07 - curve.SVENY06
    remaining = curve.SVENY06 + (0.5 - _elapsed(curve.index)) * slope
    return zero_coupon_return(
        curve.SVENY06 + 0.5 * slope, 6.5, rf, remaining_yield_percent=remaining
    ).rename("T3")


def fitted_yield(curve: pd.DataFrame, tenors: np.ndarray) -> np.ndarray:
    """GSW Svensson continuously compounded yields in decimal units.

    tenors is rows x cashflows. A missing inactive second factor is allowed
    only when BETA3 is zero (the early Nelson–Siegel specification).
    """
    beta = curve[[f"BETA{i}" for i in range(4)]].to_numpy() / 100
    tau1 = curve.TAU1.to_numpy()[:, None]
    tau2 = curve.TAU2.where(curve.BETA3.ne(0), 1.0).to_numpy()[:, None]
    x1, x2 = tenors / tau1, tenors / tau2
    a1, a2 = -np.expm1(-x1) / x1, -np.expm1(-x2) / x2
    return (
        beta[:, 0, None]
        + beta[:, 1, None] * a1
        + beta[:, 2, None] * (a1 - np.exp(-x1))
        + beta[:, 3, None] * (a2 - np.exp(-x2))
    )


def ty_par_10(curve: pd.DataFrame, rf: pd.Series) -> pd.Series:
    """T2: hold yesterday's SVENPY10-coupon bond, priced off both GSW curves.

    Semiannual coupons and principal use dirty prices (including accrual).
    The coupon is fixed during each holding period; it resets only afterward.
    Intervals of half a year or more are unavailable, not silently priced.
    """
    delta = _elapsed(curve.index)[:, None]
    tenors = np.broadcast_to(np.arange(0.5, 10.01, 0.5), (len(curve), 20))
    cashflows = np.broadcast_to(
        curve.SVENPY10.shift(1).to_numpy()[:, None] / 200, tenors.shape
    ).copy()
    cashflows[:, -1] += 1
    previous = np.sum(
        cashflows * np.exp(-tenors * fitted_yield(curve.shift(1), tenors)), axis=1
    )
    remaining = tenors - delta
    with np.errstate(invalid="ignore", divide="ignore"):
        today = np.sum(
            cashflows * np.exp(-remaining * fitted_yield(curve, remaining)), axis=1
        )
        total = pd.Series(today / previous - 1, index=curve.index)
    total = total.where((delta[:, 0] > 0) & (delta[:, 0] < 0.5))
    return excess_return(total, rf).rename("T2")


def ty_ief(ret: pd.Series, rf: pd.Series) -> pd.Series:
    """T5: CRSP distribution-inclusive IEF simple return less daily RF."""
    return excess_return(ret, rf).rename("T5")


def roll_days(close: pd.Series, reference: pd.Series, *, jump: float) -> pd.Series:
    """Conservative quarterly switch window plus absolute residual jumps.

    Calendar: eight calendar days before third Friday through the following
    Monday in March/June/September/December. Yahoo switch dates are not a
    contract-level roll history. Absolute residual cutoffs are fixed ex ante.
    Missing references cannot establish that a day is clean.
    """
    if jump <= 0:
        raise ValueError("jump must be positive")
    dates = close.index
    month_start = dates.to_period("M").to_timestamp()
    third_friday = month_start + pd.to_timedelta(
        (4 - month_start.dayofweek) % 7 + 14, unit="D"
    )
    calendar = (
        dates.month.isin([3, 6, 9, 12])
        & (dates >= third_friday - pd.Timedelta(days=8))
        & (dates <= third_friday + pd.Timedelta(days=3))
    )
    ref = reference.reindex(dates)
    residual = (close.pct_change(fill_method=None) - ref).abs()
    return pd.Series(calendar, index=dates) | residual.gt(jump) | ref.isna()


def repair_futures(close: pd.Series, reference: pd.Series, *, jump: float) -> pd.Series:
    """Replace detected roll-day returns with reference excess returns; no RF."""
    raw = close.pct_change(fill_method=None)
    repaired = raw.mask(
        roll_days(close, reference, jump=jump), reference.reindex(close.index)
    )
    # A reference return cannot manufacture futures history before inception.
    return repaired.where(raw.notna())


def es_futures(close: pd.Series, reference: pd.Series) -> pd.Series:
    """E3: repair ES=F using E2 at a fixed 2 percentage point residual cutoff."""
    return repair_futures(close, reference, jump=0.02).rename("E3")


def ty_futures(close: pd.Series, reference: pd.Series) -> pd.Series:
    """T6: repair ZN=F using T3 at a fixed 1 percentage point residual cutoff."""
    return repair_futures(close, reference, jump=0.01).rename("T6")


def load_inputs() -> tuple[dict, list[Path], str]:
    """Read projected columns with one scoped connection; retain source histories."""
    paths = [
        REPO_ROOT / "data/public/gsw/feds200628.csv",
        REPO_ROOT / "data/public/french/F-F_Research_Data_Factors_daily.csv",
        licensed_dir("crsp") / "etf_daily.parquet",
        *(
            licensed_dir("yahoo") / f"{ticker}.csv"
            for ticker in ["^SP500TR", "ES=F", "ZN=F"]
        ),
    ]
    french_exists = paths[1].is_file()
    if not french_exists:
        paths[1] = REPO_ROOT / "data/public/fred/DTB3.csv"
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(
                f"Missing TASK-003/005/006/009 input: {path}; regenerate using its source card"
            )
    # rebal has no shared DuckDB manager. Context closes all scan resources.
    with duckdb.connect() as con:
        curve = (
            con.execute("SELECT * FROM read_csv_auto(?) ORDER BY date", [str(paths[0])])
            .df()
            .set_index("date")
        )
        rates = (
            con.execute("SELECT * FROM read_csv_auto(?) ORDER BY date", [str(paths[1])])
            .df()
            .set_index("date")
        )
        etfs = con.execute(
            "SELECT date, ticker, ret FROM read_parquet(?) WHERE ticker IN ('SPY', 'IEF') ORDER BY date",
            [str(paths[2])],
        ).df()
        prices = [
            con.execute(
                'SELECT date, "Close" FROM read_csv_auto(?) ORDER BY date', [str(p)]
            )
            .df()
            .set_index("date")["Close"]
            for p in paths[3:]
        ]
    # French dates define the cash-equity trading calendar. For the DTB3 fallback,
    # use SPY dates; never treat a missing bond quote as a zero-return day.
    calendar = (
        rates.index
        if french_exists
        else pd.DatetimeIndex(etfs.loc[etfs.ticker.eq("SPY"), "date"])
    )
    if french_exists:
        rf = rates.RF / 100
        rf_note = "French daily RF / 100 (published percent/day → decimal/day)."
    else:
        # DTB3 bank-discount quote: 91-day bill price=1-d*91/360.
        # Accrue the previous known quote over actual elapsed calendar days.
        d = (
            rates.DTB3.reindex(calendar.union(rates.index))
            .sort_index()
            .ffill()
            .reindex(calendar)
            .shift(1)
            / 100
        )
        rf = (1 / (1 - d * 91 / 360)) ** (
            pd.Series(_elapsed(calendar) * 365.25, index=calendar) / 91
        ) - 1
        rf_note = "DTB3 fallback: lagged discount quote, 91-day bill, actual-days accrual; only RF quotes carried forward."
    data = {
        "curve": curve.reindex(calendar),
        "rf": rf,
        "spy": etfs.loc[etfs.ticker.eq("SPY")].set_index("date").ret.reindex(calendar),
        "ief": etfs.loc[etfs.ticker.eq("IEF")].set_index("date").ret.reindex(calendar),
        "tr": prices[0].reindex(calendar),
        "es": prices[1].reindex(calendar),
        "ty": prices[2].reindex(calendar),
    }
    return data, paths, rf_note


def demo_inputs() -> dict:
    """Plant a 6.5-year bond and noisy equity futures; no licensed data needed."""
    rng = np.random.default_rng(11)
    dates = pd.bdate_range("1997-09-09", END)
    rf = pd.Series(0.0001, index=dates)
    y = 4 + np.cumsum(rng.normal(0, 0.035, len(dates)))
    curve = pd.DataFrame({f"SVENY{i:02}": y for i in range(1, 11)}, index=dates)
    curve["SVENPY10"] = 200 * np.expm1(y / 200)
    for i in range(4):
        curve[f"BETA{i}"] = y if i == 0 else 0.0
    curve["TAU1"], curve["TAU2"] = 1.0, 2.0
    equity = pd.Series(rng.normal(0.0003, 0.01, len(dates)), index=dates)
    ty = ty_zero_65(curve, rf)
    return {
        "curve": curve,
        "rf": rf,
        "spy": equity + rng.normal(0, 0.0003, len(dates)),
        "ief": (ty + rf).where(dates >= "2002-07-26"),
        "tr": 100 * (1 + equity).cumprod(),
        "es": (
            100 * (1 + equity - rf + rng.normal(0, 0.0002, len(dates))).cumprod()
        ).where(dates >= "2000-09-18"),
        "ty": (
            100 * (1 + ty.fillna(0) + rng.normal(0, 0.0001, len(dates))).cumprod()
        ).where(dates >= "2000-09-21"),
    }


def build_candidates(data: dict) -> tuple[dict[str, pd.Series], pd.DataFrame, dict]:
    curve, rf = data["curve"], data["rf"]
    candidates = {
        "E1": es_spy(data["spy"], rf),
        "E2": es_total_return(data["tr"], rf),
        "T1": ty_zero_10(curve, rf),
        "T2": ty_par_10(curve, rf),
        "T3": ty_zero_65(curve, rf),
        "T5": ty_ief(data["ief"], rf),
    }
    candidates["E3"] = es_futures(data["es"], candidates["E2"])
    candidates["T6"] = ty_futures(data["ty"], candidates["T3"])
    flags = {
        "ES": roll_days(data["es"], candidates["E2"], jump=0.02),
        "TY": roll_days(data["ty"], candidates["T3"], jump=0.01),
    }
    benchmark = pd.DataFrame(
        {
            asset: data[key].pct_change(fill_method=None).mask(flags[asset])
            for asset, key in [("ES", "es"), ("TY", "ty")]
        }
    )
    benchmark = benchmark.loc[BENCH_START:END]
    counts = {
        asset: int(
            (
                flag
                & data[key].pct_change(fill_method=None).notna()
                & candidates["E3" if asset == "ES" else "T6"].notna()
                & data[key].index.to_series().between(START, END)
            ).sum()
        )
        for asset, key, flag in [("ES", "es", flags["ES"]), ("TY", "ty", flags["TY"])]
    }
    return candidates, benchmark, counts


def metric_rows(
    candidates: dict[str, pd.Series], benchmark: pd.DataFrame
) -> pd.DataFrame:
    """All candidates and ES−TY pairs, aggregated together by DuckDB.

    Lead/lag shifts happen before missing/roll rows are dropped. MTD sums use
    each comparison's common clean days; they do not fill excluded daily returns.
    """
    series = dict(candidates)
    es_ids = sorted(k for k in candidates if k.startswith("E"))
    ty_ids = sorted(k for k in candidates if k.startswith("T"))
    series.update(
        {f"{e}/{t}": candidates[e] - candidates[t] for e in es_ids for t in ty_ids}
    )
    rows = []
    for name, proxy in series.items():
        b = (
            benchmark.ES - benchmark.TY
            if "/" in name
            else benchmark["ES" if name.startswith("E") else "TY"]
        )
        aligned = pd.DataFrame(
            {
                "p": proxy.reindex(b.index),
                "b": b,
                "lead_b": b.shift(-1),
                "lag_b": b.shift(1),
            }
        )
        aligned["candidate"] = name
        rows.append(aligned.rename_axis("date").reset_index())
    frame = pd.concat(rows, ignore_index=True)
    with duckdb.connect() as con:
        con.register("observations", frame)
        metrics = (
            con.execute("""
            WITH clean AS (
                SELECT *, date_trunc('month', date) AS month
                FROM observations WHERE isfinite(p) AND isfinite(b)
            ), signals AS (
                SELECT *, 0.24 * sum(p) OVER w AS p_mtd,
                          0.24 * sum(b) OVER w AS b_mtd
                FROM clean WINDOW w AS (PARTITION BY candidate, month ORDER BY date ROWS UNBOUNDED PRECEDING)
            ) SELECT candidate, count(*) AS n, min(date) AS overlap_start, max(date) AS overlap_end,
                corr(p, b) AS correlation, covar_samp(p, b) / var_samp(b) AS beta,
                stddev_samp(p-b) * sqrt(252) AS tracking_error,
                avg(p-b) * 10000 AS mean_bp_day, corr(p, lead_b) AS lead,
                corr(p, lag_b) AS lag, corr(p_mtd, b_mtd) AS mtd_correlation
            FROM signals GROUP BY candidate ORDER BY candidate
        """)
            .df()
            .set_index("candidate")
        )
    for name, proxy in series.items():
        valid = proxy.loc[:END].dropna()
        metrics.loc[name, "coverage_start"] = valid.index.min()
        metrics.loc[name, "full_sample"] = bool(
            pd.notna(proxy.get(START)) and pd.notna(proxy.get(END))
        )
    return metrics


def _table(metrics: pd.DataFrame, ids: list[str]) -> str:
    lines = [
        "| Candidate | Coverage start | N | Overlap start | Overlap end | Corr | Beta | TE %/year | Mean bp/day | Lead | Lag | MTD corr |",
        "|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name in ids:
        row = metrics.loc[name]
        values = [f"{row[k]:.4f}" for k in ["correlation", "beta"]]
        values += [f"{100 * row.tracking_error:.4f}", f"{row.mean_bp_day:.4f}"]
        values += [f"{row[k]:.4f}" for k in ["lead", "lag", "mtd_correlation"]]
        lines.append(
            f"| {name} | {row.coverage_start:%Y-%m-%d} | {int(row.n)} | {row.overlap_start:%Y-%m-%d} | {row.overlap_end:%Y-%m-%d} | "
            + " | ".join(values)
            + " |"
        )
    return "\n".join(lines)


def write_report(
    data: dict, paths: list[Path], rf_note: str, report: Path, *, demo: bool = False
) -> pd.DataFrame:
    candidates, benchmark, counts = build_candidates(data)
    metrics = metric_rows(candidates, benchmark)
    full_pairs = [
        k for k in metrics.index if "/" in k and metrics.loc[k, "full_sample"]
    ]
    # Rank full-history pairs on identical daily observations, independent of
    # each candidate's different missing bond holidays. Partial series cannot win.
    common = (
        pd.concat(
            [candidates[k] for k in candidates if k not in {"E3", "T5", "T6"}], axis=1
        )
        .notna()
        .all(axis=1)
    )
    fair_benchmark = benchmark.where(common.reindex(benchmark.index), axis=0)
    fair = metric_rows(candidates, fair_benchmark)
    main = min(full_pairs, key=lambda k: fair.loc[k, "tracking_error"])
    e, t = main.split("/")
    alternatives = [
        k for k in full_pairs if k.split("/")[0] != e and k.split("/")[1] != t
    ]
    alternative = min(alternatives, key=lambda k: fair.loc[k, "tracking_error"])
    row = metrics.loc[main]
    unrepairable = {
        asset: int(
            (
                data[key].pct_change(fill_method=None).notna()
                & candidates[candidate].isna()
                & data[key].index.to_series().between(START, END)
            ).sum()
        )
        for asset, key, candidate in [("ES", "es", "E3"), ("TY", "ty", "T6")]
    }
    lines = [
        "# ES and TY proxy comparison",
        "",
        "Synthetic demo only."
        if demo
        else "Stored source data; no new downloads. Study: 1997-09-10–2023-03-17.",
        "",
        "## Inputs and methods",
        "",
        rf_note,
        "",
        "Cash proxies subtract RF. Futures returns are already excess returns and do not subtract RF.",
        "All sources are aligned to the French equity-session calendar before returns are computed.",
        "Missing prices/yields are never filled. A missing quote also makes the next holding return missing.",
        "The DTB3 fallback uses SPY sessions. No upstream file is changed.",
        "",
        "T1 uses a 10-year zero; T3 uses a **6.5-year maturity** zero as an approximate TY duration match.",
        "This is a fixed duration assumption, not a measured cheapest-to-deliver bond history.",
        "Zero holding return is exp(n*y_previous − (n−delta)*y_today(n−delta))−1, delta=calendar days/365.25.",
        "Continuous yields are divided by 100. T1 interpolates SVENY09/10; T3 interpolates SVENY06/07.",
        "T2 fixes yesterday's SVENPY10 coupon, pays semiannually, and prices that same bond on both fitted GSW curves.",
        "It uses the Svensson parameters for every cashflow, including sub-year maturities, and dirty prices for accrual.",
        "",
        "## Roll repair and benchmark",
        "",
        "Calendar flags span third Friday minus eight calendar days through the following Monday in each quarterly expiry month.",
        "Residual jumps outside that window also flag days: abs(ES−E2)>0.02 or abs(ZN−T3)>0.01.",
        "E3 replaces flagged returns with E2; T6 uses T3. Missing reference days cannot be benchmark days.",
        f"Repaired returns in the study sample: **ES {counts['ES']} days; TY {counts['TY']} days**.",
        f"Returns excluded because a repair reference is missing: ES {unrepairable['ES']} days; TY {unrepairable['TY']} days. These are not counted as repairs.",
        "These conservative flags are heuristic, not verified roll dates. Large close-time errors can also be flagged.",
        "The benchmark uses unrepaired Yahoo close-to-close ES=F / ZN=F returns on unflagged days only, from 2000-09 through 2023-03-17.",
        "An ES−TY pair requires both benchmark legs. Repaired observations never enter benchmark metrics.",
        "E3 and T6 therefore have mechanical identity metrics on their own benchmark; they are not independent validation.",
        "No benchmark exists for 1997–2000. No result establishes accuracy against Bloomberg.",
        "",
        "## Metric definitions",
        "",
        "Corr is contemporaneous Pearson correlation. Beta is Cov(proxy, benchmark)/Var(benchmark), with an intercept.",
        "TE is sample SD(proxy−benchmark)×sqrt(252), shown in percent/year. Mean is proxy−benchmark in basis points/day.",
        "Lead is Corr(proxy_t, benchmark_t+1); lag is Corr(proxy_t, benchmark_t−1). Shifts use the full session grid before filtering.",
        "MTD corr compares 0.24×within-month cumulative simple returns on each row's identical common clean days.",
        "This is an incomplete-month Calendar stand-in: omitted roll/missing sessions contribute to neither sum.",
        "It is not the full paper signal, and changing a row's overlap changes this diagnostic.",
        "Coverage start is the first usable return, before restricting the benchmark period; N counts paired clean days.",
        "The requested end is 2023-03-17; actual overlap endpoints below reflect the excluded roll window.",
        "",
        "## Available candidates",
        "",
        *[f"- **{k}**: {v}." for k, v in NAMES.items()],
        "",
        _table(metrics, sorted(candidates)),
        "",
        "## All available ES−TY pairs",
        "",
        _table(metrics, [k for k in metrics.index if "/" in k]),
        "",
        "## Full-sample pairs on a common comparison calendar",
        "",
        "Ranking uses the smallest TE among pairs whose legs cover both study endpoints. All rows below use identical clean days.",
        "This controls calendar differences when choosing among the full-history cash constructions.",
        "",
        _table(fair, full_pairs),
        "",
        "## Unavailable candidates",
        "",
        *[f"- **{k}**: {v}" for k, v in UNAVAILABLE.items()],
        "",
        "## Close times and limits",
        "",
        "Equities close at 16:00 ET; ES at 16:15 ET; Treasury futures settle at 15:00 ET.",
        "Yahoo daily closes need not reproduce the paper's Bloomberg settlement convention. GSW is a fitted cash Treasury curve.",
        "Nonzero lead/lag correlations can reflect close times, stale quotes, and market dynamics; they do not identify a cause.",
        "No future return is used to shift a candidate. Roll repair is retrospective and can bias apparent fit toward its reference.",
        "The fixed thresholds were not optimized for correlation. Different roll windows and the 6.5-year duration merit later sensitivity checks.",
        "",
        "## Input lineage",
        "",
        "Generator: `rebal.proxies`; annualization=252; GSW day count=365.25; ES cutoff=0.02; TY cutoff=0.01.",
        "",
    ]
    for path in paths:
        label = (
            path.relative_to(REPO_ROOT)
            if path.is_relative_to(REPO_ROOT)
            else Path("licensed") / path.parent.name / path.name
        )
        lines.append(
            f"- `{label}` SHA-256: `{hashlib.sha256(path.read_bytes()).hexdigest()}`"
        )
    lines += [
        "",
        "## Recommendation for DEC-001",
        "",
        f"Recommend **{main}: {NAMES[e]} / {NAMES[t]}** for the main panel.",
        f"Both cover 1997-09-10–2023-03-17. Pair correlation with the clean Yahoo futures benchmark is **{row.correlation:.4f}**; annualized tracking error is **{100 * row.tracking_error:.4f}%** (N={int(row.n)}).",
        f"On the common comparison calendar: correlation **{fair.loc[main, 'correlation']:.4f}**, TE **{100 * fair.loc[main, 'tracking_error']:.4f}%**.",
        "This pair has the lowest common-calendar tracking error among the full-sample candidates. Coverage here means both endpoints and available intervening sessions, with missing bond holidays left explicit.",
        f"Use **{alternative}: {NAMES[alternative.split('/')[0]]} / {NAMES[alternative.split('/')[1]]}** as a robustness pair with different constructions for both legs.",
        f"Its correlation is **{metrics.loc[alternative, 'correlation']:.4f}**; annualized TE is **{100 * metrics.loc[alternative, 'tracking_error']:.4f}%**.",
        "E3 starts after 2000-09-18; T6 starts after 2000-09-21; T5 starts in July 2002. They cover the study only partly.",
        f"For a later futures robustness splice, use {e}/{t} before the first common usable E3/T6 return, then repaired E3/T6; use {t} before T5 for an IEF check.",
        "Splice returns, not price levels, on a documented common session. Test the break and retain source flags. No splice is built here.",
        "TASK-012 must retain missing sessions and apply the daily-panel contract. This is evidence for DEC-001, not a recorded decision.",
        "",
    ]
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(lines))
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare ES and TY excess-return proxies."
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("docs/data/proxy_comparison.md"),
        help="Markdown destination (default: docs/data/proxy_comparison.md).",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use synthetic inputs; write reports under output/demo/.",
    )
    args = parser.parse_args()
    if args.demo and not args.report.resolve().is_relative_to(
        (REPO_ROOT / "output/demo").resolve()
    ):
        parser.error("--demo requires --report under output/demo/")
    return args


def main() -> None:
    args = parse_args()
    console = Console()
    console.log(
        f"Input: {'synthetic demo' if args.demo else 'stored source-card files'}"
    )
    console.log(f"Report: {args.report.resolve()}")
    data, paths, note = (
        (demo_inputs(), [], "Synthetic RF=0.0001/day.") if args.demo else load_inputs()
    )
    metrics = write_report(data, paths, note, args.report, demo=args.demo)
    console.print(
        f"OK {args.report} candidates={len(NAMES)} pairs={sum('/' in k for k in metrics.index)}"
    )


if __name__ == "__main__":
    main()
