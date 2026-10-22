---
id: TASK-010
title: Inventory our WRDS libraries and extract WRDS series
milestone: M-1
state: approved
depends_on: [TASK-001, TASK-002, DEC-002]
delivery: pr
route: {platform: codex, model: gpt-6-astra, effort: high}
---

## Why

Serves SC-1 and SC-2. We do not yet know what our WRDS subscription includes. This task lists the libraries we can read. It then extracts the WRDS series the plan uses:
- the CRSP 10-year Treasury index, a candidate for D2;
- the VBMFX mutual-fund return, a proxy for D5;
- any futures, MSCI, Russell or ANcerno data that turns up (D1, D2, D6, D18, D21).

## Scope

No cluster jobs in this task. Runs on the MacBook only; never connect to WRDS from the cluster. It needs TASK-002: `wrds.Connection()` must work without a prompt.

**Code.** `src/rebal/fetch/wrds_extract.py`, with two modes.

**1. `--inventory`.** Call `db.list_libraries()`. For each library, try to list its tables. Write `docs/data/wrds_inventory.md`:
- every library we can access;
- a "Relevant to this replication" section that answers yes or no for each of these, with the library and table names:
  - futures prices: any library with daily settlements for E-mini S&P 500 or 10-year T-note futures, such as a Datastream or Refinitiv futures library;
  - CRSP Treasuries (`crsp.tfz_dly_ft` / `crsp.tfz_idx`);
  - CRSP Mutual Funds (`crsp.fund_hdr`, `crsp.daily_returns` or the current table names);
  - CRSP index files (`crsp.dsp500`, `crsp.dsi`);
  - MSCI index data;
  - Russell / FTSE index data;
  - ANcerno (Abel Noser);
  - Fama–French factors.

**2. `--extract`.** Store all output under `licensed_dir("wrds")`, never committed:
- `treasury_fixed_term.parquet`: the CRSP daily fixed-term Treasury index returns for the 5-, 7-, 10- and 20-year terms, 1961 to latest. Record the index IDs.
- `bond_fund_daily.parquet`: daily total returns of VBMFX and VBTLX (Vanguard Total Bond Market Index). Find their fund numbers through the fund header by ticker and date.
- If a futures library exists: `futures_es_ty.parquet`, with daily settlement prices of the front and second ES and TY contracts, 1997 to latest. Include the contract month and expiry, so TASK-011 can roll at the end of the month before expiry, as the paper does (paper-notes §3.1).
- If ANcerno, MSCI or Russell data exists, do not extract it. Record it in the inventory for the M-3 planner.

Write `docs/data/cards/wrds.md` with the exact table names, filters and coverage.

**Test.** `tests/test_wrds_extract.py` checks the parsing helpers offline, with no WRDS connection.

Out of scope: proxy comparison (TASK-011).

## Acceptance

- `docs/data/wrds_inventory.md` exists. It lists at least one library and has the "Relevant to this replication" section with a yes or no for each item.
- `--extract` prints an `OK` line for each file it writes. `treasury_fixed_term.parquet` covers 1997-09-10 to 2023-03-17, or the card states that CRSP Treasuries are not in our subscription.
- `git status --porcelain` lists no data file.
- `uv run pytest tests/test_wrds_extract.py` passes.

## Verify

```sh
uv run python3 -m rebal.fetch.wrds_extract --inventory
uv run python3 -m rebal.fetch.wrds_extract --extract
sed -n '/Relevant to this replication/,$p' docs/data/wrds_inventory.md
uv run pytest -q tests/test_wrds_extract.py
git status --porcelain
```
