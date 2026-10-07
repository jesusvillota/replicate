#!/usr/bin/env bash
#SBATCH --job-name=socr-task005-repair
#SBATCH --partition=gpu_compute
#SBATCH --qos=gpu_compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=24G
#SBATCH --gres=gpu:1
#SBATCH --time=72:00:00
#SBATCH --signal=TERM@120
#SBATCH --output=logs/socr-%j.out
#SBATCH --error=logs/socr-%j.err

set -euo pipefail

TASK_DIR="/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-005"
INPUT_DIR="$TASK_DIR/inputs"
SOURCE_DIR="$TASK_DIR/source"
OUTPUT_DIR="$TASK_DIR/ocr/socr"
LOG_DIR="$TASK_DIR/logs"
REPAIR_ROOT="$TASK_DIR/repair_runs"
REPAIR_INPUT_DIR="$REPAIR_ROOT/input-${SLURM_JOB_ID}"
REPAIR_OUTPUT_DIR="$REPAIR_ROOT/output-${SLURM_JOB_ID}"
REPAIR_MAP="$REPAIR_ROOT/map-${SLURM_JOB_ID}.json"
REPAIR_AUDIT="$REPAIR_ROOT/audit-${SLURM_JOB_ID}.json"
VENV_DIR="$TASK_DIR/venv"
OLLAMA_DIR="$TASK_DIR/ollama"
OLLAMA_MODELS="$TASK_DIR/models/ollama"
UV_BIN="/mnt/slurm-beegfs/Users/j-vill36/.local/bin/uv"
OLLAMA_VERSION="v0.40.0"
QWEN_MODEL="qwen3-vl:30b-a3b-instruct"
QWEN_REPAIR_MODEL="qwen3-vl:30b-a3b-instruct-anti-repeat"
QWEN_JUDGE_MODEL="qwen3-vl:30b-a3b-instruct-table-judge"
QWEN_REPETITION_PENALTY="1.15"
QWEN_REPEAT_LAST_N="128"
QWEN_OCR_NUM_CTX="12288"
QWEN_OCR_MAX_PIXELS="6291456"

mkdir -p "$LOG_DIR" "$INPUT_DIR" "$SOURCE_DIR" \
  "$OUTPUT_DIR" "$OLLAMA_MODELS" "$TASK_DIR/cache" "$TASK_DIR/python"
cd "$TASK_DIR"

export TMPDIR="/tmp/socr-task005-${SLURM_JOB_ID}"
export DUCKDB_TEMP_DIR="$TMPDIR/duckdb"
export MPLCONFIGDIR="$TMPDIR/mpl"
mkdir -p "$DUCKDB_TEMP_DIR" "$MPLCONFIGDIR"
trap 'rm -rf "$TMPDIR"' EXIT

export UV_CACHE_DIR="$TASK_DIR/cache/uv"
export UV_PYTHON_INSTALL_DIR="$TASK_DIR/python"
export PIP_CACHE_DIR="$TASK_DIR/cache/pip"
export XDG_CACHE_HOME="$TASK_DIR/cache/xdg"
export HF_HOME="$TASK_DIR/cache/huggingface"
export HF_HUB_CACHE="$HF_HOME/hub"
export HUGGINGFACE_HUB_CACHE="$HF_HOME/hub"
export TRANSFORMERS_CACHE="$HF_HOME/transformers"
export TORCH_HOME="$TASK_DIR/cache/torch"
export TORCH_EXTENSIONS_DIR="$TASK_DIR/cache/torch_extensions"
export OLLAMA_MODELS
export OLLAMA_HOST="127.0.0.1:11434"
export OLLAMA_NO_CLOUD=1
export OLLAMA_KEEP_ALIVE=30m
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1
export QWEN_OCR_OLLAMA_URL="http://127.0.0.1:11434/v1"
export QWEN_OCR_OLLAMA_MODEL="$QWEN_MODEL"
# Marker runs on CPU. This leaves the L4 available for the 23 GB Qwen model.
export TORCH_DEVICE=cpu

unset GEMINI_API_KEY GOOGLE_API_KEY GOOGLE_APPLICATION_CREDENTIALS
unset MISTRAL_API_KEY DASHSCOPE_API_KEY OPENROUTER_API_KEY

echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "SLURM_JOB_PARTITION=$SLURM_JOB_PARTITION"
echo "SLURM_JOB_NODELIST=$SLURM_JOB_NODELIST"
echo "SLURMD_NODENAME=$(hostname)"
echo "Started=$(date -Is)"
echo "REPAIR_CLOUD_POLICY=local Ollama only; OLLAMA_NO_CLOUD=1"
echo "OCR_BACKEND=qwen-ocr/ollama"
echo "TABLE_JUDGE_BACKEND=local Ollama vision judge"
echo "TABLE_JUDGE_CLOUD_LADDER=disabled"
echo "SOCR_REPO_COMMIT=ed2550e259cdb09e92b3fc62c1d1349f0fb9a95a"
echo "QWEN_OCR_REPO_COMMIT=9ca56004c1733a739b1902cc2cfa4e6b9c35e3bb"
echo "MARKER_OCR_REPO_COMMIT=4d63fb5d4c7d8d0711d1c260112e7be827eba248"
echo "OCR_OUTPUT_CONTRACT_COMMIT=52554b96ec2212d161cb1eb97a381592e71f0b97"
echo "QWEN_MODEL=$QWEN_MODEL"
echo "QWEN_REPAIR_MODEL=$QWEN_REPAIR_MODEL"
echo "QWEN_JUDGE_MODEL=$QWEN_JUDGE_MODEL"
echo "QWEN_REPETITION_PENALTY=$QWEN_REPETITION_PENALTY"
echo "QWEN_REPEAT_LAST_N=$QWEN_REPEAT_LAST_N"
echo "QWEN_OCR_NUM_CTX=$QWEN_OCR_NUM_CTX"
echo "QWEN_OCR_MAX_PIXELS=$QWEN_OCR_MAX_PIXELS"
echo "FIGURE_ASSETS=preserved from initial SOCR output"
echo "Paid API credentials unset for this job."
python3 --version
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

shopt -s nullglob
inputs=("$INPUT_DIR"/*.pdf)
if [[ ${#inputs[@]} -ne 3 ]]; then
  echo "Expected 3 input PDFs, found ${#inputs[@]} in $INPUT_DIR" >&2
  exit 1
fi
sha256sum "${inputs[@]}"

if [[ ! -x "$UV_BIN" ]]; then
  echo "uv is not executable at $UV_BIN" >&2
  exit 1
fi
"$UV_BIN" python install 3.12
if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  "$UV_BIN" venv --python 3.12 "$VENV_DIR"
else
  echo "Reusing existing Python environment at $VENV_DIR"
fi
"$VENV_DIR/bin/python" --version

"$UV_BIN" pip install --python "$VENV_DIR/bin/python" \
  "click>=8.1" \
  "httpx>=0.27" \
  "markdown-it-py>=3.0.0" \
  "marker-pdf>=0.4.0" \
  "numpy>=1.26.0" \
  "opencv-python-headless>=4.9.0" \
  "pillow>=10.0,<11" \
  "pylatexenc>=2.10" \
  "pymupdf>=1.24.0" \
  "pypdf>=3.0.0" \
  "pyyaml>=6.0.0" \
  "rich>=13.0.0"

install_source_package() {
  local package="$1"
  local repo="$2"
  local revision="$3"
  local archive="$SOURCE_DIR/${package}.tar.gz"
  local source="$SOURCE_DIR/$package"
  local url="https://codeload.github.com/r-uben/$repo/tar.gz/$revision"

  if [[ ! -f "$source/pyproject.toml" ]]; then
    rm -rf "$source"
    echo "Fetching $repo at $revision"
    python3 - "$url" "$archive" <<'PY'
import sys
from urllib.request import urlopen

url, destination = sys.argv[1:]
with urlopen(url, timeout=60) as response, open(destination, "wb") as target:
    while True:
        block = response.read(1024 * 1024)
        if not block:
            break
        target.write(block)
PY
    mkdir -p "$source"
    tar -xzf "$archive" --strip-components=1 -C "$source"
    rm -f "$archive"
  fi

  "$UV_BIN" pip install --python "$VENV_DIR/bin/python" --no-deps "$source"
}

# Install source pinned to immutable commits. --no-deps avoids remote Git
# resolution; the shared output contract is installed explicitly first.
install_source_package "ocr-output-contract" "ocr-output-contract" \
  "52554b96ec2212d161cb1eb97a381592e71f0b97"
install_source_package "socr" "socr" "ed2550e259cdb09e92b3fc62c1d1349f0fb9a95a"
install_source_package "qwen-ocr-cli" "qwen-ocr-cli" \
  "9ca56004c1733a739b1902cc2cfa4e6b9c35e3bb"
install_source_package "marker-ocr-cli" "marker-ocr-cli" \
  "4d63fb5d4c7d8d0711d1c260112e7be827eba248"

export PATH="$OLLAMA_DIR/bin:$VENV_DIR/bin:$PATH"
socr --version
qwen-ocr --version
marker-ocr --version

OLLAMA_ARCHIVE="$TASK_DIR/cache/ollama-linux-amd64-${OLLAMA_VERSION}.tar.zst"
OLLAMA_URL="https://github.com/ollama/ollama/releases/download/${OLLAMA_VERSION}/ollama-linux-amd64.tar.zst"
if [[ ! -x "$OLLAMA_DIR/bin/ollama" ]]; then
  echo "Downloading Ollama $OLLAMA_VERSION"
  if command -v curl >/dev/null 2>&1; then
    curl --fail --location --retry 3 "$OLLAMA_URL" --output "$OLLAMA_ARCHIVE"
  else
    python3 - "$OLLAMA_URL" "$OLLAMA_ARCHIVE" <<'PY'
import sys
from urllib.request import urlopen

url, destination = sys.argv[1:]
with urlopen(url, timeout=120) as response, open(destination, "wb") as target:
    while True:
        block = response.read(8 * 1024 * 1024)
        if not block:
            break
        target.write(block)
PY
  fi
  mkdir -p "$OLLAMA_DIR"
  if command -v zstd >/dev/null 2>&1; then
    zstd --decompress --stdout "$OLLAMA_ARCHIVE" | tar -xf - -C "$OLLAMA_DIR"
  else
    echo "zstd is required to extract the Ollama release archive" >&2
    exit 1
  fi
fi
export PATH="$OLLAMA_DIR/bin:$VENV_DIR/bin:$PATH"
echo "OLLAMA_VERSION=$($OLLAMA_DIR/bin/ollama --version)"

"$OLLAMA_DIR/bin/ollama" serve >"$LOG_DIR/ollama-${SLURM_JOB_ID}.log" 2>&1 &
OLLAMA_PID=$!
cleanup_ollama() {
  "$OLLAMA_DIR/bin/ollama" stop "$QWEN_MODEL" >/dev/null 2>&1 || true
  kill "$OLLAMA_PID" >/dev/null 2>&1 || true
  wait "$OLLAMA_PID" >/dev/null 2>&1 || true
}
trap 'cleanup_ollama; rm -rf "$TMPDIR"' EXIT

"$VENV_DIR/bin/python" - <<'PY'
import time
from urllib.request import urlopen

for attempt in range(120):
    try:
        with urlopen("http://127.0.0.1:11434/api/version", timeout=2):
            print("Ollama API is ready")
            break
    except Exception:
        if attempt == 119:
            raise
        time.sleep(5)
PY

if ! "$OLLAMA_DIR/bin/ollama" list | awk 'NR > 1 { print $1 }' | grep -Fxq "$QWEN_MODEL"; then
  "$OLLAMA_DIR/bin/ollama" pull "$QWEN_MODEL"
fi

cat >"$TASK_DIR/repair-${SLURM_JOB_ID}.Modelfile" <<EOF
FROM $QWEN_MODEL
PARAMETER repeat_penalty $QWEN_REPETITION_PENALTY
PARAMETER repeat_last_n $QWEN_REPEAT_LAST_N
PARAMETER temperature 0
PARAMETER num_ctx $QWEN_OCR_NUM_CTX
PARAMETER num_predict 8192
EOF
"$OLLAMA_DIR/bin/ollama" create "$QWEN_REPAIR_MODEL" \
  -f "$TASK_DIR/repair-${SLURM_JOB_ID}.Modelfile"
cat >"$TASK_DIR/judge-${SLURM_JOB_ID}.Modelfile" <<EOF
FROM $QWEN_MODEL
PARAMETER repeat_penalty 1.0
PARAMETER temperature 0
PARAMETER num_ctx 8192
PARAMETER num_predict 8192
EOF
"$OLLAMA_DIR/bin/ollama" create "$QWEN_JUDGE_MODEL" \
  -f "$TASK_DIR/judge-${SLURM_JOB_ID}.Modelfile"
"$OLLAMA_DIR/bin/ollama" list
"$OLLAMA_DIR/bin/ollama" show "$QWEN_REPAIR_MODEL" --modelfile
"$OLLAMA_DIR/bin/ollama" show "$QWEN_JUDGE_MODEL" --modelfile

# qwen-ocr-cli exposes repetition_penalty in its OpenAI-compatible request.
# Raise its neutral OCR default only for these pages that hit Ollama's repeat limit.
"$VENV_DIR/bin/python" - <<'PY'
import re
from pathlib import Path

import qwen_ocr.config

config_path = Path(qwen_ocr.config.__file__)
source = config_path.read_text(encoding="utf-8")
source, repetition_updates = re.subn(
    r"(?m)^REPETITION_PENALTY = [0-9.]+$",
    "REPETITION_PENALTY = 1.15",
    source,
    count=1,
)
if repetition_updates != 1:
    raise SystemExit(f"Could not set Qwen repetition penalty in {config_path}")
prompt = '''OCR_PROMPT = (
    "Transcribe all visible text in this image into clean Markdown. "
    "Preserve document structure, including headings, lists, paragraphs, and table panels. "
    "For each table, include every row, column, and cell; preserve blank cells instead of dropping columns. "
    "Every Markdown table must have one header row followed immediately by its separator row. "
    "Join spanning group headings to each child column heading, for example Ret (1), Ret (2), and Ret (3). "
    "Do not add a separate table row for group headings or column numbers. "
    "Keep the same number of cells in every row, including empty cells between pipe characters. "
    "Do not put page numbers, headers, footers, captions, or surrounding prose into table cells. "
    "Ignore page numbers outside table borders, even when a page number is close to the final table row. "
    "Do not use LaTeX table commands; use Markdown pipes for all table structure. "
    "Keep every value in its original row and column. "
    "Do not omit values because they repeat. Copy numbers, signs, decimal points, stars, dates, and parentheses exactly. "
    "Render each table panel as a Markdown table with consistent columns and mathematics as LaTeX. "
    "Output only the transcription, with no commentary or code fences."
)'''
prompt = prompt.replace("OCR_PROMPT = (", "DEFAULT_OCR_PROMPT = (")
prompt += '\nOCR_PROMPT = __import__("os").environ.get("QWEN_OCR_PROMPT", DEFAULT_OCR_PROMPT)\n'
source, prompt_updates = re.subn(
    r'(?ms)^DEFAULT_OCR_PROMPT = \(.*?^\)\nOCR_PROMPT = __import__\("os"\)\.environ\.get\("QWEN_OCR_PROMPT", DEFAULT_OCR_PROMPT\)\n?',
    prompt,
    source,
    count=1,
)
if prompt_updates == 0:
    source, prompt_updates = re.subn(
        r"(?ms)^OCR_PROMPT = \(.*?^\)",
        prompt,
        source,
        count=1,
    )
if prompt_updates != 1:
    raise SystemExit(f"Could not set the table-focused OCR prompt in {config_path}")
config_path.write_text(source, encoding="utf-8")
print(f"QWEN_OCR_CONFIG={config_path}")
print("QWEN_REPETITION_PENALTY=1.15")
print("QWEN_OCR_MAX_PIXELS=6291456")
PY
export QWEN_OCR_OLLAMA_MODEL="$QWEN_REPAIR_MODEL"

mkdir -p "$REPAIR_ROOT" "$REPAIR_INPUT_DIR" "$REPAIR_OUTPUT_DIR"
"$VENV_DIR/bin/python" - "$INPUT_DIR" "$OUTPUT_DIR" "$REPAIR_INPUT_DIR" "$REPAIR_MAP" <<'PY'
import json
import re
import sys
from pathlib import Path

import fitz

input_dir, output_dir, repair_input_dir, repair_map = map(Path, sys.argv[1:])
targets = []
for pdf in sorted(input_dir.glob("*.pdf")):
    markdown_path = output_dir / pdf.stem / f"{pdf.stem}.md"
    if not markdown_path.is_file():
        raise SystemExit(f"Missing existing Markdown output: {markdown_path}")
    markdown = markdown_path.read_text(encoding="utf-8")
    page_numbers = sorted({int(value) for value in re.findall(
        r"(?m)^\[page (\d+) failed\b[^\r\n]*\]$", markdown
    )})
    if not page_numbers:
        continue
    source = fitz.open(pdf)
    for page_num in page_numbers:
        if page_num < 1 or page_num > source.page_count:
            raise SystemExit(f"Invalid failed page {page_num} in {pdf.name}")
        repair_stem = f"{pdf.stem}__repair_page_{page_num:04d}"
        target_pdf = fitz.open()
        target_pdf.insert_pdf(source, from_page=page_num - 1, to_page=page_num - 1)
        target_pdf.save(repair_input_dir / f"{repair_stem}.pdf")
        target_pdf.close()
        targets.append({
            "source_stem": pdf.stem,
            "source_pdf": pdf.name,
            "page_num": page_num,
            "repair_stem": repair_stem,
        })
    source.close()

if not targets:
    raise SystemExit("No [page N failed] placeholders found; nothing to repair")
repair_map.write_text(json.dumps(targets, indent=2) + "\n", encoding="utf-8")
print(f"FAILED_PAGE_REPAIRS={len(targets)}")
for target in targets:
    print(f"REPAIR_TARGET {target['source_stem']} page {target['page_num']}")
PY

"$VENV_DIR/bin/python" - "$REPAIR_ROOT" "$REPAIR_INPUT_DIR" "$REPAIR_OUTPUT_DIR" "$REPAIR_MAP" "$LOG_DIR" "$SLURM_JOB_ID" "$QWEN_REPAIR_MODEL" "$QWEN_OCR_MAX_PIXELS" "$VENV_DIR/bin/qwen-ocr" <<'PY'
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import qwen_ocr.config

repair_root, input_dir, output_dir, map_path, log_dir = map(Path, sys.argv[1:6])
job_id, model, max_pixels, qwen_cli = sys.argv[6:10]
targets = json.loads(map_path.read_text(encoding="utf-8"))
base_prompt = qwen_ocr.config.DEFAULT_OCR_PROMPT

prior_runs = []
for prior_map in repair_root.glob("map-*.json"):
    match = re.fullmatch(r"map-(\d+)\.json", prior_map.name)
    if not match or int(match.group(1)) >= int(job_id):
        continue
    prior_id = int(match.group(1))
    try:
        prior_targets = json.loads(prior_map.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        continue
    prior_runs.append((prior_id, prior_targets))
prior_runs.sort(reverse=True)

previous_outputs = []
for prior_id, prior_targets in prior_runs:
    audit_path = repair_root / f"audit-{prior_id}.json"
    try:
        prior_audit = json.loads(audit_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        prior_audit = {}
    audit_by_page = {
        (result.get("source_stem"), int(result.get("page_num", -1))): result
        for result in prior_audit.get("results", [])
    }
    prior_output_dir = repair_root / f"output-{prior_id}"
    prior_stems = {
        (target["source_stem"], int(target["page_num"])): target["repair_stem"]
        for target in prior_targets
    }
    previous_outputs.append((prior_output_dir, prior_stems, audit_by_page))


def table_text(markdown: str) -> str:
    blocks = []
    current = []
    for line in markdown.splitlines() + [""]:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current.append(line)
        elif current:
            if len(current) >= 3:
                blocks.append("\n".join(current))
            current = []
    return "\n\n".join(blocks)


log_path = log_dir / f"qwen-repair-{job_id}.log"
with log_path.open("w", encoding="utf-8") as log:
    failures = []
    for target in targets:
        key = (target["source_stem"], int(target["page_num"]))
        repair_stem = target["repair_stem"]
        page_output = output_dir / repair_stem / f"{repair_stem}.md"
        previous_markdown = None
        findings = []
        previous_error = ""
        for prior_output_dir, prior_stems, audit_by_page in previous_outputs:
            prior_stem = prior_stems.get(key)
            if prior_stem:
                prior_markdown = prior_output_dir / prior_stem / f"{prior_stem}.md"
                if prior_markdown.is_file():
                    previous_markdown = prior_markdown.read_text(encoding="utf-8")
                    previous_result = audit_by_page.get(key, {})
                    findings = previous_result.get("table_findings", [])
                    previous_error = str(previous_result.get("table_error") or "")
                    break

        page_output.parent.mkdir(parents=True, exist_ok=True)
        candidate_table = ""
        if previous_markdown:
            page_output.write_text(previous_markdown, encoding="utf-8")
            candidate_table = table_text(previous_markdown)[:12000]
        finding_text = "\n".join(
            f"- {item.get('code')}: {item.get('where')}: {item.get('detail')}"
            for item in findings[:15]
        )
        if previous_error:
            finding_text += f"\n- Reviewer error: {previous_error[:1000]}"
        correction_prompt = base_prompt
        if previous_markdown:
            correction_prompt += (
                "\n\nThis is a correction pass for a table page. The image is the source of truth. "
                "Compare the candidate and reviewer notes with the image. Reviewer notes can be wrong; "
                "do not copy a proposed value unless the image supports it. Re-read the full table, "
                "preserve every row and blank cell, and correct the full transcription.\n\n"
                f"Previous table candidate:\n{candidate_table or '(no Markdown table found)'}\n\n"
                f"Local vision reviewer notes:\n{finding_text or '(the reviewer returned no findings)'}"
            )
        env = os.environ.copy()
        env["QWEN_OCR_PROMPT"] = correction_prompt
        input_pdf = input_dir / f"{repair_stem}.pdf"
        command = [
            qwen_cli,
            "process",
            str(input_pdf),
            "--output",
            str(output_dir),
            "--backend",
            "ollama",
            "--model",
            model,
            "--dpi",
            "300",
            "--max-pixels",
            max_pixels,
            "--reprocess",
        ]
        log.write(f"CORRECTION_TARGET {key[0]} page {key[1]}\n")
        log.flush()
        result = subprocess.run(
            command,
            check=False,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(
            f"QWEN_CORRECTION {key[0]} page {key[1]} "
            f"prior_draft={bool(previous_markdown)} exit={result.returncode}"
        )
        if result.returncode:
            failures.append(f"{key[0]} page {key[1]} exit {result.returncode}")

print(f"QWEN_CORRECTION_LOG={log_path}")
print(f"QWEN_CORRECTION_FAILURES={len(failures)}")
for failure in failures:
    print(f"QWEN_CORRECTION_FAILED {failure}")
PY

"$VENV_DIR/bin/python" - "$OUTPUT_DIR" "$REPAIR_OUTPUT_DIR" "$REPAIR_MAP" "$REPAIR_AUDIT" "$QWEN_REPAIR_MODEL" "$QWEN_JUDGE_MODEL" <<'PY'
import json
import re
import sys
from pathlib import Path

from socr.judge.table_rung_ollama import build_ollama_rung

output_dir, repair_output_dir, repair_map, repair_audit = map(Path, sys.argv[1:5])
ocr_model, judge_model = sys.argv[5:7]
targets = json.loads(repair_map.read_text(encoding="utf-8"))
merged = []
unresolved = []
audit = {
    "strict_local": True,
    "ocr_backend": "ollama",
    "ocr_model": ocr_model,
    "table_judge_model": judge_model,
    "repetition_penalty": 1.15,
    "repeat_last_n": 128,
    "num_ctx": 12288,
    "ocr_max_pixels": 6291456,
    "results": [],
}

table_judge = build_ollama_rung(
    judge_model,
    "http://127.0.0.1:11434",
    timeout=300,
)


def page_body(markdown: str) -> str:
    heading = re.search(r"(?m)^## Page 1[ \t]*$", markdown)
    if not heading:
        return markdown.strip()
    body_start = heading.end()
    next_heading = re.search(r"(?m)^## Page \d+[ \t]*$", markdown[body_start:])
    body_end = body_start + next_heading.start() if next_heading else len(markdown)
    return markdown[body_start:body_end].strip()


def markdown_tables(markdown: str) -> list[str]:
    blocks = []
    current = []
    for line in markdown.splitlines() + [""]:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current.append(line)
            continue
        if current:
            rows = current
            current = []
            separators = [
                row for row in rows
                if all(
                    re.fullmatch(r":?-{3,}:?", cell.strip())
                    for cell in row.strip().strip("|").split("|")
                )
            ]
            if len(rows) >= 3 and separators:
                blocks.append("\n".join(rows))
    return blocks

for target in targets:
    source_stem = target["source_stem"]
    page_num = int(target["page_num"])
    repair_stem = target["repair_stem"]
    repair_markdown = repair_output_dir / repair_stem / f"{repair_stem}.md"
    if not repair_markdown.is_file():
        unresolved.append(f"{source_stem} page {page_num}: missing Qwen OCR output")
        continue

    page_text = page_body(repair_markdown.read_text(encoding="utf-8"))
    if not page_text or re.search(r"(?i)\*\[OCR Failed\]\*", page_text):
        unresolved.append(f"{source_stem} page {page_num}: Qwen OCR returned no page text")
        continue

    table_image = output_dir / source_stem / "figures" / f"failed_table_p{page_num}.png"
    if not table_image.is_file():
        unresolved.append(f"{source_stem} page {page_num}: missing table image {table_image.name}")
        continue
    table_candidates = markdown_tables(page_text)
    if not table_candidates:
        unresolved.append(f"{source_stem} page {page_num}: Qwen output has no Markdown table")
        continue

    table_result = table_judge(table_image, "\n\n".join(table_candidates), None)
    table_verdict = table_result.verdict
    table_passed = bool(
        table_result.ok
        and table_verdict is not None
        and table_verdict.is_confident_pass
    )
    print(
        f"LOCAL_TABLE_JUDGE {source_stem} page {page_num}: "
        f"ok={table_result.ok} verdict={getattr(table_verdict, 'verdict', None)} "
        f"confidence={getattr(table_verdict, 'confidence', None)} "
        f"findings={getattr(table_verdict, 'findings', None)} "
        f"error={table_result.error}"
    )
    result_audit = {
        "source_stem": source_stem,
        "page_num": page_num,
        "table_judge_ok": table_result.ok,
        "table_verdict": getattr(table_verdict, "verdict", None),
        "table_confidence": getattr(table_verdict, "confidence", None),
        "table_findings": [
            {
                "code": finding.code.value,
                "where": finding.where,
                "detail": finding.detail,
            }
            for finding in getattr(table_verdict, "findings", [])
        ],
        "table_doubts": getattr(table_verdict, "doubts", []),
        "table_error": table_result.error,
    }
    if not table_passed:
        unresolved.append(f"{source_stem} page {page_num}: local table judge did not give a high-confidence PASS")
        audit["results"].append(result_audit)
        continue

    document_dir = output_dir / source_stem
    markdown_path = document_dir / f"{source_stem}.md"
    markdown = markdown_path.read_text(encoding="utf-8")
    section = re.search(rf"(?m)^## Page {page_num}[ \t]*$", markdown)
    if not section:
        unresolved.append(f"{source_stem} page {page_num}: page heading not found")
        audit["results"].append(result_audit)
        continue
    next_section = re.search(r"(?m)^## Page \d+[ \t]*$", markdown[section.end():])
    end = section.end() + next_section.start() if next_section else len(markdown)
    old_body = markdown[section.end():end]
    old_figure_links = [
        line.strip()
        for line in old_body.splitlines()
        if re.match(r"!\[[^\]]*\]\(figures/[^)]+\)", line.strip())
        and "Failed table page" not in line
    ]
    if old_figure_links:
        page_text = page_text.rstrip() + "\n\n" + "\n\n".join(old_figure_links)
    replacement = "\n\n" + page_text.strip() + "\n\n"
    markdown_path.write_text(markdown[:section.end()] + replacement + markdown[end:], encoding="utf-8")
    merged.append(f"{source_stem} page {page_num}")
    result_audit["merged"] = True
    audit["results"].append(result_audit)

repair_audit.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
print(f"REPAIR_PAGES_MERGED={len(merged)}")
for page in merged:
    print(f"REPAIR_MERGED {page} judge={judge_model}")
print(f"REPAIR_PAGES_UNRESOLVED={len(unresolved)}")
for page in unresolved:
    print(f"REPAIR_UNRESOLVED {page}")
if unresolved:
    raise SystemExit("One or more failed pages did not pass the local vision judge")
PY

python3 - "$INPUT_DIR" "$OUTPUT_DIR" <<'PY'
import re
import sys
from pathlib import Path

input_dir, output_dir = map(Path, sys.argv[1:])
pdfs = sorted(input_dir.glob("*.pdf"))
expected = {pdf.stem for pdf in pdfs}
folders = {path.name for path in output_dir.iterdir() if path.is_dir()}
if len(pdfs) != 3 or folders != expected:
    raise SystemExit(f"Expected 3 document folders {sorted(expected)}; found {sorted(folders)}")

for pdf in pdfs:
    markdown = output_dir / pdf.stem / f"{pdf.stem}.md"
    if not markdown.is_file():
        raise SystemExit(f"Missing final Markdown file: {markdown}")
    text = markdown.read_text(encoding="utf-8").strip()
    words = len(text.split())
    size = markdown.stat().st_size
    failures = re.findall(r"(?m)^\[page \d+ failed\b", text)
    links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    missing_links = [link for link in links if link.startswith("figures/") and not (markdown.parent / link).is_file()]
    if size == 0 or words < 100:
        raise SystemExit(f"Output is not extracted paper text: {markdown} ({size} bytes, {words} words)")
    if failures:
        raise SystemExit(f"Unresolved failed-page placeholders in {markdown}: {len(failures)}")
    if missing_links:
        raise SystemExit(f"Missing figure files referenced in {markdown}: {missing_links[:5]}")
    print(f"OCR_RESULT {markdown.name}: {size} bytes, {words} words, {len(links)} image links resolved")
print(f"Verified {len(expected)} non-empty Markdown files with resolved image links")
PY

echo "Finished=$(date -Is)"
echo "REPAIR_CLOUD_POLICY=local Ollama only; OLLAMA_NO_CLOUD=1"
echo "QWEN_OCR_BACKEND=ollama"
echo "LOCAL_TABLE_VISION_JUDGE_BACKEND=ollama"
echo "LOCAL_TABLE_VISION_JUDGE_MODEL=$QWEN_JUDGE_MODEL"
echo "Completed validated failed-page repairs for all 3 PDFs on $(hostname)"
