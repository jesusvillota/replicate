# TASK-001 outcome

## Acceptance

- [x] `ocr/marker/` holds one output file per input PDF (three files total). Evidence: local `ls -l ocr/marker` lists three Markdown files with the input PDF base names.
- [x] Each output file is non-empty and holds extracted paper text. Evidence: `wc -c ocr/marker/*` reports 111,516, 44,951, and 190,619 bytes. Each file starts with the paper title and author text.
- [x] Marker ran on a cluster compute node. Evidence: job 23623 ran on `HPCOM-01`; its output records `SLURM_JOB_ID=23623`, `SLURMD_NODENAME=HPCOM-01`, and an NVIDIA L4 GPU. `sacct -j 23623 --format=JobID,State,Elapsed,MaxRSS` reports `COMPLETED`, 00:19:52, and 12045512K for the batch step. The log lists all three output sizes and `Completed=2026-10-07T12:05:09+02:00`.
- [x] This task never held more than one cluster job queued or running at once. Evidence: direct `squeue -u j-vill36` checks showed Marker jobs sequentially. Job 23614 failed before job 23615 was submitted. Job 23615 was canceled and left the queue before job 23623 was submitted. Job 23623 completed before any further Marker submission. The previous session's Marker job history is listed below.

## Final SLURM evidence

Job 23623 used partition `gpu_compute`, two CPUs, 16G, and one L4 GPU.

```text
$ sacct -j 23623 --format=JobID,State,Elapsed,MaxRSS
23623         COMPLETED   00:19:52
23623.batch   COMPLETED   00:19:52  12045512K
23623.extern  COMPLETED   00:19:52          0
```

Compute-node and log evidence:

```text
SLURM_JOB_ID=23623
SLURMD_NODENAME=HPCOM-01
Started=2026-10-07T11:45:18+02:00
NVIDIA L4, 23034 MiB
Produced Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.md (111516 bytes)
Produced Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.md (44951 bytes)
Produced Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md (190619 bytes)
Completed=2026-10-07T12:05:09+02:00
```

## Current resume job history

| Job ID | State | Elapsed | Result |
| --- | --- | --- | --- |
| 23614 | FAILED | 00:00:01 | Used the SLURM spool path as the repository root. |
| 23615 | CANCELLED+ | 00:18:01 | The 10G run hit an out-of-memory kill during the third paper. |
| 23623 | COMPLETED | 00:19:52 | Produced all three Markdown files with a 16G request. |

## Previous session job history

Times use the cluster's local time on 2026-10-06.

| Job ID | Start | End | State |
| --- | --- | --- | --- |
| 23508 | 13:46:22 | 13:46:22 | CANCELLED |
| 23509 | 13:48:19 | 13:48:19 | CANCELLED |
| 23518 | 13:53:32 | 13:53:33 | FAILED |
| 23521 | 13:56:07 | 13:56:08 | FAILED |
| 23526 | 13:58:32 | 14:00:39 | FAILED |
| 23529 | 14:11:02 | 14:11:59 | FAILED |
| 23530 | 14:13:32 | 14:53:35 | CANCELLED |
| 23533 | 14:55:29 | 14:55:29 | CANCELLED |
| 23534 | 14:57:33 | 14:57:33 | CANCELLED |
| 23535 | 14:58:06 | 14:58:06 | FAILED |
| 23536 | 14:58:59 | 15:15:35 | CANCELLED |

## Attempts and deviations

- Job 23614 failed after one second. SLURM ran the submitted script from its spool path, so the script chose `/var/spool/slurmd` as the repository root. The job log reported a permission error creating `/var/spool/slurmd/ocr`. The runner now uses `SLURM_SUBMIT_DIR` as its root.
- Job 23615 used 10G and reached an out-of-memory kill while processing the third paper. Its log showed repeated inference connection errors. The cgroup reported `oom_kill=1`. I canceled it and raised the request to 16G. Job 23623 then completed with a 12045512K peak.
- The standard `cluster-kit sync code` command could not run because this repo has no `src/` or `runnables/` directories. The staged PDFs matched the local files by SHA-256. I copied the updated runner with `scp` and verified its checksum before submission.

## Summary

Marker processed all three papers on the SLURM GPU node `HPCOM-01`. The Markdown files are in `ocr/marker/`. The runner uses the SLURM submission directory and requests 16G after the 10G run hit the memory limit.

Verified revision: `0636fe5dcf579a1596d07c517afe7b6ebfac1022` (runner and OCR outputs).

Follow-ups: none.
