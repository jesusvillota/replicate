"""uv run python3 -m rebal.fetch.wrds_extract --inventory
uv run python3 -m rebal.fetch.wrds_extract --extract

CLI arguments: --inventory refreshes the library catalog and access probes;
--extract writes the approved limited mutual-fund sample (either or both modes).

Reads WRDS on the MacBook. Writes docs/data/wrds_inventory.md and licensed WRDS
sample parquet/metadata. No full-product or futures coverage is inferred from aliases.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import duckdb
import pandas as pd
import wrds
from rich.console import Console
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from rebal.fetch.common import summarize
from rebal.paths import REPO_ROOT, licensed_dir

console = Console(highlight=False)
HEADER_SQL = """
SELECT crsp_fundno, nasdaq, chgdt, chgenddt, first_offer_dt
FROM crspsamp_mf.fund_hdr_hist
WHERE nasdaq IN ('VBMFX', 'VBTLX')
ORDER BY crsp_fundno, chgdt
"""
RETURNS_SQL = """
SELECT crsp_fundno, caldt, dnav, dret
FROM crspsamp_mf.daily_nav_ret
WHERE crsp_fundno IN (
    SELECT crsp_fundno FROM crspsamp_mf.fund_hdr_hist
    WHERE nasdaq IN ('VBMFX', 'VBTLX')
)
ORDER BY caldt, crsp_fundno
"""
FUTURES_SQL = """
SELECT futcode, contrname, exchtickersymb, contrdate, lasttrddate, expirationdate
FROM trsamp_dsfut.wrds_contract_info
WHERE upper(exchtickersymb) IN ('ES', 'TY', 'ZN')
   OR contrname ILIKE '%S&P%' OR contrname ILIKE '%10%TREAS%'
"""
PROBES = {
    "treasury_returns": "SELECT * FROM crsp.tfz_dly_ft LIMIT 1",
    "treasury_ids": "SELECT * FROM crsp.tfz_idx LIMIT 1",
    "full_fund_header": "SELECT * FROM crsp.fund_hdr LIMIT 1",
    "full_fund_returns": "SELECT * FROM crsp.daily_returns LIMIT 1",
    "sample_header": HEADER_SQL,
    "sample_returns": "SELECT * FROM crspsamp_mf.daily_nav_ret LIMIT 1",
    "sp500": "SELECT * FROM crsp.dsp500 LIMIT 1",
    "stock_index": "SELECT * FROM crsp.dsi LIMIT 1",
    "futures": FUTURES_SQL,
    "optionmetrics": "SELECT * FROM optionm.futures_price LIMIT 1",
    "russell": "SELECT * FROM ftsesamp.ctr_monthly_us LIMIT 1",
    "factors": "SELECT * FROM ff.factors_daily LIMIT 1",
}


def query(db, sql: str) -> pd.DataFrame:
    """Avoid WRDS raw_sql's pandas/SQLAlchemy compatibility path."""
    result = db.connection.execute(text(sql))
    return pd.DataFrame(result.fetchall(), columns=result.keys())


def probe(db, sql: str) -> dict:
    """Only explicit server permission/catalog errors mean unavailable."""
    try:
        frame = query(db, sql)
    except DBAPIError as exc:
        db.connection.connection.rollback()
        code = getattr(exc.orig, "pgcode", None)
        if code not in {"42501", "42P01", "3F000"}:
            raise
        return {
            "available": False,
            "sqlstate": code,
            "reason": str(exc.orig).splitlines()[0],
            "sql": sql,
        }
    return {
        "available": True,
        "rows": len(frame),
        "sql": sql,
        "records": frame.to_dict("records"),
    }


def access_checks(db) -> dict:
    return {name: probe(db, sql) for name, sql in PROBES.items()}


def inventory(db, path: Path) -> None:
    libraries = sorted(db.list_libraries())
    catalog = {}
    for library in libraries:
        # Failure is explicit; a transport error must not become a missing subscription.
        catalog[library] = sorted(db.list_tables(library=library))
    checks = access_checks(db)
    yes = lambda key: "**Yes**" if checks[key]["available"] else "**No**"
    rows = [
        (
            "Futures prices: ES / 10-year T-note",
            "**No**",
            (
                "`trsamp_dsfut.wrds_contract_info`: matched contracts below; standard SP is not ES. "
                "`optionm.futures_price`: see access probe."
            ),
        ),
        (
            "CRSP Treasuries",
            yes("treasury_returns"),
            "`crsp.tfz_dly_ft`, `crsp.tfz_idx`",
        ),
        (
            "CRSP Mutual Funds",
            f"{yes('full_fund_returns')} (full); {yes('sample_returns')} (sample)",
            (
                "`crsp.fund_hdr`, `crsp.daily_returns`; `crspsamp_mf.fund_hdr_hist`, `daily_nav_ret`. "
                "Sample only, 2004–2006; see source card."
            ),
        ),
        ("CRSP index files", yes("stock_index"), "`crsp.dsp500`, `crsp.dsi`"),
        (
            "MSCI index data",
            "**No**",
            "Catalog MSCI samples concern ESG/climate/issuers, not ACWI ex USA returns.",
        ),
        (
            "Russell / FTSE index data",
            yes("russell") + " (sample only)",
            "`ftsesamp.ctr_monthly_us`: monthly Russell Top 200 sample, not daily target indices.",
        ),
        (
            "ANcerno (Abel Noser)",
            "**No**",
            "No matching library/table in catalog search below.",
        ),
        ("Fama–French factors", yes("factors"), "`ff.factors_daily`"),
    ]
    futures = checks["futures"].get("records", [])
    if any(
        str(r["exchtickersymb"]).strip().upper() in {"ES", "TY", "ZN"} for r in futures
    ):
        raise ValueError("New ES/TY contracts found: inspect before reporting coverage")
    matches = [
        f"{lib}.{table}"
        for lib, tables in catalog.items()
        for table in tables
        if any(
            term in f"{lib}.{table}".lower() for term in ("ancerno", "abel", "noser")
        )
    ]
    if matches:
        raise ValueError(f"New ANcerno candidates require inspection: {matches}")
    lines = [
        "# WRDS library inventory",
        "",
        f"Observed on {datetime.now(UTC):%Y-%m-%d} UTC from the MacBook.",
        "",
        f"`db.list_libraries()` returned {len(libraries)} libraries; all table listings succeeded.",
        "Listed aliases do not prove row access. Relevant tables were probed below.",
        "",
        "## Libraries",
        "",
        "| Library | Listed tables/views |",
        "|---|---:|",
    ]
    lines += [f"| `{lib}` | {len(tables)} |" for lib, tables in catalog.items()]
    lines += [
        "",
        "## Relevant to this replication",
        "",
        "| Item | Available? | Tables and observed limits |",
        "|---|---|---|",
    ]
    lines += [
        f"| {item} | {available} | {detail} |" for item, available, detail in rows
    ]
    lines += ["", "### Live access probes", ""]
    for name, check in checks.items():
        detail = (
            f"readable ({check['rows']} probe rows)"
            if check["available"]
            else f"SQLSTATE {check['sqlstate']}: {check['reason']}"
        )
        sql = " ".join(check["sql"].split())
        lines += [f"- `{name}`: {detail}. Query: `{sql}`"]
    lines += [
        "",
        "Futures metadata matches (not extracted):",
        "```json",
        json.dumps(futures, indent=2, default=str),
        "```",
        "",
        "MSCI catalog tables (no index-return product found):",
        "",
    ]
    lines += [
        f"- `{lib}`: " + ", ".join(f"`{table}`" for table in tables)
        for lib, tables in catalog.items()
        if "msci" in lib
    ]
    lines += [
        "",
        "ANcerno/Abel/Noser catalog matches: none.",
        "",
        "Regenerate with `uv run python3 -m rebal.fetch.wrds_extract --inventory`.",
        "See [the source card](cards/wrds.md) for coverage and subscription limits.",
        "",
    ]
    path.write_text("\n".join(lines))
    console.print(f"OK {path} libraries={len(libraries)}", markup=False, soft_wrap=True)


def parse_sample(headers: pd.DataFrame, returns: pd.DataFrame) -> pd.DataFrame:
    """Keep all fund-ID returns, but assign a ticker only within dated headers."""
    # pandas: validate small WRDS inputs and normalize dates before SQL registration.
    headers, returns = headers.copy(), returns.copy()
    for column in ("chgdt", "chgenddt", "first_offer_dt"):
        headers[column] = pd.to_datetime(
            headers[column], format="ISO8601", errors="raise"
        )
    returns["caldt"] = pd.to_datetime(
        returns["caldt"], format="ISO8601", errors="raise"
    )
    if headers.empty or returns.empty or headers.isna().any().any():
        raise ValueError("Empty sample or missing header identity/date")
    if set(headers.nasdaq) != {"VBMFX", "VBTLX"}:
        raise ValueError("Expected both VBMFX and VBTLX headers")
    if returns.isna().any().any() or (headers.chgdt > headers.chgenddt).any():
        raise ValueError("Missing sample values or invalid header dates")
    if returns.duplicated(["crsp_fundno", "caldt"]).any():
        raise ValueError("Duplicate fund/date")
    with duckdb.connect() as con:
        con.register("headers", headers)
        con.register("returns", returns)
        invalid = con.execute("""
            SELECT count(*) FROM returns
            WHERE NOT isfinite(dret) OR dret < -1 OR NOT isfinite(dnav) OR dnav <= 0
               OR crsp_fundno != trunc(crsp_fundno)
        """).fetchone()[0]
        ambiguous = con.execute("""
            SELECT crsp_fundno FROM headers GROUP BY crsp_fundno
            HAVING count(DISTINCT nasdaq) != 1
        """).fetchall()
        if invalid or ambiguous:
            raise ValueError("Invalid return/NAV/fund ID or ambiguous ticker identity")
        frame = con.execute("""
            WITH identity AS (
                SELECT DISTINCT crsp_fundno, nasdaq FROM headers
            )
            SELECT r.caldt AS date, r.crsp_fundno::BIGINT AS crsp_fundno,
                   h.nasdaq AS ticker, i.nasdaq AS candidate_ticker,
                   h.nasdaq IS NOT NULL AS ticker_date_verified,
                   r.dnav::DOUBLE AS nav, r.dret::DOUBLE AS ret,
                   true AS is_sample, 'crspsamp_mf' AS source_library
            FROM returns r
            JOIN identity i USING (crsp_fundno)
            LEFT JOIN headers h ON r.crsp_fundno = h.crsp_fundno
                AND r.caldt BETWEEN h.chgdt AND h.chgenddt
                AND r.caldt >= h.first_offer_dt
            ORDER BY date, crsp_fundno
        """).fetchdf()
    if len(frame) != len(returns) or frame.duplicated(["date", "crsp_fundno"]).any():
        raise ValueError("Unmatched IDs or overlapping dated headers")
    return frame


def extract(db, directory: Path) -> None:
    checks = access_checks(db)
    if checks["treasury_returns"]["available"] or checks["treasury_ids"]["available"]:
        raise ValueError(
            "Treasury access changed; verify index IDs/units before extraction"
        )
    futures = checks["futures"].get("records", [])
    if any(
        str(r["exchtickersymb"]).strip().upper() in {"ES", "TY", "ZN"} for r in futures
    ):
        raise ValueError("Futures access changed; verify contracts before extraction")
    frame = parse_sample(query(db, HEADER_SQL), query(db, RETURNS_SQL))
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "bond_fund_daily.parquet"
    temporary = path.with_suffix(".tmp.parquet")
    try:
        frame.to_parquet(temporary, index=False)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    summarize(path, "date", key_cols=("crsp_fundno",))
    metadata = {
        "script": __name__,
        "downloaded_utc": datetime.now(UTC).isoformat(),
        "is_sample": True,
        "source_library": "crspsamp_mf",
        "header_query": HEADER_SQL,
        "returns_query": RETURNS_SQL,
        "return_definition": "CRSP dret, decimal daily total return; unchanged",
        "rows": len(frame),
        "first": str(frame.date.min().date()),
        "last": str(frame.date.max().date()),
        "undated_ticker_rows": int((~frame.ticker_date_verified).sum()),
        "identity_rule": "ticker is null outside header dates; candidate_ticker is ID-only",
        "access_probes": checks,
    }
    meta_path = path.with_suffix(".metadata.json")
    meta_path.write_text(json.dumps(metadata, indent=2, default=str) + "\n")
    console.print(f"OK {meta_path} sample=true", markup=False, soft_wrap=True)
    console.print(
        "SKIP treasury_fixed_term.parquet: no CRSP Treasury subscription. "
        "SKIP futures_es_ty.parquet: no verified ES/TY contracts.",
        markup=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--inventory", action="store_true", help="Refresh catalog and access probes."
    )
    parser.add_argument(
        "--extract", action="store_true", help="Extract approved limited fund sample."
    )
    args = parser.parse_args()
    if not (args.inventory or args.extract):
        parser.error("choose --inventory and/or --extract")
    db = wrds.Connection(
        wrds_username=os.getenv("WRDS_USERNAME") or os.getenv("PGUSER")
    )
    try:
        if args.inventory:
            inventory(db, REPO_ROOT / "docs/data/wrds_inventory.md")
        if args.extract:
            extract(db, licensed_dir("wrds"))
    finally:
        db.close()


if __name__ == "__main__":
    main()
