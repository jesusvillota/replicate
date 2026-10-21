# TASK-008 outcome

## Acceptance

- [x] `uv run python3 -m rebal.fetch.ici` prints `OK`. Final verification printed `rows=31 first=2025-10-01 last=2026-10-14`. `docs/data/cards/ici.md` explains the unrecovered 2007-01-01–2025-09-30 history and later gaps. This uses the acceptance clause permitting an explained gap.
- [x] `uv run python3 -m rebal.fetch.ppd` prints `OK` covering fiscal years 2003–2022. Final verification printed `ppd_coverage.csv rows=20 first=2003-12-31 last=2022-12-31` and `ppd_allocations.csv rows=5060 fiscal_years=2003–2022`. All six main allocation variables have observations in every required fiscal year.
- [x] `docs/data/cards/ppd.md` lists every allocation variable used: `EQTotal_Actl/Trgt`, `FITotal_Actl/Trgt`, `CashTotal_Actl/Trgt`, plus the exact domestic, international and global component names. It explicitly records the three entirely missing target series.

The spec's Verify commands ran after rebase and exited **0** on 2026-10-21:

```sh
uv run python3 -m rebal.fetch.ici && uv run python3 -m rebal.fetch.ppd
grep -H -A4 -i 'coverage' docs/data/cards/ici.md docs/data/cards/ppd.md
```

Fetcher output:

```text
OK /Users/jesusvillotamiranda/data/replicate/licensed/ici/ici_weekly_flows.csv rows=31 first=2025-10-01 last=2026-10-14
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-008/data/public/ppd/ppd_coverage.csv rows=20 first=2003-12-31 last=2022-12-31
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-008/data/public/ppd/ppd_allocations.csv rows=5060 fiscal_years=2003–2022
```

Verify output tail:

```text
docs/data/cards/ppd.md:## Coverage
docs/data/cards/ppd.md-
docs/data/cards/ppd.md-Fiscal years 2003–2022, all 20 years; 5,060 plan-year rows in `ppd_allocations.csv`.
docs/data/cards/ppd.md:`ppd_coverage.csv`: 20 rows, 2003-12-31–2022-12-31; each row counts plans.
docs/data/cards/ppd.md-The raw full file contains 7,578 rows; the raw detailed file contains 6,052 rows.
docs/data/cards/ppd.md-There are missing allocations for individual plans; no values are filled.
docs/data/cards/ppd.md-
docs/data/cards/ppd.md-## Known problems
Verify exit=0
```

Additional local verification after rebase: **104 passed in 17.76s** with `uv run pytest`. Ruff check passed, and format check reported **3 files already formatted** for the two fetchers and their test file. Both `--help` commands also exited 0. The six new tests check weekly/monthly separation, category mapping, holiday dates, schema changes, original units, missing targets, duplicate plan-year keys and missing required years/allocations.

## Summary

Added `rebal.fetch.ici` and `rebal.fetch.ppd` using shared downloads and summaries. ICI originals and tidy output remain in external licensed storage. CRR originals, codebooks, tidy allocations, annual coverage and metadata are committed under `data/public/ppd/`. Every public file is below 20 MB. Original CRR files retain published bytes, including CRLF and whitespace in the site's download definition.

ICI combines four original Wayback Excel snapshots with the current official workbook. Later publications supersede earlier estimates for overlapping dates. Monthly actual flows are excluded. Direct ICI access initially returned HTTP 403, then succeeded; archive fallback remains available. No values were fabricated or interpolated.

CRR provides 253 plans and 5,060 rows over 2003–2022. The main full dataset no longer supplies domestic/international equity fields. The official detailed investment workbook supplies the geographic components; those remain unaggregated. Global equity is kept separate. Raw fractional allocations and USD-thousand assets are unchanged. The date column labels fiscal years, while uniqueness is enforced on plan ID plus fiscal year.

Deviations and limits: ICI does not reach January 2007. The card records the missing history, checked URLs and Wayback results, as the acceptance explicitly allows. Some PPD geographic targets are missing; they remain blank. The two source vintages are documented. No figure, flow measure or unit conversion was built. No cluster job ran. No task spec, other outcome, decision, goal definition or master source map was edited.

Verified implementation revision: `a52591162b985cac9206fefceaaff697f500b0f8`, rebased onto `origin/main` without conflicts. This outcome is a documentation-only follow-up commit. PR: https://github.com/jesusvillota/replicate/pull/19, into `main`, carrying `Goal-Task: hmm-rebalancing/TASK-008` and label `goal:hmm-rebalancing`. Local verification determines readiness; GitHub Actions are ignored per owner instruction. Never merge this PR as part of this task.

Proposed follow-ups: recover additional official ICI weekly history before a full-sample Figure 5 replication. TASK-012 owns unit conversions and the master source map. Existing figure tasks own allocation aggregation and flow measures.
