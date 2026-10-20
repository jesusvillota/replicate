---
id: TASK-004
title: Fetch uncertainty and sentiment indices
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2. Table 1 uses EPU, ADS and Sentiment as control variables (D10–D12). Table D.9 uses BEX, FEARS and ARA (D13–D15). See paper-notes §2 and §4.

## Scope

No cluster jobs in this task. Runs on the MacBook.

Follow "Shared conventions" in `goals/hmm-rebalancing/README.md`. Use `rebal.fetch.common.download` and `summarize`. Write one source card per source in `docs/data/cards/<source>.md` (template: `docs/data/cards/TEMPLATE.md`). Do not edit `docs/data/sources.md`; TASK-012 updates it from your cards. Store raw files exactly as published, plus a tidy CSV (`date` + series columns, original units). Unit conversions belong to TASK-012. If a URL has moved, find the official new location. If a source is gone, try the Wayback Machine (web.archive.org) and record that in the card. Never fabricate or interpolate data. If a source is unobtainable, write a card with "Status: not available" and the reason, and report it in the outcome.

Fetchers:

1. **`rebal.fetch.epu`:** the U.S. daily news-based Economic Policy Uncertainty index, from policyuncertainty.com (the "US Daily News Index" CSV). Public; store under `data/public/epu/`.
2. **`rebal.fetch.ads`:** the Aruoba–Diebold–Scotti index, most recent vintage, from the Philadelphia Fed ADS page. Public; store under `data/public/ads/`. The card must say we use the latest vintage, not a real-time vintage.
3. **`rebal.fetch.sentiment`:** the SF Fed Daily News Sentiment Index (Shapiro, Sudhof and Wilson). Public; store under `data/public/sentiment/`.
4. **`rebal.fetch.bex`:** the Bekaert–Engstrom–Xu daily risk aversion (`ra`) and uncertainty (`unc`) indices, from the authors' public data page (Nancy Xu's website). Store under `licensed_dir("bex")`, because its redistribution terms are unclear.
5. **ARA:** aggregate retail attention (Da, Hua, Hung and Peng, 2025). Search the authors' pages and the journal's online appendix.
   - If you find a public daily file, write `rebal.fetch.ara` and store it under `licensed_dir("ara")`.
   - Otherwise, write only `docs/data/cards/ara.md` with "Status: not available".
6. **FEARS:** the authors got it privately (paper footnote 23).
   - Check Zhi Da's website and the publisher's online appendix for a public file. If one exists, fetch it as for ARA.
   - Otherwise, write only `docs/data/cards/fears.md` with "Status: not available".

Out of scope: MOVE (TASK-006), scaling, and forward-filling (TASK-012).

## Acceptance

- `epu`, `ads` and `sentiment` print `OK` lines whose coverage includes 1997-09-10 to 2023-03-17.
- `bex` prints an `OK` line with its coverage, or its card explains why it is unavailable.
- `docs/data/cards/` has `epu.md`, `ads.md`, `sentiment.md`, `bex.md`, `ara.md` and `fears.md`. Each has a Status line.
- `uv run pytest tests/test_fetch_uncertainty.py` passes.

## Verify

```sh
for m in epu ads sentiment bex; do uv run python3 -m rebal.fetch.$m || echo "FAILED $m"; done
test -f src/rebal/fetch/ara.py && uv run python3 -m rebal.fetch.ara
grep -H '^Status' docs/data/cards/{epu,ads,sentiment,bex,ara,fears}.md
uv run pytest -q tests/test_fetch_uncertainty.py
```
