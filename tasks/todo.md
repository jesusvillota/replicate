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
