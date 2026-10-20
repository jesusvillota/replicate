---
id: TASK-009
title: Extract CRSP ETF returns and daily stock dispersion on the cluster
milestone: M-1
state: approved
depends_on: [TASK-001]
delivery: pr
---

## Why

Serves SC-1 and SC-2. CRSP data from tape-kit supplies:
- the total-return ETF series used as proxies for D1, D2, D5, D6 and D18;
- the CRSP index returns;
- the daily cross-sectional return dispersion, `ivol` (D25), used in Table 6C.

See paper-notes §2 and the README's Data plan.

## Scope

This task writes the extraction code and runs it once on the cluster. Combining code and run is acceptable here: the job is one short DuckDB pass over yearly parquet files.

**Inputs.** Cluster, read-only:
- tape-kit CRSP CIZ research files: `/mnt/slurm-beegfs/Users/j-vill36/tape-kit-data/crsp/data/{daily,benchmarks}/YYYY.parquet`;
- security history: `/mnt/slurm-beegfs/Users/j-vill36/tape-kit-data/crsp/security_history/*.parquet`.

**References.** Read these in the local tape-kit repo:
- `~/GitHub/tape-kit/docs/reference/crsp-daily-stock-file.md`
- `~/GitHub/tape-kit/docs/reference/crsp-processing-policy.md`
- `~/GitHub/tape-kit/docs/reference/crsp-extraction.md`

Read files with DuckDB `read_parquet` directly, following the `duckdb-guidelines` skill. Do not add `tape-kit` as a dependency.

**Code.** `src/rebal/fetch/crsp_cluster.py`, with three outputs:

1. **`etf_daily.parquet`:** columns `date`, `ticker`, `permno`, `ret` (total return, with distributions), `retx`, `prc`, `vol`.
   - Tickers: SPY, IVV, IEF, TLT, AGG, IWB, IWM, IWD, IWF, EFA, VEU, ACWX.
   - Coverage: from each fund's inception (SPY: 1993) to latest.
   - Resolve tickers to PERMNOs through the security history, so ticker reuse cannot mix securities. Print the PERMNO and date span of each ticker.
2. **`benchmarks_daily.parquet`:** columns `date`, `vwretd`, `vwretx`, `ewretd`, `ewretx`, `sprtrn`, from 1960 to latest.
3. **`dispersion_daily.parquet`:** columns `date`, `ivol`, `ivol_w`, `n_stocks`.
   - `ivol` = the cross-sectional SD of daily total returns of U.S. common stocks.
   - `ivol_w` = the same, after winsorizing returns at 1% and 99% each day.
   - The filters are the CIZ equivalents of share codes 10/11: ordinary common shares, U.S.-incorporated, primary exchange NYSE, NYSE American (AMEX) or Nasdaq. Use no price filter.
   - Process each year separately into `parts/YYYY.parquet` and merge at the end. `--skip-existing` skips years already done.
   - Write the filters and their reason in `docs/methods/ivol.md`.

**Demo mode.** `--demo` builds a tiny synthetic CRSP-like parquet set in a temporary directory. It checks the ticker-to-PERMNO join, the year merge, and that `ivol` equals a hand-computed SD. `tests/test_crsp_cluster.py` runs the demo.

**Run.**
- Follow the `cluster` skill: `cluster-kit sync code`, then `cluster-kit launch`.
- Run only on the cluster, at most 1 SLURM job at a time, on `cpu_shared`.
- Before you submit, check live capacity with `cluster-kit resources --json`.
- Budget: 4 CPUs, 16 GB, a 1-hour time limit. Expect under 30 minutes.
- On a crash, resubmit with `--skip-existing`; never restart from scratch.

**Outputs.**
1. Write them on the cluster to `/mnt/slurm-beegfs/Users/j-vill36/replicate-data/licensed/crsp/`.
2. Copy them to the MacBook at `$REPLICATE_DATA_DIR/licensed/crsp/`, using the transfer method in the `cluster` skill.
3. Never commit them.
4. Write `docs/data/cards/crsp.md`, with the PERMNO table and the coverage.

Out of scope: return proxies (TASK-011) and the panel (TASK-012).

## Acceptance

- `uv run pytest tests/test_crsp_cluster.py` passes.
- Job evidence: `sacct -j <jobid> --format=JobID,State,Elapsed,MaxRSS` shows `COMPLETED`. The outcome records the job ID.
- On the MacBook, a DuckDB summary of the three files prints:
  - for each ticker, its rows, first date and last date;
  - for SPY, a first date of 1993-01-29 or later, and coverage to 2023-03-17 or later;
  - for `ivol`, coverage of 1997-09-10 to 2023-03-17, with `n_stocks` between 2,000 and 9,000.
- `git status --porcelain` lists no parquet file.

## Verify

```sh
uv run pytest -q tests/test_crsp_cluster.py
D="${REPLICATE_DATA_DIR:-$HOME/data/replicate}/licensed/crsp"
uv run python3 -c "
import duckdb; d='$D'
print(duckdb.sql(f\"select ticker, count(*) n, min(date), max(date) from '{d}/etf_daily.parquet' group by 1 order by 1\"))
print(duckdb.sql(f\"select count(*), min(date), max(date), min(n_stocks), max(n_stocks) from '{d}/dispersion_daily.parquet'\"))
print(duckdb.sql(f\"select count(*), min(date), max(date) from '{d}/benchmarks_daily.parquet'\"))"
git status --porcelain
```
