---
id: TASK-003
title: Fetch Fed, FRED and OFR rate, volatility and stress series
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2. These series supply the following (paper-notes §2):
- the cash rate (D7);
- VIX (D8);
- the GSW yield curve, used for the TY proxy candidates and the long sample (D2, D17);
- the liquidity-stress proxy for BofA GFSI Liquidity (D26).

## Scope

No cluster jobs in this task. Runs on the MacBook; each download takes seconds.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

Fetchers and outputs (all public, committed under `data/public/`):

1. **`rebal.fetch.fred`:** FRED series `DTB3`, `DGS10` and `VIXCLS`. Use `https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>`, which needs no API key. Output: `data/public/fred/<ID>.csv`, from each series' start to latest. FRED's missing marker is "."; parse it as NaN.
2. **`rebal.fetch.gsw`:** the Fed GSW yield-curve file (`https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv`). Skip the header notes.
   - Output: `data/public/gsw/feds200628.csv`, keeping these columns: `SVENY01`–`SVENY30`, `SVENPY01`–`SVENPY30`, `BETA0`–`BETA3`, `TAU1`, `TAU2`.
   - The file must stay under 20 MB. If it would not, drop the `SVENPY` columns above 10 years.
3. **`rebal.fetch.ofr`:** the OFR Financial Stress Index with all category columns (`https://www.financialresearch.gov/financial-stress-index/`, CSV download). Output: `data/public/ofr/fsi.csv`.
4. **`rebal.fetch.hpw`:** the Hu–Pan–Wang (2013) daily Treasury "noise" illiquidity measure, from Jun Pan's data page.
   - Output: `data/public/hpw/noise.csv`.
   - The HPW license may not allow redistribution. If so, store the file under `licensed_dir("hpw")` instead, and say so in the card.

The liquidity proxy for D26 is chosen in TASK-012:
- First choice: HPW noise, because it is daily from 1987.
- Fallback: the OFR FSI "Funding" category, which starts in 2000.

Your cards must give the coverage of both, so TASK-012 can choose.

Out of scope: unit conversion, and building the TY proxy.

## Acceptance

- Running the four fetchers prints one `OK` line per file.
- Coverage:
  - DTB3, VIXCLS and GSW cover 1997-09-10 to 2023-03-17.
  - GSW has a 10-year yield from about 1971 on.
  - The OFR and HPW coverage is printed and recorded in their cards.
- `ls docs/data/cards/` shows `fred.md`, `gsw.md`, `ofr.md` and `hpw.md`.
- `uv run pytest tests/test_fetch_rates.py` passes. The test checks columns and coverage of the stored files.

## Verify

```sh
for m in fred gsw ofr hpw; do uv run python3 -m rebal.fetch.$m || echo "FAILED $m"; done
uv run pytest -q tests/test_fetch_rates.py
ls docs/data/cards/ data/public/*/
```
