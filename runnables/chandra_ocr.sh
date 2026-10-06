#!/usr/bin/env bash
set -Eeuo pipefail

BASE_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
INPUT_DIR="$BASE_DIR/inputs/chandra"
OUTPUT_DIR="$BASE_DIR/ocr/chandra"
RUN_DIR="$BASE_DIR/.chandra-run-${SLURM_JOB_ID:-manual}"
VENV_DIR="$BASE_DIR/.venv-chandra"
JOB_TMP="/tmp/chandra-${SLURM_JOB_ID:-manual}"
SERVER_LOG="$BASE_DIR/_logs_/chandra-vllm-${SLURM_JOB_ID:-manual}.out"

mkdir -p "$BASE_DIR/_logs_" "$JOB_TMP" "$BASE_DIR/.cache/huggingface"
export TMPDIR="$JOB_TMP"
export PIP_CACHE_DIR="$JOB_TMP/pip-cache"
export HF_HOME="$BASE_DIR/.cache/huggingface"
export VLLM_API_BASE="http://localhost:8000/v1"
export VLLM_MODEL_NAME="chandra"
export VLLM_GPUS="0"
export MODEL_CHECKPOINT="datalab-to/chandra-ocr-2"

SERVER_PID=""
cleanup() {
    result=$?
    trap - EXIT
    if [[ -n "$SERVER_PID" ]]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    rm -rf "$JOB_TMP"
    exit "$result"
}
trap cleanup EXIT

echo "SLURM job: ${SLURM_JOB_ID:-unknown}"
echo "Node: $(hostname)"
echo "Partition: ${SLURM_JOB_PARTITION:-unknown}"
date -Is
nvidia-smi

shopt -s nullglob
pdfs=("$INPUT_DIR"/*.pdf)
if (( ${#pdfs[@]} != 3 )); then
    echo "Expected 3 input PDFs in $INPUT_DIR; found ${#pdfs[@]}" >&2
    exit 2
fi

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install "chandra-ocr==0.2.0" "vllm==0.17.0"

rm -rf "$RUN_DIR" "$OUTPUT_DIR"
mkdir -p "$RUN_DIR" "$OUTPUT_DIR"

"$VENV_DIR/bin/vllm" serve "$MODEL_CHECKPOINT" \
    --served-model-name "$VLLM_MODEL_NAME" \
    --no-enforce-eager \
    --max-num-seqs 8 \
    --dtype bfloat16 \
    --max-model-len 18000 \
    --max-num-batched-tokens 2048 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --mm-processor-kwargs '{"min_pixels":3136,"max_pixels":6291456}' \
    --host 127.0.0.1 \
    --port 8000 >"$SERVER_LOG" 2>&1 &
SERVER_PID=$!

ready=0
for _ in $(seq 1 360); do
    if curl --fail --silent "$VLLM_API_BASE/models" >/dev/null; then
        ready=1
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "vLLM server stopped before it became ready. Server log follows:" >&2
        tail -n 80 "$SERVER_LOG" >&2 || true
        exit 3
    fi
    sleep 10
done
if (( ready == 0 )); then
    echo "vLLM server did not become ready. Server log follows:" >&2
    tail -n 80 "$SERVER_LOG" >&2 || true
    exit 4
fi

for pdf in "${pdfs[@]}"; do
    name="$(basename "$pdf" .pdf)"
    echo "Running Chandra on $name.pdf"
    "$VENV_DIR/bin/chandra" "$pdf" "$RUN_DIR"
    markdown="$RUN_DIR/$name/$name.md"
    if [[ ! -s "$markdown" ]]; then
        echo "Chandra did not create a non-empty Markdown file for $name.pdf" >&2
        exit 5
    fi
    cp "$markdown" "$OUTPUT_DIR/$name.md"
    bytes="$(wc -c < "$OUTPUT_DIR/$name.md" | tr -d '[:space:]')"
    words="$(wc -w < "$OUTPUT_DIR/$name.md" | tr -d '[:space:]')"
    if (( bytes == 0 || words < 100 )); then
        echo "Output for $name.pdf is too small to contain extracted paper text" >&2
        exit 6
    fi
    echo "Saved $OUTPUT_DIR/$name.md ($bytes bytes, $words words)"
done

outputs=("$OUTPUT_DIR"/*.md)
if (( ${#outputs[@]} != 3 )); then
    echo "Expected 3 Markdown outputs in $OUTPUT_DIR; found ${#outputs[@]}" >&2
    exit 7
fi

rm -rf "$RUN_DIR"
echo "Chandra OCR completed for all three papers."
date -Is
