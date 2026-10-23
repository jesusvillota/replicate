# TASK-032 outcome

## Summary

Ran the merged `rebal.latest` module on the real MacBook panel and clean signals.
Committed latest Tables 1 and 3, the 120-row comparison, and run metadata under
`output/tables/robustness/latest/`. Wrote `docs/results/latest_sample.md` with
exact coefficients, t statistics and observation counts for both sample windows.

The panel and latest estimation samples end on **2026-07-31**. Table 1 column (1)
keeps both negative signs and significance at 5%. Threshold changes from
-0.46441444537986687 (t = -4.012117777680489, N = 6317) to
-0.4101349210644659 (t = -3.7502634690368497, N = 7152).
Cal × week4 changes from -0.26025581705921746 (t = -3.418692803568286, N = 6317)
to -0.2362462490035583 (t = -3.2273241198579243, N = 7152).
Both effects weaken, so these estimates do not support footnote 32's claim
that the extended results become stronger. The cause is unknown.

Table 3 keeps all eight signal signs and their 5% significance outcomes.
The stock effects and bond Threshold effect remain significant. The bond
Calendar effect is insignificant in both windows, unlike the paper's result.
The result note quotes both signals in all four Table 3 columns, including
the specifications with controls and their shorter complete-case samples.

Verified analysis and report revision: `4d3c1267990561053ed7003ce1dc64c863afd64b`.
This outcome commit also records the final Verify run's metadata timestamp;
the rerun changed no CSV values. This task branch was rebased onto
`origin/main` (`a68e41569becb83b15b163e53c6cbb38c56f9acd`) without conflicts.
No new analysis code, data rebuild, signal rebuild, cluster job, or scope
deviation was needed. No task specification, decision, goal definition,
other task file, or main exhibit was changed. No follow-up is proposed.

## Acceptance

- [x] `uv run python3 -m rebal.latest` exits 0.
  Evidence: both real runs exited 0. The final required Verify sequence printed
  all four output paths and `exit=0`.
- [x] `output/tables/robustness/latest/latest_comparison.csv` exists and its
  latest sample ends on the panel's last date.
  Evidence: the CSV contains 120 rows. A direct check of the real panel and CSV
  confirmed that all ten `latest` / `sample_end` rows equal `2026-07-31`.
- [x] `git diff --stat main -- output/tables output/figures` lists files only
  under `robustness/latest/`.
  Evidence: four files, 232 insertions: `latest.metadata.json`,
  `latest_comparison.csv`, `table_1.csv`, and `table_3.csv`, all in
  `output/tables/robustness/latest/`. No figures changed. During final Verify,
  `git status --short output/` showed only the latest metadata timestamp change.
- [x] `docs/results/latest_sample.md` quotes both samples, exact numbers, and
  whether signs and 5% significance hold.
  Evidence: Table 1 column (1) and all four Table 3 columns quote both signals'
  saved coefficients, t statistics and N. A CSV-to-document check confirmed
  every required number appears exactly. The note quotes footnote 32, gives
  actual sample dates, distinguishes our paper-end estimates from published
  estimates, and explains the bond Calendar exception without inventing a cause.
- [x] `uv run pytest -q` passes.
  Evidence: the final required Verify sequence exited 0 and ended with
  `393 passed in 240.71s (0:04:00)`. An earlier full run also passed:
  `393 passed, 4 warnings in 277.75s (0:04:37)`; those warnings were in installed
  `wrds` source. GitHub Actions were not inspected or used as a gate.

## Verify evidence

The full task Verify command block ran in order and exited 0:

```text
PANEL OK
[four paths under output/tables/robustness/latest/]
exit=0
[first 30 lines of the comparison printed by column]
 M output/tables/robustness/latest/latest.metadata.json
...
.................................                                        [100%]
393 passed in 240.71s (0:04:00)
```

Additional read-only checks confirmed the saved paper-end Tables 1 and 3 match
fresh in-memory builds from the current inputs (`rtol=1e-12`, `atol=1e-15`).
`git -c core.whitespace=cr-at-eol diff --check main` passed. The comparison CSV
uses the existing writer's CRLF line endings; its generated format was retained.

Input SHA-256 values, from the existing processed files:

| Input | SHA-256 |
|---|---|
| `daily_panel.parquet` | `0aa723f34422fae7bcedb41bfaf0e7a5c3685688a1a9c7e3addec7af0463a4cd` |
| `signals_clean.parquet` | `ac21349f54e9b1efcee38b25317dfcf7350f23490646b661a4e2caf52dddbed1` |

Delivery PR: <https://github.com/jesusvillota/replicate/pull/42>, into `main`,
with `Goal-Task: hmm-rebalancing/TASK-032` and label `goal:hmm-rebalancing`.
