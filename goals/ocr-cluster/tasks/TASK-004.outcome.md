# TASK-004 outcome

Goal-Task: ocr-cluster/TASK-004

Goal-Blocked: no CPU node had enough free memory for Paperextract

## Acceptance checklist

- [ ] `ocr/paperextract/` holds one output file per input PDF.
  Evidence: Not met. No compute job started, so the output folder was not created.
- [ ] Each output file is non-empty and holds extracted paper text.
  Evidence: Not met. Paperextract did not run on the three PDFs.
- [ ] A compute-node run is shown by its job ID, `sacct` state, and log tail.
  Evidence: Not met. Job `23532` stayed `PENDING` with reason `Resources`. Slurm estimated a start at `2026-10-06 18:59:51 +02:00`, more than four hours after submission. Jobs `23528`, `23531`, and `23532` all ended as `CANCELLED+` with elapsed time `00:00:00`. No OCR log exists.
- [x] This task never held more than one queued or running job.
  Evidence: Jobs `23528`, `23531`, and `23532` were submitted one at a time. Each was cancelled before the next was submitted. `squeue -n paperextract-task004` returned no jobs after the final cancellation. The task held at most one queued or running job.

## Summary

The three PDFs and both task scripts were copied to `/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/`. Paperextract and its default CPU model were installed on the cluster login node. `paperextract models status mineru --verify` passed. No inference ran on the MacBook.

The CPU partition was `cpu_long_unlimited`, with its matching QOS. The final request used four CPUs and 6 GB of memory. Slurm showed no node with both four free CPUs and 6 GB of allocatable memory. `HPCOM-04` had no free CPUs. The other nodes had less than 6 GB of allocatable memory. Job `23532` stayed pending. Its estimated start was more than four hours later, so it was cancelled before it started. The earlier jobs were also cancelled before they started: `23528` used the default, mismatched QOS; `23531` requested 12 GB and could not fit.

The task code revision is `93d9302`. The cluster checkout used Paperextract commit `04820bc85df378a07c7f20b0d4f03757d3b41c7c`.

Checks: `bash -n` passed for both task scripts. `git diff --check` passed. The repository has no configured test suite.

Proposed follow-up: resume when one CPU node has at least four CPUs and 6 GB of allocatable memory, and an account job slot is free. Submit one job, then collect the three Markdown files and its SLURM log.
