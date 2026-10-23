"""uv run python3 -m rebal.exhibits.calibration_figures --demo --end latest

CLI Arguments:
--demo: planted fixtures and output/demo/.
--end: inclusive sample end (default 2023-03-17), or latest.
--se: HC variant, hc0 or hc1 (default); D1/D2 always use HAC.
--hac-lags: optional nonnegative Newey–West lag count.
--timing: signal file suffix (default clean).
--weakening-critical-t: Figure 2 summary reference (default 2.58, the paper's 1%).

Reads panel/signals contracts; writes five PDFs, their plotted CSVs and lineage.
delta_pct is percent portfolio weight; window_days is trading days. coef is
decimal return per decimal weight; se and t describe the plotted coefficient.
Undefined subsets have missing estimates, an explicit status and actual nobs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console

from rebal.comparison_exports import write_figure_comparisons
from rebal.exhibits._figure_output import write_figures
from rebal.io import load_panel, load_signals
from rebal.regress import DEFAULT_SAMPLE, ols, predictive, predictive_data

EXHIBITS = ["figure_2", "figure_3", "figure_D1", "figure_D2", "figure_D3"]


def build_figures(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
    hac_lags: int | None = None,
) -> dict[str, pd.DataFrame]:
    """Compute eqs. (1)/(3) with leads aligned before conditioning on origins."""
    # pandas: small named regression matrices and final plotted tables.
    sample = (DEFAULT_SAMPLE[0], end)
    rows: dict[str, list[dict]] = {name: [] for name in EXHIBITS}

    def record(exhibit, result, term, series, **coordinates):
        row = result.tidy.set_index("term").loc[term].to_dict()
        row.pop("column")
        row.update(
            exhibit=exhibit,
            term=term,
            series=series,
            critical_t=-2.58,
            status="estimated",
            **coordinates,
        )
        rows[exhibit].append(row)

    for exhibit, covariance in (("figure_2", se), ("figure_D1", "hac")):
        for i in range(41):
            term = f"thr_{i:03d}"
            result = predictive(
                signals, panel, [term], sample=sample, se=covariance, hac_lags=hac_lags
            )
            record(exhibit, result, term, "all", delta_pct=i / 10)
        result = predictive(
            signals,
            panel,
            ["threshold"],
            sample=sample,
            se=covariance,
            hac_lags=hac_lags,
        )
        record(exhibit, result, "threshold", "aggregate", delta_pct=np.nan)

    for i in range(41):
        term = f"thr_{i:03d}"
        values = signals[term]
        for series, mask in (
            ("rebalancing", values.abs() >= i / 1000),
            ("other", values.abs() < i / 1000),
        ):
            y, x, dates = predictive_data(
                signals, panel, [term], sample=sample, subset=mask
            )
            if len(x) <= 2 or x[term].nunique() <= 1:
                rows["figure_D3"].append(
                    {
                        "exhibit": "figure_D3",
                        "term": term,
                        "series": series,
                        "delta_pct": i / 10,
                        "coef": np.nan,
                        "se": np.nan,
                        "t": np.nan,
                        "p": np.nan,
                        "nobs": len(x),
                        "adj_r2": np.nan,
                        "se_type": se,
                        "sample_start": np.nan,
                        "sample_end": np.nan,
                        "critical_t": -2.58,
                        "status": "not_estimable",
                    }
                )
                continue
            result = ols(y, x, se=se)
            result.tidy["sample_start"] = dates.min().date().isoformat()
            result.tidy["sample_end"] = dates.max().date().isoformat()
            record("figure_D3", result, term, series, delta_pct=i / 10)

    for window in range(1, 11):
        source = signals.copy()
        source["dummy"] = (source.days_to_month_end <= window).astype(float)
        for exhibit, covariance in (("figure_3", se), ("figure_D2", "hac")):
            result = predictive(
                source,
                panel,
                ["calendar", "calendar:dummy", "dummy"],
                sample=sample,
                se=covariance,
                hac_lags=hac_lags,
            )
            record(
                exhibit, result, "calendar:dummy", "calendar:dummy", window_days=window
            )
    return {name: pd.DataFrame(parts) for name, parts in rows.items()}


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
    hac_lags: int | None = None,
    timing: str = "clean",
    weakening_critical_t: float = 2.58,
) -> list[Path]:
    if not np.isfinite(weakening_critical_t) or weakening_critical_t <= 0:
        raise ValueError("weakening_critical_t must be finite and positive")
    frames = build_figures(
        load_signals(demo=demo, timing=timing),
        load_panel(demo=demo),
        end=end,
        se=se,
        hac_lags=hac_lags,
    )
    outputs = write_figures(
        frames,
        demo=demo,
        module=__name__,
        parameters={
            "start": DEFAULT_SAMPLE[0],
            "end": end,
            "se": se,
            "hac_lags": hac_lags,
            "timing": timing,
            "weakening_critical_t": weakening_critical_t,
        },
    )
    return write_figure_comparisons(
        frames, outputs, weakening_critical_t=weakening_critical_t
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Write calibration figures.")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="ISO end date or latest."
    )
    parser.add_argument("--se", choices=["hc0", "hc1"], default="hc1")
    parser.add_argument("--hac-lags", type=int)
    parser.add_argument("--timing", default="clean")
    parser.add_argument(
        "--weakening-critical-t",
        type=float,
        default=2.58,
        help="Figure 2 summary reference (default: 2.58, paper 1%%).",
    )
    args = parser.parse_args()
    if args.hac_lags is not None and args.hac_lags < 0:
        parser.error("--hac-lags must be nonnegative")
    for path in run(**vars(args)):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
