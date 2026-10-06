#!/usr/bin/env bash
#SBATCH --partition=gpu_compute
#SBATCH --qos=gpu_compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
#SBATCH --time=72:00:00
#SBATCH --gres=gpu:nvidia_l4:1
#SBATCH --job-name=marker-t001
#SBATCH --output=_logs_/marker/marker-%j.out
#SBATCH --error=_logs_/marker/marker-%j.err
set -euo pipefail

SLURM_JOB_ID="${SLURM_JOB_ID:?Run this script through SLURM}"
REPO_ROOT="${OCR_MARKER_ROOT:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)}"
TASK_DIR="${REPO_ROOT}/ocr/marker"
INPUT_DIR="$REPO_ROOT"
OUTPUT_DIR="$TASK_DIR"
SCRATCH_DIR="/tmp/${USER:-j-vill36}/marker-${SLURM_JOB_ID}"
RAW_OUTPUT_DIR="${SCRATCH_DIR}/marker-raw"
UV_BIN="/mnt/slurm-beegfs/Users/j-vill36/.local/bin/uv"
MICROMAMBA_BIN="/mnt/slurm-beegfs/Users/j-vill36/.local/bin/micromamba"
LLAMA_ENV="${SCRATCH_DIR}/llama-env"

export TMPDIR="${SCRATCH_DIR}/tmp"
export TEMP="$TMPDIR"
export TMP="$TMPDIR"
export XDG_CACHE_HOME="${SCRATCH_DIR}/xdg-cache"
export HF_HOME="${SCRATCH_DIR}/huggingface"
export MODEL_CACHE_DIR="${SCRATCH_DIR}/datalab/models"
export TORCH_HOME="${SCRATCH_DIR}/torch"
export UV_CACHE_DIR="${SCRATCH_DIR}/uv-cache"
export MAMBA_ROOT_PREFIX="${SCRATCH_DIR}/mamba-root"
export PYTHONPYCACHEPREFIX="${SCRATCH_DIR}/pycache"

mkdir -p "$TMPDIR" "$XDG_CACHE_HOME" "$HF_HOME" "$MODEL_CACHE_DIR" "$TORCH_HOME" "$OUTPUT_DIR"
rm -rf "$RAW_OUTPUT_DIR"
mkdir -p "$RAW_OUTPUT_DIR"

shopt -s nullglob
old_outputs=("$OUTPUT_DIR"/*.md)
if [[ ${#old_outputs[@]} -gt 0 ]]; then
  rm -- "${old_outputs[@]}"
fi

printf 'SLURM_JOB_ID=%s\n' "$SLURM_JOB_ID"
printf 'SLURMD_NODENAME=%s\n' "${SLURMD_NODENAME:-$(hostname)}"
printf 'Started=%s\n' "$(date -Is)"

pdfs=("$INPUT_DIR"/*.pdf)
if [[ ${#pdfs[@]} -ne 3 ]]; then
  printf 'Expected 3 input PDFs in %s; found %s\n' "$INPUT_DIR" "${#pdfs[@]}" >&2
  exit 1
fi

venv="${SCRATCH_DIR}/venv"
"$UV_BIN" venv "$venv" --python /usr/bin/python3.10
"$UV_BIN" pip install --python "${venv}/bin/python" marker-pdf

# The cluster has no Docker, so use Surya's llama.cpp backend with a CUDA build.
# One inference slot and two server threads fit this job's small CPU allocation.
"$MICROMAMBA_BIN" create --yes --prefix "${SCRATCH_DIR}/llama-env" \
  --channel conda-forge "llama.cpp=11351=cuda129_h0b4778f_0"
export LD_LIBRARY_PATH="${LLAMA_ENV}/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export SURYA_INFERENCE_BACKEND=llamacpp
export SURYA_INFERENCE_PARALLEL=1
export LLAMA_CPP_BINARY="${LLAMA_ENV}/bin/llama-server"
export LLAMA_CPP_NGL=99
export LLAMA_CPP_EXTRA_ARGS="--threads 2 --threads-batch 2"
if [[ ! -x "$LLAMA_CPP_BINARY" ]]; then
  printf 'llama-server was not installed at %s\n' "$LLAMA_CPP_BINARY" >&2
  exit 1
fi
"$LLAMA_CPP_BINARY" --version
printf 'SURYA_INFERENCE_BACKEND=%s\n' "$SURYA_INFERENCE_BACKEND"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# Marker uses Markdown output by default. Process one PDF at a time to fit the
# available memory while keeping GPU inference inside this SLURM job.
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
