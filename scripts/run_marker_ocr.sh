#!/usr/bin/env bash
set -euo pipefail

SLURM_JOB_ID="${SLURM_JOB_ID:?Run this script through SLURM}"
REPO_ROOT="${OCR_MARKER_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
TASK_DIR="${REPO_ROOT}/ocr/marker"
INPUT_DIR="${TASK_DIR}/inputs"
OUTPUT_DIR="${TASK_DIR}/outputs"
RAW_OUTPUT_DIR="${TASK_DIR}/.marker-raw-${SLURM_JOB_ID}"
SCRATCH_DIR="/tmp/${USER:-j-vill36}/marker-${SLURM_JOB_ID}"
UV_BIN="/mnt/slurm-beegfs/Users/j-vill36/.local/bin/uv"

export TMPDIR="${SCRATCH_DIR}/tmp"
export TEMP="$TMPDIR"
export TMP="$TMPDIR"
export XDG_CACHE_HOME="${SCRATCH_DIR}/xdg-cache"
export HF_HOME="${SCRATCH_DIR}/huggingface"
export TORCH_HOME="${SCRATCH_DIR}/torch"
export UV_CACHE_DIR="${SCRATCH_DIR}/uv-cache"
export PYTHONPYCACHEPREFIX="${SCRATCH_DIR}/pycache"

mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$HF_HOME" "$TORCH_HOME" "$OUTPUT_DIR"
rm -rf "$RAW_OUTPUT_DIR"
mkdir -p "$RAW_OUTPUT_DIR"

printf 'SLURM_JOB_ID=%s\n' "$SLURM_JOB_ID"
printf 'SLURMD_NODENAME=%s\n' "${SLURMD_NODENAME:-$(hostname)}"
printf 'Started=%s\n' "$(date -Is)"

shopt -s nullglob
pdfs=("$INPUT_DIR"/*.pdf)
if [[ ${#pdfs[@]} -ne 3 ]]; then
  printf 'Expected 3 input PDFs in %s; found %s\n' "$INPUT_DIR" "${#pdfs[@]}" >&2
  exit 1
fi

venv="${SCRATCH_DIR}/venv"
"$UV_BIN" venv "$venv" --python /usr/bin/python3.10
"$UV_BIN" pip install --python "${venv}/bin/python" marker-pdf

# Marker uses Markdown output by default. Process one PDF at a time to fit the
# available memory while keeping inference inside this SLURM job.
for pdf in "${pdfs[@]}"; do
  "${venv}/bin/marker_single" "$pdf" --output_dir "$RAW_OUTPUT_DIR"
done

for pdf in "${pdfs[@]}"; do
  filename="$(basename -- "$pdf")"
  stem="${filename%.pdf}"
  extracted="$(find "$RAW_OUTPUT_DIR" -type f -name "${stem}.md" -print -quit)"
  if [[ -z "$extracted" || ! -s "$extracted" ]]; then
    printf 'Missing or empty Marker output for %s\n' "$filename" >&2
    exit 1
  fi

  target="${OUTPUT_DIR}/${stem}.md"
  cp -- "$extracted" "${target}.part"
  mv -- "${target}.part" "$target"
  printf 'Produced %s (%s bytes)\n' "$(basename -- "$target")" "$(wc -c < "$target" | tr -d ' ')"
done

output_count="$(find "$OUTPUT_DIR" -mindepth 1 -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
if [[ "$output_count" -ne 3 ]]; then
  printf 'Expected 3 Markdown outputs in %s; found %s\n' "$OUTPUT_DIR" "$output_count" >&2
  exit 1
fi

rm -rf "$RAW_OUTPUT_DIR"
printf 'Completed=%s\n' "$(date -Is)"
