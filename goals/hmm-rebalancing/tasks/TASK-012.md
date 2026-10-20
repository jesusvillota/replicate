---
id: TASK-012
title: Build the daily panel and finalize the data source map
milestone: M-1
state: approved
depends_on: [TASK-004, TASK-005, TASK-007, TASK-008, DEC-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2, and is the exit of M-1. This task:
- builds the one daily panel that every analysis reads, per `docs/contracts/daily_panel.md`, using the proxies accepted in DEC-001;
- turns `docs/data/sources.md` into the final record of what the paper needs, the authors' source, and the source we actually use.

## Scope

No cluster jobs in this task. Runs on the MacBook. Inputs:
- the merged fetch outputs and their cards (`docs/data/cards/*.md`);
- `docs/data/proxy_comparison.md`;
- `src/rebal/proxies.py`;
- the accepted DEC-001 (`goals/hmm-rebalancing/decisions/DEC-001.md`).

**1. Builder.** Write `src/rebal/panel.py`.

`--build` writes `processed_dir()/daily_panel.parquet`, with exactly the contract columns. Rules:
- **`r_es`, `r_ty`:** the DEC-001 main pair, built with the `rebal.proxies` functions. Also write the robustness pair to `processed_dir()/daily_panel_alt.parquet` (the same columns; only `r_es` and `r_ty` differ).
- **Calendar:**
  - The trading days are the days where both `r_es` and `r_ty` exist.
  - Drop 2001-09-11 to 2001-09-14 (paper-notes §2, D3).
  - The panel starts at the earliest common date, for the burn-in (paper-notes §5.3), and ends at the latest common date.
- **Rates:**
  - `rf` = French RF / 100.
  - `rf_3m` = DTB3 as a daily return: (DTB3 / 100) × (calendar days to the next trading day) / 360.
- **Controls:**
  - `vix` = VIXCLS / 100.
  - `move` = `^MOVE` / 100. If `^MOVE` starts after 1997-09-10, leave the gap as NaN and record it.
  - `epu`, `ads`, `sentiment`, `ra_bex`, `unc_bex`, `ara` keep their published units. Record their scaling in `docs/methods/panel.md`.
  - `liquidity`: HPW noise if it covers 1997–2023, else OFR FSI Funding. Record which one you used.
  - `ivol` from CRSP dispersion.
  - Controls may be forward-filled for at most 5 trading days. Returns are never forward-filled.
- **Factors:** convert percent to decimals.
- **Indices** (simple daily returns):
  - `r_sp500tr` from `^SP500TR`.
  - `r_agg` from VBMFX (WRDS) if available, else AGG.
  - `r_acwxus` from MSCI if available, else the best CRSP ETF.
  - `r_r1k`, `r_r2k`, `r_r1kv`, `r_r1kg` from IWB, IWM, IWD, IWF.
  - `r_mkt_french` = (Mkt-RF + RF) / 100.
  - `r_10y_gsw` = the GSW 10-year zero-coupon return.

`--check` validates the panel and prints:
- schema and dtypes against the contract;
- that dates are sorted and unique;
- one line per column: first non-NaN date, last date, NaN share;
- the row count for 1997-09-10 to 2023-03-17;
- a final `PANEL OK` line.

It exits non-zero if any check fails.

**2. Methods doc.** `docs/methods/panel.md`: each transform and each choice above, with the reason.

**3. Final source map.** Update every row of `docs/data/sources.md` from the cards:
- "Our source": the exact series and URL or table;
- "Exact or proxy";
- "Storage": the path;
- "Status": one of `available`, `partial (<coverage>)` or `not available (<reason>)`;
- a link to the card.

The D1 and D2 rows must name the DEC-001 choice and the robustness pair.

**4. Tests.** `tests/test_panel.py` checks the transforms on small synthetic inputs:
- the `rf_3m` conversion;
- the 5-day forward-fill limit;
- that returns are not forward-filled;
- the 9/11 drop.

Out of scope: signals and regressions; weekly CFTC/ICI and annual PPD processing (M-3).

## Acceptance

- `uv run python3 -m rebal.panel --build && uv run python3 -m rebal.panel --check` ends with `PANEL OK`.
- The check output shows coverage of 1997-09-10 to 2023-03-17 for `r_es`, `r_ty`, `rf`, `vix`, `epu`, `ads`, `sentiment` and the factors.
- The row count for that window is printed. The outcome compares it with the paper's N (6,226 for regressions; about 6,473 days in total; paper-notes §5.3).
- `grep -cE '^\| D[0-9]+ ' docs/data/sources.md` prints 28, and `grep -cE '\| planned \|' docs/data/sources.md` prints 0.
- `uv run pytest tests/test_panel.py` passes.

## Verify

```sh
uv run python3 -m rebal.panel --build && uv run python3 -m rebal.panel --check
grep -cE '^\| D[0-9]+ ' docs/data/sources.md; grep -cE '\| planned \|' docs/data/sources.md
uv run pytest -q tests/test_panel.py
```
