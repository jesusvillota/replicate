# TASK-005 outcome

## Acceptance

- [x] Both fetchers print `OK` lines. The complete Verify block exited 0 twice on 2026-10-21. Each live run printed 10 French `OK` lines and two HXZ `OK` lines.
- [x] The French three-factor daily file covers 1961-06-16 through 2023-03-17. A separate stored-data check confirmed 15544 rows in this interval, both endpoints present, and every series observed. The full file contains 26317 rows, from 1926-07-01 through 2026-08-31.
- [x] The five-factor, momentum and HXZ files cover 1997-09-10 through 2023-03-17. A separate stored-data check confirmed 6422 rows in each interval, both endpoints present, and every series observed. Full histories: five-factor 1963-07-01 through 2026-08-31 (15897 rows); momentum 1926-11-03 through 2026-08-31 (26216 rows); HXZ 1967-01-03 through 2025-12-31 (14848 rows).
- [x] `docs/data/cards/french.md` and `docs/data/cards/hxz.md` exist. The Verify listing, source-card tests and separate file-existence checks confirmed both. The cards record URLs, download date, storage class, series, original units, transforms, coverage and known problems.
- [x] `uv run pytest tests/test_fetch_factors.py` passes. Verify ran `uv run pytest -q tests/test_fetch_factors.py`: **30 passed in 2.90s** after the rebase. Tests compare every generated file across repeated offline runs, including JSON metadata, with no extension exclusions.

Exact Verify commands:

```sh
uv run python3 -m rebal.fetch.french && uv run python3 -m rebal.fetch.hxz
uv run pytest -q tests/test_fetch_factors.py
ls data/public/french data/public/hxz docs/data/cards/
```

The second block ran with `set -e` and exited **0** at implementation revision `c157b02e960fe14d0678b28a1c89b04a3b4cb362`. Its live summaries included the following (repository-relative paths):

```text
OK data/public/french/F-F_Research_Data_Factors_daily.csv rows=26317 first=1926-07-01 last=2026-08-31
OK data/public/french/F-F_Research_Data_5_Factors_2x3_daily.csv rows=15897 first=1963-07-01 last=2026-08-31
OK data/public/french/F-F_Momentum_Factor_daily.csv rows=26216 first=1926-11-03 last=2026-08-31
OK data/public/french/F-F_ST_Reversal_Factor_daily.csv rows=26446 first=1926-01-26 last=2026-08-31
OK data/public/french/F-F_LT_Reversal_Factor_daily.csv rows=25216 first=1930-03-20 last=2026-08-31
OK data/public/hxz/q5_factors_daily.raw.csv rows=14848 first=1967-01-03 last=2025-12-31
OK data/public/hxz/q5_factors_daily.csv rows=14848 first=1967-01-03 last=2025-12-31
30 passed in 2.90s
```

French also printed one `OK` for each of the five original ZIP daily blocks. The listing confirmed all five ZIPs, five French tidy CSVs, both HXZ CSVs, `source.json`, and both source cards.

Additional local verification:

- The strengthened repeat-run test first reproduced the review failure: **1 failed, 1 passed**, with only `source.json` differing because of `downloaded_utc`.
- After the fix, both offline repeat-run tests pass as part of the 30 factor tests.
- After the second live fetch and Verify block, `git status --porcelain` printed nothing. `test -z "$(git status --porcelain)"` exited **0**. All committed files remained unchanged, including `source.json`.
- Full suite after the rebase: `uv run pytest -q` — **128 passed in 19.67s**.
- `uv run --with ruff ruff check src/rebal/fetch/hxz.py tests/test_fetch_factors.py` — **All checks passed!**
- `uv run --with ruff ruff format --check src/rebal/fetch/hxz.py tests/test_fetch_factors.py` — **2 files already formatted**.
- `git diff --check` passed. The raw HXZ CSV retains the publisher's unchanged CRLF bytes.

## Summary

Added `rebal.fetch.french` and `rebal.fetch.hxz` with the shared download, summarize, storage and validation helpers. French retains all five official ZIP archives and parses only daily records into tidy CSVs. HXZ chooses the newest official daily q5 year and stores its unchanged CSV and tidy CSV. Full histories and original percent units remain intact. Each public data file is under 1 MB.

Review correction: `source.json` now contains only `data_url` and `sha256`. It has no timestamp. The source card retains the download date. The repeat-run test compares every output file, including JSON, and the stored-metadata test requires exactly those two fields. Both live fetchers can run again without changing the committed tree.

The newest linked HXZ daily file is `q5_factors_daily_2025.csv`. HXZ retains the published `R_F`, `R_MKT`, `R_ME`, `R_IA`, `R_ROE`, `R_EG` names. French retains Mkt-RF and RF for TASK-012 to construct D16. Current vintages can revise historical returns; both cards record this limitation.

Deviations: none. No mirror, material decision or cluster job was needed. No task specs, other task outcomes, decisions, goal configuration or master source map changed.

Verified implementation revision: `c157b02e960fe14d0678b28a1c89b04a3b4cb362`, after a conflict-free rebase onto `origin/main` at `dbf1814`. The following documentation-only commit updates this outcome.

PR: https://github.com/jesusvillota/replicate/pull/17, into `main`, with `Goal-Task: hmm-rebalancing/TASK-005` and label `goal:hmm-rebalancing`. The GitHub review-thread query returned no open threads. The review finding supplied in the resume request is fixed. Local Verify determines delivery; GitHub Actions were not read or used. The PR remains open and ready for review. No merge was performed.

Proposed follow-ups: none beyond the existing TASK-012 unit conversion, source-map update and panel assembly.
