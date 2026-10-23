"""uv run python3 -m rebal.exhibits.trading_corr --demo
uv run python3 -m rebal.exhibits.trading_corr --end latest --aggregation mean

CLI Arguments:
--demo: synthetic weekly inputs and shared demo signals; output/demo/.
--end: inclusive response-date limit (default 2023-03-17), or latest.
--timing: signal file suffix (default clean).
--contract: E-mini (default emini) or full-size S&P (large).
--cftc-report: legacy (default) or TFF dealer/nondealer sensitivity proxy.
--lag-weeks: signal lag in report weeks (default 1; nonnegative).
--aggregation: signal at the reference date (default date), or trailing week mean.

Reads shared signals, public CFTC positions/LTPos, and external ICI flows.
Writes Figure 5 PDF, comparison-key CSV, and JSON lineage/block diagnostics.
See docs/methods/trading_corr.md for units, alignment and pooling choices.
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from rich.console import Console

from rebal.io import load_signals
from rebal.paths import licensed_dir, output_dir, public_dir
from rebal.regress import DEFAULT_SAMPLE

EXHIBITS = ["figure_5"]
TERMS = ["threshold", "calendar"]
GROUPS = {
    "cftc_hedgers": "CFTC\nHedgers",
    "cftc_speculators": "CFTC\nSpeculators",
    "ltpos_asset_managers": "LTPos\nAsset managers",
    "ltpos_leveraged_funds": "LTPos\nLeveraged funds",
    "ici": "ICI\nMutual funds",
}


# pandas: these are small, ordered weekly time series (at most a few thousand
# rows), with explicit time-index alignment; no large panel or SQL scans.
def dated(frame: pd.DataFrame, keys: tuple[str, ...] = ("date",)) -> pd.DataFrame:
    result = frame.copy()
    result["date"] = pd.to_datetime(result["date"])
    if result.date.isna().any() or result.date.dt.tz is not None:
        raise ValueError("dates must be nonmissing and timezone naive")
    if result.duplicated(list(keys)).any():
        raise ValueError(f"duplicate keys: {keys}")
    return result.sort_values(list(keys)).reset_index(drop=True)


def sample_signals(
    signals: pd.DataFrame, reference: pd.Series, aggregation: str = "date"
) -> pd.DataFrame:
    """Use only signals at or before each reference, never after it."""
    if aggregation not in {"date", "mean"}:
        raise ValueError("aggregation must be date or mean")
    daily = dated(signals).set_index("date")[TERMS]
    ref = pd.DatetimeIndex(reference)
    if aggregation == "date":
        values = daily.reindex(ref, method="ffill", tolerance=pd.Timedelta(days=4))
    else:
        # Include only existing trading days in (reference - 7 days, reference].
        union = daily.index.union(ref.dropna()).sort_values()
        values = daily.reindex(union).rolling("7D", closed="right").mean().reindex(ref)
    return values.reset_index(drop=True)


def cftc_trading(positions: pd.DataFrame, group: str) -> pd.DataFrame:
    """Q ending at t+1: each net change / OI[t], equity minus Treasury."""
    source = dated(positions, ("date", "market"))
    net = source.pivot(index="date", columns="market", values=group)
    oi = source.pivot(index="date", columns="market", values="oi")
    changes = net.diff().div(oi.shift().where(oi.shift() > 0))
    # Keep missing-market rows before differencing: do not bridge a source gap.
    valid = net.index.to_series().diff().dt.days.between(6, 8)
    value = (changes.equity - changes.bond).where(valid)
    return pd.DataFrame({"date": net.index, "value": value.to_numpy(), "block": 0})


def ltpos_trading(flows: pd.DataFrame, group: str) -> pd.DataFrame:
    """Subtract published mean daily flows, without differencing or summing."""
    source = dated(flows, ("date", "market"))
    if source.groupby("date").period_start.nunique().gt(1).any():
        raise ValueError("LTPos period starts differ across markets")
    wide = source.pivot(index="date", columns="market", values=group)
    starts = source.groupby("date").period_start.first().reindex(wide.index)
    return pd.DataFrame(
        {
            "date": wide.index,
            "value": (wide.equity - wide.bond).to_numpy(),
            "period_start": pd.to_datetime(starts).to_numpy(),
            "block": 0,
        }
    )


def ici_trading(flows: pd.DataFrame) -> pd.DataFrame:
    source = dated(flows)
    source["value"] = (
        source.domestic_equity - source.taxable_bond - source.municipal_bond
    )
    source["block"] = source.date.diff().dt.days.gt(8).cumsum()
    return source[["date", "value", "block"]]


def align_trading(
    trading: pd.DataFrame,
    signals: pd.DataFrame,
    *,
    lag_weeks: int = 1,
    aggregation: str = "date",
    start: str = DEFAULT_SAMPLE[0],
    end: str = DEFAULT_SAMPLE[1],
) -> pd.DataFrame:
    if not isinstance(lag_weeks, int) or lag_weeks < 0:
        raise ValueError("lag_weeks must be a nonnegative integer")
    source = dated(trading)
    if "period_start" in source:
        reference = (
            source.period_start - pd.Timedelta(days=1 + 7 * (lag_weeks - 1))
            if lag_weeks
            else source.date
        )
    else:
        reference = source.groupby("block").date.shift(lag_weeks)
        # CFTC gaps and ICI gaps must never turn a one-week lag into months.
        distance = (source.date - reference).dt.days
        reference = reference.where(distance.between(lag_weeks, 8 * lag_weeks))
    sampled = sample_signals(signals, reference, aggregation)
    source["signal_date"] = reference
    source[TERMS] = sampled[TERMS]
    stop = source.date.max() if end == "latest" else pd.Timestamp(end)
    mask = source.date.between(pd.Timestamp(start), stop) & reference.ge(
        pd.Timestamp(start)
    )
    return source.loc[mask].reset_index(drop=True)


def correlations(aligned: pd.DataFrame, *, within_blocks: bool = False) -> pd.DataFrame:
    """Pool within-block centered cross-products, retaining pairwise N."""
    rows = []
    for term in TERMS:
        pairs = (
            aligned[["block", "value", term]]
            .replace([np.inf, -np.inf], np.nan)
            .dropna()
        )
        if within_blocks:
            # Singleton blocks have no within-block variation and contribute no N.
            pairs = pairs[pairs.groupby("block").value.transform("size") >= 2]
            values = pairs[["value", term]] - pairs.groupby("block")[
                ["value", term]
            ].transform("mean")
        else:
            values = pairs[["value", term]] - pairs[["value", term]].mean()
        x, y = values[term].to_numpy(), values.value.to_numpy()
        denominator = np.sqrt(np.dot(x, x) * np.dot(y, y))
        corr = float(np.dot(x, y) / denominator) if denominator > 0 else np.nan
        rows.extend([(term, "value", corr), (term, "nobs", len(pairs))])
    return pd.DataFrame(rows, columns=["term", "stat", "value"])


def read_inputs(
    contract: str, report: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    code = {"emini": "13874A", "large": "138741"}[contract]
    folder = public_dir("cftc")
    raw = pd.read_csv(
        folder / ("cot_legacy.csv" if report == "legacy" else "tff.csv"),
        dtype={"market_code": str},
        low_memory=False,
    )
    raw = raw[raw.market_code.isin([code, "043602"])].copy()
    positions = raw[["date"]].copy()
    positions["market"] = np.where(raw.market_code == code, "equity", "bond")
    if report == "legacy":
        positions["oi"] = raw["Open Interest (All)"]
        for group, prefix in (
            ("hedgers", "Commercial"),
            ("speculators", "Noncommercial"),
        ):
            positions[group] = (
                raw[f"{prefix} Positions-Long (All)"]
                - raw[f"{prefix} Positions-Short (All)"]
            )
    else:
        positions["oi"] = raw.Open_Interest_All
        positions["hedgers"] = (
            raw.Dealer_Positions_Long_All - raw.Dealer_Positions_Short_All
        )
        positions["speculators"] = sum(
            raw[f"{prefix}_Positions_Long_All"] - raw[f"{prefix}_Positions_Short_All"]
            for prefix in ("Asset_Mgr", "Lev_Money", "Other_Rept")
        )
    raw = pd.read_csv(folder / "ltpos.csv", parse_dates=["date", "period_start"])
    equity = "CME E-Mini S&P 500 (ES)" if contract == "emini" else "CME S&P 500 (SP)"
    # The market names are retained verbatim by the fetcher.
    selected = raw.market.str.endswith("(ES)" if contract == "emini" else "(SP)")
    selected |= raw.market.str.endswith("(TY)")
    flows = raw.loc[selected, ["date", "period_start"]].copy()
    flows["market"] = np.where(
        raw.loc[selected].market.str.endswith("(TY)"), "bond", "equity"
    )
    for group in ("asset_managers", "leveraged_funds"):
        flows[group] = raw.loc[selected, f"{group}_net_change"]
    if set(flows.market) != {"equity", "bond"}:
        raise ValueError(f"missing LTPos contract {equity} or TY")
    return positions, flows, pd.read_csv(licensed_dir("ici") / "ici_weekly_flows.csv")


def demo_inputs(
    signals: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Plant negative rebalancer and positive liquidity-provider correlations."""
    dates = pd.date_range("2006-08-01", "2023-03-14", freq="W-TUE")
    x = sample_signals(signals, pd.Series(dates))[TERMS].to_numpy()
    x = x / x.std(axis=0)
    rng = np.random.default_rng(28)
    q = np.r_[0, -0.003 * x[:-1].sum(axis=1) + rng.normal(0, 0.003, len(dates) - 1)]
    position = np.cumsum(q) * 100000
    positions = pd.concat(
        [
            pd.DataFrame(
                {
                    "date": dates,
                    "market": market,
                    "oi": 100000,
                    "hedgers": position if market == "equity" else 0,
                    "speculators": -position if market == "equity" else 0,
                }
            )
            for market in ("equity", "bond")
        ],
        ignore_index=True,
    )
    ends = pd.date_range("2009-01-09", "2011-05-27", freq="W-FRI")
    z = sample_signals(signals, pd.Series(ends - pd.Timedelta(days=7))).sum(axis=1)
    flow = -100000 * z.to_numpy() + rng.normal(0, 500, len(ends))
    ltpos = pd.concat(
        [
            pd.DataFrame(
                {
                    "date": ends,
                    "period_start": ends - pd.Timedelta(days=4),
                    "market": market,
                    "asset_managers": flow if market == "equity" else 0,
                    "leveraged_funds": -flow if market == "equity" else 0,
                }
            )
            for market in ("equity", "bond")
        ],
        ignore_index=True,
    )
    dates = pd.date_range("2008-12-03", "2023-03-15", freq="W-WED")
    z = sample_signals(signals, pd.Series(dates - pd.Timedelta(days=7))).sum(axis=1)
    ici = pd.DataFrame(
        {
            "date": dates,
            "domestic_equity": -100000 * z + rng.normal(0, 500, len(dates)),
            "taxable_bond": 0,
            "municipal_bond": 0,
        }
    )
    ici = ici[(np.arange(len(ici)) // 12) % 2 == 0].reset_index(drop=True)
    return positions, ltpos, ici


def build_figure(
    signals: pd.DataFrame,
    positions: pd.DataFrame,
    ltpos: pd.DataFrame,
    ici: pd.DataFrame,
    *,
    end: str = DEFAULT_SAMPLE[1],
    lag_weeks: int = 1,
    aggregation: str = "date",
) -> tuple[pd.DataFrame, dict]:
    series = {
        f"cftc_{group}": cftc_trading(positions, group)
        for group in ("hedgers", "speculators")
    }
    series.update(
        {
            f"ltpos_{group}": ltpos_trading(ltpos, group)
            for group in ("asset_managers", "leveraged_funds")
        }
    )
    series["ici"] = ici_trading(ici)
    frames, diagnostics = [], {}
    for column, trading in series.items():
        start = "2006-08-01" if column.startswith("cftc") else DEFAULT_SAMPLE[0]
        aligned = align_trading(
            trading,
            signals,
            end=end,
            start=start,
            lag_weeks=lag_weeks,
            aggregation=aggregation,
        )
        result = correlations(aligned, within_blocks=column == "ici")
        result.insert(0, "column", column)
        result.insert(0, "exhibit", "figure_5")
        frames.append(result)
        diagnostics[column] = {
            "first_response": str(aligned.date.min()),
            "last_response": str(aligned.date.max()),
        }
        if column == "ici":
            blocks = []
            for block, raw in trading.groupby("block"):
                part = aligned[aligned.block == block]
                blocks.append(
                    {
                        "block": int(block),
                        "start": str(raw.date.min().date()),
                        "end": str(raw.date.max().date()),
                        "source_nobs": len(raw),
                        "statistics": correlations(part).to_dict("records"),
                    }
                )
            diagnostics[column]["blocks"] = blocks
    return pd.concat(frames, ignore_index=True), diagnostics


def plot_figure(frame: pd.DataFrame, demo: bool) -> Figure:
    figure = Figure(figsize=(9, 4.8), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    for offset, term, color in (
        (-0.18, "threshold", "#245a81"),
        (0.18, "calendar", "#268574"),
    ):
        values = (
            frame[(frame.term == term) & (frame.stat == "value")]
            .set_index("column")
            .value.reindex(GROUPS)
        )
        axis.bar(
            np.arange(5) + offset,
            values,
            width=0.34,
            label=term.capitalize(),
            color=color,
        )
    axis.set_xticks(np.arange(5), GROUPS.values())
    axis.axhline(0, color="black", linewidth=0.7)
    axis.set(
        ylabel="Correlation",
        ylim=(-1, 1),
        title="Figure 5: Trading and lagged rebalancing signals"
        + (" (synthetic demo)" if demo else ""),
    )
    axis.legend()
    axis.grid(axis="y", alpha=0.2)
    return figure


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    timing: str = "clean",
    contract: str = "emini",
    cftc_report: str = "legacy",
    lag_weeks: int = 1,
    aggregation: str = "date",
) -> list[Path]:
    signals = load_signals(demo=demo, timing=timing)
    inputs = demo_inputs(signals) if demo else read_inputs(contract, cftc_report)
    frame, diagnostics = build_figure(
        signals, *inputs, end=end, lag_weeks=lag_weeks, aggregation=aggregation
    )
    if not np.isfinite(frame.value).all():
        raise ValueError(
            "Figure 5 has an undefined correlation; inspect sample coverage and variation"
        )
    destination = output_dir("demo" if demo else "figures")
    csv, pdf, metadata = [
        destination / f"figure_5.{suffix}" for suffix in ("csv", "pdf", "metadata.json")
    ]
    frame.to_csv(csv, index=False)
    figure = plot_figure(frame, demo)
    figure.savefig(pdf)
    figure.clear()
    sources = (
        ["rebal.demo signals and synthetic weekly inputs"]
        if demo
        else [
            str(
                public_dir("cftc")
                / ("cot_legacy.csv" if cftc_report == "legacy" else "tff.csv")
            ),
            str(public_dir("cftc") / "ltpos.csv"),
            str(licensed_dir("ici") / "ici_weekly_flows.csv"),
            f"signals_{timing}.parquet",
        ]
    )
    # JSON uses null for undefined correlations in blocks outside the sample.
    payload = {
        "module": __name__,
        "created_utc": datetime.now(UTC).isoformat(),
        "demo": demo,
        "parameters": {
            "end": end,
            "timing": timing,
            "contract": contract,
            "cftc_report": cftc_report,
            "lag_weeks": lag_weeks,
            "aggregation": aggregation,
        },
        "inputs": sources,
        "diagnostics": diagnostics,
        "outputs": [csv.name, pdf.name],
    }
    metadata.write_text(pd.Series(payload).to_json(indent=2) + "\n")
    return [csv, pdf, metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Figure 5 trading correlations.")
    parser.add_argument("--demo", action="store_true", help="Use synthetic fixtures.")
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="Inclusive end date, or latest."
    )
    parser.add_argument(
        "--timing", default="clean", help="Signal file suffix (default clean)."
    )
    parser.add_argument("--contract", choices=["emini", "large"], default="emini")
    parser.add_argument("--cftc-report", choices=["legacy", "tff"], default="legacy")
    parser.add_argument(
        "--lag-weeks", type=int, default=1, help="Nonnegative signal lag (default 1)."
    )
    parser.add_argument("--aggregation", choices=["date", "mean"], default="date")
    args = parser.parse_args()
    if args.lag_weeks < 0:
        parser.error("--lag-weeks must be nonnegative")
    return args


def main() -> None:
    console = Console()
    try:
        for path in run(**vars(parse_args())):
            console.print(str(path), markup=False)
    except Exception:
        console.print_exception()
        raise


if __name__ == "__main__":
    main()
