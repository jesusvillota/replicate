# Exhibits contract

Exhibit IDs:

- `table_1`
- `table_2a`
- `table_2b`
- `table_3`
- `table_C1`
- `table_C2`
- `table_D1`
- `table_D2`
- `table_D3`
- `table_D4`
- `table_D5`
- `table_D6`
- `table_D7`
- `table_D8`
- `table_D9`
- `table_D10`
- `table_D11`
- `table_D12`
- `table_D13`
- `table_D14`
- `figure_2`
- `figure_3`
- `figure_4`
- `figure_6`
- `figure_C1`
- `figure_D1`
- `figure_D2`
- `figure_D3`
- `figure_D4`
- `figure_D5`
- `costs`
- `table_6a`
- `table_6b`
- `table_6c`

Regression tables are long-format CSV files at `output/tables/<id>.csv`.
Use exactly these columns, in this order:

```text
exhibit,column,term,coef,se,t,p,nobs,adj_r2,se_type,sample_start,sample_end
```

Each row describes one estimated term in one table column.
`exhibit`, `column`, `term` and `se_type` are strings. Estimates and statistics are numeric.
`nobs` is an integer. Sample dates use ISO `YYYY-MM-DD` strings.
Record the actual standard-error method in `se_type`.

Figures are `output/figures/<id>.pdf`, with plotted data in `output/figures/<id>.csv`.
Use named columns with units in the relevant module documentation.
Demo runs write files directly under `output/demo/` instead, with the same IDs and extensions.
Demo outputs must never enter git.

The default sample is 1997-09-10 to 2023-03-17, inclusive.
Each exhibit module also takes `--end latest` to use its latest available date.
It records the actual sample used. The runner's API does not override module sample defaults.

## Module registration

`uv run python3 -m rebal.exhibits --all [--demo] [--only ID ...]`
uses `pkgutil` to discover modules. There is no central registration list.
Each module exposes `EXHIBITS: list[str]` and `run(demo: bool) -> list[Path]`.
Use unique exhibit IDs across modules. Keep helper module names private (start with `_`).
`--only` selects modules which own the requested IDs. A selected module may produce all its IDs.
Unknown IDs fail with a clear error. With no modules, the runner prints `0 exhibit modules` and exits 0.
