# TASK-003 Work Plan

- [x] Inspect the OCR tools, cluster-kit setup, and current SLURM queue.
- [x] Fast-forward this task branch to `origin/main`; it was two commits behind.
- [x] Prepare one PaddleOCR runner that reads the three PDFs and writes one text file per PDF.
- [x] Probe cluster capacity, then submit and monitor no more than one task job at a time. Job 23527 was the only PaddleOCR task job in the last queue view.
- [ ] Fetch the outputs and verify all three files contain extracted paper text.
- [ ] Record the job ID, `sacct` state, and log tail in the task outcome.
- [ ] Run the required checks, commit the outcome and task changes, then open a PR into `main`.

## Review

Plan was shared before implementation. No change request arrived during the check-in.

## Blocked review

Cluster SSH now refuses connections on `192.168.1.61:22`. The task outcome records the last known job state, log tail, output listing, and the access block. The draft PR stays open for follow-up.
