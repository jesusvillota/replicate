# TASK-008 outcome

## Acceptance

- [x] `uv run python3 -m rebal.fetch.ici` printed `OK` on 2026-10-22: `rows=278 first=2008-12-03 last=2026-10-14`. `docs/data/cards/ici.md` explains the starting gap, 2007-01-01–2008-12-02, and every later gap across 39 recovered blocks. This satisfies the acceptance clause permitting an explained gap.
- [x] `uv run python3 -m rebal.fetch.ppd` printed `OK` covering fiscal years 2003–2022: `ppd_coverage.csv rows=20 first=2003-12-31 last=2022-12-31`, followed by `ppd_allocations.csv rows=5060 fiscal_years=2003–2022`. All six main actual/target allocation variables have observations in each required fiscal year.
- [x] `docs/data/cards/ppd.md` lists all 28 allocation variable names used. A local assertion checked each exact name from `TOTALS` and `GEOGRAPHY` against the card. These include `EQTotal_Actl`, `EQTotal_Trgt`, `FITotal_Actl`, `FITotal_Trgt`, `CashTotal_Actl`, `CashTotal_Trgt`, and every domestic, international and global equity component. The card records three entirely missing geographic target series.

The spec's exact Verify block ran after rebase onto `origin/main` and exited **0** on 2026-10-22:

```sh
uv run python3 -m rebal.fetch.ici && uv run python3 -m rebal.fetch.ppd
grep -H -A4 -i 'coverage' docs/data/cards/ici.md docs/data/cards/ppd.md
```

Fetcher output:

```text
OK /Users/jesusvillotamiranda/data/replicate/licensed/ici/ici_weekly_flows.csv rows=278 first=2008-12-03 last=2026-10-14
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-008/data/public/ppd/ppd_coverage.csv rows=20 first=2003-12-31 last=2022-12-31
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-008/data/public/ppd/ppd_allocations.csv rows=5060 fiscal_years=2003–2022
```

Coverage output included:

```text
docs/data/cards/ici.md-2008-12-03–2026-10-14; weekly; 278 rows in `ici_weekly_flows.csv`.
docs/data/cards/ici.md-Requested starting-history gap: 2007-01-01–2008-12-02.
docs/data/cards/ppd.md-Fiscal years 2003–2022, all 20 years; 5,060 plan-year rows in `ppd_allocations.csv`.
docs/data/cards/ppd.md:`ppd_coverage.csv`: 20 rows, 2003-12-31–2022-12-31; each row counts plans.
```

Additional output assertions passed: ICI has unique weekly dates and the documented coverage; PPD has 5,060 unique plan-year rows, 253 plans, every required fiscal year, and every public file below 20 MB. Re-running both fetchers left committed data unchanged.

Local checks on this revision also passed:

- `uv run pytest`: **245 passed in 182.62s**, including 12 ICI/PPD cases and the full demo exhibit run.
- `uv run --with ruff ruff check src/rebal/fetch/ici.py src/rebal/fetch/ppd.py tests/test_fetch_ici_ppd.py`: `All checks passed!`
- `uv run --with ruff ruff format --check src/rebal/fetch/ici.py src/rebal/fetch/ppd.py tests/test_fetch_ici_ppd.py`: `3 files already formatted`.
- `git diff --check`: no whitespace errors.

## Summary

Added `rebal.fetch.ici` and `rebal.fetch.ppd` using shared downloads and summaries. ICI originals and tidy output remain in external licensed storage. CRR originals, codebooks, tidy allocations, annual coverage and metadata are committed under `data/public/ppd/`. Original CRR bytes are retained unchanged.

The resumed ICI fix searches older official paths, including `/info/flows_data_<year>.xls`. A manifest records 56 distinct Wayback originals: 47 Excel files and nine PDFs. The parser supports nine-column and 40-column Excel layouts and older PDF tables. CDX SHA-1 digests validate immutable archive bytes. Later publications supersede earlier overlapping estimates. Monthly actual flows are excluded; holiday week-ending dates remain unchanged. The current live workbook is fetched on each run. No values are fabricated, interpolated or scaled.

Removed the committed website JavaScript from PPD data. The fetcher now reads that download definition in a temporary directory. CRR provides 253 plans over 2003–2022. The official detailed workbook supplies geographic equity components absent from the current full CSV. Components stay unaggregated, global equity stays separate, and missing targets stay blank. Fractional allocations and USD-thousand assets remain in original units. Plan ID plus fiscal year identifies each row.

Deviations and limits: ICI still does not reach January 2007. Its card documents archive searches, each recovered block, every remaining gap, and an excluded capture whose replay bytes fail the indexed digest. Incomplete weekly coverage limits a full-sample Figure 5 replication. Some PPD geographic targets remain missing, as documented. No figure, flow measure or unit conversion was built. No cluster job ran. No task spec, other outcome, decision, goal definition or master source map was edited.

Verified implementation revision: `25e5c7f9693615b00d9365431edeecd05b102532`, after a conflict-free rebase onto `origin/main`. This outcome is a documentation-only follow-up. The previous remote feature commits were patch-equivalent to the local rebased versions; no independent remote changes were discarded.

PR: https://github.com/jesusvillota/replicate/pull/19, into `main`, with `Goal-Task: hmm-rebalancing/TASK-008` and label `goal:hmm-rebalancing`. The session found no PR review comments, reviews, issue comments or review threads. The prior handoff's two requested fixes—older ICI archive recovery and removal of `download.raw.js`—are included. Local verification determines readiness; GitHub Actions are ignored under owner rules. This task does not merge the PR.

Proposed follow-ups: recover additional official ICI weekly history before full-sample Figure 5 replication. TASK-012 owns unit conversions and the master source map. Existing figure tasks own allocation aggregation and flow measures.
