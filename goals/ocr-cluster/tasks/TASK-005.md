---
id: TASK-005
title: OCR papers with SOCR strict-local on cluster
milestone: M-1
state: approved
depends_on: []
delivery: pr
---

## Why

Serves SC-5: SOCR output covers all three papers.

## Scope

Run SOCR (https://github.com/r-uben/socr) on the SLURM cluster (account `j-vill36`), with `socr batch` in strict-local mode (`--strict-local --judge-backend heuristic`), so no API key, subscription, or paid call is needed. Never run model inference on the MacBook. The MacBook only submits the job, monitors it, and fetches results. Ship the three PDFs and the run script to shared storage (`/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/`). Before you submit, probe live capacity with `cluster-kit resources --json` and send the job to a GPU partition with a free GPU (all four nodes carry one GPU; `gpu_compute` fits a small CPU/mem ask plus 1 GPU). Keep at most one SLURM job of this task queued or running at a time (the account cap of 4 is shared with the four sibling tasks). SOCR needs Python 3.11 or 3.12 (install with `uv`; the cluster default 3.10 is too old), Ollama with the `qwen3-vl:30b-a3b-instruct` model (about 20 GB download), and the Marker fallback (about 2 GB); point `OLLAMA_MODELS` and all model caches at the task folder on shared storage, about 30 GB total. The 20 GB Qwen model needs about 23 GB of GPU memory, so keep only one model loaded at a time and keep the CPU/mem ask small (for example 4-8 CPUs, 16-32G, 1 GPU). Write output to `ocr/socr/`, one folder per paper holding its final stitched `.md` file. SOCR is fail-closed: pages it cannot verify ship UNVERIFIED and the run ends PARTIAL, which is acceptable evidence as long as the three final `.md` files exist. Out of scope: cloud engines, text cleanup, comparison with other methods, accuracy scoring.

## Acceptance

- `ocr/socr/` holds one folder per input PDF (three folders total), each with a non-empty final `.md` file holding extracted paper text.
- The OCR ran on a cluster compute node, shown by the SLURM job ID, its `sacct` state, and a log tail in the outcome file.
- This task never held more than one cluster job queued or running at once.
- No paid API call was made: the run used `--strict-local` only.

## Verify

```sh
ls ocr/socr/
wc -c ocr/socr/*/*.md
sacct -j <job-id> --format=JobID,State,Elapsed,MaxRSS
```
