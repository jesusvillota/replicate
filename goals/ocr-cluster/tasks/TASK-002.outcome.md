# TASK-002 outcome: OCR papers with Chandra on cluster

## Acceptance

- [ ] `ocr/chandra/` holds one output file per input PDF (three files total).
  Evidence: No remote `ocr/chandra/` directory or local output files exist.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: No OCR output files were created.
- [ ] OCR ran on a cluster compute node, shown by the SLURM job ID, its
  `sacct` state, and a log tail.
  Evidence: Job `23613` requested `gpu_compute`, 32 CPUs, 88G, and one L4 GPU.
  It stayed `PENDING` with reason `QOSMaxMemoryPerUser` and was canceled
  immediately. `sacct -j 23613 --format=JobID,State,Elapsed,MaxRSS,NodeList,ExitCode`
  reports `CANCELLED+`, `00:00:00`, blank `MaxRSS`, no assigned node, and
  `0:0`. No SLURM stdout log was created, so there is no compute log tail.
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: This resume submitted only job `23613`. It was canceled before any
  further submission. `squeue -j 23613` is empty after cancellation. No task
  job remains queued or running.

## Summary

I synced the runner to the isolated worktree deployment and copied all three
PDFs to its `inputs/chandra/` directory. Their remote SHA-256 hashes were
verified. The fresh `cluster-kit resources --json` probe showed HPCOM-02 with
40 free CPUs, 160G, and one free GPU. The `gpu_compute` ceiling is 32 CPUs,
88G, and 72 hours. The probe listed an empty queue. A direct `squeue` check
showed two other account jobs running in CPU partitions (`23589` and `23609`).

I submitted one job with the requested partition ceiling and one L4 GPU. SLURM
left job `23613` pending with `QOSMaxMemoryPerUser`, despite the available
node-level capacity. I canceled it as instructed. `sacct` confirms zero runtime
and no assigned node. Chandra did not run, and no OCR outputs or compute log
were created.

Goal-Blocked: SLURM kept the requested 32-CPU, 88G gpu_compute job pending with QOSMaxMemoryPerUser, so it was canceled before cluster execution.

Verified revision: `b41cb63`. No compute run or output verification was
possible.

Proposed follow-up: Resume TASK-002 when SLURM can start the requested
`gpu_compute` job under the per-user memory QoS.
