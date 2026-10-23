# Table 5: equity segments

`rebal.exhibits.segments` implements paper-notes §3.6 and resolves §5.14.
Inputs follow [the daily panel contract](../contracts/daily_panel.md).
Signals follow [the signal contract](../contracts/signals.md).
Outputs follow [the exhibit contract](../contracts/exhibits.md).

Column `1` uses Russell 1000 versus Russell 2000, with weights 90/10.
Column `2` uses Russell 1000 Value versus Growth, also with weights 90/10.
The paper does not state the Value/Growth weights. We use the same construction
to keep the comparison consistent. `--value-weight 0.5` selects 50/50 instead.
The first named asset receives the stated target weight.

The panel supplies CRSP total returns for IWB, IWM, IWD and IWF.
These ETFs are substitutes for the paper's Russell series. The paper does not
identify its source or state whether it uses price returns or total returns.
We use total returns because they include distributions to the investor.
See [the source map](../data/sources.md), D18. This task does not run the
Russell price-index check.

We subtract daily cash return `rf_3m` from both ETF returns before simulation.
This follows the cash-funded return convention used for the main futures pair.
There is no third portfolio asset. Cash cancels from the return difference,
but affects the simulated weights through the portfolio growth denominator.

`rebal.signals.build` simulates each segment pair separately at its target.
Threshold is the mean deviation across bands from 0% through 2.5%, in 0.1% steps.
Calendar is the deviation before the month-end reset.
The default `clean` timing resets weights at the same close.
`--timing literal` exposes the alternative timing from the shared engine.
The default Momentum averages the medium and slow sign families of the
segment return difference. `--momentum all15` gives each lookback equal weight.
`ret` is the current segment return difference. No futures-pair signal or
precomputed shared signal file enters either segment regression.

The requested sample is 2006-08-17 through 2023-03-17, inclusive.
All earlier available ETF history initializes the signals and Momentum.
The real panel starts both segment histories on 2000-05-30.
Leading and trailing missing history is trimmed separately for each pair.
An interior missing return or cash rate stops the calculation. We never fill
returns or join across missing trading days.

The dependent variable is the next trading day's first-minus-second ETF return.
Regressors use date t; the dependent variable uses date t+1. Both dates must
belong to the requested sample, as in the shared regression toolkit.
The CSV records actual outcome dates and the number of complete pairs, `nobs`.
The paper reports N = 4,175. Our trading calendar and pairing rule can change N.
`--end latest` extends the endpoint without changing the start.

Each regression includes an intercept, Threshold, Calendar, week4,
Calendar × week4, Momentum and current `ret`. Week4 is the last five trading
days of each month, counted before sample selection.
This matches equation (4) and Table 1 column (1).
That column has no external controls: VIX, MOVE, EPU, ADS and Sentiment are excluded.
`--controls all` adds those five controls in levels at date t, using the panel's
existing scaling and missing-value rules. We do not fill them here.
This option makes the more extensive specification available without silently
changing the requested baseline. Missing regression values are removed jointly.

The default errors use White HC1, which adjusts for unequal error variance.
The paper does not identify its HC correction. We follow the main table's HC1
default for consistency. `--se hc0` and `--se hac --hac-lags N` expose alternatives.

The shared demo makes all four ETF returns identical. Our module therefore
creates its own distinct segment returns on the shared demo calendar.
The size pair has planted next-day Threshold and Calendar × week4 coefficients
of −0.4 and −0.3. The Value/Growth pair has zero planted effects.
The fixture generates causal returns first. Estimation then independently
builds the segment signals with the shared engine. Shared demo code is unchanged.
Synthetic results test the code; they are not estimates from market data.

Run the default demo:

```sh
uv run python3 -m rebal.exhibits --all --demo --only table_5
```

Run alternatives through the module CLI:

```sh
uv run python3 -m rebal.exhibits.segments --demo --value-weight 0.5 --controls all
```

The CSV includes all fitted terms in columns `1` and `2`, including `threshold`
and `calendar:week4`. `segments.metadata.json` records input, weights, options,
regressors, actual samples and N. TASK-025 reports a real-data smoke check in its
outcome but commits no real output. TASK-030 owns the final real-data run.
