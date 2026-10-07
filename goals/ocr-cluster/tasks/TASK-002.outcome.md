# TASK-002 outcome: OCR papers with Chandra on cluster

## Acceptance

- [ ] `ocr/chandra/` holds one output file per input PDF (three files total).
  Evidence: The isolated worktree output folder and the shared `ocr/chandra/`
  folder contain no files.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: No OCR output files were created.
- [ ] The OCR ran on a cluster compute node, shown by the SLURM job ID, its
  `sacct` state, and a log tail.
  Evidence: SLURM job `23607` requested `gpu:nvidia_l4:1`, 22 CPUs, and 84G on
  `gpu_compute`. The first `squeue` check reported `PENDING` with reason
  `(None)`. I canceled it immediately. `sacct` reports `CANCELLED+`, elapsed
  `00:00:00`, no `MaxRSS`, and no assigned node. The SLURM output log was not
  created, so there is no compute log tail. The job did not run.
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: Jobs `23510`, `23512`, `23524`, and `23607` all show
  `CANCELLED+` with elapsed `00:00:00` in `sacct`. The earlier three were
  canceled before the next was submitted. On resume, the explicit node-pin
  submission was rejected before creating a job; job `23607` was the only
  accepted submission and was canceled when it pended. No task job remains in
  `squeue`.

## Summary

I confirmed the runner and all three PDFs were staged in the isolated cluster
worktree. Their SHA-256 hashes matched the local files. The live resource probe
showed HPCOM-02 with 24 free CPUs, 132G free memory, and one free L4 GPU.
`gpu_compute` allows up to 32 CPUs and 88G.

The first submission requested HPCOM-02 directly. SLURM rejected node selection
for this partition before creating a job. I then submitted one job without a
node pin, requesting one L4 GPU, 22 CPUs, 84G, and the `gpu_compute` QoS. SLURM
reported it as `PENDING` during the initial check, so I canceled it as
instructed. `sacct` shows zero runtime and no assigned node. No OCR ran, and no
log or output files exist.

Goal-Blocked: SLURM left job 23607 PENDING (reason None); cluster execution was unavailable before the required cancellation.

Verified runner revision: `36cd02b`. Its SHA-256 matched the staged cluster
copy. No compute run or output verification was possible.

Proposed follow-up: Resume TASK-002 when SLURM can start one eligible L4 job on
`gpu_compute`; then fetch and verify all three OCR outputs.
