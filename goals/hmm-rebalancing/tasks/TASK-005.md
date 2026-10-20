---
id: TASK-005
title: Fetch French and HXZ factor libraries
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2. Factor returns (D24) are needed for the alphas in Table 6B. The French market return (D16) is needed for the long sample in Table 4. See paper-notes §2, §3.6 and §3.9.

## Scope

No cluster jobs in this task. Runs on the MacBook.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

Fetchers (public, committed):

1. **`rebal.fetch.french`:** daily files from the Kenneth French data library (`https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/<name>_CSV.zip`):
   - `F-F_Research_Data_Factors_daily`: Mkt-RF, SMB, HML and RF, from 1926;
   - `F-F_Research_Data_5_Factors_2x3_daily`;
   - `F-F_Momentum_Factor_daily`;
   - `F-F_ST_Reversal_Factor_daily`;
   - `F-F_LT_Reversal_Factor_daily`.

   Parse only the daily block of each file. Store tidy CSVs under `data/public/french/` in the original units (percent).
2. **`rebal.fetch.hxz`:** the Hou–Xue–Zhang q5 factors, daily (MKT, ME, IA, ROE, EG), from global-q.org. Use the newest daily file listed on the factors page. Store under `data/public/hxz/`, in the original units.

Out of scope: unit conversion to decimals (TASK-012).

## Acceptance

- Both fetchers print `OK` lines.
- The French 3-factor daily file covers 1961-06-16 to 2023-03-17.
- The 5-factor, momentum and HXZ files cover 1997-09-10 to 2023-03-17.
- `docs/data/cards/french.md` and `docs/data/cards/hxz.md` exist.
- `uv run pytest tests/test_fetch_factors.py` passes.

## Verify

```sh
uv run python3 -m rebal.fetch.french && uv run python3 -m rebal.fetch.hxz
uv run pytest -q tests/test_fetch_factors.py
ls data/public/french data/public/hxz docs/data/cards/
```
