# TASK-003 outcome

## Acceptance

1. [x] Running all four fetchers prints one `OK` line per file. The exact Verify block exited 0. Its captured output contains 12 unique `OK` lines for 12 files and no `FAILED` lines: six FRED files, two GSW files, two OFR files, and two external HPW files.
2. [x] Coverage is validated on the stored files, not inferred from download success. The 16 rate tests check schemas, unique sorted dates, observed study endpoints, long-sample GSW history, raw/tidy equality, and OFR/HPW coverage. All values remain in the original units.
3. [x] DTB3, VIXCLS and GSW cover 1997-09-10–2023-03-17. Stored DTB3 spans 1954-01-04–2026-07-06; VIXCLS spans 1990-01-02–2026-10-08; GSW spans 1961-06-14–2026-10-16. Tests verify nonmissing observations on both study endpoints for DTB3, VIXCLS, DGS10, SVENY10 and SVENPY10.
4. [x] GSW has a 10-year yield from about 1971. Both SVENY10 and SVENPY10 first have observed values on 1971-08-16. Both reach 2026-10-16. The raw file is 16,661,023 bytes; the tidy file is 10,812,413 bytes. All requested 66 yield/parameter series fit below 20 MB; no par-yield columns were dropped.
5. [x] OFR and HPW coverage is printed and recorded in their cards. OFR, including Funding: 2000-01-03–2026-10-19, 6,783 rows. HPW Noise_bp: 1987-01-02–2025-12-31, 9,751 rows. Both have no missing values within their published rows. The Verify output below shows both. `docs/data/cards/ofr.md` and `hpw.md` record these same endpoints; tests check the card dates against the files.
6. [x] `ls docs/data/cards/` lists `fred.md`, `gsw.md`, `ofr.md` and `hpw.md`, alongside the existing template. Exact output is below.
7. [x] `uv run pytest -q tests/test_fetch_rates.py` passes: **16 passed in 0.73s** in the final Verify block. Tests read all stored files, including HPW in external storage. Full local suite: **36 passed in 11.17s**. Ruff lint passed and its format check reported 15 files already formatted. All four module `--help` commands exited 0.

## Summary

Implemented four CLI fetchers with `rebal.fetch.common.download` and `summarize`, plus a small shared schema/coverage validator. Extended `summarize` to accept CSV/Excel reader options so it can validate the unchanged GSW file with header notes and the HPW workbook with side notes. Each fetcher validates columns, dates, numeric data, and coverage before reporting success. Kept raw publications and tidy CSVs; no interpolation or return/unit conversion was added. Added four source cards and stored-file tests.

FRED returned HTTP 200 maintenance HTML from its live graph, legacy CSV and API routes. As the spec permits, the fetcher falls back to exact Wayback snapshots. The cards and console output identify those snapshots. Their dates are older than the download day: DTB3 ends July 6, DGS10 October 9, and VIXCLS October 8, 2026. The live source is retried on every invocation; this is the obtainable archived history, not a claim of current FRED data. All required study coverage is present. No data was fabricated.

Jun Pan's current faculty page links the end-2025 workbook. Neither the page nor workbook provides an explicit redistribution grant. Used the task's permitted external-storage route: `licensed_dir("hpw")`, default `~/data/replicate/licensed/hpw/`, configurable with `REPLICATE_DATA_DIR`. Both HPW files remain outside git. Run the HPW fetcher in a fresh checkout before the stored-file tests. The card records the source's warning about occasional data-quality spikes. No change to data licensing terms is assumed.

OFR Funding starts in 2000. HPW starts in 1987. TASK-012 retains ownership of the liquidity-proxy choice. OFR category contributions can differ from the total by 0.002 points due to published rounding. The consistency test uses the theoretical 0.003 rounding bound for five contributions plus the total.

Verified implementation revision: `fc91afd1d3972c86613d5f73c9019cb4490dc791`, after a conflict-free rebase onto `origin/main`. Re-running the fetchers left the tracked implementation and data unchanged. This outcome is a documentation-only follow-up commit. PR: https://github.com/jesusvillota/replicate/pull/12, into `main`, with `Goal-Task: hmm-rebalancing/TASK-003` and label `goal:hmm-rebalancing`. The PR is marked ready after this outcome is committed and pushed. No GitHub Actions were read or used for verification. No cluster jobs ran. No task specs, decisions, other task files, goal.yaml, or the master source map were edited.

Proposed follow-ups: none beyond TASK-012's existing work. The FRED archive fallback and HPW download requirement remain documented limitations.

## Verify

Executed on 2026-10-21 (UTC):

```sh
for m in fred gsw ofr hpw; do uv run python3 -m rebal.fetch.$m || echo "FAILED $m"; done
uv run pytest -q tests/test_fetch_rates.py
ls docs/data/cards/ data/public/*/
```

Exit status: **0**. A separate log assertion confirmed **12 unique OK lines** and **no FAILED fetchers**. Captured output:

```text
FRED DTB3: live source unavailable (Error tokenizing data. C error: Expected 1 fields in line 5, saw 3
); using https://web.archive.org/web/20260708052657id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/DTB3.raw.csv rows=18916 first=1954-01-04 last=2026-07-06
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/DTB3.csv rows=18916 first=1954-01-04 last=2026-07-06
FRED DGS10: live source unavailable (Error tokenizing data. C error: Expected 1 fields in line 5, saw 3
); using https://web.archive.org/web/20261014114807id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/DGS10.raw.csv rows=16899 first=1962-01-02 last=2026-10-09
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/DGS10.csv rows=16899 first=1962-01-02 last=2026-10-09
FRED VIXCLS: live source unavailable (Error tokenizing data. C error: Expected 1 fields in line 5, saw 3
); using https://web.archive.org/web/20261012093245id_/https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/VIXCLS.raw.csv rows=9593 first=1990-01-02 last=2026-10-08
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/fred/VIXCLS.csv rows=9593 first=1990-01-02 last=2026-10-08
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/gsw/feds200628.raw.csv rows=17048 first=1961-06-14 last=2026-10-16
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/gsw/feds200628.csv rows=17048 first=1961-06-14 last=2026-10-16
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/ofr/fsi.raw.csv rows=6783 first=2000-01-03 last=2026-10-19
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-003/data/public/ofr/fsi.csv rows=6783 first=2000-01-03 last=2026-10-19
OK /Users/jesusvillotamiranda/data/replicate/licensed/hpw/Noise_Measure_2025.xlsx rows=9751 first=1987-01-02 last=2025-12-31
OK /Users/jesusvillotamiranda/data/replicate/licensed/hpw/noise.csv rows=9751 first=1987-01-02 last=2025-12-31
................                                                         [100%]
16 passed in 0.73s
data/public/fred/:
DGS10.csv
DGS10.raw.csv
DTB3.csv
DTB3.raw.csv
VIXCLS.csv
VIXCLS.raw.csv

data/public/gsw/:
feds200628.csv
feds200628.raw.csv

data/public/ofr/:
fsi.csv
fsi.raw.csv

docs/data/cards/:
TEMPLATE.md
fred.md
gsw.md
hpw.md
ofr.md
```
