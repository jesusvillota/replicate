# TASK-003 outcome

## Acceptance

- [x] `ocr/paddleocr/` holds one output file per input PDF (three files total).
  `ls -l ocr/paddleocr/` and `wc -c ocr/paddleocr/*` show exactly these three files:
  - `Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.txt` — 80,447 bytes.
  - `Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.txt` — 42,508 bytes.
  - `Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.txt` — 151,456 bytes.
  Their base names match the three input PDFs.
- [x] Each output file is non-empty and holds extracted paper text.
  A local content check found 10,624 words across 39 page markers, 5,582 words
  across 21 page markers, and 18,544 words across 76 page markers, respectively.
  Each file starts with readable paper text. Local SHA-256 hashes match the
  remote files exactly:

  ```text
  9f2ff4f711241cb508a590c1561c2e1fc1075b8767058c9f6b206340fc6d26de  Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.txt
  c7a7781c707734825970023b5ce8edd8a19f4cc82b258324d6d8d35e1aa1290c  Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.txt
  a8c008324ee87fe2592058af2f85c80ab3682733deadc54882c2aee9850a4411  Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.txt
  ```
- [x] The OCR ran on a cluster compute node, shown by the SLURM job ID, its
  `sacct` state, and a log tail.
  `sacct -j 23527 --format=JobID,JobName,Partition,State,Elapsed,MaxRSS,NodeList`
  reports job `23527`, state `COMPLETED`, elapsed `02:20:07`, batch MaxRSS
  `3792852K`, and node `HPCOM-01` in partition `cpu_shared`. The remote log tail:

  ```text
  SLURM_JOB_ID=23527
  SLURM_JOB_PARTITION=cpu_shared
  SLURMD_NODENAME=HPCOM-01
  Started=2026-10-06T14:00:03+02:00
  Python 3.10.12
  paddlepaddle 3.3.1
  paddleocr 3.7.0
  Wrote Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.txt: 39 pages, 80339 characters
  Wrote Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.txt: 21 pages, 42026 characters
  Wrote Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.txt: 76 pages, 151117 characters
  Completed OCR for 3 PDFs on HPCOM-01
  Finished=2026-10-06T16:20:09+02:00
  ```
- [x] This task never held more than one cluster job queued or running at once.
  `sacct` for job name `ocr-paddleocr` on 2026-10-06 listed only these jobs.
  Each job reached a terminal state before the next job was submitted:

  | Job | Submitted | Terminal | State |
  | --- | --- | --- | --- |
  | 23511 | 13:48:40 | 13:49:12 | CANCELLED |
  | 23514 | 13:50:18 | 13:50:47 | CANCELLED |
  | 23516 | 13:51:51 | 13:52:03 | FAILED |
  | 23519 | 13:54:23 | 13:55:48 | FAILED |
  | 23527 | 13:59:36 | 16:20:09 | COMPLETED |

  This resumed session submitted no cluster job.

## Summary

Fetched the three completed PaddleOCR outputs from
`/mnt/slurm-beegfs/Users/j-vill36/scripts_replicate/ocr-cluster-task-003/ocr/paddleocr/`
to `ocr/paddleocr/`. The remote and local SHA-256 hashes match for all files.
The output set matches all input PDFs, and each file contains extracted text.
OCR inference ran on `HPCOM-01`; no OCR inference ran locally.
Deviation: none from the task scope. This resumed session fetched the completed
outputs and submitted no new cluster job.

Verified runner revision: `ce6590e`. Job `23527` used PaddleOCR `3.7.0` and
PaddlePaddle `3.3.1`, with the default OCR model and settings. The runner disables
the failing automatic oneDNN backend, as recorded in the job script.

Follow-up: none for TASK-003.
