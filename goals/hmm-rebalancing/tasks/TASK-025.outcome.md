# TASK-025 outcome

## Acceptance

- [x] `uv run pytest -q tests/test_segments.py` passes.
  Final Verify on this branch returned `9 passed in 13.77s`, exit 0.
  The tests cover planted effects, zero effects, insignificant Value/Growth,
  segment inputs, futures input isolation, independent next-day OLS, sample
  boundaries, missing history, output schema, metadata and CLI option behavior.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only table_5` writes
  `output/demo/table_5.csv`, exit 0. Reading it with `column` as a string verified
  exactly columns `['1', '2']`, 14 rows, and terms `threshold` and `calendar:week4`.
  `head -5 output/demo/table_5.csv` also returned exit 0. The CSV uses exactly
  `rebal.regress.TABLE_COLUMNS` in the contract order.
- [x] `docs/methods/segments.md` states weights, sample, controls and reasons.
  Both default targets are 90/10; Value/Growth also accepts 50/50. The sample is
  2006-08-17–2023-03-17 with earlier history for initialization. Base controls
  follow Table 1 column (1). `--controls all` adds VIX, MOVE, EPU, ADS and
  Sentiment. The document also states cash treatment, timing, momentum,
  standard errors, calendar limits, ETF substitution and the local demo design.
- [x] Real-data smoke results, with N, appear next to the paper below.
  The actual panel was available; the smoke run completed successfully.

## Summary

Added the automatically discovered `rebal.exhibits.segments` module for Table 5.
It uses `rebal.signals.build` separately for each equity pair and
`rebal.regress.predictive` for the next-day return difference.
It writes the contract CSV and a JSON record of inputs, parameters and sample.
No shared module, contract, task spec, other task, decision or goal.yaml changed.
No cluster job ran.

The shared demo gives identical returns to all segment ETFs. A local fixture
therefore generates distinct causal segment returns on the shared demo calendar.
The size pair plants Threshold = −0.4 and Calendar × week4 = −0.3. The style
pair plants zero effects. This is confined to the task module; shared fixtures
remain unchanged. The default demo estimates are −0.403853 and −0.362109 for
the size pair, and −0.020818 and +0.045432 for the style pair. Both style
effects are insignificant (p = 0.3723 and 0.6446).

Verified code revision: `f0f35bc3fb383a31cb67892f5daa36ab3d0cd555`.
Later changes only add the smoke-count explanation and this outcome.
The branch was rebased onto `origin/main` without conflicts before final Verify.
PR: https://github.com/jesusvillota/replicate/pull/34, base `main`.

### Real-data smoke check

Command: `uv run python3 -m rebal.exhibits.segments`, exit 0. A second in-memory
`build_table(load_panel())` run after the rebase reproduced these estimates.
Defaults: 90/10 for both pairs, clean reset, medium-slow Momentum, base controls,
White HC1 errors. Returns are CRSP ETF total returns less `rf_3m` in each leg.
The cash rate cancels from the dependent return difference.

| Pair | Term | Smoke coefficient | HC1 SE | p | Smoke N | Paper coefficient | Paper N |
|---|---|---:|---:|---:|---:|---:|---:|
| R1K/R2K | Threshold | +0.0000581835 | 0.0392838131 | 0.998818 | 4,109 | −0.2054 | 4,175 |
| R1K/R2K | Cal × week4 | −0.0743923613 | 0.1712124166 | 0.663923 | 4,109 | −0.1174 | 4,175 |
| Value/Growth | Threshold | +0.0109585543 | 0.0332113555 | 0.741427 | 4,109 | −0.0339 | 4,175 |
| Value/Growth | Cal × week4 | −0.1516649730 | 0.1765838927 | 0.390405 | 4,109 | −0.0678 | 4,175 |

Both histories have 6,472 complete return/cash rows, 2000-05-30–2026-07-13.
There are no interior gaps in those retained histories. The study window has
4,110 panel rows, with complete segment returns and cash on every row.
Requiring both prediction and outcome dates inside the window yields 4,109 pairs.
Actual outcome dates: 2006-08-18–2023-03-17 for both regressions.
The shared panel uses the main equity/bond calendar, which removes dates with
missing GSW-based returns. This calendar and the ETF proxies limit comparison
with the paper's unspecified Russell source. We do not force N to match.
These estimates do not reproduce the paper's size-segment effects.

Input: `~/data/replicate/processed/daily_panel.parquet`.
SHA-256: `0aa723f34422fae7bcedb41bfaf0e7a5c3685688a1a9c7e3addec7af0463a4cd`.
After the smoke run, `git restore output/` restored tracked outputs and the two
new real-output files were deleted. No real output is committed.
The final demo artifacts remain ignored under `output/demo/`.

### Verify evidence

All three required commands ran in sequence with `set -e` and returned exit 0:

```sh
uv run pytest -q tests/test_segments.py
uv run python3 -m rebal.exhibits --all --demo --only table_5
head -5 output/demo/table_5.csv
```

Tail of the captured output (Rich wrapped the absolute output paths):

```text
9 passed in 13.77s
1 exhibit modules
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
25/output/demo/table_5.csv
/Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-0
25/output/demo/segments.metadata.json
exhibit,column,term,coef,se,t,p,nobs,adj_r2,se_type,sample_start,sample_end
table_5,1,const,-4.9549690047257313e-05,7.075960144220487e-05,-0.7002539448689318,0.48376872797429205,4326,0.01772417138667748,hc1,2006-08-18,2023-03-17
table_5,1,threshold,-0.40385348284977074,0.06198855356610305,-6.514968645285641,7.270484360699231e-11,4326,0.01772417138667748,hc1,2006-08-18,2023-03-17
table_5,1,calendar,0.046011644614565306,0.09225543286983957,0.4987418429815592,0.6179612628527181,4326,0.01772417138667748,hc1,2006-08-18,2023-03-17
table_5,1,week4,-1.4213556588027479e-06,0.00014540819153522025,-0.00977493526187259,0.9922008542724651,4326,0.01772417138667748,hc1,2006-08-18,2023-03-17
Verified columns: ['1', '2'] ; rows: 14
```

Ruff lint and formatting checks passed with `uv tool run --from ruff ruff`.
The project environment does not include `ruff`; the direct `uv run ruff`
invocation could not find it. The tool invocation leaves dependencies unchanged.
The module's `--help` command also returned exit 0.
`uv run pytest -q tests/test_scaffold.py tests/test_signals.py tests/test_regress.py`
returned `73 passed in 175.42s (0:02:55)`, exit 0. This includes the full demo
exhibit runner and verifies integration with the existing modules.

### Follow-up

TASK-030 owns final real outputs and the comparison report. It can use the
documented flags to assess Value/Growth weight and control choices. This task
does not establish the cause of differences from the paper. No new decision is
needed to implement the defaults explicitly required by this task.
