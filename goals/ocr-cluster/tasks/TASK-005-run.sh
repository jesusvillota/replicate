#!/usr/bin/env bash
#SBATCH --job-name=socr-task005
#SBATCH --partition=gpu_compute
#SBATCH --qos=gpu_compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
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
VENV_DIR="$TASK_DIR/venv"
OLLAMA_DIR="$TASK_DIR/ollama"
OLLAMA_MODELS="$TASK_DIR/models/ollama"
UV_BIN="/mnt/slurm-beegfs/Users/j-vill36/.local/bin/uv"
OLLAMA_VERSION="v0.40.0"
QWEN_MODEL="qwen3-vl:30b-a3b-instruct"

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
export OLLAMA_KEEP_ALIVE=0
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
echo "SOCR_STRICT_LOCAL=1"
echo "SOCR_JUDGE_BACKEND=heuristic"
echo "SOCR_REPO_COMMIT=ed2550e259cdb09e92b3fc62c1d1349f0fb9a95a"
echo "QWEN_OCR_REPO_COMMIT=9ca56004c1733a739b1902cc2cfa4e6b9c35e3bb"
echo "MARKER_OCR_REPO_COMMIT=4d63fb5d4c7d8d0711d1c260112e7be827eba248"
echo "OCR_OUTPUT_CONTRACT_COMMIT=52554b96ec2212d161cb1eb97a381592e71f0b97"
echo "QWEN_MODEL=$QWEN_MODEL"
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
"$UV_BIN" venv --python 3.12 "$VENV_DIR"
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
"$OLLAMA_DIR/bin/ollama" list

set +e
"$VENV_DIR/bin/socr" batch "$INPUT_DIR" -o "$OUTPUT_DIR" \
  --primary qwen \
  --qwen-backend ollama \
  --qwen-model "$QWEN_MODEL" \
  --strict-local \
  --judge-backend heuristic \
  --no-figure-descriptions 2>&1 | tee "$LOG_DIR/socr-pipeline-${SLURM_JOB_ID}.log"
socr_status=${PIPESTATUS[0]}
set -e
echo "SOCR_BATCH_EXIT_CODE=$socr_status"

python3 - "$INPUT_DIR" "$OUTPUT_DIR" <<'PY'
import sys
from pathlib import Path

input_dir, output_dir = map(Path, sys.argv[1:])
pdfs = sorted(input_dir.glob("*.pdf"))
expected = {pdf.stem for pdf in pdfs}
folders = {path.name for path in output_dir.iterdir() if path.is_dir()}
if len(pdfs) != 3 or folders != expected:
    raise SystemExit(
        f"Expected 3 document folders {sorted(expected)}; found {sorted(folders)}"
    )
for pdf in pdfs:
    markdown = output_dir / pdf.stem / f"{pdf.stem}.md"
    if not markdown.is_file():
        raise SystemExit(f"Missing final Markdown file: {markdown}")
    text = markdown.read_text(encoding="utf-8").strip()
    words = len(text.split())
    size = markdown.stat().st_size
    if size == 0 or words < 100:
        raise SystemExit(f"Output is not extracted paper text: {markdown} ({size} bytes, {words} words)")
    print(f"OCR_RESULT {markdown.name}: {size} bytes, {words} words")
print(f"Verified {len(expected)} non-empty final Markdown files")
PY

echo "Finished=$(date -Is)"
echo "SOCR_STRICT_LOCAL=1"
echo "SOCR_JUDGE_BACKEND=heuristic"
echo "Completed validated OCR outputs for all 3 PDFs on $(hostname)"
