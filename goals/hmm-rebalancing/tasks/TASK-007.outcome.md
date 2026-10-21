# TASK-007 outcome

## Acceptance

- [x] `rebal.fetch.cftc` prints `OK` for `cot_legacy.csv` and `tff.csv`. The required default Verify run exited 0: legacy has 4,316 rows, 1997-01-07–2026-10-13; TFF has 2,882 rows, 2006-06-13–2026-10-13. Both include every required year through 2023. A separate `--end-year 2023` run exited 0 with 4,024 legacy rows and 2,590 TFF rows, both ending 2023-12-26.
- [x] The same Verify run prints `OK` for `ltpos.csv`: 750 rows, 2009-01-09–2011-05-27. The first period starts 2009-01-05. All six equity-index and Treasury markets have 125 periods. The official CSV was recovered from the CFTC's Net Position Changes page; no unavailable-data fallback was needed.
- [x] `du -h data/public/cftc/*` exits 0. Every file is below 20 MB. The largest is `cot_legacy.csv` at 5.0M; `tff.csv` is 3.0M and `ltpos.csv` is 132K. The local size test checks every raw and tidy file against 20,000,000 bytes.

## Summary

Added `rebal.fetch.cftc`, original ZIPs and LTPos CSV, tidy data, a SHA-256 manifest, and `docs/data/cards/cftc.md`. Legacy and TFF preserve all published columns for codes `043602`, `138741`, and `13874A`. Added text market keys preserve leading zeros. Header whitespace is normalized; all original headers remain in the ZIPs. Extended shared `summarize` with optional series keys so multiple markets can share a date, while duplicate market/date pairs fail.

LTPos keeps the published buys and sells for dealers, asset managers, leveraged funds, and other reportables. Its signed changes are buys minus sells, in contracts per day. The source aggregate and volume remain separate. The card explains the source aggregate's different definition and links the archived explanatory notes. Legacy supports commercial/non-commercial classification; TFF and LTPos support asset-manager/leveraged-fund classification.

Deviation: use annual legacy files for early years. The redundant 1986–2016 ZIP is 22,917,634 bytes, above the per-file limit. The annual originals supply all required years without altering or splitting source files. Raw downloads retain every published market; only tidy files are filtered. The full-size S&P history stops at 2021-09-14; source reporting gaps are preserved and documented.

Verified implementation revision: `7e18960aec7e7444060c4b520b6e4d7b2e2b1367`, after a conflict-free rebase onto `origin/main`. The worktree was clean after Verify. This outcome is a documentation-only follow-up commit. Branch: `goal/hmm-rebalancing/task-007`. PR: https://github.com/jesusvillota/replicate/pull/20, into `main`, with marker `Goal-Task: hmm-rebalancing/TASK-007` and label `goal:hmm-rebalancing`.

Local validation:

- Exact task Verify block: exit 0; output below.
- `uv run pytest -q`: **105 passed in 17.84s**.
- `uv run --with ruff ruff check src/rebal/fetch/cftc.py src/rebal/fetch/common.py tests/test_fetch_cftc.py`: **All checks passed!**
- Corresponding `ruff format --check`: **3 files already formatted**.
- `uv run python3 -m rebal.fetch.cftc --help`: exit 0.
- `git diff --check`: exit 0. A default rerun reproduced the committed outputs without changes.

No cluster jobs ran. GitHub Actions were not read or used. No Q measure, correlation, or panel construction was added. Proposed follow-ups: existing TASK-012 consumes the documented source fields and units. No new decision is required.

## Verify output

The three commands from the task's Verify block ran sequentially with `set -e` and exited 0:

```text
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-007/data/public/cftc/cot_legacy.csv rows=4316 first=1997-01-07 last=2026-10-13
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-007/data/public/cftc/tff.csv rows=2882 first=2006-06-13 last=2026-10-13
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-007/data/public/cftc/ltpos.csv rows=750 first=2009-01-09 last=2011-05-27
5.0M	data/public/cftc/cot_legacy.csv
844K	data/public/cftc/deacot1997.zip
864K	data/public/cftc/deacot1998.zip
844K	data/public/cftc/deacot1999.zip
592K	data/public/cftc/deacot2000.zip
532K	data/public/cftc/deacot2001.zip
544K	data/public/cftc/deacot2002.zip
588K	data/public/cftc/deacot2003.zip
636K	data/public/cftc/deacot2004.zip
704K	data/public/cftc/deacot2005.zip
852K	data/public/cftc/deacot2006.zip
848K	data/public/cftc/deacot2007.zip
876K	data/public/cftc/deacot2008.zip
940K	data/public/cftc/deacot2009.zip
1.0M	data/public/cftc/deacot2010.zip
1.0M	data/public/cftc/deacot2011.zip
1.1M	data/public/cftc/deacot2012.zip
1.3M	data/public/cftc/deacot2013.zip
1.5M	data/public/cftc/deacot2014.zip
1.5M	data/public/cftc/deacot2015.zip
1.6M	data/public/cftc/deacot2016.zip
1.6M	data/public/cftc/deacot2017.zip
1.8M	data/public/cftc/deacot2018.zip
1.8M	data/public/cftc/deacot2019.zip
1.8M	data/public/cftc/deacot2020.zip
1.8M	data/public/cftc/deacot2021.zip
1.9M	data/public/cftc/deacot2022.zip
2.0M	data/public/cftc/deacot2023.zip
2.2M	data/public/cftc/deacot2024.zip
2.3M	data/public/cftc/deacot2025.zip
1.9M	data/public/cftc/deacot2026.zip
3.0M	data/public/cftc/fin_fut_txt_2006_2016.zip
388K	data/public/cftc/fut_fin_txt_2017.zip
448K	data/public/cftc/fut_fin_txt_2018.zip
448K	data/public/cftc/fut_fin_txt_2019.zip
424K	data/public/cftc/fut_fin_txt_2020.zip
456K	data/public/cftc/fut_fin_txt_2021.zip
484K	data/public/cftc/fut_fin_txt_2022.zip
496K	data/public/cftc/fut_fin_txt_2023.zip
552K	data/public/cftc/fut_fin_txt_2024.zip
616K	data/public/cftc/fut_fin_txt_2025.zip
568K	data/public/cftc/fut_fin_txt_2026.zip
388K	data/public/cftc/lgtraderpos-csv.csv
132K	data/public/cftc/ltpos.csv
 12K	data/public/cftc/manifest.json
3.0M	data/public/cftc/tff.csv
         date market_code                          Market_and_Exchange_Names
0  2006-06-13      043602  10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF...
1  2006-06-13      138741  S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE
2  2006-06-13      13874A  E-MINI S&P 500 STOCK INDEX - CHICAGO MERCANTIL...
3  2006-06-20      043602  10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF...
4  2006-06-20      138741  S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE
5  2006-06-20      13874A  E-MINI S&P 500 STOCK INDEX - CHICAGO MERCANTIL...
6  2006-06-27      043602  10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF...
7  2006-06-27      138741  S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE
8  2006-06-27      13874A  E-MINI S&P 500 STOCK INDEX - CHICAGO MERCANTIL...
9  2006-07-03      043602  10-YEAR U.S. TREASURY NOTES - CHICAGO BOARD OF...
```
