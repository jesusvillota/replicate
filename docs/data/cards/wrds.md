# WRDS source card

Status: blocked pending full CRSP Mutual Funds access or an approved scope change.

## Source, access date and license

Source: https://wrds-www.wharton.upenn.edu/ (PostgreSQL).
Live checks ran on the MacBook on 2026-10-22 UTC (2026-10-23 in Madrid).
Authentication worked without a prompt. No cluster connection was made.

License class: licensed. Any eventual series files must use `licensed_dir("wrds")`.
No series file was written in this session. The inventory contains catalog metadata only.
See [the inventory](../wrds_inventory.md) for all 229 listed libraries and eight relevance checks.

## CRSP fixed-term Treasuries

**CRSP Treasuries are not in our subscription.** Both queries below fail with
`permission denied for schema crsp_a_treasuries` (SQLSTATE `42501`):

```sql
SELECT * FROM crsp.tfz_dly_ft LIMIT 3;
SELECT * FROM crsp.tfz_idx LIMIT 2;
```

The alias tables are visible in the catalog. That visibility does not grant access.
The underlying `crsp_a_treasuries` library is absent from `db.list_libraries()`.

The planned source fields are `caldt`, `kytreasnox` and `tdretadj` in `crsp.tfz_dly_ft`.
Index metadata lives in `crsp.tfz_idx`, including `ttermlbl`, `ttermmin` and `ttermmax`.
No 5-, 7-, 10- or 20-year index ID was verified because metadata row access was denied.
No return units or transformations were inferred from field names alone.

Requested coverage: 1961 to latest, including 1997-09-10 through 2023-03-17.
Observed coverage: unavailable. `treasury_fixed_term.parquet` was not created.
The task explicitly permits this subscription limitation.

## CRSP mutual funds

These row reads all fail with `permission denied for schema crsp_q_mutualfunds`
(SQLSTATE `42501`): `crsp.fund_hdr`, `crsp.fund_hdr_hist`, `crsp.fund_names`,
`crsp.daily_returns` and `crsp.daily_nav_ret`.
The full product uses `ticker`; the readable sample uses `nasdaq`.

The sample is readable through `crspsamp_mf`. These exact filters identify the funds:

```sql
SELECT DISTINCT crsp_fundno, nasdaq
FROM crspsamp_mf.fund_names
WHERE nasdaq IN ('VBMFX', 'VBTLX');

SELECT crsp_fundno, min(chgdt), max(chgenddt)
FROM crspsamp_mf.fund_names
WHERE nasdaq IN ('VBMFX', 'VBTLX')
GROUP BY crsp_fundno;

SELECT crsp_fundno, min(caldt), max(caldt), count(*), count(dret)
FROM crspsamp_mf.daily_nav_ret
WHERE crsp_fundno IN (31239, 31244)
GROUP BY crsp_fundno
ORDER BY crsp_fundno;
```

| Ticker | Fund number | Sample return dates | Rows / nonmissing returns | Sample name-history bounds |
|---|---:|---|---:|---|
| VBMFX | 31239 | 2004-01-02 to 2006-12-29 | 755 / 755 | 2004-12-31 to 2008-05-14 |
| VBTLX | 31244 | 2004-01-02 to 2006-12-29 | 755 / 755 | 2004-12-31 to 2008-05-14 |

The same fund numbers were confirmed through `crspsamp_mf.fund_hdr_hist`.
The sample provides `caldt`, `crsp_fundno`, `dnav` and `dret`.
WRDS labels `dret` as Daily Return per share. No return transformation was applied.
The table above reports coverage of the IDs, not a completed dated ticker join.
Name-history coverage starts after some return observations; an extractor must not
silently assign earlier returns to a ticker without further identity evidence.

The sample cannot supply the planned 1997–2023 comparison. We did not choose a shorter
study period, splice another fund, or treat sample observations as full-product access.
`bond_fund_daily.parquet` was not created. The outcome requests a scope decision or access.

## Futures

The readable Datastream sample is `trsamp_dsfut`, also exposed through `trdssamp`.
Its `wrds_contract_info` table contains 100 sample contracts.
The exact discovery filter was:

```sql
SELECT futcode, contrname, exchtickersymb, contrdate, lasttrddate, expirationdate
FROM trsamp_dsfut.wrds_contract_info
WHERE upper(exchtickersymb) IN ('ES', 'TY', 'ZN')
   OR contrname ILIKE '%S&P%'
   OR contrname ILIKE '%10%TREAS%';
```

Only standard S&P 500 contract `SP`, ID 359638, contract month `0620`, matched.
Its last trading date was 2020-06-18 and its expiration field was null.
This is not E-mini ES. No 10-year Treasury contract matched.
A name search of `wrds_cseries_info` found standard S&P continuous series, not the targets.
The sample's complete `wrds_fut_contract` table has 34,377 rows from 1984-10-01 to
2021-11-17 across unrelated instruments. Those bounds are not ES/TY coverage.

`optionm.futures` and `optionm.futures_price` also appear in the catalog, but actual
row reads return `permission denied for schema optionm_europe`.
No front/second ES/TY series with verified contract months and expiry was available.
`futures_es_ty.parquet` was not created.

## Other providers and known limits

CRSP stock indices and Fama–French factors are readable. Russell data is a limited
monthly Russell Top 200 sample. MSCI samples concern ESG and climate, not index returns.
No ANcerno tables were found. These findings are recorded for later planners;
no ANcerno, MSCI or Russell data was extracted.

The installed WRDS `raw_sql` helper failed before querying, because pandas rejected
its SQLAlchemy connection. Live probes instead used
`db.connection.execute(sqlalchemy.text(sql)).mappings()`.
This avoided changing shared dependencies. A future extractor must test that query path.

No CLI or parsing helpers were committed: this task stopped at the access/scope gate.
