"""uv run python3 -m rebal.exhibits --all --demo --only table_C1 table_C2 figure_C1
uv run python3 -m rebal.exhibits.signals_descriptive --demo --end latest

CLI Arguments:
--demo: compute signals from synthetic panel returns; write output/demo/.
--end: inclusive sample end, default 2023-03-17; 'latest' uses all available dates.

Reads the panel and built signals (builds in memory for demo). Writes descriptive
CSVs table_C1/table_C2, figure_C1 PDF and its plotted CSV, plus JSON lineage.
Mean is daily decimal deviation times 252; SD is daily SD times sqrt(252).
Figure columns threshold/calendar are decimal weights, plotted in percent.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from rich.console import Console
from scipy import stats

from rebal.io import load_panel, load_signals
from rebal.paths import output_dir
from rebal.signals import build

EXHIBITS = ["table_C1", "table_C2", "figure_C1"]
SAMPLE_START = "1997-09-10"
SAMPLE_END = "2023-03-17"
PREDICTORS = (
    "threshold",
    "calendar",
    "momentum",
    "vix",
    "move",
    "epu",
    "ads",
    "sentiment",
)


def describe(signals: pd.DataFrame) -> pd.DataFrame:
    """C.1 statistics on each signal's finite observations; sample SD (ddof=1)."""
    rows = []
    for name in ("threshold", "calendar"):
        values = signals[name].to_numpy(dtype=float)
        finite = values[np.isfinite(values)]
        pairs = np.isfinite(values[:-1]) & np.isfinite(values[1:])
        rows.append(
            {
                "signal": name,
                "mean": np.mean(finite) * 252,
                "sd": np.std(finite, ddof=1) * np.sqrt(252),
                "ar1": np.corrcoef(values[:-1][pairs], values[1:][pairs])[0, 1],
                "skewness": stats.skew(finite, bias=False),
                "excess_kurtosis": stats.kurtosis(finite, fisher=True, bias=False),
                "nobs": len(finite),
            }
        )
    # pandas: final small table assembly only.
    return pd.DataFrame(rows)


def correlations(frame: pd.DataFrame) -> pd.DataFrame:
    """C.2 correlations on one common complete-case sample, after momentum warm-up."""
    values = frame[list(PREDICTORS)].to_numpy(dtype=float)
    values = values[np.isfinite(values).all(axis=1)]
    if len(values) < 3:
        raise ValueError("table_C2 needs at least three complete observations")
    # pandas: label the final 8 by 8 NumPy correlation matrix.
    result = pd.DataFrame(np.corrcoef(values, rowvar=False), columns=PREDICTORS)
    result.insert(0, "predictor", PREDICTORS)
    return result


def plot_signals(frame: pd.DataFrame, path: Path, demo: bool) -> None:
    figure = Figure(figsize=(10, 6), layout="constrained")
    FigureCanvasAgg(figure)
    axes = figure.subplots(2, 1, sharex=True)
    for axis, name in zip(axes, ("threshold", "calendar")):
        axis.plot(frame.date, frame[name].to_numpy() * 100, linewidth=0.6)
        axis.axhline(0, color="black", linewidth=0.5)
        axis.set_ylabel(f"{name.capitalize()} (%)")
        axis.grid(alpha=0.2)
    axes[-1].set_xlabel("Date")
    figure.suptitle("Rebalancing signals" + (" — synthetic demo" if demo else ""))
    figure.savefig(path)
    figure.clear()


def run(demo: bool, *, end: str = SAMPLE_END) -> list[Path]:
    # pandas: small date-indexed input alignment and final sample selection.
    panel = load_panel(demo=demo).set_index("date")
    signals = (
        build(panel.r_es, panel.r_ty, r_sp500tr=panel.r_sp500tr)
        if demo
        else load_signals()
    )
    signals = signals.set_index("date")
    frame = signals.join(
        panel[["vix", "move", "epu", "ads", "sentiment"]],
        how="left",
        validate="one_to_one",
    )
    stop = frame.index.max() if end == "latest" else pd.Timestamp(end)
    frame = frame.loc[
        (frame.index >= SAMPLE_START) & (frame.index <= stop)
    ].reset_index()
    if len(frame) < 3:
        raise ValueError("descriptive exhibits need at least three sample dates")
    tables = output_dir("demo" if demo else "tables")
    figures = output_dir("demo" if demo else "figures")
    c1, c2 = tables / "table_C1.csv", tables / "table_C2.csv"
    plotted, pdf = figures / "figure_C1.csv", figures / "figure_C1.pdf"
    summary = describe(frame)
    summary["sample_start"] = frame.date.min().date().isoformat()
    summary["sample_end"] = frame.date.max().date().isoformat()
    summary.to_csv(c1, index=False)
    correlations(frame).to_csv(c2, index=False)
    frame[["date", "threshold", "calendar"]].to_csv(plotted, index=False)
    plot_signals(frame, pdf, demo)
    metadata = tables / "signals_descriptive.json"
    metadata.write_text(
        json.dumps(
            {
                "script": "rebal.exhibits.signals_descriptive",
                "created_utc": datetime.now(UTC).isoformat(),
                "source": "synthetic panel returns, actual signal engine"
                if demo
                else "rebal.io panel and signals_clean.parquet",
                "parameters": {
                    "timing": "clean",
                    "momentum": "medium-slow",
                    "start": SAMPLE_START,
                    "end": end,
                },
                "sample_start": str(frame.date.min()),
                "sample_end": str(frame.date.max()),
                "rows": len(frame),
                "correlation_nobs": int(
                    np.isfinite(frame[list(PREDICTORS)].to_numpy(dtype=float))
                    .all(axis=1)
                    .sum()
                ),
                "outputs": [str(path) for path in (c1, c2, plotted, pdf)],
            },
            indent=2,
        )
        + "\n"
    )
    return [c1, c2, plotted, pdf, metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write descriptive signal exhibits.")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument(
        "--end", default=SAMPLE_END, help="Inclusive end date or 'latest'."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in run(args.demo, end=args.end):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
