# TASK-004 outcome

Goal-Task: ocr-cluster/TASK-004

## Acceptance

- [x] `ocr/paperextract/` holds one output file per input PDF (three files total).
  Evidence: `ls -l ocr/paperextract` lists three Markdown files matching the three input paper names.
- [x] Each output file is non-empty and holds extracted paper text.
  Evidence: `wc -c ocr/paperextract/*` reports 93,203, 49,338, and 174,922 bytes. The files contain 15,598, 8,538, and 26,038 words. The remote finalizer also confirmed three non-empty outputs.
- [x] The OCR ran on a cluster compute node, shown by the SLURM job ID, its `sacct` state, and a log tail.
  Evidence: `sacct` reports job `23609` as `COMPLETED`, exit `0:0`, on `HPCOM-05`, with 4 CPUs and 12G requested. Elapsed time was `01:18:57`; batch `MaxRSS` was `8060792K`.

  Log tail from `paperextract-23609.out`:

  ```text
  SLURM_JOB_ID=23609
  SLURM_JOB_NODELIST=HPCOM-05
  hpcom-05
  paperextract commit: 04820bc85df378a07c7f20b0d4f03757d3b41c7c
  Input: /mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/inputs/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.pdf
  Input: /mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/inputs/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.pdf
  Input: /mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/inputs/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.pdf
  staged	Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.pdf	/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/staged/20261007T084959Z-81022379704f-519f02
  staged	Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.pdf	/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/staged/20261007T090608Z-54bf534f3c34-76a3cf
  staged	Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.pdf	/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/staged/20261007T091309Z-3696f1d0720c-4e4808
  library	/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/task-004/library (option)
  3 staged
  ```
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: the earlier jobs `23528`, `23531`, and `23532` were canceled before allocation, one at a time. Their recorded times were `14:10:41`, `14:26:34`, and `14:46:14` on 2026-10-06. Later, `23606` ended at `10:43:46`, before `23608` started at `10:45:55`; `23608` ended at `10:46:03`, before `23609` started at `10:49:57` on 2026-10-07. A final `squeue -j 23528,23531,23532,23606,23608,23609` check returned no jobs.

## Summary

Paperextract processed all three PDFs on cluster node HPCOM-05. The successful run was job `23609`, using the `cpu_shared` partition, 4 CPUs, and 12G. Earlier jobs `23606` and `23608` failed because the remote worker environment lacked dependencies. After installing `psutil==7.2.2` and CPU-only `torch==2.13.0` there, job `23609` completed all three papers. No OCR inference ran on the MacBook.

The finalizer initially tried to republish papers already present in the Paperextract library. Paperextract reported conflicts and stopped before copying outputs. The updated finalizer skips papers already published for the same PDF, publishes only missing papers, and validates each output. Its successful run reported 93,203, 49,338, and 174,922 bytes and verified all three outputs. The files were fetched to `ocr/paperextract/` and checked locally.

Verified run revision: branch `goal/ocr-cluster/task-004` at `671eb28`. Checks: `bash -n goals/ocr-cluster/tasks/TASK-004-run.sh goals/ocr-cluster/tasks/TASK-004-finalize.sh` passed. `git diff --check` passes for the task scripts and outcome. A full diff check flags trailing spaces on extracted footnote lines; these remain untouched because text cleanup is out of scope. Local output count, byte count, and extracted-word checks passed. PR checks are not configured.
