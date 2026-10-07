# TASK-002 outcome: OCR papers with Chandra on cluster

## Acceptance

- [x] `ocr/chandra/` holds one output file per input PDF (three files total).
  Evidence: `ls ocr/chandra/` lists the three matching Markdown files. Their
  sizes are 102,726, 53,892, and 195,204 bytes.
- [x] Each output file is non-empty and holds extracted paper text.
  Evidence: `wc -c ocr/chandra/*` reports 351,822 bytes total. The OCR run
  reports 13,010, 7,379, and 24,016 words. `rg` finds Abstract and Introduction
  headings in the files. Local and cluster SHA-256 hashes match for all three.
- [x] OCR ran on a cluster compute node, shown by the SLURM job ID, its
  `sacct` state, and a log tail.
  Evidence: Job `23624` ran on HPCOM-02 with one L4 in `gpu_long`. `sacct`
  reports `COMPLETED`, elapsed `00:32:01`, `MaxRSS=10644012K`, and exit code
  `0:0`.

  Log tail:

  ```text
  Saved /mnt/slurm-beegfs/Users/j-vill36/scripts_replicate__goal-ocr-cluster-task-002/ocr/chandra/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md (195204 bytes, 24016 words)
  Chandra OCR completed for all three papers.
  2026-10-07T12:20:12+02:00
  ```
- [x] This task never held more than one cluster job queued or running at once.
  Evidence: Task jobs were sequential. Jobs `23616` and `23617` were canceled
  while pending. Job `23618` ran from 11:35:25 to 11:35:26; `23620` ran from
  11:38:10 to 11:38:26; `23621` ended at 11:46:11; and `23624` ran from
  11:48:16 to 12:20:17. `sacct` start and end times show no overlap. Final
  direct `squeue` showed no Chandra task job queued or running.

## Summary

Chandra processed all three PDFs with its local CLI and the `datalab-to/chandra-ocr-2`
model on an L4 compute node. The CLI used its default OCR invocation. The final
job requested 4 CPUs, 16G, and 48 hours. It completed in 32 minutes.

Fresh direct `squeue` checks found `marker-t001` already using the per-user L4
allocation in `gpu_compute`. I routed this task to the idle `gpu_long` partition.
The account defaulted to the `cpu_express` QOS, so the final `sbatch` command
set `--qos=gpu_long` explicitly. Earlier jobs were canceled or failed before
the successful run. Their failures identified the needed runner fixes: use the
shared `uv` binary, pin Python to the cluster's Python 3.10, and replace the
missing `curl` readiness check with Python's built-in HTTP client.

The runner and PDFs were deployed to the isolated worktree directory. I fetched
the three completed outputs into local `ocr/chandra/` and verified their hashes
against the cluster copies. I kept raw OCR spacing intact because text cleanup
is out of scope.

Verified revision: `fcedd1081f424c2b211428414afc8bfdf21a0b01`.

Proposed follow-ups: None for TASK-002.
