# TASK-005 outcome: OCR papers with SOCR strict-local on cluster

## Acceptance

- [x] `ocr/socr/` has one folder per input PDF. Each folder has one non-empty final Markdown file with extracted paper text.

  ```text
  $ ls ocr/socr/
  Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs
  Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs
  Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing

  $ wc -c ocr/socr/*/*.md
    82430 ocr/socr/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs/Bessembinder_SSRN_2026_RebalancingFrictionalCostsAndReturnsToLeveredSingleStockETFs.md
    43640 ocr/socr/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs/Bessembinder_SSRN_2026_VolatilityAndReturnsToLeveragedETFs.md
   151923 ocr/socr/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md
   277993 total
  ```

  The files contain 13,382, 6,659, and 22,682 words. Their `figures/` folders contain 42 images. All 37 Markdown image links resolve. The local vision judge accepted repairs for pages 19, 36, 68, 70, 75, 76, and 34. It rejected 13 pages, which remain fail-closed: first paper page 31; third paper pages 32, 40, 63–67, 69, and 71–74. The task spec permits partial output when all three final Markdown files exist.

- [x] OCR ran on a cluster compute node. Initial job `23631` completed on `HPCOM-01`. Repair job `23650` ran on `HPCOM-01` and ended `FAILED` because the local judge rejected 13 pages.

  ```text
  $ sacct -j 23631,23650 --format=JobID,JobName%24,State,ExitCode,Elapsed,MaxRSS,NodeList -n -P
  23631|socr-task005|COMPLETED|0:0|01:14:34||HPCOM-01
  23631.batch|batch|COMPLETED|0:0|01:14:34|1036552K|HPCOM-01
  23650|socr-task005-repair|FAILED|1:0|00:13:28||HPCOM-01
  23650.batch|batch|FAILED|1:0|00:13:28|8940344K|HPCOM-01
  ```

  Log tails:

  ```text
  # logs/socr-23631.out
  SOCR_BATCH_EXIT_CODE=1
  Verified 3 non-empty final Markdown files
  SOCR_STRICT_LOCAL=1
  SOCR_JUDGE_BACKEND=heuristic
  Completed validated OCR outputs for all 3 PDFs on HPCOM-01

  # logs/socr-23650.out
  QWEN_CORRECTION_FAILURES=0
  REPAIR_PAGES_MERGED=0
  REPAIR_PAGES_UNRESOLVED=13
  REPAIR_UNRESOLVED Bessembinder... page 31: local table judge did not give a high-confidence PASS
  REPAIR_UNRESOLVED Harvey... page 32: local table judge did not give a high-confidence PASS
  ... 11 additional pages remained fail-closed
  ```

- [x] This task never held more than one cluster job queued or running at once. Repair jobs ran one after another. The fresh resource probe before job `23650` showed an idle GPU node. Direct `squeue` after submission showed one TASK-005 job, alongside three sibling jobs:

  ```text
  23628 R stock-universe-shard-1 cpu_long HPCOM-02
  23630 R stock-universe-shard-3 cpu_long_unlimited HPCOM-02
  23629 R stock-universe-shard-2 cpu_shared HPCOM-02
  23650 R socr-task005-repair gpu_compute HPCOM-01
  ```

  Final direct `squeue` showed only the three sibling jobs. It showed no active TASK-005 job.

- [x] No paid API call was made. The initial SOCR run used `--strict-local`. It disabled Ollama cloud access and unset paid API credentials. Repair jobs used only local Ollama at `127.0.0.1`; their logs record `OLLAMA_NO_CLOUD=1` and `TABLE_JUDGE_CLOUD_LADDER=disabled`. Job `23650` completed all 13 local Qwen correction calls without an OCR abort.

## Summary

The runner now retries only `[page N failed]` pages. It uses stronger Qwen anti-repeat settings and includes prior local judge findings in correction prompts. It judges tables with a local Ollama vision model. It merges only high-confidence passes and keeps rejected pages fail-closed. The repair runner does not pass `--no-figure-descriptions`. The PR includes all 42 existing figure files, so all 37 Markdown image links resolve.

The local judge accepted seven repaired pages across jobs `23642`, `23643`, and `23644`. Job `23650` used the judge feedback for a second correction pass, but the judge still rejected 13 pages. The task spec allows this partial result because all three final Markdown files exist. No unverified table text was merged.

The cluster-kit code sync command could not run because this repository has no local `src/` directory. I copied the task-specific shell runner directly to the cluster and verified it with `bash -n` before submission. No package dependencies changed.

- Verified code and output revision: `21d31c4`.
- Local checks passed: `bash -n`, parsing all eight embedded Python blocks, `git diff --check`, three-folder and Markdown-size checks, and figure-link resolution.
- PR checks: none are configured.
- Proposed follow-ups: none for this task. The 13 rejected pages remain explicit fail-closed placeholders.
