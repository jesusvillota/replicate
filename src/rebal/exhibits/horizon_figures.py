"""uv run python3 -m rebal.exhibits.horizon_figures --demo --end latest

CLI Arguments:
--demo: planted fixtures and output/demo/.
--end: inclusive sample end (default 2023-03-17), or latest.
--se: HC variant for D4, hc0 or hc1 (default); Figure 4 always uses Hodrick 1B.
--timing: signal file suffix (default clean).

Reads panel/signals contracts. Writes Figure 4/D4 PDFs, plotted CSVs, lineage.
horizon_days counts trading days; coef, se, ci_low and ci_high are decimal
return per decimal portfolio weight. Figure 4 uses sums of log1p(ret).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console
from scipy.stats import norm

from rebal.exhibits._figure_output import write_figures
from rebal.exhibits.predictive_tables import BASE
from rebal.io import load_panel, load_signals
from rebal.regress import DEFAULT_SAMPLE, dated, predictive, predictive_data
from rebal.regress_hodrick import hodrick

EXHIBITS = ["figure_4", "figure_D4"]
PLOTTED_TERMS = ["threshold", "calendar:week4"]


def build_figures(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
) -> dict[str, pd.DataFrame]:
    """Build future outcomes on the full calendar before selecting each sample."""
    # pandas: small ordered time-series inputs for statsmodels, not panel aggregation.
    calendar = dated(panel).index
    source = dated(signals)
    if not source.index.isin(calendar).all():
        raise ValueError("signal dates must belong to the panel trading calendar")
    source = source.reindex(calendar)
    if (source.ret <= -1).any():
        raise ValueError("log1p(ret) requires ret > -1")
    one_period = np.log1p(source.ret)
    rows: dict[str, list[pd.DataFrame]] = {name: [] for name in EXHIBITS}
    sample = (DEFAULT_SAMPLE[0], end)
    for horizon in range(1, 16):
        source["cumulative_log_ret"] = one_period.rolling(
            horizon, min_periods=horizon
        ).sum()
        s = source.reset_index()
        response, design, dates = predictive_data(
            s, panel, BASE, y="cumulative_log_ret", lead=horizon, sample=sample
        )
        cumulative = hodrick(response, design, one_period, horizon)
        cumulative.tidy["sample_start"] = dates.min().date().isoformat()
        cumulative.tidy["sample_end"] = dates.max().date().isoformat()
        single = predictive(s, panel, BASE, lead=horizon, sample=sample, se=se)
        for exhibit, result in (("figure_4", cumulative), ("figure_D4", single)):
            table = result.tidy[result.tidy.term.isin(PLOTTED_TERMS)].copy()
            table = table.drop(columns="column")
            table["exhibit"] = exhibit
            table["horizon_days"] = horizon
            table["ci_low"] = table.coef - norm.ppf(0.975) * table.se
            table["ci_high"] = table.coef + norm.ppf(0.975) * table.se
            table["outcome"] = "cumulative_log_ret" if exhibit == "figure_4" else "ret"
            rows[exhibit].append(table)
    return {name: pd.concat(parts, ignore_index=True) for name, parts in rows.items()}


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
    timing: str = "clean",
) -> list[Path]:
    frames = build_figures(
        load_signals(demo=demo, timing=timing), load_panel(demo=demo), end=end, se=se
    )
    return write_figures(
        frames,
        demo=demo,
        module=__name__,
        parameters={
            "start": DEFAULT_SAMPLE[0],
            "end": end,
            "se": se,
            "timing": timing,
            "cumulative_se": "hodrick_1b",
            "confidence": 0.95,
            "cumulative_transform": "sum(log1p(ret))",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Write horizon figures.")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="ISO end date or latest."
    )
    parser.add_argument("--se", choices=["hc0", "hc1"], default="hc1")
    parser.add_argument("--timing", default="clean")
    args = parser.parse_args()
    for path in run(**vars(args)):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
