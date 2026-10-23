"""uv run python3 -m rebal.exhibits.pension --demo

CLI Arguments:
--demo: use local synthetic plan allocations and output/demo/.
--weighting: assets (default) or equal, for a sensitivity check.
--start: first fiscal year (default 2003).
--end: last fiscal year or ISO date (default 2022), or latest.

Reads public PPD allocations and coverage, or an in-memory demo fixture.
Writes figure_1.pdf, comparison keys in figure_1.csv, plotted annual shares
(fractions) and plan counts in figure_1_yearly.csv, and lineage metadata.
See docs/contracts/exhibits.md and docs/methods/pension.md.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, date, datetime
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator, PercentFormatter
from rich.console import Console

from rebal.paths import output_dir, public_dir

EXHIBITS = ["figure_1"]
FIELDS = ["ppd_id", "fy", "MktAssets_net", "EQTotal_Actl", "EQTotal_Trgt"]


def make_demo_allocations(effect: float = 0.025) -> pd.DataFrame:
    """Plant a known annual actual-target gap, with unequal assets and coverage."""
    return pd.DataFrame(
        [
            {
                "ppd_id": plan,
                "fy": year,
                "MktAssets_net": assets,
                "EQTotal_Actl": 0.65 + effect * np.cos(np.pi * (year - 2003)),
                "EQTotal_Trgt": np.nan if plan == 3 else 0.65,
            }
            for year in range(2003, 2023)
            for plan, assets in ((1, 100.0), (2, 300.0), (3, 200.0))
            if plan != 3 or year >= 2005
        ]
    )


def load_allocations(demo: bool = False) -> pd.DataFrame:
    if demo:
        return make_demo_allocations()
    directory = public_dir("ppd")
    frame = pd.read_csv(directory / "ppd_allocations.csv", usecols=FIELDS)
    coverage = pd.read_csv(directory / "ppd_coverage.csv")
    with duckdb.connect() as con:
        con.register("allocations", frame)
        con.register("coverage", coverage)
        mismatch = con.execute("""
            WITH observed AS (
                SELECT fy, count(*) AS plans FROM allocations GROUP BY fy
            ), expected AS (
                SELECT year(CAST(date AS DATE)) AS fy, plan_count FROM coverage
            )
            SELECT count(*) FROM observed FULL JOIN expected USING (fy)
            WHERE plans IS DISTINCT FROM plan_count
        """).fetchone()[0]
    if mismatch:
        raise ValueError("PPD coverage does not match allocation plan counts")
    return frame


def yearly_allocations(
    allocations: pd.DataFrame,
    *,
    weighting: str = "assets",
    start: int = 2003,
    end: int = 2022,
) -> pd.DataFrame:
    """Compute independent available-case means; retain empty years as gaps."""
    if weighting not in {"assets", "equal"}:
        raise ValueError("weighting must be assets or equal")
    if start > end:
        raise ValueError("start must not exceed end")
    missing = set(FIELDS) - set(allocations.columns)
    if missing:
        raise ValueError(f"Missing PPD fields: {sorted(missing)}")
    # pandas: validation of a small input before registration in DuckDB.
    frame = allocations[FIELDS].copy()
    for field in FIELDS:
        frame[field] = pd.to_numeric(frame[field], errors="raise")
    if frame[["ppd_id", "fy"]].isna().any().any():
        raise ValueError("Plan IDs and fiscal years must be nonmissing")
    keys = frame[["ppd_id", "fy"]].to_numpy()
    if not np.isfinite(keys).all() or (keys != np.floor(keys)).any():
        raise ValueError("Plan IDs and fiscal years must be finite integers")
    if frame.duplicated(["ppd_id", "fy"]).any():
        raise ValueError("Duplicate plan-year keys")
    shares = frame[["EQTotal_Actl", "EQTotal_Trgt"]].to_numpy()
    if ((~np.isnan(shares)) & ((shares < 0) | (shares > 1))).any():
        raise ValueError("Equity shares must be fractions in [0, 1] or missing")
    weight = "MktAssets_net" if weighting == "assets" else "1.0"
    # This package has no DuckDBManager; the connection owns this small computation.
    with duckdb.connect() as con:
        con.register("allocations", frame)
        return con.execute(
            f"""
            WITH eligible AS (
                SELECT *,
                    isfinite(MktAssets_net) AND MktAssets_net > 0 AS valid_assets,
                    CASE WHEN isfinite({weight}) AND {weight} > 0
                         THEN {weight} END AS weight
                FROM allocations WHERE fy BETWEEN $start AND $end
            ), annual AS (
                SELECT fy, count(*) AS plan_count,
                    count(*) FILTER (WHERE NOT coalesce(valid_assets, false))
                        AS invalid_assets_count,
                    count(*) FILTER (WHERE EQTotal_Actl IS NULL) AS actual_missing_count,
                    count(*) FILTER (WHERE EQTotal_Trgt IS NULL) AS target_missing_count,
                    count(*) FILTER (WHERE weight IS NOT NULL AND EQTotal_Actl IS NOT NULL)
                        AS actual_plan_count,
                    count(*) FILTER (WHERE weight IS NOT NULL AND EQTotal_Trgt IS NOT NULL)
                        AS target_plan_count,
                    sum(weight * EQTotal_Actl) /
                        sum(weight) FILTER (WHERE EQTotal_Actl IS NOT NULL) AS actual_share,
                    sum(weight * EQTotal_Trgt) /
                        sum(weight) FILTER (WHERE EQTotal_Trgt IS NOT NULL) AS target_share
                FROM eligible GROUP BY fy
            )
            SELECT years.fy, coalesce(plan_count, 0) AS plan_count,
                coalesce(actual_plan_count, 0) AS actual_plan_count,
                coalesce(target_plan_count, 0) AS target_plan_count,
                coalesce(actual_missing_count, 0) AS actual_missing_count,
                coalesce(target_missing_count, 0) AS target_missing_count,
                coalesce(invalid_assets_count, 0) AS invalid_assets_count,
                actual_share, target_share
            FROM range($start, $end + 1) AS years(fy)
            LEFT JOIN annual USING (fy) ORDER BY fy
        """,
            {"start": start, "end": end},
        ).fetchdf()


def comparison_values(yearly: pd.DataFrame) -> pd.DataFrame:
    with duckdb.connect() as con:
        con.register("yearly", yearly)
        values = con.execute("""
            SELECT min(actual_share), max(actual_share), median(target_share) FROM yearly
        """).fetchone()
    return pd.DataFrame(
        [
            ("figure_1", "equity_share", term, "value", value)
            for term, value in zip(
                ("actual_min", "actual_max", "target_typical"), values, strict=True
            )
        ],
        columns=["exhibit", "column", "term", "stat", "value"],
    )


def plot_allocations(yearly: pd.DataFrame, *, demo: bool = False) -> Figure:
    figure = Figure(figsize=(8, 4.8), layout="constrained")
    FigureCanvasAgg(figure)
    axis = figure.subplots()
    for field, label, style in (
        ("actual_share", "Actual", "-"),
        ("target_share", "Target", "--"),
    ):
        axis.plot(yearly.fy, yearly[field], style, label=label, linewidth=2)
    axis.set(
        xlabel="Fiscal year",
        ylabel="Public equity share",
        title="Figure 1: Public pension equity allocations"
        + (" (synthetic demo)" if demo else ""),
    )
    axis.yaxis.set_major_formatter(PercentFormatter(1))
    axis.xaxis.set_major_locator(MaxNLocator(integer=True))
    axis.grid(alpha=0.2)
    axis.legend()
    return figure


def run(
    demo: bool = False,
    *,
    weighting: str = "assets",
    start: int = 2003,
    end: str = "2022",
) -> list[Path]:
    allocations = load_allocations(demo)
    last_year = (
        int(allocations.fy.max())
        if end == "latest"
        else date.fromisoformat(end).year
        if "-" in end
        else int(end)
    )
    yearly = yearly_allocations(
        allocations, weighting=weighting, start=start, end=last_year
    )
    destination = output_dir("demo" if demo else "figures")
    csv, pdf, annual, metadata = (
        destination / name
        for name in (
            "figure_1.csv",
            "figure_1.pdf",
            "figure_1_yearly.csv",
            "pension.metadata.json",
        )
    )
    comparison_values(yearly).to_csv(csv, index=False)
    yearly.to_csv(annual, index=False)
    figure = plot_allocations(yearly, demo=demo)
    figure.savefig(pdf)
    figure.clear()
    metadata.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "weighting": weighting,
                "start": start,
                "end": last_year,
                "inputs": ["local synthetic pension fixture"]
                if demo
                else [
                    "data/public/ppd/ppd_allocations.csv",
                    "data/public/ppd/ppd_coverage.csv",
                ],
                "outputs": [csv.name, pdf.name, annual.name],
                "units": "fraction of net market assets; counts are plans",
            },
            indent=2,
        )
        + "\n"
    )
    return [csv, pdf, annual, metadata]


def main() -> None:
    parser = argparse.ArgumentParser(description="Public pension equity allocations.")
    parser.add_argument("--demo", action="store_true", help="Use synthetic plan data.")
    parser.add_argument("--weighting", choices=["assets", "equal"], default="assets")
    parser.add_argument("--start", type=int, default=2003, help="First fiscal year.")
    parser.add_argument(
        "--end", default="2022", help="Last fiscal year, ISO date, or latest."
    )
    args = parser.parse_args()
    for path in run(**vars(args)):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
