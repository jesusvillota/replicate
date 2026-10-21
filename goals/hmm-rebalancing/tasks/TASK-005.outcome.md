# TASK-005 outcome

## Acceptance

- [x] Both fetchers print `OK` lines. The exact Verify block exited 0 on 2026-10-21: French printed 10 `OK` lines (five unchanged ZIP daily blocks plus five tidy CSVs); HXZ printed two (raw and tidy daily CSVs). Output is recorded below.
- [x] The French three-factor daily file covers 1961-06-16 through 2023-03-17. The stored file spans 1926-07-01 through 2026-08-31 (26317 rows). A separate stored-data check selected 15544 observations in the required interval and confirmed both endpoint dates and every series observed throughout that interval.
- [x] The French five-factor, momentum and HXZ files cover 1997-09-10 through 2023-03-17. A separate stored-data check found 6422 rows in each required interval, both endpoints present, and every series observed. Full histories: five-factor 1963-07-01 through 2026-08-31 (15897 rows); momentum 1926-11-03 through 2026-08-31 (26216 rows); HXZ 1967-01-03 through 2025-12-31 (14848 rows).
- [x] `docs/data/cards/french.md` and `docs/data/cards/hxz.md` exist. The Verify listing and two source-card tests confirmed them. Both cards record source URLs, download date, public storage class, series and original units, transforms, coverage, known problems and paper dataset numbers.
- [x] `uv run pytest tests/test_fetch_factors.py` passes. The exact Verify invocation with `-q` printed `30 passed in 2.72s`. Tests cover committed file schemas, dates, complete values, exact raw-to-tidy numeric equality, preserved percent units, French daily-block parsing and missing markers, invalid input failures, newest official daily q5 link selection, HXZ source checksum, and repeated offline CLI runs.

Exact Verify commands:

```sh
uv run python3 -m rebal.fetch.french && uv run python3 -m rebal.fetch.hxz
uv run pytest -q tests/test_fetch_factors.py
ls data/public/french data/public/hxz docs/data/cards/
```

The block ran with `set -e` and exited **0**. Output below uses repository-relative paths in place of the worktree prefix:

```text
OK data/public/french/F-F_Research_Data_Factors_daily_CSV.zip rows=26317 first=1926-07-01 last=2026-08-31
OK data/public/french/F-F_Research_Data_Factors_daily.csv rows=26317 first=1926-07-01 last=2026-08-31
OK data/public/french/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip rows=15897 first=1963-07-01 last=2026-08-31
OK data/public/french/F-F_Research_Data_5_Factors_2x3_daily.csv rows=15897 first=1963-07-01 last=2026-08-31
OK data/public/french/F-F_Momentum_Factor_daily_CSV.zip rows=26216 first=1926-11-03 last=2026-08-31
OK data/public/french/F-F_Momentum_Factor_daily.csv rows=26216 first=1926-11-03 last=2026-08-31
OK data/public/french/F-F_ST_Reversal_Factor_daily_CSV.zip rows=26446 first=1926-01-26 last=2026-08-31
OK data/public/french/F-F_ST_Reversal_Factor_daily.csv rows=26446 first=1926-01-26 last=2026-08-31
OK data/public/french/F-F_LT_Reversal_Factor_daily_CSV.zip rows=25216 first=1930-03-20 last=2026-08-31
OK data/public/french/F-F_LT_Reversal_Factor_daily.csv rows=25216 first=1930-03-20 last=2026-08-31
OK data/public/hxz/q5_factors_daily.raw.csv rows=14848 first=1967-01-03 last=2025-12-31
OK data/public/hxz/q5_factors_daily.csv rows=14848 first=1967-01-03 last=2025-12-31
..............................                                           [100%]
30 passed in 2.72s
data/public/french:
F-F_LT_Reversal_Factor_daily.csv
F-F_LT_Reversal_Factor_daily_CSV.zip
F-F_Momentum_Factor_daily.csv
F-F_Momentum_Factor_daily_CSV.zip
F-F_Research_Data_5_Factors_2x3_daily.csv
F-F_Research_Data_5_Factors_2x3_daily_CSV.zip
F-F_Research_Data_Factors_daily.csv
F-F_Research_Data_Factors_daily_CSV.zip
F-F_ST_Reversal_Factor_daily.csv
F-F_ST_Reversal_Factor_daily_CSV.zip

data/public/hxz:
q5_factors_daily.csv
q5_factors_daily.raw.csv
source.json

docs/data/cards/:
TEMPLATE.md
crsp.md
fred.md
french.md
gsw.md
hpw.md
hxz.md
ofr.md
Verify exit=0
```

Additional local verification after rebasing onto `origin/main`:

- `uv run pytest -q`: **75 passed in 6.97s**.
- `uv run --with ruff ruff check src/rebal/fetch/french.py src/rebal/fetch/hxz.py tests/test_fetch_factors.py`: **All checks passed!**
- `uv run --with ruff ruff format --check src/rebal/fetch/french.py src/rebal/fetch/hxz.py tests/test_fetch_factors.py`: **3 files already formatted**.
- Both fetcher `--help` commands exited 0.
- Code, tests and cards passed `git diff --check`. The raw HXZ CSV retains the publisher's CRLF line endings; these bytes are intentionally unchanged.

## Summary

Added `rebal.fetch.french` and `rebal.fetch.hxz`, using the shared `download`, `summarize`, storage paths and existing small daily-file validation helpers. French stores all five official ZIP archives and parses only daily records into matching CSVs. HXZ discovers the newest official daily q5 year from the factors page, stores the original CSV and tidy CSV, and writes URL/timestamp/SHA-256 metadata. Public data files are each under 1 MB, below the 20 MB cap.

Full histories and original percent units are retained. No return scaling, interpolation, panel construction or market-return construction occurs. HXZ keeps the published `R_F`, `R_MKT`, `R_ME`, `R_IA`, `R_ROE`, `R_EG` names; the card maps these to the factor names. French keeps both Mkt-RF and RF, which TASK-012 can use to construct the D16 total return. The newest listed HXZ daily file is `q5_factors_daily_2025.csv`; no mirror or material decision was needed.

Deviations: none. No cluster jobs ran. No task specs, other task outcomes, decisions, goal configuration or master source map were edited. Current source vintages can revise historical returns; this limitation is recorded in both cards.

Verified implementation revision: `606e87fdc1a83f092b682e4133c8e8249e67fcb3`, after a conflict-free rebase onto `origin/main`. This follow-up commit records the outcome and refreshed HXZ download timestamp; the downloaded source values and checksum remain the same.

PR: https://github.com/jesusvillota/replicate/pull/17, into `main`, with `Goal-Task: hmm-rebalancing/TASK-005` and label `goal:hmm-rebalancing`. Local Verify determines delivery; GitHub Actions were not read or used. The worker marks this PR ready after committing this outcome and never merges it.

Proposed follow-ups: none beyond the existing TASK-012 unit conversion, source-map update and panel assembly.
