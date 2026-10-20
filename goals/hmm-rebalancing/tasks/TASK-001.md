---
id: TASK-001
title: Scaffold the rebal package, data contracts and demo fixtures
milestone: M-1
state: approved
depends_on: []
delivery: pr
priority: 1
---

## Why

Serves SC-1, SC-2 and SC-3. Every later task needs these four things from this task: the `rebal` package, the storage rules, the three data contracts and the demo fixtures. With the contracts and fixtures merged, the fetch tasks (M-1) and the analysis tasks (M-2) can run in parallel.

## Scope

No cluster jobs in this task. No data downloads.

Read first:
- `goals/hmm-rebalancing/README.md`, sections "Shared conventions" and "Data plan".
- `goals/hmm-rebalancing/paper-notes.md`, sections 2–4.

### 1. Package and tooling

1. Write a tracked `pyproject.toml` at the repo root.
   - Project `replicate`, `requires-python = ">=3.11"`, src layout with the package `rebal` in `src/rebal/`.
   - Runtime dependencies: `pandas`, `numpy`, `pyarrow`, `duckdb`, `statsmodels`, `scipy`, `matplotlib`, `requests`, `rich`, `yfinance`, `openpyxl`, `xlrd`, `wrds`, and `cluster-kit`. Get `cluster-kit` from git: `[tool.uv.sources] cluster-kit = { git = "https://github.com/jesusvillota/cluster-kit" }`.
   - Dev dependency: `pytest`.
   - Run `uv lock` and commit `uv.lock`.
   - Later tasks should need no new dependency. A task that does need one adds only that one dependency.
2. Write `.gitignore`. Keep the existing `.DS_Store` lines, and add:
   - `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`
   - `output/demo/`
   - `/data/*` with the exception `!/data/public/`
3. Write a short repo `README.md`:
   - what the repo replicates;
   - the run order: `uv sync`, then the fetchers, then `rebal.panel --build`, then `rebal.signals --build`, then `rebal.exhibits --all`;
   - links into `docs/`.

### 2. Shared modules

1. **`src/rebal/paths.py`:**
   - `REPO_ROOT`
   - `public_dir(source)` returns `data/public/<source>/`.
   - `licensed_dir(source)` returns `$REPLICATE_DATA_DIR/licensed/<source>/`. The default `REPLICATE_DATA_DIR` is `~/data/replicate`.
   - `processed_dir()` and `output_dir(kind)`, where kind is `tables`, `figures` or `demo`.
   - Every function creates its directory.
2. **`src/rebal/fetch/common.py`:**
   - `download(url, dest, *, retries=3)` uses a browser-like User-Agent and fails loudly on HTTP errors.
   - `summarize(path, date_col)` validates the file: the date column parses, no duplicate dates, and at least one row. It prints exactly one line: `OK <path> rows=<n> first=<date> last=<date>`. Every fetcher calls it on every file it writes.
3. **`src/rebal/io.py`:**
   - `load_panel(demo=False)`: in real mode, reads `processed_dir()/daily_panel.parquet`. If the file is missing, raise a clear error that names `rebal.panel --build`.
   - `load_signals(demo=False, timing="clean")`: reads `processed_dir()/signals_<timing>.parquet`.
   - In demo mode, both return the fixtures below.
4. **`src/rebal/demo.py`:**
   - `make_panel(start="1996-01-02", end="2023-12-29", seed=0)` returns a synthetic panel with every column in `docs/contracts/daily_panel.md`. Use realistic scales:
     - `r_es` about 18% annual volatility;
     - `r_ty` about 6% annual volatility, with correlation about −0.2 to `r_es`;
     - controls as AR(1) series at plausible levels.
   - `make_signals(panel, beta_threshold=-0.4, beta_calweek4=-0.3, seed=0)` returns a frame with every column in `docs/contracts/signals.md`. Make the synthetic signals AR(1), with daily SD about 0.48% (`threshold`) and about 1% (`calendar`). Then overwrite `ret` so that ret_{t+1} = β_T·threshold_t + β_C·calendar_t·week4_t + noise.
   - `python3 -m rebal.demo --check` fits that equation by plain OLS. It prints the recovered betas and exits non-zero if either beta misses its planted value by more than 0.05. It runs the same check with both betas set to 0.
5. **`src/rebal/exhibits/__main__.py`:**
   - `python3 -m rebal.exhibits --all [--demo] [--only ID ...]` auto-discovers every module in `rebal.exhibits` with `pkgutil`. There is no central list, so parallel tasks never edit the same file.
   - Each exhibit module exposes `EXHIBITS: list[str]` and `run(demo: bool) -> list[Path]`.
   - With no exhibit modules yet, the runner prints `0 exhibit modules` and exits 0.

### 3. Contracts (the single source of truth; later tasks cite them)

1. **`docs/contracts/daily_panel.md`:** one row per trading day, keyed by `date` (a naive date, sorted and unique). All returns are simple decimal daily returns. Columns:
   - **Returns:** `r_es` (ES proxy, excess of cash), `r_ty` (TY proxy, excess of cash), `rf` (French daily RF), `rf_3m` (DTB3 as a daily return).
   - **Controls:** `vix` (level/100), `move` (level/100), `epu`, `ads`, `sentiment`, `ra_bex`, `unc_bex`, `ara`, `liquidity`, `ivol`.
   - **Factors:** `mkt_rf`, `smb`, `hml`, `rmw`, `cma`, `mom`, `q_mkt`, `q_me`, `q_ia`, `q_roe`, `q_eg`.
   - **Indices:** `r_sp500tr`, `r_agg`, `r_acwxus`, `r_r1k`, `r_r2k`, `r_r1kv`, `r_r1kg`, `r_mkt_french` (Mkt-RF + RF), `r_10y_gsw`.
   - For each column, give the dtype, the units, whether it may be NaN, and the dataset ID (D-number) it comes from.
   - State these rules:
     - Returns are never forward-filled.
     - Controls may be forward-filled for at most 5 trading days.
     - TASK-012 is the only writer.
2. **`docs/contracts/signals.md`:** the output of `rebal.signals.build(r_eq, r_bd, target=0.60, timing="clean", deltas=...)`, keyed by `date`. Columns:
   - `ret` = r_eq − r_bd.
   - `thr_000` … `thr_040`: Threshold^δ for δ = 0.0% … 4.0% in 0.1% steps. The suffix is δ in tenths of a percent.
   - `threshold`: the mean of `thr_000`…`thr_025`.
   - `calendar`.
   - `week1` … `week4`. week4 = the last 5 trading days of the month; week3 = trading days 6–10 before month-end; week2 = days 11–15; week1 = the rest.
   - `days_to_month_end`: 1 on the last trading day.
   - `mom_fast`, `mom_medium`, `mom_slow`, `momentum`.
   - `rev_st`, `rev_lt`, `eom_rev`.
   - Variants for other targets: `threshold_t86`, `calendar_t86`, `threshold_t50`, `calendar_t50`, `threshold_t70`, `calendar_t70`.
   - Simulation API, used by the cost and strategy code. Each function returns `w_pre`, `w_post` and `trade`:
     - `simulate_threshold(r_eq, r_bd, delta, target, timing)`
     - `simulate_calendar(r_eq, r_bd, target, timing)`
     - `simulate_dates(r_eq, r_bd, dates, target)`
   - Point to paper-notes §3.2, §3.4 and §3.6 for the definitions. TASK-013 implements this contract.
3. **`docs/contracts/exhibits.md`:**
   - Exhibit IDs: `table_1`, `table_2a`, `table_2b`, `table_3`, `table_C1`, `table_C2`, `table_D1` … `table_D14`, `figure_2`, `figure_3`, `figure_4`, `figure_6`, `figure_C1`, `figure_D1` … `figure_D5`, `costs`, `table_6a`, `table_6b`, `table_6c`.
   - Regression tables are long-format CSV in `output/tables/<id>.csv` with the columns `exhibit, column, term, coef, se, t, p, nobs, adj_r2, se_type, sample_start, sample_end`.
   - Figures are `output/figures/<id>.pdf`, plus the plotted data in `output/figures/<id>.csv`.
   - Demo runs write to `output/demo/` instead.
   - The default sample is 1997-09-10 to 2023-03-17. Each exhibit module also takes `--end latest`.

### 4. Data documentation

1. **`docs/data/sources.md`:** the master source map. Use exactly one table row per dataset D1–D28; each row starts with `| D<n> |`. The columns are:
   - D
   - Variable
   - Authors' source (quote paper-notes §2)
   - Used in (exhibits)
   - Our source
   - Exact or proxy
   - Fetch task
   - Storage (`data/public/…` or `$REPLICATE_DATA_DIR/licensed/…`)
   - Status
   Fill "Our source" from the README's Data plan table and set every Status to `planned`.
   Add these sections:
   - A legend: what "exact", "proxy" and "none" mean.
   - The two storage classes.
   - "Not replicable": D14, D21, D28, footnote 28 and footnote 32, with the reason for each.
   - A note that only TASK-012 updates the table after this task.
2. **`docs/data/cards/TEMPLATE.md`:** the source-card template, with these fields:
   - Source and URL or WRDS table
   - Downloaded (date)
   - License class
   - Series, with units
   - Transforms
   - Coverage
   - Known problems
   - Paper datasets served (D-numbers)

### 5. Tests

`tests/test_scaffold.py`:
- The demo panel has exactly the contract columns.
- The demo signals have exactly the contract columns.
- `make_signals` passes the planted-effect check and the zero-effect check.
- The exhibits runner exits 0.

Out of scope: any fetcher, signal logic or regression code.

## Acceptance

- `uv sync` and `uv run pytest` succeed; the output shows the passing tests.
- `uv run python3 -m rebal.demo --check` prints recovered betas within 0.05 of −0.4 and −0.3, and about 0 (within 0.05) for the zero-effect run.
- `uv run python3 -m rebal.exhibits --all --demo` exits 0.
- `grep -cE '^\| D[0-9]+ ' docs/data/sources.md` prints 28.
- `ls docs/contracts/` lists `daily_panel.md`, `signals.md` and `exhibits.md`.
- `git check-ignore .env output/demo/x data/foo` prints all three paths, and `git check-ignore data/public/x` prints nothing.

## Verify

```sh
uv sync && uv run pytest -q
uv run python3 -m rebal.demo --check
uv run python3 -m rebal.exhibits --all --demo; echo "exit=$?"
grep -cE '^\| D[0-9]+ ' docs/data/sources.md
ls docs/contracts/
git check-ignore .env output/demo/x data/foo; git check-ignore data/public/x || echo "data/public not ignored"
```
