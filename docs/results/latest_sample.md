# Latest sample: footnote 32

The main result holds through **2026-07-31**: Table 1 column (1) keeps both
negative signs and significance at 5%. However, the estimates weaken.
This run does not support the paper's claim that the extended results become stronger.

Footnote 32 states:

> We have extended the sample through 2025 and find that the results become even stronger.

Source: [local paper text, footnote 32](../../ocr/paperextract/Harvey-Mazzoleni-Melone_SSRN_2026_TheUnintendedConsequencesOfRebalancing.md).
Our endpoint is July 2026. This is not a separate test ending in 2025.
Our cash-market proxies also differ from the paper's Bloomberg futures data.
The cause of the weaker estimates is unknown; this comparison does not identify it.

## Samples and method

The real run used `uv run python3 -m rebal.latest`, with `clean` signal timing
and HC1 standard errors. HC1 adjusts uncertainty estimates for unequal return variances.
The existing panel and signals were used without rebuilding them.
See [the method](../methods/latest_sample.md) and
[regression definitions](../methods/regressions.md).

Both requested samples start on 1997-09-10. The `paper_end` window ends on
2023-03-17; the `latest` window ends on 2026-07-31, the panel's last date.
Actual outcome dates start on 1997-09-11 in Table 1 column (1) and Table 3
columns (1) and (3). The next-day return alignment accounts for this difference.
Table 3 columns (2) and (4) require all controls and start on 2002-11-14.
All reported latest specifications end on 2026-07-31. All paper-end specifications
end on 2023-03-17. Missing controls change the available sample; no values are filled.

Below, a coefficient measures the predicted return change per unit of signal.
The t statistic measures that estimate relative to its standard error.
N is the number of daily observations. A two-sided 5% test rejects zero when
the absolute t statistic exceeds 1.959963984540054, under the method's normal approximation.
The tables quote the saved CSV numbers without display rounding.

## Table 1, column (1): stock-minus-bond return

| Signal | 1997–2023 coefficient | 1997–2023 t | N | Latest coefficient | Latest t | N | Significant at 5%, old / latest |
|---|---:|---:|---:|---:|---:|---:|---|
| Threshold | -0.46441444537986687 | -4.012117777680489 | 6317 | -0.4101349210644659 | -3.7502634690368497 | 7152 | Yes / Yes |
| Cal × week4 (`calendar:week4`) | -0.26025581705921746 | -3.418692803568286 | 6317 | -0.2362462490035583 | -3.2273241198579243 | 7152 | Yes / Yes |

Both signs and 5% significance hold. Both coefficients move toward zero,
and both absolute t statistics fall. Thus, neither signal becomes stronger
by these measures. The extension adds 835 observations.

For context, the paper's Table 1 column (1) reports Threshold -0.4144
(standard error 0.1148) and Cal × week4 -0.3029 (standard error 0.0808).
These published values differ from our estimates for the same sample window.

Source: [latest_comparison.csv](../../output/tables/robustness/latest/latest_comparison.csv).
Here `paper_end` means our estimate through the paper's endpoint, not the paper's published estimate.

## Table 3: separate stock and bond returns

Columns (1) and (2) predict the stock proxy return (`r_es`). Columns (3)
and (4) predict the bond proxy return (`r_ty`). Columns (2) and (4) include
all five controls. Each row below refers to one of the two rebalancing signals.

| Column / outcome | Signal | 1997–2023 coefficient | 1997–2023 t | N | Latest coefficient | Latest t | N | Significant at 5%, old / latest |
|---|---|---:|---:|---:|---:|---:|---:|---|
| (1) Stock | Threshold | -0.3685825918549203 | -3.455850719167533 | 6317 | -0.3196375387647175 | -3.174910044424543 | 7152 | Yes / Yes |
| (1) Stock | Cal × week4 | -0.24502849745986957 | -3.4526266980810876 | 6317 | -0.2245104722916116 | -3.291891938960849 | 7152 | Yes / Yes |
| (2) Stock, controls | Threshold | -0.34691710869731796 | -2.8179255732249073 | 5043 | -0.2874813027286825 | -2.5067838722757134 | 5878 | Yes / Yes |
| (2) Stock, controls | Cal × week4 | -0.27285688862513235 | -3.204049608951777 | 5043 | -0.2457660036715297 | -3.0417689114521407 | 5878 | Yes / Yes |
| (3) Bond | Threshold | 0.09583185352494658 | 3.551137791898603 | 6317 | 0.09049738229974832 | 3.5071174453142104 | 7152 | Yes / Yes |
| (3) Bond | Cal × week4 | 0.015227319599347864 | 1.2342775716551315 | 6317 | 0.011735776711946571 | 0.9860872895113619 | 7152 | No / No |
| (4) Bond, controls | Threshold | 0.10619590532501401 | 3.328517224777067 | 5043 | 0.09934100832140073 | 3.2940659924888376 | 5878 | Yes / Yes |
| (4) Bond, controls | Cal × week4 | 0.0072938800598873425 | 0.503159444066469 | 5043 | 0.003014887830113051 | 0.21810286714738303 | 5878 | No / No |

All eight signs hold: negative for stocks and positive for bonds.
The 5% test outcomes also remain unchanged. Both stock effects and the bond
Threshold effect remain significant. The bond Calendar effect is not significant
in either sample, with or without controls. Therefore, the paper's significant
bond Calendar effect is not reproduced in either window.

For context, the paper's Table 3 reports these coefficients and standard errors:

| Signal | (1) Stock | (2) Stock, controls | (3) Bond | (4) Bond, controls |
|---|---|---|---|---|
| Threshold | -0.3302 (0.1062) | -0.3261 (0.1049) | 0.0842 (0.0269) | 0.0841 (0.0270) |
| Cal × week4 | -0.2667 (0.0758) | -0.2671 (0.0762) | 0.0362 (0.0128) | 0.0372 (0.0127) |

The paper marks all eight effects significant at 1%. Our Table 3 estimates
all move toward zero after extension, and all absolute t statistics fall.
They do not support a claim of stronger extended results.

Sources: [paper-end Table 3](../../output/tables/table_3.csv) and
[latest Table 3](../../output/tables/robustness/latest/table_3.csv).
The saved paper-end Tables 1 and 3 were checked against a fresh in-memory
build using the current inputs. The build did not write main exhibits.

The latest outputs, including [run metadata](../../output/tables/robustness/latest/latest.metadata.json),
are confined to `output/tables/robustness/latest/`. No analysis code was changed.
