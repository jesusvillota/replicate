# Task work plans (merged from parallel workers; scratch notes, no authority)

## TASK-002 plan (from goal/ocr-cluster/task-002)

# TASK-002 plan

## Plan

- [x] Check the task inputs, Chandra access, cluster tools, GitHub access, and this worktree branch.
- [x] Check live cluster capacity immediately before submission. Submit at most one Chandra job.
- [ ] Run Chandra with its default settings on a cluster compute node. Fetch the three outputs into `ocr/chandra/`.
- [ ] Verify the three output files contain extracted text. Record the job ID, `sacct` state, and log tail in the outcome.
- [x] Commit the blocked outcome and task artifacts. Keep the PR in draft state and record why OCR could not run.

## Review

Plan shared before implementation. Proceeding under the task authorization.

The runner and all three PDFs reached the worktree's shared cluster path. SLURM had no available L4 slot with enough host memory. It estimated a start at 18:59:51 for job 23524. I canceled the job before stopping.

## TASK-003 plan (from main)

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
