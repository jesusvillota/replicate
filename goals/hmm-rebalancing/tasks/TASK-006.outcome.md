# TASK-006 outcome

## Acceptance

- [x] `uv run python3 -m rebal.fetch.yahoo` exits 0 and prints exactly ten `OK` lines, one per required ticker. `^SP500TR`: 9,774 rows, 1988-01-04 through 2026-10-21; validation confirms observations on both 1997-09-10 and 2023-03-17. `ES=F` starts 2000-09-18; `ZN=F` starts 2000-09-21. Both start before 2001. Full session output appears below.
- [x] `^MOVE` prints 5,920 rows, first=2002-11-12, last=2026-10-21. `docs/data/cards/yahoo.md` records this coverage and explicitly states that it does not cover 1997-09-10. No early history is filled.
- [x] `uv run python3 -m rebal.fetch.msci` exits 0 and prints `OK` with 6,733 rows, first=2000-12-29, last=2026-10-20. `docs/data/cards/msci.md` documents the missing early years and the verified index code 899901. The service identifies the workbook as ACWI ex USA, Net, USD. Code 991000 instead identifies WORLD ex USA.
- [x] `git status --porcelain` prints no data file under `data/`. It printed nothing during Verify. All downloaded series, raw responses and metadata are under `~/data/replicate/licensed/yahoo/` or `~/data/replicate/licensed/msci/`, outside this repository. No data file is included in this task's diff.

## Summary

Added daily Yahoo and MSCI CLI fetchers, two source cards and 20 focused tests. Yahoo uses `yfinance` with `auto_adjust=False`, preserves Close and Adj Close separately, retains original daily chart response bytes, and backs off after rate or transport failures. MSCI uses `common.download` to save its original Excel workbook and validates the index identity, Net variant and USD before exporting. Both use `licensed_dir`, validate schemas, dates and prices, write lineage metadata with raw SHA-256, and call `common.summarize` on each tidy CSV. Runs overwrite only their own source outputs.

Plan completed: locate public services; implement fetchers; retain raw files; document coverage; run local acceptance checks. No cluster work, return calculation, roll correction, proxy selection, source-map edit or task-spec edit.

Deviations: verified and corrected the spec's tentative MSCI code from 991000 to 899901. The public Excel service works, so MSCI is available rather than skipped. It supplies history only from 2000-12-29 despite a request from 1997-01-01. Yahoo currently supplies only one `^RLG` observation. These source limits are documented, without fabricated data. No material method decision was needed.

Verified implementation revision: `780cbad3213fb83928d96569fbe60af6aeccb5e4` (rebased onto `origin/main` without conflicts). This outcome-only commit does not change the tested implementation. Branch: `goal/hmm-rebalancing/task-006`. PR: https://github.com/jesusvillota/replicate/pull/15, base `main`; never merged.

Local validation: `uv run pytest` passed all 40 tests after the rebase. Tests guard both required sample boundaries, futures start dates, duplicate/unsorted dates, missing prices, MSCI index/variant/currency identity, raw-byte preservation, and rate-limit backoff/exhaustion. Ruff lint and format checks passed for both fetchers and their tests. Both `--help` commands passed. `git diff --check` passed. GitHub Actions were not read or used.

Proposed follow-ups within existing tasks: TASK-009 supplies CRSP ETF proxy candidates; TASK-011 handles the unadjusted front-month rolls and proxy comparison; TASK-012 accounts for MOVE/MSCI/Russell coverage gaps during panel integration. These are source limits, not an authorization to splice proxies in this task.

## Verify

The exact task Verify commands ran on the revision above. The shell block exited **0**. Output (including the empty `git status --porcelain` result):

```text
[22:32:51] Output:                                                  yahoo.py:191
           /Users/jesusvillotamiranda/data/replicate/licensed/yahoo             
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/ES=F.csv rows=6588 first=2000-09-18 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/ZN=F.csv rows=6550 first=2000-09-21 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^GSPC.csv rows=24819 first=1927-12-30 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^MOVE.csv rows=5920 first=2002-11-12 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^RLG.csv rows=1 first=2026-10-21 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^RLV.csv rows=6053 first=2002-09-30 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^RUI.csv rows=8523 first=1992-12-10 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^RUT.csv rows=9853 first=1987-09-10 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^SP500TR.csv rows=9774 first=1988-01-04 last=2026-10-21
OK /Users/jesusvillotamiranda/data/replicate/licensed/yahoo/^VIX.csv rows=9271 first=1990-01-02 last=2026-10-21
[22:33:00] Output:                                                   msci.py:134
           /Users/jesusvillotamiranda/data/replicate/licensed/msci              
OK /Users/jesusvillotamiranda/data/replicate/licensed/msci/acwi_ex_usa_net_usd.csv rows=6733 first=2000-12-29 last=2026-10-20
docs/data/cards/yahoo.md:## Coverage
docs/data/cards/yahoo.md-
docs/data/cards/yahoo.md:`^MOVE` coverage: **2002-11-12 to 2026-10-21**, 5,920 daily observations.
docs/data/cards/yahoo.md-It **does not cover 1997-09-10**. The initial sample gap remains unfilled.
docs/data/cards/yahoo.md-
docs/data/cards/yahoo.md-| Ticker | First date | Last date | Rows | Longest gap, calendar days |
--
docs/data/cards/yahoo.md:An `OK` line confirms the downloaded file's validity, not complete paper-sample coverage.
docs/data/cards/yahoo.md-
docs/data/cards/yahoo.md-## Paper datasets served (D-numbers)
docs/data/cards/yahoo.md-
--
docs/data/cards/msci.md:Status: available, with partial sample coverage.
docs/data/cards/msci.md-
docs/data/cards/msci.md-## License class
docs/data/cards/msci.md-
--
docs/data/cards/msci.md:coverage, download time, and original workbook SHA-256. `latest_world_date.txt`
docs/data/cards/msci.md-preserves the service's date response. No downloaded data enters git.
docs/data/cards/msci.md-
docs/data/cards/msci.md-## Series, with units
--
docs/data/cards/msci.md:## Coverage
docs/data/cards/msci.md-
docs/data/cards/msci.md-**2000-12-29 to 2026-10-20**, daily, **6,733 rows**. Requested from 1997-01-01.
docs/data/cards/msci.md-It **does not cover 1997-09-10**; the public download supplies no earlier observations.
Verify exit=0
```
