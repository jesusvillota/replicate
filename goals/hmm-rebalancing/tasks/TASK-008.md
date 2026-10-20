---
id: TASK-008
title: Fetch ICI fund flows and CRR pension allocations
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1, and SC-6 later. Two exhibits need these sources (paper-notes §2):
- **Figure 5** uses ICI weekly fund flows, equity minus bond (D22).
- **Figure 1** uses the Public Plans Data (PPD) from the Center for Retirement Research at Boston College (CRR): DB pension actual and target allocations (D23).

## Scope

No cluster jobs in this task. Runs on the MacBook.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

1. **`rebal.fetch.ici`:** ICI "Estimated Long-Term Mutual Fund Flows", weekly, from January 2007 to latest.
   - Columns: total equity, domestic equity, world equity, hybrid, taxable bond, municipal bond and total, in millions of dollars.
   - ICI posts recent years on its statistics page. Get older weekly history from the archived files (Wayback Machine if needed).
   - Store the original files plus a tidy `ici_weekly_flows.csv` under `licensed_dir("ici")`, because ICI's terms are unclear.
   - The card must give the coverage you achieved and any gaps.
2. **`rebal.fetch.ppd`:** the CRR Public Plans Data full dataset, from publicplansdata.org.
   - Keep the plan ID, plan name, fiscal year, total assets, and the actual and target allocations for equity (domestic, international, total), fixed income and cash. Record the variable names you used.
   - Store it under `data/public/ppd/` (public data; cite CRR in the card).
   - If the full file is over 20 MB, keep only the needed columns.

Out of scope: building Figure 1 or the flow measure (M-3).

## Acceptance

- `rebal.fetch.ici` prints an `OK` line. The coverage in `docs/data/cards/ici.md` starts on or before 2007-01-31, or the card explains the gap.
- `rebal.fetch.ppd` prints an `OK` line covering fiscal years 2003–2022.
- `docs/data/cards/ppd.md` lists the allocation variable names you used.

## Verify

```sh
uv run python3 -m rebal.fetch.ici && uv run python3 -m rebal.fetch.ppd
grep -H -A4 -i 'coverage' docs/data/cards/ici.md docs/data/cards/ppd.md
```
