# TASK-009 outcome

## Acceptance

1. [x] `uv run pytest tests/test_crsp_cluster.py` passes: **9 passed**.
   The exact Verify block also printed `9 passed in 0.93s` (see captured output below
   for the measured duration). Full local suite: **29 passed in 3.25s**.
   Ruff on both task Python files: `All checks passed!`.
2. [x] Cluster accounting confirms **COMPLETED** for job **25495**, the job named
   in final `extraction.json`, and initial job **25494**. Exact accounting output:

   ```text
   JobID             State    Elapsed     MaxRSS
   ------------ ---------- ---------- ----------
   25494         COMPLETED   00:00:10
   25494.batch   COMPLETED   00:00:10          0
   25494.extern  COMPLETED   00:00:10          0
   25495         COMPLETED   00:00:09
   25495.batch   COMPLETED   00:00:09          0
   25495.extern  COMPLETED   00:00:09          0
   ```

   Command: `cluster-kit exec 'sacct -j 25494,25495 --format=JobID,State,Elapsed,MaxRSS'`.
   The cluster did not provide a useful MaxRSS measurement.
3. [x] The MacBook DuckDB summary read **all three** licensed parquet files.
   The exact Verify block exited **0**; its complete output is below.
4. [x] The ETF summary printed **12 tickers**, each with rows, first date,
   and last date. See the captured output and the PERMNO table in
   [the source card](../../../docs/data/cards/crsp.md).
5. [x] SPY: **8,433 rows**, **1993-01-29 through 2026-07-31**.
   This covers the required end date, 2023-03-17.
6. [x] Dispersion: **7,267 rows**, **1997-09-10 through 2026-07-31**.
   `n_stocks` ranges from **3,562 to 7,465** across the entire output,
   within the required 2,000–9,000 range.
7. [x] `git status --porcelain` printed nothing during Verify. No parquet
   is tracked or appears in git status. All licensed files remain outside git.

## Summary

Added `src/rebal/fetch/crsp_cluster.py`, synthetic demo inputs and nine tests,
`docs/methods/ivol.md`, and `docs/data/cards/crsp.md`. The extractor reads
parquet directly with DuckDB. It resolves FUND/ETF securities through dated
security history, rejects ambiguous identities and overlapping intervals,
and avoids older stocks that reused SPY or AGG tickers. Benchmarks start in
1960. Dispersion starts on 1997-09-10 and uses the documented CIZ common-stock
filters, no price screen, one-period finite returns, sample SD, and daily
1%/99% winsorization. Annual parts support validation, atomic replacement,
restart, sharding, and a dry run.

Ran `uv run cluster-kit sync code`, checked live capacity with
`cluster-kit resources --json`, and submitted with `cluster-kit launch` on
`cpu_shared`, 4 CPUs, 16 GB, and a one-hour limit. Real extraction used only
cluster CPUs. Both jobs completed without stderr. The source publication
metadata hash and SLURM job ID are in the external `extraction.json`.

Copied the three final parquets and metadata with `cluster-kit sync cp` to
`/Users/jesusvillotamiranda/data/replicate/licensed/crsp/`. All three local
SHA-256 hashes equal the cluster hashes; the source card records each hash.
The benchmark summary reports **16,755 rows**, **1960-01-04 through 2026-07-31**.

Deviation: the launcher returned exit 0 without a job ID or log path.
The worker incorrectly retried the submission instead of checking accounting
first. Job 25494 ran 22:30:46–22:30:56; job 25495 ran 22:30:52–22:31:01
(cluster local time), so they overlapped for four seconds. This breached the
one-job budget. No crash occurred. Both jobs completed, final keys and schemas
validated, the MacBook Verify passed, and copied hashes match the final cluster
files. No further job was submitted. The missing launch receipt is reported at
https://github.com/jesusvillota/cluster-kit/issues/57; this PR does not change
cluster-kit. Future submissions must inspect accounting before retrying a
silent launcher response.

Verified local revision: `a5113cf4b55ee51d4e0aecda00f592ed3191fece`, after a
clean rebase onto `origin/main`. The actual cluster implementation was submitted
at pre-rebase commit `99764c1`; subsequent implementation changes only corrected
a CLI example. An extra date-boundary test passes. This outcome and a source-card
D-number note are documentation-only follow-ups. No spec, other task, decision,
or goal configuration was edited. GitHub Actions were not inspected or used.

PR: https://github.com/jesusvillota/replicate/pull/11, into `main`, with
`Goal-Task: hmm-rebalancing/TASK-009` and label `goal:hmm-rebalancing`.
Proposed follow-ups: existing TASK-011 and TASK-012 consume these outputs.
No material decision or missing data blocks this task.

## Verify output

The exact task Verify block ran on the MacBook and exited 0. `git status`
contributed no output.

```text
.........                                                                [100%]
9 passed in 0.93s
┌─────────┬───────┬────────────┬────────────┐
│ ticker  │   n   │ min(date)  │ max(date)  │
│ varchar │ int64 │    date    │    date    │
├─────────┼───────┼────────────┼────────────┤
│ ACWX    │  4615 │ 2008-03-28 │ 2026-07-31 │
│ AGG     │  5747 │ 2003-09-26 │ 2026-07-31 │
│ EFA     │  6274 │ 2001-08-17 │ 2026-07-31 │
│ IEF     │  6042 │ 2002-07-26 │ 2026-07-31 │
│ IVV     │  6588 │ 2000-05-19 │ 2026-07-31 │
│ IWB     │  6588 │ 2000-05-19 │ 2026-07-31 │
│ IWD     │  6583 │ 2000-05-26 │ 2026-07-31 │
│ IWF     │  6583 │ 2000-05-26 │ 2026-07-31 │
│ IWM     │  6583 │ 2000-05-26 │ 2026-07-31 │
│ SPY     │  8433 │ 1993-01-29 │ 2026-07-31 │
│ TLT     │  6042 │ 2002-07-26 │ 2026-07-31 │
│ VEU     │  4881 │ 2007-03-08 │ 2026-07-31 │
└─────────┴───────┴────────────┴────────────┘
  12 rows                         4 columns

┌──────────────┬────────────┬────────────┬───────────────┬───────────────┐
│ count_star() │ min(date)  │ max(date)  │ min(n_stocks) │ max(n_stocks) │
│    int64     │    date    │    date    │     int64     │     int64     │
├──────────────┼────────────┼────────────┼───────────────┼───────────────┤
│         7267 │ 1997-09-10 │ 2026-07-31 │          3562 │          7465 │
└──────────────┴────────────┴────────────┴───────────────┴───────────────┘

┌──────────────┬────────────┬────────────┐
│ count_star() │ min(date)  │ max(date)  │
│    int64     │    date    │    date    │
├──────────────┼────────────┼────────────┤
│        16755 │ 1960-01-04 │ 2026-07-31 │
└──────────────┴────────────┴────────────┘

```
