#!/usr/bin/env bash
#SBATCH --job-name=ocr-paddleocr
#SBATCH --partition=cpu_shared
#SBATCH --qos=cpu_shared
#SBATCH --nodes=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=12G
#SBATCH --time=12:00:00
#SBATCH --output=/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/ocr-cluster-task-003/logs/paddleocr-%j.out
#SBATCH --error=/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/ocr-cluster-task-003/logs/paddleocr-%j.err

set -euo pipefail

TASK_ROOT="/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/ocr-cluster-task-003"
VENV="$TASK_ROOT/.venv"
export PADDLE_PDX_CACHE_HOME="$TASK_ROOT/model-cache"
export PIP_CACHE_DIR="$TASK_ROOT/.pip-cache"
export TMPDIR="/tmp/paddleocr-${SLURM_JOB_ID}"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

mkdir -p "$PADDLE_PDX_CACHE_HOME" "$PIP_CACHE_DIR" "$TMPDIR" "$TASK_ROOT/ocr/paddleocr"
trap 'rm -rf "$TMPDIR"' EXIT

echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "SLURM_JOB_PARTITION=$SLURM_JOB_PARTITION"
echo "SLURMD_NODENAME=$SLURMD_NODENAME"
echo "Started=$(date -Is)"
python3 --version

if [[ ! -x "$VENV/bin/python" ]]; then
    python3 -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install paddlepaddle paddleocr
"$VENV/bin/python" -m pip show paddlepaddle paddleocr
"$VENV/bin/python" "$TASK_ROOT/paddleocr_extract.py" \
    --input-dir "$TASK_ROOT/input" \
    --output-dir "$TASK_ROOT/ocr/paddleocr"

echo "Finished=$(date -Is)"
