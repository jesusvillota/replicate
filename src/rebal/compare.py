"""uv run python3 -m rebal.compare --demo --out output/demo/compare.md

CLI Arguments:
--demo: read output/demo instead of output/tables and output/figures.
--variant NAME: read only robustness/NAME under the selected output folders.
--out FILE: Markdown destination (default: output/demo/compare.md with --demo,
otherwise output/compare.md).

Reads docs/results/targets.csv and keyed exhibit CSVs (see
docs/methods/comparison.md). Writes a comparison report with input lineage,
coverage, sign and significance checks; never runs an exhibit.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

import duckdb
from rich.console import Console

from rebal.comparison_exports import coverage_report, discover_csvs
from rebal.paths import REPO_ROOT

STATS = ("coef", "se", "t", "adj_r2", "nobs", "value")
KEY = ("exhibit", "column", "term")


def _read_csv(path: Path, required: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream, strict=True)
        missing = set(required) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns {', '.join(sorted(missing))}")
        rows = list(reader)
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{path}: row width differs from header")
        if any(not row.get(key, "").strip() for key in KEY):
            raise ValueError(f"{path}: exhibit, column and term must be nonempty")
    return rows


def _read_actual(path: Path) -> list[tuple]:
    """Normalize keyed estimates, including TASK-014's signed one-SD effects."""
    rows = _read_csv(path, KEY)
    actual = []
    for row in rows:
        key = tuple(row[name] for name in KEY)
        if path.name == "magnitudes.csv":
            if "magnitude_bps" not in row:
                raise ValueError("magnitudes need a magnitude_bps column")
            actual.append((*key, "value", row["magnitude_bps"]))
        elif "stat" in row:
            if "value" not in row:
                raise ValueError("long-format statistics need a value column")
            actual.append((*key, row["stat"], row["value"]))
        else:
            actual.extend((*key, stat, row[stat]) for stat in STATS if stat in row)
    if not actual:
        raise ValueError("no supported numeric statistics")
    normalized = []
    seen = set()
    for *key, value in actual:
        key = tuple(key)
        if key in seen:
            raise ValueError("duplicate exhibit/column/term/stat key")
        seen.add(key)
        if key[-1] not in STATS:
            raise ValueError(f"invalid statistic {key[-1]!r}")
        number = float(value) if value.strip() else None
        if number is not None and not math.isfinite(number):
            raise ValueError("non-finite value")
        normalized.append((*key, number))
    return normalized


def compare(
    targets_path: Path,
    exhibit_dirs: list[Path],
    *,
    skipped: list[str] | None = None,
    variant: str | None = None,
) -> list[dict]:
    """Join exact string keys and statistic names; missing estimates stay NULL.

    Regression files follow docs/contracts/exhibits.md. Other exhibits can use
    the same keys with wide statistic columns, or long stat,value columns.
    No shared DuckDB manager exists in rebal; use one scoped connection here.
    """
    targets = _read_csv(
        targets_path, (*KEY, "stat", "paper_value", "approx", "source_page")
    )
    target_keys = {tuple(row[key] for key in KEY) for row in targets}
    skipped = skipped if skipped is not None else []
    paths = discover_csvs(exhibit_dirs, variant)
    actual = []
    seen = set()
    for path in paths:
        try:
            incoming = _read_actual(path)
            incoming = [row for row in incoming if row[:3] in target_keys]
            if not incoming:
                raise ValueError("no matching target keys")
            keys = {row[:4] for row in incoming}
            if seen & keys:
                raise ValueError("duplicate key across CSV files")
        except (OSError, UnicodeError, csv.Error, ValueError) as exc:
            reason = str(exc)
            skipped.append(
                reason if reason.startswith(f"{path}:") else f"{path}: {reason}"
            )
            continue
        seen.update(keys)
        actual.extend(incoming)

    with duckdb.connect() as con:
        con.execute("""CREATE TEMP TABLE targets (
            exhibit VARCHAR, "column" VARCHAR, term VARCHAR, stat VARCHAR,
            paper_value DOUBLE, approx INTEGER, source_page VARCHAR)""")
        con.execute("""CREATE TEMP TABLE actual (
            exhibit VARCHAR, "column" VARCHAR, term VARCHAR, stat VARCHAR, value DOUBLE)""")
        if targets:
            con.executemany(
                "INSERT INTO targets VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    tuple(
                        row[key]
                        for key in (
                            *KEY,
                            "stat",
                            "paper_value",
                            "approx",
                            "source_page",
                        )
                    )
                    for row in targets
                ],
            )
        if actual:
            con.executemany(
                "INSERT INTO actual VALUES (?, ?, ?, ?, ?)",
                actual,
            )
        for table, value in (("targets", "paper_value"), ("actual", "value")):
            # Table/column names are constants above, never user-provided SQL.
            if con.execute(f"""SELECT count(*) FROM (
                SELECT exhibit, "column", term, stat FROM {table}
                GROUP BY ALL HAVING count(*) > 1)""").fetchone()[0]:
                raise ValueError(f"{table}: duplicate exhibit/column/term/stat key")
            if con.execute(f"""SELECT count(*) FROM {table}
                WHERE stat NOT IN ('coef', 'se', 't', 'adj_r2', 'nobs', 'value')
                OR stat IS NULL OR ({value} IS NOT NULL AND NOT isfinite({value}))""").fetchone()[
                0
            ]:
                raise ValueError(f"{table}: invalid statistic or non-finite value")
        if con.execute("""SELECT count(*) FROM targets
            WHERE paper_value IS NULL OR approx NOT IN (0, 1) OR approx IS NULL
                OR source_page IS NULL OR trim(source_page) = '' """).fetchone()[0]:
            raise ValueError(
                "targets: paper_value, approx and source_page are required"
            )

        result = con.execute("""
            WITH paper_tests AS (
                SELECT exhibit, "column", term,
                    coalesce(max(paper_value) FILTER (WHERE stat = 't'),
                        max(paper_value) FILTER (WHERE stat = 'coef') /
                        nullif(max(paper_value) FILTER (WHERE stat = 'se'), 0)) AS t
                FROM targets GROUP BY ALL
            ), actual_tests AS (
                SELECT exhibit, "column", term,
                    coalesce(max(value) FILTER (WHERE stat = 't'),
                        max(value) FILTER (WHERE stat = 'coef') /
                        nullif(max(value) FILTER (WHERE stat = 'se'), 0)) AS t
                FROM actual GROUP BY ALL
            )
            SELECT p.*, a.value AS ours, a.stat IS NOT NULL AS exported,
                a.value / nullif(p.paper_value, 0) AS ratio,
                CASE WHEN p.stat IN ('coef', 't', 'value') AND a.value IS NOT NULL
                    THEN sign(p.paper_value) = sign(a.value) END AS sign_match,
                CASE WHEN p.stat IN ('coef', 't') AND a.value IS NOT NULL
                        AND pt.t IS NOT NULL AND ot.t IS NOT NULL
                    THEN (abs(pt.t) >= 1.96) = (abs(ot.t) >= 1.96)
                    END AS significance_match
            FROM targets p
            LEFT JOIN actual a USING (exhibit, "column", term, stat)
            LEFT JOIN paper_tests pt USING (exhibit, "column", term)
            LEFT JOIN actual_tests ot USING (exhibit, "column", term)
            ORDER BY p.exhibit, p."column", p.term, p.stat
        """)
        names = [column[0] for column in result.description]
        return [dict(zip(names, row)) for row in result.fetchall()]


def _number(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.6g}"


def _match(value: bool | None) -> str:
    return "N/A" if value is None else ("yes" if value else "no")


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def render_report(
    rows: list[dict],
    targets_path: Path,
    exhibit_dirs: list[Path],
    *,
    skipped: list[str] | None = None,
) -> str:
    groups = defaultdict(list)
    for row in rows:
        groups[row["exhibit"]].append(row)
    missing = [
        name
        for name, group in groups.items()
        if all(row["ours"] is None for row in group)
    ]
    matched = sum(row["ours"] is not None for row in rows)
    matched_exhibits = [name for name in groups if name not in missing]
    lines = [
        "# Paper comparison",
        "",
        "## Summary",
        "",
        f"- Targets matched: {matched}/{len(rows)}",
    ]
    for label, key in (
        ("Sign-match rate", "sign_match"),
        ("Significance-match rate", "significance_match"),
    ):
        eligible = [row[key] for row in rows if row[key] is not None]
        rate = f"{sum(eligible) / len(eligible):.1%}" if eligible else "N/A"
        lines.append(
            f"- {label}: {rate} ({sum(eligible)}/{len(eligible)} eligible targets)"
        )
    lines.extend(
        [
            f"- Missing exhibits: {', '.join(missing) if missing else 'none'}",
            f"- Matched exhibits: {', '.join(matched_exhibits) if matched_exhibits else 'none'}",
            f"- Skipped CSVs: {len(skipped or [])}",
            *[f"  - {_cell(reason)}" for reason in (skipped or [])],
            "",
            f"Targets: `{targets_path}`. Inputs: "
            + ", ".join(f"`{folder}`" for folder in exhibit_dirs)
            + ".",
            "",
            (
                "Each row compares one statistic. Approximate chart readings have a `~` prefix. "
                "Sign checks apply to coef, t and value. Significance checks apply to coef and t, "
                "using |t| ≥ 1.96 on both sides (or neither). Where t is absent, coef/se is used. "
                "N/A means missing data, an inapplicable check, or division by zero. "
                "Missing exhibits have no matched numeric targets; partial exhibits retain N/A rows."
            ),
            "",
        ]
    )
    for exhibit, group in groups.items():
        lines.extend(
            [
                f"## {_cell(exhibit)}",
                "",
                "| term | paper | ours | ours/paper | sign match | significance match |",
                "|---|---:|---:|---:|---|---|",
            ]
        )
        for row in group:
            label = _cell(f"{row['column']}: {row['term']} [{row['stat']}]")
            paper = ("~" if row["approx"] else "") + _number(row["paper_value"])
            lines.append(
                f"| {label} | {paper} | {_number(row['ours'])} | "
                f"{_number(row['ratio'])} | {_match(row['sign_match'])} | "
                f"{_match(row['significance_match'])} |"
            )
        lines.append("")
    return "\n".join(lines) + coverage_report(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare produced exhibits with paper targets."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Read only output/demo CSVs."
    )
    parser.add_argument(
        "--variant", help="Compare only robustness/NAME; default: main outputs."
    )
    parser.add_argument(
        "--out",
        type=Path,
        help="Markdown destination (default: output/[demo/]compare.md).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = REPO_ROOT / "docs" / "results" / "targets.csv"
    folders = [
        REPO_ROOT / "output" / kind
        for kind in (("demo",) if args.demo else ("tables", "figures"))
    ]
    skipped: list[str] = []
    rows = compare(targets, folders, skipped=skipped, variant=args.variant)
    destination = args.out or REPO_ROOT / "output" / (
        "demo/compare.md" if args.demo else "compare.md"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render_report(
            rows,
            targets,
            [folder / "robustness" / args.variant for folder in folders]
            if args.variant
            else folders,
            skipped=skipped,
        ),
        encoding="utf-8",
    )
    Console().print(f"Comparison report: {destination}", markup=False)


if __name__ == "__main__":
    main()
