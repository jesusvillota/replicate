"""Shared figure rendering and lineage, consuming the exact plotted tables."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from rebal.paths import output_dir

LABELS = {
    "threshold": "Threshold",
    "calendar:week4": "Calendar × week4",
    "all": "All days",
    "rebalancing": "Predicted rebalancing days",
    "other": "Other days",
    "calendar:dummy": "Calendar × month-end window",
}


def plot_data(data: pd.DataFrame, exhibit: str, demo: bool) -> Figure:
    """Render only values recorded in data, including bands and references."""
    figure = Figure(figsize=(8, 4.8), layout="constrained")
    FigureCanvasAgg(figure)
    horizon = "horizon_days" in data
    if horizon:
        axes = figure.subplots(1, 2, sharex=True)
        for axis, term in zip(axes, ("threshold", "calendar:week4"), strict=True):
            part = data[data.term == term]
            axis.plot(part.horizon_days, part.coef, color="#245a81")
            axis.fill_between(
                part.horizon_days,
                part.ci_low,
                part.ci_high,
                alpha=0.2,
                color="#245a81",
                label="95% confidence band",
            )
            axis.axhline(0, color="black", linewidth=0.7)
            axis.set(title=LABELS[term], xlabel="Horizon (trading days)")
            axis.set_ylabel("Return / decimal portfolio weight")
            axis.legend(fontsize=8)
    else:
        axis = figure.subplots()
        axes = [axis]
        x = "delta_pct" if "delta_pct" in data else "window_days"
        # pandas: final small display grouping, with no regression computation.
        for name, part in data[data.series != "aggregate"].groupby(
            "series", sort=False
        ):
            axis.plot(part[x], part.t, marker="o", markersize=3, label=LABELS[name])
        aggregate = data[data.series == "aggregate"]
        if not aggregate.empty:
            axis.axhline(
                aggregate.t.iloc[0],
                linestyle=":",
                color="#245a81",
                label="Aggregate Threshold",
            )
        axis.axhline(
            data.critical_t.iloc[0],
            linestyle="--",
            color="#b33232",
            label="1% reference (−2.58)",
        )
        axis.set(
            xlabel="δ (% portfolio weight)"
            if x == "delta_pct"
            else "Month-end window (trading days)",
            ylabel="t-statistic",
        )
        axis.legend(fontsize=8)
    for axis in axes:
        axis.grid(alpha=0.2)
    title = exhibit.replace("figure_", "Figure ")
    figure.suptitle(title + (" — synthetic demo" if demo else ""))
    return figure


def write_figures(
    frames: dict[str, pd.DataFrame], *, demo: bool, module: str, parameters: dict
) -> list[Path]:
    destination = output_dir("demo" if demo else "figures")
    outputs = []
    for exhibit, frame in frames.items():
        csv, pdf = (
            destination / f"{exhibit}.{extension}" for extension in ("csv", "pdf")
        )
        frame.to_csv(csv, index=False)
        figure = plot_data(frame, exhibit, demo)
        figure.savefig(pdf)
        figure.clear()
        outputs.extend([csv, pdf])
    metadata = destination / f"{module.rsplit('.', 1)[-1]}.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "module": module,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "parameters": parameters,
                "inputs": ["rebal.demo panel and planted signals"]
                if demo
                else ["daily_panel.parquet", f"signals_{parameters['timing']}.parquet"],
                "outputs": [path.name for path in outputs],
            },
            indent=2,
        )
        + "\n"
    )
    return outputs + [metadata]
