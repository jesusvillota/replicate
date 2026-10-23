"""Canonical comparison sidecars and main/variant discovery for TASK-023.

Export helpers consume the existing small exhibit tables, without re-estimation.
Blank values preserve keys whose paper convention has not been resolved.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

FIELDS = ("exhibit", "column", "term", "stat", "value")
COST_ITEMS = {
    "calendar": ("calendar", "annual_bps"),
    "threshold_min": ("threshold", "annual_min_bps"),
    "threshold_max": ("threshold", "annual_max_bps"),
    "threshold_average": ("threshold", "annual_mean_bps"),
    "threshold_fixed_1pct_average": ("threshold", "annual_one_pct_trade_bps"),
    "headline": ("headline", "annual_bps"),
    "dollar_cost_paper": ("headline", "annual_usd"),
    "per_household_paper": ("household", "annual_usd"),
}


def discover_csvs(folders: list[Path], variant: str | None = None) -> list[Path]:
    """Select one run, retaining only the named legacy magnitudes subfolder."""
    if variant is not None and (
        not variant or variant in {".", ".."} or Path(variant).name != variant
    ):
        raise ValueError("variant must be one directory name")
    roots = [
        folder / "robustness" / variant if variant else folder for folder in folders
    ]
    paths = {path for root in roots for path in root.glob("*.csv")}
    paths.update(
        root / "magnitudes" / "magnitudes.csv"
        for root in roots
        if (root / "magnitudes" / "magnitudes.csv").is_file()
    )
    return sorted(paths)


def write_comparison(path: Path, rows: list[tuple]) -> Path:
    """Write a long sidecar beside its plotted or regression source CSV."""
    destination = path.with_name(f"{path.stem}_comparison.csv")
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for *key, value in rows:
            writer.writerow(
                (*key, value if value is not None and math.isfinite(value) else "")
            )
    return destination


def cost_rows(frame) -> list[tuple]:
    # pandas: convert an existing small output table to final display records.
    values = dict(zip(frame.item, frame.value))
    return [
        ("costs", column, term, "value", values[item])
        for item, (column, term) in COST_ITEMS.items()
    ] + [("costs", "random", "annual_bps", "value", None)]


def strategy_rows(exhibit: str, frame) -> list[tuple]:
    # pandas: final reshaping of already annualized exhibit output, no computation.
    rows = []
    for row in frame.to_dict("records"):
        if exhibit == "table_6a":
            asset = {"r_es": "sp500", "r_ty": "ty", "strategy": "strategy"}.get(
                row["asset"]
            )
            if asset:
                for field, term in (
                    ("mean_pct_pa", "mean_pct_pa"),
                    ("volatility_pct_pa", "vol_pct_pa"),
                    ("sharpe", "sharpe"),
                    ("skewness", "skewness"),
                ):
                    rows.append((exhibit, asset, term, "value", row[field]))
        else:
            column = row["column"].lower()
            term = "alpha_pct_pa"
            if exhibit == "table_6c":
                column, regime = column.split(":")
                term = f"{'high' if regime == 'h' else 'low'}_mean_pct_pa"
            rows.extend(
                (exhibit, column, term, stat, row[stat]) for stat in ("coef", "se")
            )
    return rows


def figure_rows(
    exhibit: str, frame, *, weakening_critical_t: float = 2.58
) -> list[tuple]:
    """Use plotted coordinates exactly; do not infer ambiguous units or signs."""
    if exhibit == "figure_6":
        return [
            (exhibit, "sample_end", term, "value", None)
            for term in ("strategy", "sp500")
        ]
    if exhibit == "figure_D5":
        return [
            (exhibit, "random", term, "value", None)
            for term in ("mean_bps", "ci95_low_bps", "ci95_high_bps")
        ]
    rows = []
    # pandas: small plotted output records only; all estimates were computed upstream.
    records = frame.to_dict("records")
    for row in records:
        if "horizon_days" in row:
            rows.append(
                (
                    exhibit,
                    f"day_{int(row['horizon_days'])}",
                    row["term"],
                    "coef",
                    row["coef"],
                )
            )
        elif "window_days" in row:
            rows.append(
                (
                    exhibit,
                    f"days_{int(row['window_days'])}",
                    "calendar_interaction",
                    "t",
                    row["t"],
                )
            )
        elif row["series"] != "aggregate":
            term = {
                "rebalancing": "during_rebalancing",
                "other": "outside_rebalancing",
            }.get(row["series"], "threshold")
            rows.append(
                (exhibit, f"delta_{row['delta_pct']:.1f}_pct", term, "t", row["t"])
            )
    if exhibit == "figure_2":
        crossings = [
            row["delta_pct"]
            for row in records
            if row["series"] == "all" and abs(row["t"]) < weakening_critical_t
        ]
        rows.append(
            (
                exhibit,
                "summary",
                "one_pct_weakening_delta_pct",
                "value",
                min(crossings) if crossings else None,
            )
        )
    if exhibit == "figure_4":
        for term, summary in (
            ("threshold", "threshold_first_insignificant_day"),
            ("calendar:week4", "calendar_week4_first_insignificant_day"),
        ):
            crossings = [
                row["horizon_days"]
                for row in records
                if row["term"] == term and row["ci_low"] <= 0 <= row["ci_high"]
            ]
            rows.append(
                (
                    exhibit,
                    "summary",
                    summary,
                    "value",
                    min(crossings) if crossings else None,
                )
            )
    return rows


def write_figure_comparisons(frames: dict, outputs: list[Path], **kwargs) -> list[Path]:
    """Add canonical figure sidecars to the existing output list and lineage."""
    sidecars = [
        write_comparison(path, figure_rows(path.stem, frames[path.stem], **kwargs))
        for path in outputs
        if path.suffix == ".csv"
    ]
    for path in outputs:
        if path.name.endswith(".metadata.json"):
            metadata = json.loads(path.read_text(encoding="utf-8"))
            metadata["outputs"].extend(sidecar.name for sidecar in sidecars)
            path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return outputs + sidecars


def unmatched_reason(row: dict) -> str:
    """Classify missing targets without treating inaccessible sources as failures."""
    key = " ".join(str(row.get(field, "")) for field in FIELDS[:3]).lower()
    if (
        "fears" in key
        or "ancerno" in key
        or (row["exhibit"] == "table_D9" and row["column"] == "3")
    ):
        return "not available: FEARS is private; ANcerno is licensed and unavailable"
    if row["exhibit"] == "figure_6":
        return "paper-only data: Figure 6 axis transformation is unresolved"
    if row["exhibit"] == "figure_D5" or (
        row["exhibit"] == "costs" and row["column"] == "random"
    ):
        return "paper-only data: random-date cost sign conflicts between text and Figure D.5"
    if row.get("exported"):
        return "not available: no finite estimate or reference crossing on the exported grid"
    return "no export: no selected CSV provides this target statistic"


def coverage_report(rows: list[dict]) -> str:
    """List joined keys separately from numeric matches and explain every gap."""
    exhibits = sorted({row["exhibit"] for row in rows if row.get("exported")})
    lines = [
        "",
        "## Export coverage",
        "",
        "Joined exhibit keys: " + (", ".join(exhibits) or "none"),
        "",
        "Blank canonical values join keys only; they do not count as numeric matches.",
        "",
        "## Unmatched targets",
        "",
        "| exhibit | column | term | stat | reason |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        if row["ours"] is None:
            cells = [str(row[field]) for field in FIELDS[:4]] + [unmatched_reason(row)]
            lines.append(
                "| "
                + " | ".join(
                    cell.replace("|", "\\|").replace("\n", " ") for cell in cells
                )
                + " |"
            )
    if all(row["ours"] is not None for row in rows):
        lines.append("No unmatched targets.")
    return "\n".join(lines) + "\n"
