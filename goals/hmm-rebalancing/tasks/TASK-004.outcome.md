# TASK-004 outcome

## Acceptance

- [x] `epu`, `ads` and `sentiment` print `OK` lines covering 1997-09-10 through 2023-03-17. Exact Verify output below: EPU 1985-01-01–2026-10-20 (15,268 rows), ADS 1960-03-01–2026-10-10 (24,330 rows), sentiment 1980-01-01–2026-10-18 (17,074 rows). Tests also require observed values on both required endpoints and exact agreement with unchanged raw downloads.
- [x] `bex` prints `OK`: 1986-05-30–2026-09-30, 10,073 rows, both `ra` and `unc`. Raw workbook and tidy CSV are outside git under `licensed_dir("bex")`.
- [x] All six cards exist with a `Status:` line: `epu.md`, `ads.md`, `sentiment.md`, `bex.md`, `ara.md`, `fears.md`. The exact `grep -H '^Status'` output is below. All have available data; FEARS explicitly limits availability to its archived public subset.
- [x] `uv run pytest -q tests/test_fetch_uncertainty.py`: **23 passed in 2.15s**. The complete task Verify block exited **0** on 2026-10-21.

## Summary

Implemented six independent CLI fetchers using `rebal.fetch.common.download` and `summarize`. They validate date uniqueness, source columns, numerical values and source-specific coverage. They retain original units and published gaps. Public EPU, latest-vintage ADS and SF Fed sentiment raw files plus tidy CSVs are committed. BEX, ARA and FEARS raw and tidy files stay under `licensed_dir`, outside git.

Extended `summarize` to accept separate year/month/day fields and a CSV member within a ZIP. Existing CSV, Excel and parquet behavior is preserved. Dropbox requires `raw=1` for ARA; `dl=1` serves HTML with the helper's user agent. The ARA ZIP preserves the authors' README. BEX resolves the current workbook link from Nancy Xu's page instead of freezing an old vintage.

Source research found public ARA data (2004-07-01–2019-12-31, 3,903 rows) on Lin Peng's author page. It also found a Wayback copy of public FEARS data (2004-07-01–2011-12-30, 1,891 rows). The paper's privately supplied FEARS extension remains unavailable. This is a documented public subset, not a substitute for the paper's full FEARS column. No material decision is required.

Verified implementation revision: `cecadd0c630d198810a57cb53632c420116a31aa`, after a conflict-free rebase onto `origin/main`. This outcome commit adds documentation only. The task remains on `goal/hmm-rebalancing/task-004`; the PR targets `main` and carries `goal:hmm-rebalancing`. No task specs, other task outcomes, decisions, `goal.yaml` or source master map changed.

Additional local verification: all six `--help` commands exit 0; Ruff passes on every changed Python file; `git diff --check` passes; `uv run pytest -q tests/test_fetch_uncertainty.py tests/test_scaffold.py` reports **43 passed in 4.46s** before the rebase. The standalone FEARS fetch printed two `OK` lines with its public coverage. GitHub Actions were not read or used.

Follow-up for TASK-012: use the documented original units, latest-vintage ADS caveat and supplied dates. ARA ends in 2019; the complete private FEARS series is unavailable. No fabricated, interpolated or forward-filled observations were added here.

## Verify evidence

The exact task Verify commands were run as a shell script, with exit status **0**:

```sh
for m in epu ads sentiment bex; do uv run python3 -m rebal.fetch.$m || echo "FAILED $m"; done
test -f src/rebal/fetch/ara.py && uv run python3 -m rebal.fetch.ara
grep -H '^Status' docs/data/cards/{epu,ads,sentiment,bex,ara,fears}.md
uv run pytest -q tests/test_fetch_uncertainty.py
```

```text
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/epu/All_Daily_Policy_Data.raw.csv rows=15268 first=1985-01-01 last=2026-10-20
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/epu/epu.csv rows=15268 first=1985-01-01 last=2026-10-20
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/ads/ADS_Index_Most_Current_Vintage.xlsx rows=24330 first=1960-03-01 last=2026-10-10
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/ads/ads.csv rows=24330 first=1960-03-01 last=2026-10-10
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/sentiment/news_sentiment_data.xlsx rows=17074 first=1980-01-01 last=2026-10-18
OK /Users/jesusvillotamiranda/orca/workspaces/replicate/goal-hmm-rebalancing-task-004/data/public/sentiment/sentiment.csv rows=17074 first=1980-01-01 last=2026-10-18
OK /Users/jesusvillotamiranda/data/replicate/licensed/bex/bex.raw.xlsx rows=10073 first=1986-05-30 last=2026-09-30
OK /Users/jesusvillotamiranda/data/replicate/licensed/bex/bex.csv rows=10073 first=1986-05-30 last=2026-09-30
OK /Users/jesusvillotamiranda/data/replicate/licensed/ara/ara.raw.zip rows=3903 first=2004-07-01 last=2019-12-31
OK /Users/jesusvillotamiranda/data/replicate/licensed/ara/ara.csv rows=3903 first=2004-07-01 last=2019-12-31
docs/data/cards/epu.md:Status: available
docs/data/cards/ads.md:Status: available
docs/data/cards/sentiment.md:Status: available
docs/data/cards/bex.md:Status: available
docs/data/cards/ara.md:Status: available
docs/data/cards/fears.md:Status: available (archived public 2004–2011 subset); paper's private extension not available
.......................                                                  [100%]
23 passed in 2.15s
```
