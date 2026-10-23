# TASK-022 outcome

Status: BLOCKED — delta=0 cost-summary policy requires a material decision.

## Summary

Corrected the missing portfolio-share factor in `annual_cost`. The regression
slope times the mean absolute trade gives the price change; multiply again by
the share traded to get portfolio cost. Annual cost is now
`-beta * decimal_size**2 * trades_per_year * 10000`. This gives 4.68 bps for
the paper's worked example. The same helper covers Calendar, Threshold,
fixed-size, full-sample interaction and random-date costs. Tracking error,
gross utility and dollar conversion keep their existing units.

Added `--delta-zero include|exclude` for the audit. Inclusion retains the prior
default provisionally. Neither option changes the individual zero-delta
estimate or removes its row. Means, range, headline and dollars use the selected
grid. Output column layouts are unchanged. Metadata records the formula and
policy. The methods document explains both the paper's suppressed units and
the unresolved daily-reset identification problem.

No shared modules, task specifications, decisions, contracts or goal.yaml were
changed. No cluster jobs or new data were used. Real smoke estimates stayed
in memory; no real exhibit outputs are committed. The only additional task
file is this required outcome. The PR remains draft because the 34.25x policy
sensitivity exceeds the task's 2x decision threshold.

Verified analysis revision: 0eed9f42f071f9f9ac69a473b2b2af7299494592 (only outcome documentation follows).
Rebased onto `origin/main` without conflicts. Proposed follow-up: resolve the
decision below, then resume TASK-022. No additional task was created.

## Acceptance

- [x] `uv run pytest -q tests/test_costs.py` passes: 13 tests passed in this
  session. New tests reproduce 4.68 bps and guard explicit inclusion/exclusion
  without clipping or deleting delta=0. Existing planted-effect, zero-effect,
  random-date, trade, dollar and output-schema checks pass with corrected units.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5`
  exits 0 and writes `costs.csv`, `costs.metadata.json`, `figure_D5.csv` and
  `figure_D5.pdf` under `output/demo/`. The CSV has 10,000 finite simulation
  rows, unchanged columns, and a valid PDF. Metadata confirms 10,000 schedules
  and the inclusion policy. `ls output/demo/costs* output/demo/figure_D5*` exits 0.
- [x] Real-panel smoke reports the headline in bps and dollars and the Threshold
  range next to the paper; see the table below. It explicitly rejects agreement
  in size and explains the remaining differences.
- [ ] Delivery approval: a material decision is missing. PR #33 remains open
  and draft into `main`, labelled `goal:hmm-rebalancing`, with `Goal-Task`,
  `Goal-Blocked` and `Goal-Decision` markers. Do not mark the native goal complete.

Additional local checks: Ruff passes using
`uv run --with ruff ruff check src/rebal/exhibits/costs.py tests/test_costs.py`.
The unaugmented `uv run ruff check ...` could not start because Ruff is absent
from the project environment; the isolated `--with ruff` invocation changes no
dependency files. `uv run python3 -m rebal.exhibits.costs --help` exits 0 and
lists `--delta-zero {include,exclude}`. `git diff --check` passes.

## Real-panel smoke

Inputs: existing `~/data/replicate/processed/daily_panel.parquet` and
`signals_clean.parquet`. Default sample: 1997-09-10 through 2023-03-17;
no macro controls; 100 random schedules; seed 16. Both policies were run through
the corrected `costs.estimate` API. These were not runs of the real-output writer.

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

## Decision request

Should delta=0 be excluded from Threshold cost summaries while retaining its raw estimate?

The paper describes costs across 0–2.5%, but does not explain how it handles
the separate daily-reset slope with current return present. Equation (2),
footnotes 10 and 16, and Table D.6 describe the aggregate signal or robustness
checks on it; they do not settle the average of per-delta costs. Footnote 17's
interaction alternative also leaves this problem unresolved. The task requires
a decision because the headline changes by more than 2x.

Options and trade-offs:

1. **Include zero.** Keep the literal 26-delta grid. Report 41.84 bps and
   $83.67B. This preserves coverage but makes the headline depend heavily on
   a slope with large uncertainty and weak separation from current return.
2. **Exclude zero from summaries and retain its raw estimate.** Report
   1.22 bps and $2.44B using 25 deltas. This makes the unstable case visible
   without letting it dominate, but changes the stated cost grid. It still
   does not reproduce the paper's 8 bps or 6–27 bps range.
3. **Change the delta=0 model.** For example, omit current return for zero
   only. This gives a much smaller daily-reset slope, but treats that delta
   differently and changes the equation (4) specification. It requires an
   explicit methodological justification; it is not implemented here.

### Recommendation

Choose option 2. Retain delta=0 as a separate diagnostic and exclude it from
all Threshold summary statistics. Document the 25-delta convention, retain
an inclusion flag for sensitivity, and report that the remaining estimates
still fail to reproduce the paper. Keep the PR draft until this decision is
accepted and TASK-022 is resumed. Do not change the model to match a target.

## Verify evidence

All three Verify commands ran successfully in this session. The full demo
command exited 0; the final local test rerun after the rebase exited 0.
Console tail (absolute exhibit paths shortened here to repository-relative paths):

```text
$ uv run pytest -q tests/test_costs.py
.............                                                            [100%]
13 passed in 9.49s
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

Additional artifact validation: 10,000 draws; both schemas unchanged; finite
data; PDF header and metadata valid. `git restore output/` ran after the
in-memory real smoke; no new untracked real outputs were present. The ignored
demo files remain available. GitHub Actions were not inspected or used as a gate.
