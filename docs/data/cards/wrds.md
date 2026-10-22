# WRDS and public bond-fund source card

Status: available with the access limits accepted in DEC-002. Full CRSP Mutual
Funds access will not become available. The study remains 1997-09-10–2023-03-17.

## Source, access date and license

WRDS: https://wrds-www.wharton.upenn.edu/ (PostgreSQL). Live checks ran on the
MacBook on 2026-10-22 UTC (2026-10-23 in Madrid). Authentication required no prompt.
No cluster connection was made. [The inventory](../wrds_inventory.md) records
229 libraries, table counts, eight relevance checks and actual row-access probes.

WRDS files use `licensed_dir("wrds")`. Public Yahoo downloads are terms-restricted
and use `licensed_dir("yahoo_bond_funds")`. Both are outside git under
`$REPLICATE_DATA_DIR/licensed/`, default `~/data/replicate/licensed/`.
No downloaded data belongs in this PR.

## Regeneration and outputs

```sh
uv run python3 -m rebal.fetch.wrds_extract --inventory
uv run python3 -m rebal.fetch.wrds_extract --extract
uv run python3 -m rebal.fetch.yahoo_bond_funds
```

The WRDS extractor writes `bond_fund_daily.parquet` and
`bond_fund_daily.metadata.json`, with an `OK` line for each file.
The metadata includes exact SQL, access-probe results, coverage and sample status.
The public fetcher writes these five files for each of VBMFX and VBTLX:

- `<ticker>.json`: original Yahoo daily chart response.
- `<ticker>.csv`: original price and distribution fields.
- `<ticker>.metadata.json`: retrieval time, URL, version, raw SHA-256 and coverage.
- `<ticker>_daily.parquet`: validated daily returns and supporting fields.
- `<ticker>_daily.metadata.json`: lineage and distribution-validation results.

The public command supports `--tickers`, `--retries`, `--skip-existing`,
`--shard i/N` and `--list-remaining`. Existing outputs are validated before skipping.
Repeated downloads overwrite only their own files. Vendor revisions can alter
historical adjusted prices; raw responses and hashes identify each download.

## CRSP fixed-term Treasuries

**CRSP Treasuries are not in our subscription.** These queries return
`permission denied for schema crsp_a_treasuries` (SQLSTATE `42501`):

```sql
SELECT * FROM crsp.tfz_dly_ft LIMIT 1;
SELECT * FROM crsp.tfz_idx LIMIT 1;
```

Catalog aliases do not grant row access. Planned fields are `caldt`, `kytreasnox`
and `tdretadj`; index labels are in `tfz_idx`. No 5-, 7-, 10- or 20-year index ID
or return units could be verified. Requested coverage is 1961 to latest,
including the full study period. No `treasury_fixed_term.parquet` is created.
The extractor stops for inspection if Treasury access changes.

## CRSP mutual funds: limited sample only

`crsp.fund_hdr` and `crsp.daily_returns` deny access to `crsp_q_mutualfunds`.
Earlier probes also denied `crsp.fund_hdr_hist`, `fund_names` and `daily_nav_ret`.
Full-product headers use `ticker`; sample headers use `nasdaq`.
The extractor selects IDs from dated sample headers, without hard-coded fund IDs:

```sql
SELECT crsp_fundno, nasdaq, chgdt, chgenddt, first_offer_dt
FROM crspsamp_mf.fund_hdr_hist
WHERE nasdaq IN ('VBMFX', 'VBTLX')
ORDER BY crsp_fundno, chgdt;

SELECT crsp_fundno, caldt, dnav, dret
FROM crspsamp_mf.daily_nav_ret
WHERE crsp_fundno IN (
    SELECT crsp_fundno FROM crspsamp_mf.fund_hdr_hist
    WHERE nasdaq IN ('VBMFX', 'VBTLX')
)
ORDER BY caldt, crsp_fundno;
```

| Candidate ticker | Fund ID | Return dates | Rows | Dated ticker matches |
|---|---:|---|---:|---:|
| VBMFX | 31239 | 2004-01-02–2006-12-29 | 755 | 504 |
| VBTLX | 31244 | 2004-01-02–2006-12-29 | 755 | 504 |

The file contains 1,510 rows. Each row has `is_sample=true` and
`source_library=crspsamp_mf`. `ret` preserves `dret` as a decimal ratio;
`nav` preserves `dnav` in dollars per share. Keys are `date, crsp_fundno`.
Missing/invalid values, duplicate keys, ambiguous IDs and overlapping headers fail.

Headers span 2004-12-31–2008-05-14. We retain the 502 earlier fund-ID rows but
leave `ticker` null and set `ticker_date_verified=false`. `candidate_ticker`
records the ID-level identity only. Consumers requiring a dated ticker must
filter `ticker_date_verified`; no ticker date is silently backfilled.

The [CRSP Mutual Fund Database Guide](https://indexes.morningstar.com/api/docs/6a46d1e69bb8191824e38fa2),
effective 2026-06-30, page 9, defines `dret` as “Total daily return per share.”
It includes reinvested dividends, net of management expenses and 12b fees;
front and rear load fees are excluded. No NAV percentage-change substitution is used.
The guide states that daily availability begins 1998-09-02, even for the full product.

## Public fund-history searches

All sources below were checked on 2026-10-22 UTC. Both target tickers were searched
at Vanguard and Yahoo. Public access does not imply redistribution permission.

| Source and exact route | Live result | Return definition and usable coverage |
|---|---|---|
| Vanguard [VBMFX profile](https://investor.vanguard.com/investment-products/mutual-funds/profile/vbmfx) and [VBTLX profile](https://investor.vanguard.com/investment-products/mutual-funds/profile/vbtlx) | HTTP 200. Embedded `distributions.incomeCapitalGains` contains only 18 distributions per fund, 2025-04-30–2026-09-30. | Official cash distributions, insufficient to rebuild study-period daily total returns. |
| Vanguard [VBMFX-AdditionalFundData](https://investor.vanguard.com/irr/funds/profile/VBMFX-AdditionalFundData) and [VBTLX-AdditionalFundData](https://investor.vanguard.com/irr/funds/profile/VBTLX-AdditionalFundData) | HTTP 200. `historicalPrice["1Y"]["nav"]`: 251 daily observations, 2025-10-22–2026-10-21. `historicalPrice["10Y"]["nav"]`: 120 monthly observations, 2016-10-31–2026-09-30. | Raw NAV, not total return. Neither frequency/coverage combination supplies the study. |
| Yahoo [VBMFX chart](https://query2.finance.yahoo.com/v8/finance/chart/VBMFX) and [VBTLX chart](https://query2.finance.yahoo.com/v8/finance/chart/VBTLX) | Successful daily `period="max"` download through yfinance, with original responses retained. HTML history returned HTTP 429, but the chart route worked. | Usable adjusted prices and cash-event fields; verified below. No login was needed. |
| Stooq [VBTLX daily CSV](https://stooq.com/q/d/l/?s=vbtlx.us&i=d) | HTTP 404. | No history obtained; no assumption about distributions or coverage. |

### Verified public return calculation

`rebal.fetch.yahoo_bond_funds` reuses the source-specific Yahoo downloader with
`interval="1d"`, `auto_adjust=False`, `back_adjust=False`, `repair=False`, and
`rounding=False`. It computes `ret = Adj Close_t / Adj Close_(t-1) - 1`.
[Yahoo's adjustment definition](https://help.yahoo.com/kb/SLN28256.html) (HTTP 200)
explicitly includes dividend distributions and splits. For these downloads,
split counts and separately reported capital gains are zero. The code includes
both `Dividends` and `Capital Gains` in the validation, and rejects unreviewed splits.

Every noninitial adjusted return is checked against Yahoo's event formula:
`Close_t / (Close_(t-1) - Dividends_t - Capital Gains_t) - 1`.
Tolerance is `1e-5` in decimal returns. Raw NAV returns fail this test on distribution
days. Missing prices/events, duplicate or unsorted dates, nonfinite values and
missing study boundaries also fail. The first observation has no prior price,
so its return stays missing. Returns are never filled.

| Fund | Price rows | Price coverage | First usable return | Study price rows | Study distribution days |
|---|---:|---|---|---:|---:|
| VBMFX | 10,041 | 1986-12-11–2026-10-21 | 1986-12-12 | 6,422 | 316 |
| VBTLX | 6,275 | 2001-11-12–2026-10-21 | 2001-11-13 | 5,373 | 249 |

VBMFX has valid returns on both 1997-09-10 and 2023-03-17. VBTLX cannot supply the
1997–2001 interval; its first study price also has a missing return.
Live maximum distribution-check errors were below `4e-6` for both full histories.
Exact run-specific errors appear in each `_daily.metadata.json`.

For example, on 2023-02-28, VBMFX's raw NAV return was about `0.00105488` while
its adjusted return was about `0.00327743`, including the reported $0.021 distribution.
VBTLX reported $0.022 and an adjusted return about `0.00338327`.
These are **Yahoo distribution-adjusted returns**, not exact official NAV returns.
Yahoo uses a multiplicative adjustment and rounds distributions. For example,
Vanguard's 2026-09-30 payments were $0.03204488/$0.032891918 for VBMFX/VBTLX;
Yahoo reports $0.032/$0.033. Its convention differs slightly from
`(NAV_t + cash_t) / NAV_(t-1) - 1`. These limits matter for exact replication.

### Handoff to TASK-012

Use `licensed_dir("yahoo_bond_funds") / "VBMFX_daily.parquet"`, columns `date, ret`,
as the available full-study broad bond-fund candidate for `r_agg`. This is a
recommendation for TASK-012 to assess and document, not a change to the source map.
VBTLX is a later-starting share class and can serve as an overlap check.
Do not let the short WRDS sample replace longer usable public history.

Both funds track a broad U.S. investment-grade bond portfolio, but fund expenses,
benchmark differences and the vendor return convention distinguish them from the
paper's Bloomberg U.S. Aggregate Total Return Index. No cross-source splice was made.

If the public history later becomes unusable, the available fallback is CRSP AGG
from TASK-009: PERMNO 89848, 5,747 observations, 2003-09-26–2026-07-31, per
[the CRSP card](crsp.md). AGG is an ETF broad aggregate-bond proxy with expenses,
tracking differences and market-price effects. It leaves 1997-09-10–2003-09-25
uncovered. Leave gaps missing; do not shorten the main study or forward-fill returns.
ES/TY proxy choices remain with TASK-011/DEC-001.

## Futures and other products

`trsamp_dsfut.wrds_contract_info` is readable, also aliased through `trdssamp`.
The search filters symbols `ES`, `TY`, `ZN`, or names containing `S&P` or
`10%TREAS`. Only standard S&P contract `SP`, ID 359638, month `0620`, matched;
last trading date is 2020-06-18 and expiry is null. It is not E-mini ES.
No verified front/second ES/TY contracts were found. `optionm.futures_price`
denies access to `optionm_europe`. No `futures_es_ty.parquet` is created.
The extractor fails for inspection if target contract symbols appear later.

CRSP stock indices and Fama–French factors are readable. Russell data is a
limited monthly Russell Top 200 sample. MSCI samples concern ESG/climate,
not the required index. No ANcerno catalog match was found. These findings
are for later planners; no ANcerno, MSCI or Russell series was extracted.

The installed WRDS `raw_sql` helper is incompatible with this pandas/SQLAlchemy
combination. Queries use `db.connection.execute(sqlalchemy.text(sql))` and fetch
rows directly. Failed probes roll back through the underlying database connection,
which also works with the installed legacy SQLAlchemy connection. Only explicit
permission or missing-catalog SQLSTATEs become access limits; network errors fail.
