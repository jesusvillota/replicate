# TASK-016 outcome

## Acceptance

- [x] `uv run pytest tests/test_costs.py` passes. The exact Verify command
  `uv run pytest -q tests/test_costs.py` passed **11 tests in 8.38s**, exit 0.
  Tests recover Calendar impact −0.39 and Threshold impact −0.4 to 1e-12,
  independently check trade sizes and annual frequencies, and verify that
  zero-impact costs and the random-date distribution are near zero. They also
  check full-sample interactions, seeded schedules, lagged portfolio weights,
  utility, dollar scaling, output files and all required item names.
- [x] `uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5`
  exited 0 and wrote `output/demo/costs.csv`, `figure_D5.csv`, `figure_D5.pdf`
  and `costs.metadata.json`. The plotted CSV has **10,000 rows**. The PDF is
  **17,461 bytes**, starts with a valid PDF header, and was rendered with
  `pdftoppm` and visually checked. Its title, signed axis labels, histogram
  and mean legend are readable without clipping. All demo artifacts are ignored.
- [x] The exact requested pandas print command exited 0 and printed **203
  rows with 203 unique items**, indexed 0 through 202. The table includes all
  paper-notes §3.8 items: Calendar, 26 Threshold costs, their range and average,
  fixed-1%-size costs, headline, T−4, pre/post-2006, full-sample alternatives,
  random mean/median/95% interval/tracking error, both dollar bases and per-household
  costs, and all three utility levels with both buy-and-hold comparisons.

The complete exact Verify block exited **0** at implementation revision
`7708cc97794b6e86e3a997604ffd66018031e53e`, after a conflict-free rebase onto
`origin/main`:

```sh
uv run pytest -q tests/test_costs.py
uv run python3 -m rebal.exhibits --all --demo --only costs figure_D5
uv run python3 -c "import pandas as pd; print(pd.read_csv('output/demo/costs.csv').to_string())"
```

Start and final tail from this session's Verify log:

```text
...........                                                              [100%]
11 passed in 8.38s
1 exhibit modules
[paths for costs.csv, figure_D5.csv, figure_D5.pdf, costs.metadata.json]
...
195                      per_household_fed_z1  1.657776e+03       USD/household/year                                                 Two-thirds of 127M households
196                                households  1.270000e+08               households                                                        Census 2022; paper D27
197                   household_participation  6.666667e-01                 fraction                                                                SCF; paper D27
198                          utility_buy_hold  3.871470e+02                 bps/year                               Gross arithmetic mean-variance utility; gamma=3
199                     utility_threshold_025  4.164459e+02                 bps/year                               Gross arithmetic mean-variance utility; gamma=3
200                          utility_calendar  4.155946e+02                 bps/year                               Gross arithmetic mean-variance utility; gamma=3
201          utility_threshold_minus_buy_hold  2.929890e+01                 bps/year                                         Footnote 36; gross utility difference
202           utility_calendar_minus_buy_hold  2.844753e+01                 bps/year                                         Footnote 36; gross utility difference
```

Additional local verification at the same revision:

- `uv run pytest -q`: **109 passed in 174.83s**, exit 0. This includes the
  scaffold's full exhibit-runner smoke test with another 10,000-simulation run.
- Ruff check over both new Python files: **All checks passed!**
- Ruff format check: **2 files already formatted**.
- Module `--help` exits 0. Integration tests exercise `--end latest`, macro
  controls and a different asset base with two simulations.
- `git diff --check` passes; `git check-ignore` confirms all demo outputs stay ignored.

## Summary

Added `rebal.exhibits.costs`, automatically discovered as `costs` and `figure_D5`.
It uses TASK-013 simulations and TASK-014 regressions, preserves full-history
portfolio paths, and aligns next-day outcomes before selecting regression days.
Utility and tracking error use yesterday's post-trade weight, avoiding look-ahead.
The CSV reports signed losses in annual basis points and contains calculation
components as well as results. JSON metadata records sources, parameters and sample.

`docs/methods/costs.md` resolves all four §5.9 questions and cites each D27
constant: Fed Financial Accounts, CRS R47699, SCF, Census and ICI. It documents
full-sample slope sums, fixed-size assumptions, the excluded 2006 transition year,
random-date sampling and the paper's conflicting random-cost sign. CLI flags
expose simulation count, seed, sample end, macro controls and both asset bases.

Demo construction follows the descriptive exhibits: load the synthetic panel
through `rebal.io`, then build actual simulated signals. The scaffold's planted
placeholder signals do not describe executed Threshold trades. Tests plant
known effects on actual simulated signals instead. Demo cost numbers therefore
are software outputs, not a real-data reproduction of the paper's targets.
No unresolved material decision remains. No real data was fetched, no real panel
was run and no cluster job was submitted. TASK-018 owns that follow-up.

Verified implementation: `7708cc97794b6e86e3a997604ffd66018031e53e`.
This outcome is a documentation-only follow-up commit in the same PR.
PR: https://github.com/jesusvillota/replicate/pull/22 into `main`, with marker
`Goal-Task: hmm-rebalancing/TASK-016` and label `goal:hmm-rebalancing`.
GitHub Actions were not read or used. No specs, decisions, other tasks or goal
configuration were changed. No additional follow-up task is proposed.
