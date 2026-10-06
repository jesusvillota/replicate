#!/usr/bin/env bash

set -euo pipefail

TASK_DIR="/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004"
PAPEREXTRACT_BIN="$TASK_DIR/paperextract/.venv/bin/paperextract"
LIBRARY="$TASK_DIR/library"
OUTPUT_DIR="$TASK_DIR/outputs"

mkdir -p "$OUTPUT_DIR" "$TASK_DIR/logs"
exec > >(tee "$TASK_DIR/logs/finalize.log") 2>&1

"$PAPEREXTRACT_BIN" publish "$TASK_DIR/staged" --library "$LIBRARY"

python3 - "$TASK_DIR" <<'PY'
from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path


task_dir = Path(sys.argv[1])
input_dir = task_dir / "inputs"
library = task_dir / "library"
output_dir = task_dir / "outputs"
inputs = sorted(input_dir.glob("*.pdf"))
if len(inputs) != 3:
    raise SystemExit(f"Expected 3 input PDFs, found {len(inputs)}")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


published: dict[str, set[Path]] = {}
for source in library.rglob("*.pdf"):
    paper_dir = next(
        (parent for parent in source.parents if (parent / "paper.md").is_file()),
        None,
    )
    if paper_dir is not None:
        published.setdefault(digest(source), set()).add(paper_dir)

expected_names: set[str] = set()
for source in inputs:
    matches = published.get(digest(source), set())
    if len(matches) != 1:
        raise SystemExit(
            f"Expected one published paper for {source.name}; found {len(matches)}"
        )
    paper_dir = next(iter(matches))
    markdown = paper_dir / "paper.md"
    body = markdown.read_text(encoding="utf-8").strip()
    if len(body.split()) < 100:
        raise SystemExit(f"Extracted text is too short: {markdown}")
    destination = output_dir / f"{source.stem}.md"
    shutil.copyfile(markdown, destination)
    if destination.stat().st_size == 0:
        raise SystemExit(f"Empty output: {destination}")
    expected_names.add(destination.name)
    print(
        f"{destination.name}\t{destination.stat().st_size} bytes\t"
        f"{len(body.split())} words"
    )

actual_names = {path.name for path in output_dir.glob("*.md")}
if actual_names != expected_names:
    raise SystemExit(
        f"Output names differ: expected {sorted(expected_names)}, "
        f"found {sorted(actual_names)}"
    )
print(f"Verified {len(actual_names)} non-empty Markdown outputs")
PY
