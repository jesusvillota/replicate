# TASK-028 outcome

## Acceptance

- [x] `uv run pytest -q tests/test_trading_corr.py` passes. Final local Verify at code revision `6cad1db`: **14 passed in 2.53s**, exit 0. Tests cover planted and zero correlations, lag direction, beginning-open-interest scaling, source gaps, LTPos mean changes, ICI blocks and pooling, source header/contract mappings, missing pairs, sample boundaries, and written artifacts.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only figure_5` exits 0. `ls output/demo/figure_5*` lists the PDF, CSV and metadata. A separate CSV inspection confirms 20 rows, exactly five `column` values, and no ANcerno row. The PDF was rendered with Poppler and visually inspected: five groups, two bars each, clear labels and no clipping.
- [x] `docs/methods/trading_corr.md` records the report and contract choices, Q formula and scaling, weekly lag and signal aggregation, LTPos units and aggregation, ICI categories, block rules, pooled formula and N, sample and missing-data rules, and unavailable ANcerno. The cheap alternatives have CLI flags.
- [x] The real-data smoke correlations are recorded next to all five paper pairs below. `uv run python3 -m rebal.exhibits.trading_corr` exits 0 using the local real signals, public CFTC files and external ICI file. All ten correlations are finite. No real outputs are committed.

## Summary

Implemented the isolated auto-discovered `figure_5` module, its tests, and its methods guide.
Legacy COT uses future net changes divided by beginning open interest for each market.
LTPos uses the published mean daily directional changes without differencing.
ICI uses domestic equity less taxable and municipal bond flows.
Weekly references precede trading. ICI references stay inside their source block.
The pooled ICI correlation removes each block's paired-sample means.

The shared demo, IO, regressions, signals, panel, comparison, contracts and source map are unchanged.
No cluster jobs ran. No task spec, decision or goal definition was edited.
No scope deviations or missing acceptance inputs remain.

Verified code revision: `6cad1db`.
The outcome-only commit follows that revision on `goal/hmm-rebalancing/task-028`.
The branch was rebased onto `origin/main` without conflicts before the code commit.
Local verification decides delivery; GitHub Actions were not consulted.
PR: https://github.com/jesusvillota/replicate/pull/38 (base `main`, label `goal:hmm-rebalancing`).

Proposed follow-up: TASK-030 runs and commits the final real outputs and discusses the gaps below.
No additional task or decision is required for this demo-code delivery.

## Real-data smoke comparison

Run date: 2026-10-23. Defaults: legacy COT, E-mini/TY, clean signals,
one report-week lag, reference-date signals, inclusive end 2023-03-17.
Sources: `data/public/cftc/cot_legacy.csv`, `data/public/cftc/ltpos.csv`,
`~/data/replicate/licensed/ici/ici_weekly_flows.csv`, and
`~/data/replicate/processed/signals_clean.parquet`.
Numbers are correlations, not percentage points. Paper targets are approximate.

| Investor group | Smoke Threshold | Paper Threshold | Smoke Calendar | Paper Calendar | N per signal |
|---|---:|---:|---:|---:|---:|
| cftc_hedgers | -0.089722 | -0.10 | -0.128595 | -0.13 | 867 |
| cftc_speculators | +0.094024 | +0.11 | +0.153255 | +0.17 | 867 |
| ltpos_asset_managers | -0.021851 | -0.08 | -0.041240 | -0.12 | 125 |
| ltpos_leveraged_funds | +0.018780 | +0.18 | +0.089058 | +0.13 | 125 |
| ici | -0.044615 | -0.17 | -0.174532 | -0.19 | 194 |

All five signs agree with the paper for both signals. Magnitudes differ, particularly
for LTPos and ICI Threshold. This smoke check does not establish numerical replication.
The signals use the goal's return proxies. LTPos uses unscaled contract-count spreads
and the documented prior-week reference. ICI has sparse recovered weekly blocks and
uses within-block pooling. Those differences limit direct comparison with the paper.
No parameters were selected to match its numbers.

CFTC response dates are 2006-08-08–2023-03-14, LTPos 2009-01-09–2011-05-27,
and ICI 2008-12-10–2022-03-23. The ICI file has 39 blocks, of which 32 enter
the default sample. They supply 194 pairs for each signal. No missing interval is bridged.

### ICI observations per source block

N below is the usable paired count after the lag, sample and signal filters.
All 39 source blocks remain visible, including those outside the sample.
Short holiday intervals are retained. The 2013-12-04 block includes a five-day
interval ending 2013-12-23 and an eight-day interval ending 2013-12-31.
Both pairs remain within that block. A dedicated regression test checks this case.

| Block | First source date | Last source date | Source rows | Threshold N | Calendar N |
|---:|---|---|---:|---:|---:|
| 0 | 2008-12-03 | 2009-03-04 | 14 | 13 | 13 |
| 1 | 2009-12-02 | 2010-01-20 | 8 | 7 | 7 |
| 2 | 2010-03-03 | 2010-03-24 | 4 | 3 | 3 |
| 3 | 2010-10-06 | 2010-12-15 | 11 | 10 | 10 |
| 4 | 2011-01-05 | 2011-02-09 | 6 | 5 | 5 |
| 5 | 2011-03-02 | 2011-04-20 | 8 | 7 | 7 |
| 6 | 2011-05-04 | 2011-06-15 | 7 | 6 | 6 |
| 7 | 2011-08-03 | 2011-08-24 | 4 | 3 | 3 |
| 8 | 2011-10-05 | 2011-12-14 | 11 | 10 | 10 |
| 9 | 2012-01-04 | 2012-02-08 | 6 | 5 | 5 |
| 10 | 2012-03-07 | 2012-04-11 | 6 | 5 | 5 |
| 11 | 2012-05-02 | 2012-06-20 | 8 | 7 | 7 |
| 12 | 2012-08-01 | 2012-09-05 | 6 | 5 | 5 |
| 13 | 2012-10-03 | 2012-11-07 | 6 | 5 | 5 |
| 14 | 2012-12-05 | 2013-01-09 | 6 | 5 | 5 |
| 15 | 2013-02-06 | 2013-03-20 | 7 | 6 | 6 |
| 16 | 2013-04-03 | 2013-05-15 | 7 | 6 | 6 |
| 17 | 2013-07-02 | 2013-08-28 | 9 | 8 | 8 |
| 18 | 2013-10-02 | 2013-11-06 | 6 | 5 | 5 |
| 19 | 2013-12-04 | 2013-12-31 | 5 | 4 | 4 |
| 20 | 2014-02-05 | 2014-04-09 | 10 | 9 | 9 |
| 21 | 2014-06-04 | 2014-08-20 | 12 | 11 | 11 |
| 22 | 2014-09-03 | 2014-10-01 | 5 | 4 | 4 |
| 23 | 2015-02-25 | 2015-03-25 | 5 | 4 | 4 |
| 24 | 2015-12-02 | 2015-12-30 | 5 | 4 | 4 |
| 25 | 2016-02-03 | 2016-04-06 | 10 | 9 | 9 |
| 26 | 2017-01-04 | 2017-01-25 | 4 | 3 | 3 |
| 27 | 2017-06-07 | 2017-06-28 | 4 | 3 | 3 |
| 28 | 2017-08-02 | 2017-09-20 | 8 | 7 | 7 |
| 29 | 2019-12-04 | 2019-12-31 | 5 | 4 | 4 |
| 30 | 2020-05-27 | 2020-06-24 | 5 | 4 | 4 |
| 31 | 2022-02-02 | 2022-03-23 | 8 | 7 | 7 |
| 32 | 2024-01-03 | 2024-02-14 | 7 | 0 | 0 |
| 33 | 2024-10-02 | 2024-11-20 | 8 | 0 | 0 |
| 34 | 2024-12-04 | 2025-01-08 | 6 | 0 | 0 |
| 35 | 2025-10-01 | 2025-11-12 | 7 | 0 | 0 |
| 36 | 2025-12-03 | 2026-02-18 | 12 | 0 | 0 |
| 37 | 2026-03-04 | 2026-04-01 | 5 | 0 | 0 |
| 38 | 2026-09-02 | 2026-10-14 | 7 | 0 | 0 |

## Local verification

The required Verify block exited 0 after rebasing. Its tail was:

```text
..............                                                            [100%]
14 passed in 2.53s
1 exhibit modules
[absolute output paths printed by the runner]
output/demo/figure_5.csv
output/demo/figure_5.metadata.json
output/demo/figure_5.pdf
```

The exact commands were:

```sh
uv run pytest -q tests/test_trading_corr.py
uv run python3 -m rebal.exhibits --all --demo --only figure_5
ls output/demo/figure_5*
```

Additional checks:

- Task tests plus `tests/test_scaffold.py::test_exhibit_discovery_and_selection`: 15 passed (final combined check).
- Ruff check: all checks passed. Ruff format check: two files already formatted.
- Real sensitivity smoke: E-mini/TFF/reference-date/latest and full-size/legacy/weekly-mean/latest both produce 20 finite CSV rows.
- `pdftoppm -scale-to 1200 -png -singlefile output/demo/figure_5.pdf /tmp/task028-figure5`: exit 0, PNG visually inspected.
- `git diff --check`: exit 0.

After recording the real smoke results, `git restore output/` restored tracked outputs.
Only the three newly generated real `figure_5` files were deleted.
Demo artifacts remain ignored and available locally.
