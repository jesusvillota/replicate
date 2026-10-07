# TASK-005 outcome: OCR papers with SOCR strict-local on cluster

## Acceptance

- [x] `ocr/socr/` has one folder per input PDF, each with a non-empty final Markdown file containing extracted paper text. Evidence from the required commands:

  ```text
  $ ls ocr/socr/
  Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs
  Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs
  Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing

  $ wc -c ocr/socr/*/*.md
    82430 ocr/socr/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.md
    43640 ocr/socr/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.md
   143670 ocr/socr/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md
   269740 total
  ```

  The cluster runner counted 13,382, 6,659, and 21,037 words in those files.

- [x] OCR ran on a cluster compute node. Job `23631` ran in `gpu_compute` on `HPCOM-01`. `sacct -j 23631 --format=JobID,State,Elapsed,MaxRSS` returned:

  ```text
  JobID             State    Elapsed     MaxRSS
  23631         COMPLETED   01:14:34
  23631.batch   COMPLETED   01:14:34   1036552K
  23631.extern  COMPLETED   01:14:34          0
  ```

  The SLURM log header recorded `SLURM_JOB_ID=23631`, `SLURM_JOB_PARTITION=gpu_compute`, and `SLURMD_NODENAME=HPCOM-01`.

  Tail of the SLURM log `logs/socr-23631.out`:

  ```text
  SOCR_BATCH_EXIT_CODE=1
  OCR_RESULT Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.md: 82430 bytes, 13382 words
  OCR_RESULT Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.md: 43640 bytes, 6659 words
  OCR_RESULT Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md: 143670 bytes, 21037 words
  Verified 3 non-empty final Markdown files
  Finished=2026-10-07T14:51:24+02:00
  SOCR_STRICT_LOCAL=1
  SOCR_JUDGE_BACKEND=heuristic
  Completed validated OCR outputs for all 3 PDFs on HPCOM-01
  ```

- [x] The task held no more than one SLURM job queued or running at a time. The task submitted only job `23631`. Queue checks throughout the run showed only `socr-task005` for this task; the other running jobs had sibling-task names. No second TASK-005 job was submitted.

- [x] No paid API call was made. The runner invoked `socr batch` with `--strict-local --judge-backend heuristic` at `goals/ocr-cluster/tasks/TASK-005-run.sh:215-222`. It set `OLLAMA_NO_CLOUD=1` and unset paid API credentials at lines 51 and 60-61. The SLURM log records `SOCR_STRICT_LOCAL=1` and `Paid API credentials unset for this job.` The pipeline used local routes `qwen($0) -> marker($0)`.

## Summary

The pinned SOCR, Qwen OCR, and Marker sources ran on the `gpu_compute` node `HPCOM-01`. The run used Python 3.12, Ollama's local `qwen3-vl:30b-a3b-instruct` model, and CPU-only Marker fallback. The runner copied all three final Markdown files from shared cluster storage and verified each file was non-empty and contained extracted text.

SOCR reported a partial result: `SOCR_BATCH_EXIT_CODE=1`, `Completed: 0/3 files`, and `Failed/partial: 3`. Its log reports 14 pages still failing and untrusted tables on 26 pages. The task spec permits partial output when all three final Markdown files exist, and they do.

- Verified runner revision: `546b26f`.
- PR checks: `gh pr checks 9` reported no checks configured.
- `git diff --cached --check` flags trailing spaces from OCR output. The task excludes text cleanup, so extracted text was left unchanged.
- Proposed follow-ups: none for this task.
