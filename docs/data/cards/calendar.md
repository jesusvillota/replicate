# Source card: derived trading calendar

Status: available

## Source and storage

D3 uses the common observed return dates of the accepted DEC-001 main pair.
Inputs are documented in [CRSP](crsp.md), [GSW](gsw.md), [Yahoo](yahoo.md),
and [French](french.md). This is a proxy for the paper's futures calendar.

`rebal.panel` derives dates when it builds the two panels. Their `date` columns
are stored in `$REPLICATE_DATA_DIR/processed/daily_panel.parquet` and
`daily_panel_alt.parquet`, outside git. No calendar download is required.

## Transforms and coverage

Keep dates with both selected returns. Remove 2001-09-11 through 2001-09-14.
Never fill returns or add missing sessions. Preserve the earliest common history
for portfolio initialization. The alternative uses the same calendar and must
have both returns on every retained date. Only its `r_es` and `r_ty` columns differ.
`rebal.panel --check` reports observed coverage and counts.
See [panel methods](../../methods/panel.md).

## Known problems

Cash-market and Treasury-curve publication calendars differ from futures trading.
Calendar differences can therefore change the paper's sample size.
