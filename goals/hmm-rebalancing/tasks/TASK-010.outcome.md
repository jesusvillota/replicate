# TASK-010 outcome

## Summary

Delivered with existing access under accepted DEC-002. Full CRSP Mutual Funds
access is unavailable and is no longer a blocker. The study period is unchanged.
Fresh `origin/main` TASK-010, TASK-012, DEC-002 and the worker protocol were read
before implementation. Base: `e4ca5ed2d31b0570c59757782b2edb0c9d2ff070`.

Added the WRDS inventory/extraction CLI and offline tests. Extracted the approved
2004–2006 sample outside git. Added a source-specific public Yahoo fund fetcher,
with distribution validation, original responses, lineage and offline tests.
The source card records Vanguard, Yahoo and Stooq attempts and the TASK-012 handoff.

VBMFX's public distribution-adjusted returns cover the full study. VBTLX starts
in 2001. The WRDS sample remains separate and clearly labelled. Earlier sample
rows retain fund IDs but have null dated tickers where header dates do not cover
them. No series was spliced, no return was filled, and no final proxy was selected.
TASK-012 owns panel integration; TASK-011/DEC-001 retain ES/TY choices.

Only this task's two fetch modules, two test files, inventory, source card and
outcome changed. No specs, other tasks, decisions, goal.yaml or source map changed.
No cluster jobs ran. No PR was merged. GitHub Actions were not read or used.

## Acceptance

1. [x] `docs/data/wrds_inventory.md` exists. The live `--inventory` command exited
   0 and printed `OK ... libraries=229`. Every library's table listing succeeded.
   The required `sed` command displayed all eight yes/no relevance rows.
   An independent assertion counted 229 library rows and eight relevance answers.
2. [x] `--extract` exited 0 and printed an `OK` line for each of its two files:
   `bond_fund_daily.parquet` and `bond_fund_daily.metadata.json`.
   The parquet has 1,510 rows, 2004-01-02–2006-12-29, 755 per fund, all marked
   `is_sample=true`. Of these, 502 lack a dated ticker match and are flagged.
   The source card explicitly states that CRSP Treasuries are not in our
   subscription. Both Treasury probes returned SQLSTATE `42501` for
   `crsp_a_treasuries`. No Treasury or unverified futures file was fabricated.
3. [x] `git status --porcelain` showed no data file. All WRDS and Yahoo artifacts
   are under `~/data/replicate/licensed/`; only task code, tests and documentation
   were present in status. `git diff --check` passed.
4. [x] `uv run pytest tests/test_wrds_extract.py`: **19 passed**.
   The exact quiet Verify command also passed: **19 passed**.
   Tests cover dated identities, ambiguous/overlapping headers, invalid returns,
   access-error classification, complete inventory answers, idempotent extraction
   and an `OK` line for every written WRDS file.
5. [x] The source card records provider and adjusted-price searches, their dates,
   exact routes, return definitions, access limits and coverage. The repeatable
   command `uv run python3 -m rebal.fetch.yahoo_bond_funds` exited 0 live.
   VBMFX: 10,041 price rows, 1986-12-11–2026-10-21; 6,422 nonmissing study returns,
   including 1997-09-10 and 2023-03-17. VBTLX: 6,275 price rows,
   2001-11-12–2026-10-21; first usable return 2001-11-13, 5,372 study returns.
   Both series passed full-history distribution checks at `1e-5` tolerance;
   observed maximum errors were `2.49483e-6` and `2.29863e-6` respectively.
   All **51 relevant offline tests** passed, including 12 public fund tests and
   the existing Yahoo/MSCI tests. The card recommends the available VBMFX
   candidate and documents AGG from TASK-009 as a fallback with its pre-2003 gap.

## Local verification

All TASK-010 Verify commands ran successfully:

```sh
uv run python3 -m rebal.fetch.wrds_extract --inventory
uv run python3 -m rebal.fetch.wrds_extract --extract
sed -n '/Relevant to this replication/,$p' docs/data/wrds_inventory.md
uv run pytest -q tests/test_wrds_extract.py
git status --porcelain
```

The complete local suite also passed: `uv run pytest -q` — **276 passed in 195.74s**.

Additional checks:

```sh
uv run pytest tests/test_wrds_extract.py
uv run pytest -q tests/test_wrds_extract.py tests/test_yahoo_bond_funds.py tests/test_fetch_prices.py
uv run python3 -m rebal.fetch.yahoo_bond_funds
uv run python3 -m rebal.fetch.yahoo_bond_funds --skip-existing
uv run python3 -m rebal.fetch.yahoo_bond_funds --list-remaining --shard 1/2
uv run --with ruff ruff check src/rebal/fetch/wrds_extract.py src/rebal/fetch/yahoo_bond_funds.py tests/test_wrds_extract.py tests/test_yahoo_bond_funds.py
uv run python3 -m rebal.fetch.wrds_extract --help
uv run python3 -m rebal.fetch.yahoo_bond_funds --help
git diff --check
```

All exited 0. Skip-existing validated both stored public series. The shard dry run
listed only VBMFX. Ruff printed `All checks passed!`. CLI help worked without WRDS.
A live compatibility failure in initial WRDS probes was fixed before the successful
Verify run: rollback now uses the underlying database connection.

## Remaining limits and handoff

Yahoo's returns include distributions but use its multiplicative adjustment and
rounded cash events. They are not exact official Vanguard NAV returns or the
paper's Bloomberg aggregate index. The source card documents this distinction.
Vanguard's accessible endpoint supplied only one year of daily NAV and ten years
of monthly NAV; its available distributions cannot reconstruct the study history.

No access decision remains open for this task. DEC-002 resolves the prior request.
No new task or decision is needed. TASK-012 should assess and document the public
VBMFX source for `r_agg`, keeping all missing dates explicit. AGG remains a shorter
broad bond-market fallback. Licensed files stay outside git and require regeneration
or a separate licensed-data transfer on another machine.

PR: https://github.com/jesusvillota/replicate/pull/25, base `main`.
There were no PR review threads, reviews or general comments when checked this session.
