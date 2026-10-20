---
id: TASK-007
title: Fetch CFTC positioning data
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1, and SC-6 later. Figure 5 relates the signals to trader positions from two CFTC sources (paper-notes §2 and §3.7):
- the CFTC Commitments of Traders (COT) reports (D19);
- the one-time Large Trader Net Position Changes (LTPos) report (D20).

## Scope

No cluster jobs in this task. Runs on the MacBook.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

`rebal.fetch.cftc`. CFTC data is public, so commit it under `data/public/cftc/`. Keep only the markets below, but keep all columns of those rows:

1. **Legacy COT, futures only:** the yearly history archives `https://www.cftc.gov/files/dea/history/deacot<YYYY>.zip`, plus the multi-year archive for the early years. Cover 1997 to latest. Markets:
   - S&P 500 Stock Index (CME, code 138741);
   - E-mini S&P 500 (13874A);
   - 10-Year U.S. Treasury Notes (CBOT, 043602).

   Verify the codes in the files. Output: `cot_legacy.csv`.
2. **Traders in Financial Futures (TFF), futures only:** `fut_fin_txt_<YYYY>.zip` and the 2006–2016 archive. Cover 2006 to latest, for the same markets. Output: `tff.csv`.
3. **LTPos:** the one-time CFTC report of June 30, 2011, "Large Trader Net Position Changes", covering January 2009 to May 2011. Find it on cftc.gov, or in the Wayback Machine.
   - Store the original files.
   - Store a tidy CSV, `ltpos.csv`, with one row per market and period, holding the net position change of dealers, asset managers, leveraged funds and other reportables.
   - Keep the equity-index and Treasury markets only.

The card must state which report supports the "commercial / non-commercial" split used by the paper (legacy) and which supports the "asset managers / leveraged funds" split (TFF, LTPos).

Out of scope: building the Q measure or any correlation (M-3).

## Acceptance

- `rebal.fetch.cftc` prints `OK` lines for `cot_legacy.csv` and `tff.csv`. Legacy covers 1997–2023; TFF covers 2006-06 to 2023.
- It prints an `OK` line for `ltpos.csv` covering 2009–2011, or `docs/data/cards/cftc.md` says "LTPos: not available" and lists the URLs tried.
- Each file in `data/public/cftc/` is under 20 MB (shown by `du -h`).

## Verify

```sh
uv run python3 -m rebal.fetch.cftc
du -h data/public/cftc/*
uv run python3 -c "import pandas as pd; d=pd.read_csv('data/public/cftc/tff.csv'); print(d.iloc[:,:3].drop_duplicates().head(10))"
```
