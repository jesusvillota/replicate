# TASK-002 outcome: OCR papers with Chandra on cluster

## Acceptance

- [ ] `ocr/chandra/` holds one output file per input PDF (three files total).
  Evidence: `ocr/chandra/` is absent in this worktree. No compute job ran.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: No output files were created.
- [ ] The OCR ran on a cluster compute node, shown by the SLURM job ID, its `sacct` state, and a log tail.
  Evidence: Job `23524` stayed `PENDING` with reason `Resources`. SLURM estimated a start at `2026-10-06T18:59:51` on `HPCOM-04`. I canceled it before it started. `sacct` reports `CANCELLED+`, elapsed `00:00:00`, with no `MaxRSS`. No compute log exists.
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: I submitted jobs `23510`, `23512`, and `23524` one at a time. I confirmed each earlier job was canceled before submitting the next. The final `squeue` query showed no queued task jobs. `sacct` reports all three as `CANCELLED+` with elapsed `00:00:00`.

## Summary

I added `runnables/chandra_ocr.sh` and synced it with the three source PDFs to the isolated worktree path `/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate__goal-ocr-cluster-task-002/`.

Deviation: Chandra's Docker helper needs Docker. The cluster login node has no Docker. The script is set to prepare a vLLM server directly on a compute node. Chandra's CLI keeps its default `vllm` mode and OCR options.

The cluster had no L4 slot with enough host memory for this job. A 20 GB per-GPU request stayed pending. SLURM estimated its start at `2026-10-06T18:59:51`. I canceled the job before it started. Chandra did not run, so this task has no OCR outputs or compute log tail.

Goal-Blocked: Cluster GPU capacity is unavailable; SLURM job 23524 remained pending for Resources with estimated start 2026-10-06T18:59:51.

Verified runner revision: `36cd02b`. `bash -n runnables/chandra_ocr.sh` passed. `gh pr checks 6` reported no checks.

Proposed follow-up: resume TASK-002 when an L4 node has enough host memory. Submit one job and complete the OCR run and output checks.
