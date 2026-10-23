"""uv run python3 -m rebal.latest --demo

CLI Arguments:
--demo: use synthetic fixtures and output/demo/robustness/latest/.
--timing: clean (default) or literal signal timing.

Reads the panel and signals contracts. Writes latest-sample Tables 1 and 3,
a paper-end/latest comparison and metadata under robustness/latest/ only.
No figures or main-run outputs are written.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
from rich.console import Console

from rebal.exhibits.predictive_tables import (
    DEFAULT_SAMPLE,
    build_tables,
    load_panel,
    load_signals,
)
from rebal.paths import output_dir

COMPARISON_COLUMNS = ["exhibit", "column", "term", "stat", "sample", "value"]
COMPARISON_STATS = ["coef", "se", "t", "nobs", "sample_start", "sample_end"]
TERMS = {"threshold", "calendar:week4"}


def comparison_rows(table: pd.DataFrame, sample: str) -> list[dict]:
    """Export the two Table 1 effects, including each column's actual dates."""
    return [
        {
            "exhibit": row.exhibit,
            "column": row.column,
            "term": row.term,
            "stat": stat,
            "sample": sample,
            "value": getattr(row, stat),
        }
        for row in table.itertuples(index=False)
        if row.term in TERMS
        for stat in COMPARISON_STATS
    ]


def run(demo: bool = False, *, timing: str = "clean") -> list[Path]:
    """Build both samples in memory; write only the dedicated latest folder."""
    if timing not in {"clean", "literal"}:
        raise ValueError("timing must be clean or literal")
    panel = load_panel(demo=demo)
    signals = load_signals(demo=demo, timing=timing)
    tables, _ = build_tables(signals, panel, end="latest")
    paper, _ = build_tables(signals, panel, end=DEFAULT_SAMPLE[1])
    destination = output_dir("demo" if demo else "tables") / "robustness/latest"
    destination.mkdir(parents=True, exist_ok=True)
    outputs = []
    for exhibit in ("table_1", "table_3"):
        path = destination / f"{exhibit}.csv"
        tables[exhibit].to_csv(path, index=False)
        outputs.append(path)
    comparison = destination / "latest_comparison.csv"
    with comparison.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=COMPARISON_COLUMNS)
        writer.writeheader()
        writer.writerows(comparison_rows(paper["table_1"], "paper_end"))
        writer.writerows(comparison_rows(tables["table_1"], "latest"))
    outputs.append(comparison)
    metadata = destination / "latest.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "module": "rebal.latest",
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "timing": timing,
                "se": "hc1",
                "samples": {
                    "paper_end": list(DEFAULT_SAMPLE),
                    "latest": [
                        DEFAULT_SAMPLE[0],
                        pd.Timestamp(panel.date.max()).date().isoformat(),
                    ],
                },
                "inputs": [
                    "rebal.demo" if demo else "daily_panel.parquet",
                    "rebal.demo" if demo else f"signals_{timing}.parquet",
                ],
                "outputs": [path.name for path in outputs],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return outputs + [metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare paper-end and latest samples."
    )
    parser.add_argument("--demo", action="store_true", help="Use synthetic fixtures.")
    parser.add_argument("--timing", choices=["clean", "literal"], default="clean")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    console = Console()
    for path in run(**vars(args)):
        console.print(str(path), markup=False)


if __name__ == "__main__":
    main()
