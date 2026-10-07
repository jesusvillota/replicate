#!/usr/bin/env bash
#SBATCH --job-name=paperextract-task004
#SBATCH --partition=cpu_shared
#SBATCH --qos=cpu_shared
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --time=04:00:00
#SBATCH --signal=TERM@120
#SBATCH --output=logs/paperextract-%j.out
#SBATCH --error=logs/paperextract-%j.err

set -euo pipefail

TASK_DIR="/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004"
PAPEREXTRACT_DIR="$TASK_DIR/paperextract"
PAPEREXTRACT_BIN="$PAPEREXTRACT_DIR/.venv/bin/paperextract"
TMPDIR="/tmp/paperextract-${SLURM_JOB_ID}"

export TMPDIR
export DUCKDB_TEMP_DIR="$TMPDIR/duckdb"
export MPLCONFIGDIR="$TMPDIR/mpl"
mkdir -p "$DUCKDB_TEMP_DIR" "$MPLCONFIGDIR" "$TASK_DIR/staged" "$TASK_DIR/library"
trap 'rm -rf "$TMPDIR"' EXIT

cd "$TASK_DIR"
cat > "$TASK_DIR/cpu.toml" <<EOF
[worker]
root = "$PAPEREXTRACT_DIR"
timeout_seconds = 3600

[registry]
offline = true
EOF

echo "SLURM_JOB_ID=$SLURM_JOB_ID"
echo "SLURM_JOB_NODELIST=$SLURM_JOB_NODELIST"
hostname
echo "paperextract commit: $(cat "$TASK_DIR/paperextract.commit")"

shopt -s nullglob
inputs=("$TASK_DIR"/inputs/*.pdf)
if [[ ${#inputs[@]} -ne 3 ]]; then
  echo "Expected 3 input PDFs, found ${#inputs[@]}" >&2
  exit 1
fi
printf 'Input: %s\n' "${inputs[@]}"

"$PAPEREXTRACT_BIN" batch "$TASK_DIR/inputs" \
  --library "$TASK_DIR/library" \
  --runs-to "$TASK_DIR/staged" \
  --config "$TASK_DIR/cpu.toml"
