# TASK-020 outcome

## Acceptance

- [x] `uv run pytest tests/test_compare.py` passes. On implementation revision `9f964f89f93134915f1987113ea10f8180b3ce8f`, the exact command collected 22 tests and reported **22 passed in 5.03s** (exit 0).
- [x] `wc -l docs/results/targets.csv` reports at least 150 rows. It printed **400**: one header and **399 numeric targets** across **34 exhibits**.
- [x] `uv run python3 -m rebal.compare --demo --out output/demo/compare.md` exits 0 after `uv run python3 -m rebal.exhibits --all --demo`. The summary reports **238/399 matched targets**, lists **22 missing exhibits**, and explains **six skipped CSVs**. Both commands exited 0. The shorthand `uv run python3 -m rebal.compare --demo` also exited 0.

Final report summary:

```text
Targets matched: 238/399
Sign-match rate: 59.0% (62/105 eligible targets)
Significance-match rate: 74.7% (74/99 eligible targets)
Missing exhibits: costs, figure_1, figure_2, figure_3, figure_4, figure_5, figure_6, figure_D1, figure_D2, figure_D3, figure_D4, figure_D5, table_4, table_5, table_6a, table_6b, table_6c, table_C1, table_C2, table_D14, table_D4, table_D9
Matched exhibits: table_1, table_2a, table_2b, table_3, table_D1, table_D10, table_D11, table_D12, table_D3, table_D6, table_D7, table_D8
Skipped CSVs: 6
```

Audit of all emitted CSVs from the two modules on main:

| Exhibit | Matched / targets | Evidence |
|---|---:|---|
| table_1 | 92/92 | All target rows join, including two signed magnitudes. |
| table_2a | 24/24 | Includes `threshold:week4` as well as `calendar:week4`. |
| table_2b | 18/18 | All quarter-month columns join. |
| table_3 | 60/60 | Includes four signed leg magnitudes. |
| table_D1 | 4/4 | Columns 1/2 and `ret_1`. |
| table_D3 | 6/6 | `mom_fast`, `mom_medium`, `mom_slow`. |
| table_D6 | 4/4 | Both target variants join. |
| table_D7 | 12/12 | Columns 1/2/3. |
| table_D8 | 6/6 | Includes `threshold_perp`. |
| table_D10 | 5/5 | `rev_st`. |
| table_D11 | 3/3 | `eom_rev`. |
| table_D12 | 4/4 | `calendar:week1` and `calendar:week3`. |
| table_C1 | 0/10 | Skipped and reported: signal layout lacks comparison keys. |
| table_C2 | 0/4 | Skipped and reported: predictor matrix lacks comparison keys. |
| figure_C1 | No targets | Skipped and reported: plotted data lacks comparison keys. |
| table_D2, table_D5, table_D13 | No targets | Each skipped and reported: no matching target keys in section 4. |
| magnitudes/magnitudes.csv | 6/6 | Signed `magnitude_bps` joins Table 1 column 1 and Table 3 columns 1/3. |

The 238 matched targets include the six magnitude targets; they are not added twice.
The integration test writes every current module export to an isolated directory.
It checks every target for all produced predictive tables and all six skip reasons.
It also compares magnitude estimates directly with the emitted `magnitude_bps` values.
Demo values test software behavior, not agreement with market returns.

Additional checks passed: Ruff check, Ruff format check, `git diff --check`, and CLI help.
A filesystem check confirmed `docs/results/` contains only `targets.csv`.
No real-data exhibits or cluster jobs were run. GitHub Actions were not consulted.

## Summary

Merged `origin/main` at `778987391417b6676741c4dfe8f91dc5e9c4719e` into the existing
`goal/hmm-rebalancing/task-020` branch without conflicts. This brought in TASK-013
signals and TASK-014 predictive tables. Reproduced the reported C1 layout crash.

The comparison now validates each CSV before loading any of its rows. It skips
unsupported layouts, malformed rows, invalid statistics, non-finite values and
ambiguous duplicate keys. It records each file and reason in the report, while
valid files still join. Invalid target data still fails. Recursive discovery reads
the demo magnitude subdirectory and the flat real magnitude file. Magnitude input
contributes only `stat=value`, avoiding duplicate regression coefficients.

Aligned all interaction, momentum, reversal, residualized-threshold and trailing-return
keys with the actual exports. Replaced descriptive D1 and D7 column labels with the
emitted numeric columns. One-SD targets now use the actual baseline column/term keys
and signed effects: spread/equity negative, bonds positive. Their absolute source
numbers are unchanged. Corrected the bond 4.1/2.3 bps citations to PDF page 33;
`pdftotext -f 33 -l 33` showed both values in the source paragraph.

Moved conventions from `docs/results/targets.md` to `docs/methods/comparison.md` and
updated the code reference. Kept all 399 targets. Added a default report destination
so the requested `--demo` shorthand runs. All six requested review fixes are covered.
The PR API showed no review threads, reviews or issue comments awaiting a response.

Verified implementation revision: `9f964f89f93134915f1987113ea10f8180b3ce8f`.
This outcome is a documentation-only follow-up. Delivery PR:
https://github.com/jesusvillota/replicate/pull/16, into `main`, with
`Goal-Task: hmm-rebalancing/TASK-020` and label `goal:hmm-rebalancing`.
No task specifications, other tasks, decisions, goal.yaml or paper-notes were edited
by this task. The PR is not merged.

### Source corrections and clarifications

- Table D.1 (PDF page 62): Calendar adjusted R-squared is **0.7194**, preserving precision beyond the notes' 0.719.
- Table 3 (PDF page 34): all four columns have **6,223** observations, rather than the section's general default of 6,226.
- Figure D.3 (PDF page 59): outside predicted rebalancing days is not uniformly insignificant. The chart has t about **+2.5** at delta 0.3% and **-3.0** at delta 2.3%. Its during-rebalancing minimum is about **-6.1** at delta 1.8%.
- Figure 2 (PDF page 13) uses a **1%** reference line, about 2.58. The report uses the task's **1.96** cutoff. The notes' rough 2.7% threshold refers to the chart's reference line.
- Figure D.5 (PDF page 61) prints a signed mean of **-0.6 bps**. Text (PDF page 22) reports a positive **0.6 bps** cost magnitude. Both are retained as separate targets.
- Figure 6 (PDF page 42) labels the axis "Cumulative Gains (Log Scale)". Targets retain its approximately 6.2 and 2.3 axis readings without assuming a conversion to wealth multiples or unshifted log returns.

- The bond one-SD **4.1/2.3 bps** targets are on PDF page **33**, not 35.
- One-SD target signs now describe coefficient times positive SD, matching the emitted signed estimates.

These findings are reported here; paper-notes remains unchanged as required. All other section 4 numeric estimates agree at their stated precision. Source pages are one-based PDF pages; printed pages are two lower.

Proposed follow-ups: keyed exports for C1/C2 would enable their comparisons; they are
explicitly skipped under this review's requested behavior. No material decision or
missing access blocks this task. Approximate charts and rounded coefficients still
limit precision near a significance cutoff.
