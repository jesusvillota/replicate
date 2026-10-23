"""uv run python3 -m rebal.report --demo --out /tmp/replication_report_demo.md

CLI Arguments:
--demo: read only fixture exports in output/demo (generate them with rebal.exhibits).
--out FILE: report destination (default: docs/results/replication_report.md).
--size-tolerance: relative size tolerance, default 0.25.
--absolute-tolerance: absolute tolerance in each target's units, default 0.0001.
--gap-notes FILE: checked-in cause annotations, default docs/results/gap_notes.csv.
--variant NAME: read only robustness/NAME within each selected output folder.

Reads comparison targets, exhibit outputs, contracts, source map and method links.
Writes only the requested Markdown report, including its input lineage and options.
Does not estimate models, generate fixtures or change any upstream output.
"""

from __future__ import annotations

import argparse
import csv
import logging
import math
import os
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit

from rebal.compare import compare
from rebal.comparison_exports import unmatched_reason
from rebal.paths import REPO_ROOT

STATUSES = ("replicates", "partly", "fails", "not available", "not run")
CAUSES = {"proxy", "timing", "sample", "method", "data"}


def contract_ids(path: Path) -> list[str]:
    ids = re.findall(
        r"^- `([^`]+)`\s*$", path.read_text(encoding="utf-8"), re.MULTILINE
    )
    if not ids or len(ids) != len(set(ids)):
        raise ValueError(f"{path}: expected unique exhibit IDs")
    return ids


def read_gap_notes(path: Path, ids: list[str]) -> dict[str, list[dict[str, str]]]:
    notes = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["exhibit", "cause", "note"]:
            raise ValueError(f"{path}: expected exhibit,cause,note")
        for row in reader:
            if (
                None in row
                or any(value is None for value in row.values())
                or row["exhibit"] not in ids
                or row["cause"] not in CAUSES
                or not row["note"].strip()
            ):
                raise ValueError(f"{path}: invalid gap annotation {row!r}")
            notes[row["exhibit"]].append(row)
    return dict(notes)


def _unavailable(row: dict) -> bool:
    reason = unmatched_reason(row)
    return row["ours"] is None and reason.startswith("not available: FEARS")


def classify(rows: list[dict], relative: float, absolute: float) -> str:
    """Apply conservative whole-exhibit rules; missing estimates never fail."""
    available = [row for row in rows if not _unavailable(row)]
    numeric = [row for row in available if row["ours"] is not None]
    if not numeric:
        return "not available" if rows and not available else "not run"
    # Coefficients carry size; do not double-count their t-statistic as size.
    coefficient_keys = {
        (row["column"], row["term"]) for row in rows if row["stat"] == "coef"
    }
    primary = [
        row
        for row in numeric
        if row["stat"] in {"coef", "value"}
        or (row["stat"] == "t" and (row["column"], row["term"]) not in coefficient_keys)
    ]
    signs = [row["sign_match"] for row in primary if row["sign_match"] is not None]
    if len(numeric) < len(rows) or not primary:
        return "partly"
    if signs and not any(signs):
        return "fails"
    sizes = all(
        abs(row["ours"] - row["paper_value"])
        <= max(absolute, relative * abs(row["paper_value"]))
        for row in primary
    )
    significance = all(row["significance_match"] is not False for row in primary)
    # A coefficient without a comparable significance test cannot certify replication.
    tested = all(
        row["stat"] != "coef" or row["significance_match"] is not None
        for row in primary
    )
    return (
        "replicates" if sizes and significance and tested and all(signs) else "partly"
    )


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
        *["| " + " | ".join(_cell(cell) for cell in row) + " |" for row in rows],
        "",
    ]


def _link(path: Path, destination: Path) -> str:
    return (
        Path(os.path.relpath(path, destination.parent)).as_posix().replace(" ", "%20")
    )


def _rebase_links(text: str, source: Path, destination: Path) -> str:
    def replace(match: re.Match) -> str:
        label, target = match.groups()
        if urlsplit(target).scheme or target.startswith(("/", "#")):
            return match.group(0)
        path, marker, fragment = target.partition("#")
        return (
            f"[{label}]({_link(source.parent / path, destination)}{marker}{fragment})"
        )

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, text)


def source_rows(path: Path, destination: Path) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^\| D\d+ \|", line):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 10:
                raise ValueError(f"{path}: unexpected source-map table layout")
            rows.append(
                [
                    cells[0],
                    cells[1],
                    _rebase_links(cells[4], path, destination),
                    cells[5],
                    cells[8],
                    _rebase_links(cells[9], path, destination),
                ]
            )
    if [row[0] for row in rows] != [f"D{i}" for i in range(1, 29)]:
        raise ValueError(f"{path}: expected D1–D28 exactly once, in order")
    return rows


def _headline(rows: list[dict]) -> dict | None:
    # Stable semantic preferences, then comparison key order. Never pick by fit.
    return next(
        iter(
            sorted(
                rows,
                key=lambda row: (
                    row["stat"] not in {"coef", "value", "t"},
                    row["term"] not in {"threshold", "annual_bps", "sharpe"},
                    row["column"] not in {"1", "headline", "strategy"},
                    row["column"],
                    row["term"],
                    row["stat"],
                ),
            )
        ),
        None,
    )


def _number(value: float | None) -> str:
    return "N/A" if value is None else f"{value:.6g}"


def _latest_sample(root: Path, destination: Path, demo: bool) -> list[str]:
    path = (
        root
        / "output"
        / ("demo" if demo else "tables")
        / "robustness/latest/latest_comparison.csv"
    )
    lines = ["## Latest sample (footnote 32)", ""]
    if not path.is_file():
        return lines + ["not run", ""]
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = ["exhibit", "column", "term", "stat", "sample", "value"]
        if reader.fieldnames != fields:
            raise ValueError(f"{path}: expected {','.join(fields)}")
        rows = [[row[field] for field in fields] for row in reader]
    lines += [
        (
            f"[Latest-sample comparison]({_link(path, destination)}). "
            "Table 1 compares paper_end with latest; sample dates are actual outcome dates."
        ),
        "",
    ]
    return lines + _table(fields, rows)


def generate_report(
    root: Path,
    destination: Path,
    *,
    demo: bool = False,
    relative: float = 0.25,
    absolute: float = 0.0001,
    gap_notes: Path | None = None,
    variant: str | None = None,
) -> str:
    """Read inputs and return Markdown without writing any file."""
    if any(not math.isfinite(value) or value < 0 for value in (relative, absolute)):
        raise ValueError("size tolerances must be finite and nonnegative")
    ids = contract_ids(root / "docs/contracts/exhibits.md")
    notes_path = gap_notes or root / "docs/results/gap_notes.csv"
    notes = read_gap_notes(notes_path, ids)
    targets = root / "docs/results/targets.csv"
    folders = [
        root / "output" / kind
        for kind in (("demo",) if demo else ("tables", "figures"))
    ]
    skipped: list[str] = []
    comparisons = compare(targets, folders, skipped=skipped, variant=variant)
    groups = defaultdict(list)
    for row in comparisons:
        if row["exhibit"] not in ids:
            raise ValueError(f"target exhibit absent from contract: {row['exhibit']}")
        groups[row["exhibit"]].append(row)
    statuses = {name: classify(groups[name], relative, absolute) for name in ids}
    lines = [
        "# Replication report",
        "",
        "## Summary",
        "",
        "Synthetic fixture outputs; these are not real-data replication findings."
        if demo
        else "Main-run output comparison with the paper.",
        "",
        f"- Target keys joined: {sum(bool(row['exported']) for row in comparisons)}/{len(comparisons)}",
        f"- Numeric targets joined: {sum(row['ours'] is not None for row in comparisons)}/{len(comparisons)}",
    ]
    for label, key in (
        ("Sign-match rate", "sign_match"),
        ("Significance-match rate", "significance_match"),
    ):
        eligible = [row[key] for row in comparisons if row[key] is not None]
        rate = f"{sum(eligible) / len(eligible):.1%}" if eligible else "N/A"
        lines.append(
            f"- {label}: {rate} ({sum(eligible)}/{len(eligible)} eligible targets)"
        )
    for status in STATUSES:
        names = [name for name in ids if statuses[name] == status]
        lines.append(f"- {status} ({len(names)}): {', '.join(names) or 'none'}")
    selected = [
        folder / "robustness" / variant if variant else folder for folder in folders
    ]
    lines += [
        "",
        f"Targets: `{targets}`. Inputs: " + ", ".join(f"`{p}`" for p in selected) + ".",
        (
            f"Gap annotations: `{notes_path}`. Size tolerance: {relative:.1%} relative, "
            f"{absolute:g} absolute (target units). Significance: abs(t) ≥ 1.96, from rebal.compare."
        ),
        "",
        "## Exhibit table",
        "",
        (
            "One row per contract ID, including text costs and strategy results (table_6a–table_6c). "
            "The status covers all primary targets; the headline is one named statistic. "
            "Missing values cannot establish a failed replication."
        ),
        "",
    ]
    exhibit_rows = []
    for name in ids:
        rows = groups[name]
        headline = _headline(rows)
        note = [
            f"{sum(row['ours'] is not None for row in rows)}/{len(rows)} numeric targets"
        ]
        if headline:
            note.append(
                f"headline {headline['column']}:{headline['term']} [{headline['stat']}]"
            )
        else:
            note.append("no numeric paper targets; status not assessed")
        note.extend(
            dict.fromkeys(unmatched_reason(row) for row in rows if row["ours"] is None)
        )
        exhibit_rows.append(
            [
                name,
                statuses[name],
                ("~" if headline["approx"] else "") + _number(headline["paper_value"])
                if headline
                else "N/A",
                _number(headline["ours"]) if headline else "N/A",
                "; ".join(note),
            ]
        )
    lines += _table(
        ["exhibit", "status", "headline paper value", "our value", "note"], exhibit_rows
    )
    lines += [
        "## Gap notes",
        "",
        (
            "Only checked-in annotations assign causes. Blank means no recorded cause. "
            "Notes preserve the historical core run, including its tentative explanations; "
            "they do not diagnose the current or synthetic run."
        ),
        "",
    ]
    lines += _table(
        ["exhibit", "cause", "note"],
        [
            [name, note["cause"], note["note"]]
            for name in ids
            for note in notes.get(name, [{"cause": "", "note": ""}])
        ],
    )
    if skipped:
        lines += [
            "Skipped comparison inputs:",
            "",
            *[f"- {_cell(reason)}" for reason in skipped],
            "",
        ]
    sources = root / "docs/data/sources.md"
    lines += [
        "## Data and proxies",
        "",
        (
            f"[Master source map]({_link(sources, destination)}) · "
            f"[Proxy comparison]({_link(root / 'docs/data/proxy_comparison.md', destination)})"
        ),
        "",
    ]
    lines += _table(
        [
            "dataset",
            "variable",
            "our source or proxy",
            "class",
            "availability",
            "source card",
        ],
        source_rows(sources, destination),
    )
    lines += ["## Method choices", ""]
    lines += [
        f"- [{path.name}]({_link(path, destination)})"
        for path in sorted((root / "docs/methods").glob("*.md"))
    ]
    lines += [""] + _latest_sample(root, destination, demo)
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the replication report.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Read only synthetic fixture exports in output/demo.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "docs/results/replication_report.md",
        help="Markdown destination.",
    )
    parser.add_argument(
        "--gap-notes", type=Path, help="CSV with exhibit,cause,note annotations."
    )
    parser.add_argument(
        "--size-tolerance",
        type=float,
        default=0.25,
        help="Relative size tolerance (default: 0.25).",
    )
    parser.add_argument(
        "--absolute-tolerance",
        type=float,
        default=0.0001,
        help="Absolute size tolerance in target units (default: 0.0001).",
    )
    parser.add_argument(
        "--variant", help="Read only robustness/NAME; no fallback to main."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destination = args.out.expanduser().resolve()
    text = generate_report(
        REPO_ROOT,
        destination,
        demo=args.demo,
        relative=args.size_tolerance,
        absolute=args.absolute_tolerance,
        gap_notes=args.gap_notes,
        variant=args.variant,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.getLogger(__name__).info("Replication report: %s", destination)


if __name__ == "__main__":
    main()
