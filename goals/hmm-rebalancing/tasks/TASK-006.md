---
id: TASK-006
title: Fetch public futures and index price series
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2. These series feed several parts of the plan (paper-notes §2):
- **ES and TY benchmarks:** public futures series, used to judge the ES/TY proxies (D1, D2; used in TASK-011).
- **D4:** S&P 500 total return.
- **D6:** MSCI ACWI ex USA.
- **D9:** MOVE.
- **D18:** the Russell price indices, as a check on the CRSP ETF proxies.

## Scope

No cluster jobs in this task. Runs on the MacBook.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

These sources have terms of use, so store every file under `licensed_dir(<source>)` and never commit it.

1. **`rebal.fetch.yahoo`:** use `yfinance` with `auto_adjust=False`, so the raw Close and Adj Close are both kept.
   - Tickers: `ES=F`, `ZN=F`, `^GSPC`, `^SP500TR`, `^MOVE`, `^VIX`, `^RUI`, `^RUT`, `^RLV`, `^RLG`.
   - Daily, full history.
   - Output: one CSV per ticker in `licensed_dir("yahoo")`.
   - Retry with backoff on rate limits.
   - The card must note that `ES=F` and `ZN=F` are front-month series without roll adjustment, so returns across a roll date are wrong. Give their first dates. TASK-011 handles the rolls.
2. **`rebal.fetch.msci`:** the MSCI ACWI ex USA index, Net Total Return, USD, daily, from 1997 on. MSCI's code for this index is believed to be 991000; verify it.
   - Use MSCI's public end-of-day index data service (msci.com "End of day index data search").
   - Output: `licensed_dir("msci")/acwi_ex_usa_net_usd.csv`.
   - If MSCI offers no daily history before some date, record the coverage. Its proxy is the CRSP ETFs from TASK-009.

Out of scope: return calculation, roll correction and proxy choice (TASK-011, TASK-012).

## Acceptance

- `rebal.fetch.yahoo` prints one `OK` line per ticker. `^SP500TR` covers 1997-09-10 to 2023-03-17. `ES=F` and `ZN=F` start no later than 2001.
- `^MOVE` coverage is printed and recorded in `docs/data/cards/yahoo.md`. State whether it covers 1997-09-10.
- `rebal.fetch.msci` prints an `OK` line with its coverage, or `docs/data/cards/msci.md` explains why it is unavailable.
- `git status --porcelain` shows no data file under `data/`.

## Verify

```sh
uv run python3 -m rebal.fetch.yahoo
uv run python3 -m rebal.fetch.msci || echo "msci unavailable, see card"
grep -H -A3 -i 'coverage' docs/data/cards/yahoo.md docs/data/cards/msci.md
git status --porcelain
```
