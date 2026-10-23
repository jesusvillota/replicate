# TASK-022 outcome

Status: Delivered — DEC-005 applied; all local acceptance checks pass.

## Summary

Corrected the missing portfolio-share factor in `annual_cost`. The regression
slope times the mean absolute trade gives the price change. Multiplying again
by the share traded gives portfolio cost. Annual cost is
`-beta * decimal_size**2 * trades_per_year * 10000`, which gives 4.68 bps for
the paper's worked example. The same helper covers Calendar, Threshold,
fixed-size, full-sample interaction and random-date costs.

Applied DEC-005, accepted by jesusvillota on 2026-10-23. The API, CLI and
metadata now default to excluding delta=0 from Threshold cost summaries.
All 26 raw estimates remain available. Means, range, both headlines and dollars
use 25 deltas, 0.1–2.5%. `--delta-zero include` retains the sensitivity check.
Tests guard the default, raw-estimate retention, CLI and metadata. Output
column layouts stay unchanged. The methods document records the unit
convention, accepted treatment and retained daily-reset diagnostics.

No shared modules, task specifications, decisions, contracts or goal.yaml
changed. No cluster jobs or new data were used. Real smoke results stayed in
memory; no real exhibit outputs are committed. Demo outputs are ignored.

Verified analysis revision: 8102a73c68d44f6805d8a612ec06c51cb8db1109.
Only outcome documentation follows this revision. Proposed follow-up:
TASK-030 should report the remaining magnitude gap; no new task was created.

## Acceptance

- [x] `uv run pytest -q tests/test_costs.py`: **13 passed in 12.25s** in this
  resume session. Tests include the 4.68 bps worked example and default
  delta=0 exclusion while retaining its raw estimate. Planted-effect,
  zero-effect, trade, dollar and output-schema checks also pass.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5`
  exited 0 in this resume session. It wrote `costs.csv`, `costs.metadata.json`,
  `figure_D5.csv` and `figure_D5.pdf` under `output/demo/`.
  `ls output/demo/costs* output/demo/figure_D5*` exited 0. Artifact checks
  confirmed 10,000 finite draws, unchanged columns, a one-page PDF, exclusion
  metadata, correct 25-delta summaries and the retained raw delta=0 estimate.
- [x] Real-panel smoke was rerun in this session with 100 schedules per policy,
  seed 16. The default headline is **1.22151 bps/year and $2,443,029,137/year**,
  versus the paper's **8 bps and $16B**. The Threshold range is
  **−18.57023 to 6.56819 bps**, versus **6–27 bps**. These do not agree in size;
  see the table and explanation below.

Additional local checks in this resume session: Ruff lint and format checks
pass with `uv run --with ruff ruff check src/rebal/exhibits/costs.py tests/test_costs.py`
and `uv run --with ruff ruff format --check src/rebal/exhibits/costs.py tests/test_costs.py`.
The isolated Ruff invocation changes no dependency files. CLI `--help` exits 0
and documents exclusion as the default. `git diff --check` passes.

## Real-panel smoke

Inputs: existing `~/data/replicate/processed/daily_panel.parquet` and
`signals_clean.parquet`. Default sample: 1997-09-10 through 2023-03-17;
no macro controls; 100 random schedules; seed 16. Both policies were rerun in this resume session through
the corrected `costs.estimate` API. Exclusion used the default without a policy
argument; inclusion used `delta_zero="include"`. Input hashes match the original
audit. These were not runs of the real-output writer.

| Quantity | Include delta=0 | Exclude delta=0 | Paper |
|---|---:|---:|---:|
| Headline, bps/year | 41.83650 | 1.22151 | 8 |
| Headline, USD/year on $20T | $83,673,006,255 | $2,443,029,137 | $16,000,000,000 |
| Threshold range, bps/year | −18.57023 to 110.05903 | −18.57023 to 6.56819 | 6–27 |
| Threshold mean, bps/year | −1.10750 | −5.55416 | 15 |
| Fixed-1%-trade Threshold mean, bps/year | 80.34020 | −0.88978 | 11 |
| Calendar, bps/year | 3.33281 | 3.33281 | about 5 |
| Calendar T−4, bps/year | 9.84560 | 9.84560 | about 9 |
| Random-date mean, bps/year (100 draws) | 0.03113 | 0.03113 | 0.6 (10,000 draws) |

The worked example matches at 4.68 bps. T−4 agrees roughly in size. Calendar
has the same order of magnitude but is lower. The corrected headline and
Threshold range do **not** agree under either policy. Inclusion is dominated
by the weakly separated daily-reset slope. Exclusion leaves negative costs
at other deltas: the fitted slopes imply gains rather than the paper's losses.
The panel uses documented proxies instead of Bloomberg ES/TY futures; its
coefficients and simulated trades differ. Correcting units does not resolve
those data and specification differences. The 100-draw random mean is only a
smoke result; it does not establish the paper's 10,000-draw mean or its sign.
No coefficient, schedule or policy was tuned to reach the paper's headline.

Input SHA-256:

```text
daily_panel.parquet   0aa723f34422fae7bcedb41bfaf0e7a5c3685688a1a9c7e3addec7af0463a4cd
signals_clean.parquet ac21349f54e9b1efcee38b25317dfcf7350f23490646b661a4e2caf52dddbed1
```

## Delta=0 sensitivity

Retained diagnostics from the initial TASK-022 audit follow. This resume
reran both policy smoke checks above and confirmed the raw zero-delta slope
and fixed-size cost below. The model and its raw estimates did not change.

The design has shape 6,317 × 7 and rank seven. Its condition number is 16,277;
after centering/scaling the nonconstant columns, it is 110. Thus the design is
full rank, not singular. `max(abs(thr_000 - 0.24*ret)) = 0.0018975973`.
For a daily-reset 60/40 portfolio, the exact drift is
`0.24*ret / (1 + 0.6*r_es + 0.4*r_ty)`. The current-return regressor leaves
little independent variation for estimating the daily-reset slope.

| Diagnostic | Delta=0 slope | HC1 standard error | Observations |
|---|---:|---:|---:|
| Baseline | −8.37734 | 7.36926 | 6,317 |
| Omit current return | −0.38963 | 0.09850 | 6,317 |
| Before 2006 | −15.70496 | 10.06761 | 2,050 |
| After 2006, excluding 2006 | −7.36068 | 8.55226 | 4,017 |
| Add macro controls | −7.75663 | 9.29822 | 5,043 |

Rounding only `thr_000` to four/five/six decimals gives slopes
−6.80283 / −8.26869 / −8.36786. Omission of current return is a changed model,
not a numerical repair. No such changes are applied to production estimates.
The corrected zero-delta fixed-1%-trade cost is 2,111.09 bps/year. The headline
with zero is 34.25 times its value without zero.

## Accepted decision

The initial request asked whether to exclude delta=0 from Threshold cost
summaries while retaining its raw estimate. The alternatives were inclusion
(41.84 bps, $83.67B), exclusion (1.22 bps, $2.44B), or changing the zero-delta
model. Inclusion lets the unstable daily-reset slope dominate. Exclusion
changes the summary grid but keeps all raw evidence. Changing the model would
change equation (4) and require a separate methodological justification.

The owner accepted the recommended exclusion in DEC-005 on 2026-10-23.
This resolves the material decision. The aggregate signal and regression
specification stay unchanged. The corrected estimates still do not reproduce
the paper's headline or Threshold range. No estimate was tuned to a target.

## Verify evidence

All three exact Verify commands completed successfully in this resume session:

```text
$ uv run pytest -q tests/test_costs.py
.............                                                            [100%]
13 passed in 12.25s
$ uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5
1 exhibit modules
output/demo/costs.csv
output/demo/figure_D5.csv
output/demo/figure_D5.pdf
output/demo/costs.metadata.json
$ ls output/demo/costs* output/demo/figure_D5*
output/demo/costs.csv
output/demo/costs.metadata.json
output/demo/figure_D5.csv
output/demo/figure_D5.pdf
```

Absolute output paths above are shortened to repository-relative paths.
The cost tests, lint, format and both real-panel policy smoke checks passed.
No real output writer ran; `output/` has no tracked changes or untracked real
artifacts. GitHub Actions were not inspected or used as a gate.

PR #33 is open and ready for review, with label `goal:hmm-rebalancing` and
`Goal-Task: hmm-rebalancing/TASK-022` in its body. Resolved decision/blocker
markers were removed. No review threads, reviews or PR comments were present
when checked in this session. All task changes are committed and pushed on
`goal/hmm-rebalancing/task-022`; the PR has not been merged.
