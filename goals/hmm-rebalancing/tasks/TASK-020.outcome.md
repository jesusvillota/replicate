# TASK-020 outcome

## Acceptance

- [x] `uv run pytest tests/test_compare.py` passes. After rebasing onto `origin/main`, the exact command collected seven tests and reported **7 passed in 0.38s**. The final Verify command below also passed seven tests.
- [x] `wc -l docs/results/targets.csv` reports at least 150 rows. It reports **400 lines**: one header and **399 numeric targets**, covering **34 exhibits**.
- [x] `uv run python3 -m rebal.compare --demo --out output/demo/compare.md` exits 0. Its top summary reports **0/399 matched targets**, N/A agreement rates with zero eligible targets, and explicitly lists **all 34 missing exhibits**. No demo exhibits have been produced in this checkout. The generated report stays git-ignored.

The complete task Verify block exited **0** after the rebase. Its output, including the requested report head and tail, was:

```text
.......                                                                  [100%]
7 passed in 0.34s
     400 docs/results/targets.csv
Comparison report: output/demo/compare.md
# Paper comparison

## Summary

- Targets matched: 0/399
- Sign-match rate: N/A (0/0 eligible targets)
- Significance-match rate: N/A (0/0 eligible targets)
- Missing exhibits: costs, figure_1, figure_2, figure_3, figure_4, figure_5, figure_6, figure_D1, figure_D2, figure_D3, figure_D4, figure_D5, table_1, table_2a, table_2b, table_3, table_4, table_5, table_6a, table_6b, table_6c, table_C1, table_C2, table_D1, table_D10, table_D11, table_D12, table_D14, table_D3, table_D4, table_D6, table_D7, table_D8, table_D9

Targets: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-020/docs/results/targets.csv`. Inputs: `/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-020/output/demo`.

Each row compares one statistic. Approximate chart readings have a `~` prefix. Sign checks apply to coef, t and value. Significance checks apply to coef and t, using |t| ≥ 1.96 on both sides (or neither). Where t is absent, coef/se is used. N/A means missing data, an inapplicable check, or division by zero. Missing exhibits have no matched numeric targets; partial exhibits retain N/A rows.

## costs

| term | paper | ours | ours/paper | sign match | significance match |
|---|---:|---:|---:|---|---|
| calendar: annual_bps [value] | 5 | N/A | N/A | N/A | N/A |
| headline: annual_bps [value] | 8 | N/A | N/A | N/A | N/A |
| headline: annual_usd [value] | 1.6e+10 | N/A | N/A | N/A | N/A |
| household: annual_usd [value] | 200 | N/A | N/A | N/A | N/A |
| random: annual_bps [value] | 0.6 | N/A | N/A | N/A | N/A |
| threshold: annual_max_bps [value] | 27 | N/A | N/A | N/A | N/A |
| threshold: annual_mean_bps [value] | 15 | N/A | N/A | N/A | N/A |
| threshold: annual_min_bps [value] | 6 | N/A | N/A | N/A | N/A |
| threshold: annual_one_pct_trade_bps [value] | 11 | N/A | N/A | N/A | N/A |

## figure_1

| term | paper | ours | ours/paper | sign match | significance match |
```

## Summary

Encoded the numeric targets from paper-notes section 4 in `docs/results/targets.csv`. Checked table entries against the original PDF and chart readings against rendered pages. Each value has a source PDF page and a chart approximation flag. Added companion standard errors, complete baseline Tables 1 and 3, and model statistics to support significance checks and exceed the minimum target count.

Added `rebal.compare`, which reads existing real or demo exhibit CSVs and writes one Markdown section per exhibit. It joins exact exhibit/column/term keys and selects the target statistic. It computes ratios and sign agreement. Significance agreement uses the required absolute t-statistic cutoff of 1.96; missing t-statistics can be derived from coefficient/standard error. Missing values remain N/A. The summary shows eligible denominators and missing exhibits. Duplicate keys and non-finite estimates fail clearly. It never runs an exhibit or starts a cluster job.

Documented target keys, units, page numbering and produced CSV formats in `docs/results/targets.md`. Regression CSVs follow `docs/contracts/exhibits.md`; figure and scalar exporters can use the documented keyed wide or long forms. Arbitrary plotting columns need an exporter using these keys. Figure 1, Figure 5, Table 4 and Table 5 are retained from section 4, although the scaffold contract does not list their IDs.

Local validation: all **27 tests passed in 17.00s** before the documentation-only target completion. After rebase, the seven comparison tests, Ruff check and Ruff format check passed. Tests cover exact joins, statistic selection, coefficient signs, two-sided significance including the exact 1.96 boundary, derived t-statistics, zero denominators, missing estimates/exhibits, figure formats, demo isolation and invalid outputs. The final task Verify block above passed after all implementation and target changes.

Verified implementation revision: `77b1be182350ba1de55b3b50df89b980d37ce8bf`. This outcome is a documentation-only follow-up commit. Delivery PR: https://github.com/jesusvillota/replicate/pull/16 into `main`. The branch stays `goal/hmm-rebalancing/task-020`. No task specifications, other tasks, decisions, goal.yaml or paper-notes were edited. No merge was performed.

### Source corrections and clarifications

- Table D.1 (PDF page 62): Calendar adjusted R-squared is **0.7194**, preserving precision beyond the notes' 0.719.
- Table 3 (PDF page 34): all four columns have **6,223** observations, rather than the section's general default of 6,226.
- Figure D.3 (PDF page 59): outside predicted rebalancing days is not uniformly insignificant. The chart has t about **+2.5** at delta 0.3% and **-3.0** at delta 2.3%. Its during-rebalancing minimum is about **-6.1** at delta 1.8%.
- Figure 2 (PDF page 13) uses a **1%** reference line, about 2.58. The report uses the task's **1.96** cutoff. The notes' rough 2.7% threshold refers to the chart's reference line.
- Figure D.5 (PDF page 61) prints a signed mean of **-0.6 bps**. Text (PDF page 22) reports a positive **0.6 bps** cost magnitude. Both are retained as separate targets.
- Figure 6 (PDF page 42) labels the axis "Cumulative Gains (Log Scale)". Targets retain its approximately 6.2 and 2.3 axis readings without assuming a conversion to wealth multiples or unshifted log returns.

These findings are reported here; paper-notes remains unchanged as required. All other section 4 numeric estimates agree at their stated precision. Source pages are one-based PDF pages; printed pages are two lower.

Proposed follow-ups: the existing exhibit tasks should export the documented exact keys and units. Approximate chart values and rounded source coefficients limit the precision of agreement near a significance cutoff. No material decision or missing access blocked this task.
