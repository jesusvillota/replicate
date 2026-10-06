# TASK-004 outcome

Goal-Task: ocr-cluster/TASK-004

Goal-Blocked: cluster VPN is unavailable: FortiClient reports its VPN app is not installed

## Acceptance

- [ ] `ocr/paperextract/` holds one output file per input PDF.
  Evidence: Not met. `ls -ld ocr ocr/paperextract` reports that neither path exists. The retry could not submit a cluster job.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: Not met. Paperextract did not run on the three PDFs during this retry.
- [ ] The OCR ran on a cluster compute node, shown by the SLURM job ID, its `sacct` state, and a log tail.
  Evidence: Not met. No job ID or compute log exists for this retry.
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: No job was submitted during this retry. Outcome commit `666b3e5` records that earlier jobs `23528`, `23531`, and `23532` were submitted one at a time and cancelled before the next submission. Direct `squeue` checks showed no TASK-004 job; one check showed only unrelated jobs `23495` and `23527`.

## Summary

The retry updated `TASK-004-run.sh` to use `cpu_shared`, 4 CPUs, 12 GB of memory, and a four-hour limit. Revision `5e254f1` passed `bash -n` and `git diff --check`, and it was pushed to `goal/ocr-cluster/task-004`.

The resource probe showed usable CPU capacity. Its queue field was empty. A direct `squeue` check briefly listed two unrelated running jobs, `23495` and `23527`; a later check listed none. No TASK-004 job was submitted.

The cluster VPN then became unavailable. `cluster-kit sync cp` could not connect. SSH to `cluster` failed with `Connection refused`. `scutil --nc status` reported `Disconnected` and said the VPN app for the saved profile was not installed. FortiClient showed its cloud agent connected, but Remote Access was disabled. The repository has no local `src/` or `runnables/` directories, so `cluster-kit sync code` also could not complete. No OCR inference ran on the MacBook.

Checks: `bash -n goals/ocr-cluster/tasks/TASK-004-run.sh goals/ocr-cluster/tasks/TASK-004-finalize.sh` passed. `git diff --check` passed. Output and `sacct` checks could not run because cluster access was unavailable.

Proposed follow-up: restore the FortiClient VPN app or another approved cluster connection. Then stage the run script and PDFs, submit one `cpu_shared` job, fetch the three outputs, and record its `sacct` state and log tail.
