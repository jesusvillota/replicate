# Latest sample (footnote 32)

Run `uv run python3 -m rebal.latest --demo` for synthetic data. Omit `--demo`
to read the processed panel and signals. `--timing clean|literal` selects the
signal file; the default is `clean`. Demo mode uses the shared synthetic fixtures.

The module imports `build_tables`, `DEFAULT_SAMPLE`, `load_panel` and
`load_signals` from `rebal.exhibits.predictive_tables`. It calls the pure table
builder twice: once with `end="latest"`, once with `DEFAULT_SAMPLE[1]`
(2023-03-17). Both samples start at `DEFAULT_SAMPLE[0]` (1997-09-10).
The latest endpoint comes from the panel, with no fixed year or date.
Both runs retain the existing next-day alignment, complete-case selection,
column definitions and HC1 standard errors. See [regressions.md](regressions.md)
and the [exhibits contract](../contracts/exhibits.md).

Only latest-sample `table_1.csv` and `table_3.csv` are saved. The builder also
computes other tables in memory; these are discarded. The runner never calls
the predictive-table writer. Every file goes under
`output/tables/robustness/latest/`, or `output/demo/robustness/latest/` in demo
mode. The main exhibits remain separate. No outputs are committed by TASK-031.

`latest_comparison.csv` has columns `exhibit,column,term,stat,sample,value`.
For every Table 1 column, it includes `threshold` and `calendar:week4`, with
`coef`, `se`, `t` and `nobs` statistics for `paper_end` and `latest`.
`sample_start` and `sample_end` rows record the actual first and last outcome
dates for that column. These dates can differ between columns when controls
are missing. `value` therefore contains numbers or ISO dates, depending on
`stat`. `latest.metadata.json` records the requested sample windows, panel
endpoint, timing, covariance method, input sources and output names.

The report adds one section, **Latest sample (footnote 32)**. It reads and
displays this comparison CSV when present; otherwise it says `not run`.
Demo reports read the demo folder only. This section uses the same fixed
latest folder even when `--variant` selects other main comparison inputs.
It does not change the main exhibit classifications or estimate regressions.
The comparison is descriptive; it does not automatically claim that the
paper's result holds. TASK-032 will run and interpret the real-data results.
