"""Extract licensed CRSP series with bounded annual DuckDB scans.

Commands:
    uv run python3 -m rebal.fetch.crsp_cluster --demo
    cluster-kit launch src/rebal/fetch/crsp_cluster.py --partition cpu_shared \
        --slurm-cpus 4 --slurm-mem 16G --slurm-time 01:00:00

CLI arguments:
    --input-dir: CRSP root containing data/ and security_history/.
    --output-dir: destination (default: cluster replicate-data/licensed/crsp).
    --skip-existing: reuse validated annual ETF and dispersion parts.
    --shard i/N: annual slice; merge only when all annual parts exist.
    --list-remaining: list this slice without extracting.
    --threads: DuckDB CPUs (default: SLURM_CPUS_PER_TASK or 4).
    --demo: build synthetic inputs and check the complete extraction in a tempdir.

Reads tape-kit research parquets directly, without a tape-kit dependency.
Writes three daily parquets and extraction.json outside git. Processing only.
"""

import argparse
import hashlib
import json
import os
from datetime import UTC, date, datetime
from pathlib import Path
from statistics import stdev
from tempfile import TemporaryDirectory

import duckdb
from rich.console import Console

TICKERS = (
    "SPY",
    "IVV",
    "IEF",
    "TLT",
    "AGG",
    "IWB",
    "IWM",
    "IWD",
    "IWF",
    "EFA",
    "VEU",
    "ACWX",
)
INPUT_ROOT = Path("/mnt/slurm-beegfs/Users/j-vill36/tape-kit-data/crsp")
OUTPUT_ROOT = Path("/mnt/slurm-beegfs/Users/j-vill36/replicate-data/licensed/crsp")
DISPERSION_START = date(1997, 9, 10)
CONSOLE = Console()
ETF_COLUMNS = ["date", "ticker", "permno", "ret", "retx", "prc", "vol"]
DISPERSION_COLUMNS = ["date", "ivol", "ivol_w", "n_stocks"]
BENCHMARK_COLUMNS = ["date", "vwretd", "vwretx", "ewretd", "ewretx", "sprtrn"]
# Explicit historical CIZ equivalent of SHRCD 10/11; no price/volume screen.
COMMON_STOCK = """
    sharetype = 'NS' AND securitytype = 'EQTY' AND securitysubtype = 'COM'
    AND usincflg = 'Y' AND issuertype IN ('ACOR', 'CORP')
    AND primaryexch IN ('N', 'A', 'Q')
    AND isfinite(dlyret) AND dlyret >= -1
    AND dlyretdurflg IN ('D1', 'D2', 'D3', 'D4', 'DU')
"""


def validate(
    con, path: Path, columns: list[str], keys: str, *, empty: bool = False
) -> int:
    """Reject incomplete schemas, null keys, duplicate dates, and invalid measures."""
    actual = [
        r[0]
        for r in con.execute(
            "DESCRIBE SELECT * FROM read_parquet(?)", [str(path)]
        ).fetchall()
    ]
    if actual != columns:
        raise ValueError(f"{path}: columns {actual}, expected {columns}")
    n, unique, null_dates = con.execute(
        f"SELECT count(*), count(DISTINCT ({keys})), count(*) FILTER (WHERE date IS NULL) FROM read_parquet(?)",
        [str(path)],
    ).fetchone()
    if (not n and not empty) or n != unique or null_dates:
        raise ValueError(f"{path}: invalid rows/keys: {n}, {unique}, {null_dates}")
    if columns == DISPERSION_COLUMNS:
        bad = con.execute(
            """SELECT count(*) FROM read_parquet(?) WHERE
            n_stocks < 2 OR ivol IS NULL OR ivol_w IS NULL
            OR NOT isfinite(ivol) OR NOT isfinite(ivol_w) OR ivol < 0 OR ivol_w < 0""",
            [str(path)],
        ).fetchone()[0]
        if bad:
            raise ValueError(f"{path}: {bad} invalid dispersion rows")
    if columns == ETF_COLUMNS:
        bad = con.execute(
            "SELECT count(*) FROM read_parquet(?) WHERE ticker IS NULL OR permno IS NULL",
            [str(path)],
        ).fetchone()[0]
        if bad:
            raise ValueError(f"{path}: null ETF identifiers")
    return n


def write_parquet(
    con,
    query: str,
    params: list,
    path: Path,
    columns: list[str],
    keys: str,
    *,
    empty: bool = False,
) -> None:
    """Publish only a fully written, validated parquet."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp.parquet")
    try:
        con.execute(
            f"COPY ({query}) TO ? (FORMAT PARQUET, COMPRESSION ZSTD)",
            [*params, str(temporary)],
        )
        validate(con, temporary, columns, keys, empty=empty)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def resolve_etfs(con, history: Path) -> None:
    con.execute(
        """CREATE TEMP TABLE etf_history AS
        SELECT DISTINCT ticker, permno, secinfostartdt, secinfoenddt
        FROM read_parquet(?) WHERE ticker IN (SELECT unnest(?))
        AND securitytype = 'FUND' AND securitysubtype = 'ETF'""",
        [str(history), list(TICKERS)],
    )
    rows = con.execute(
        "SELECT ticker, count(DISTINCT permno) FROM etf_history GROUP BY ticker"
    ).fetchall()
    if dict(rows) != dict.fromkeys(TICKERS, 1):
        raise ValueError(f"Expected one ETF PERMNO per ticker, found {rows}")
    overlap = con.execute("""SELECT count(*) FROM (
        SELECT secinfostartdt, lag(secinfoenddt) OVER (
            PARTITION BY ticker ORDER BY secinfostartdt) AS previous_end
        FROM etf_history) WHERE secinfostartdt <= previous_end""").fetchone()[0]
    if overlap:
        raise ValueError("Overlapping ETF security-history intervals")


def annual_parts(output: Path, year: str) -> tuple[Path, Path]:
    return (
        output / "parts" / "etf" / f"{year}.parquet",
        output / "parts" / f"{year}.parquet",
    )


def complete_parts(con, output: Path, year: str) -> bool:
    etf, dispersion = annual_parts(output, year)
    try:
        validate(con, etf, ETF_COLUMNS, "date, ticker", empty=True)
        validate(con, dispersion, DISPERSION_COLUMNS, "date", empty=True)
        return True
    except (OSError, ValueError, duckdb.Error):
        return False


def extract(
    input_dir: Path,
    output: Path,
    *,
    skip_existing: bool = False,
    threads: int = 4,
    shard: tuple[int, int] = (1, 1),
    list_remaining: bool = False,
) -> dict:
    daily = sorted(
        p
        for p in (input_dir / "data/daily").glob("[0-9][0-9][0-9][0-9].parquet")
        if int(p.stem) >= 1993
    )
    benchmarks = sorted(
        p
        for p in (input_dir / "data/benchmarks").glob("[0-9][0-9][0-9][0-9].parquet")
        if int(p.stem) >= 1960
    )
    if not daily or not benchmarks:
        raise FileNotFoundError(f"Missing yearly CRSP research files under {input_dir}")
    # This repo has no DuckDBManager. Configure one scoped connection explicitly.
    with (
        TemporaryDirectory(
            prefix="crsp-duckdb-", dir=os.environ.get("TMPDIR")
        ) as scratch,
        duckdb.connect(
            config={
                "threads": threads,
                "memory_limit": "12GB",
                "temp_directory": scratch,
                "preserve_insertion_order": False,
            }
        ) as con,
    ):
        units = daily[shard[0] - 1 :: shard[1]]
        remaining = [
            p
            for p in units
            if not (skip_existing and complete_parts(con, output, p.stem))
        ]
        CONSOLE.log(f"Annual work: {[p.stem for p in remaining]}")
        if list_remaining:
            return {}
        resolve_etfs(con, input_dir / "security_history/security_info.parquet")
        for path in remaining:
            etf, dispersion = annual_parts(output, path.stem)
            write_parquet(
                con,
                """SELECT d.dlycaldt AS date, h.ticker, d.permno,
                d.dlyret AS ret, d.dlyretx AS retx, d.dlyprc AS prc, d.dlyvol AS vol
                FROM read_parquet(?) d JOIN etf_history h ON d.permno = h.permno
                AND d.dlycaldt BETWEEN h.secinfostartdt AND h.secinfoenddt
                ORDER BY date, ticker""",
                [str(path)],
                etf,
                ETF_COLUMNS,
                "date, ticker",
                empty=True,
            )
            write_parquet(
                con,
                f"""WITH eligible AS (
                SELECT dlycaldt AS date, dlyret AS ret FROM read_parquet(?)
                WHERE {COMMON_STOCK} AND dlycaldt >= ?
            ), bounds AS (
                SELECT date, quantile_cont(ret, 0.01) AS lo,
                    quantile_cont(ret, 0.99) AS hi FROM eligible GROUP BY date
            ) SELECT date, stddev_samp(ret) AS ivol,
                stddev_samp(greatest(lo, least(hi, ret))) AS ivol_w,
                count(*) AS n_stocks FROM eligible JOIN bounds USING (date)
                GROUP BY date ORDER BY date""",
                [str(path), DISPERSION_START],
                dispersion,
                DISPERSION_COLUMNS,
                "date",
                empty=True,
            )
            CONSOLE.log(f"Completed {path.stem}")
        if not all(complete_parts(con, output, p.stem) for p in daily):
            CONSOLE.log("Annual slice finished; merge awaits the remaining parts")
            return {}
        for index, name, columns, keys in [
            (0, "etf_daily", ETF_COLUMNS, "date, ticker"),
            (1, "dispersion_daily", DISPERSION_COLUMNS, "date"),
        ]:
            paths = [str(annual_parts(output, p.stem)[index]) for p in daily]
            write_parquet(
                con,
                f"SELECT {', '.join(columns)} FROM read_parquet(?) ORDER BY {keys}",
                [paths],
                output / f"{name}.parquet",
                columns,
                keys,
            )
        write_parquet(
            con,
            """SELECT dlycaldt AS date, vwretd, vwretx, ewretd, ewretx, sprtrn
            FROM read_parquet(?) WHERE dlycaldt >= DATE '1960-01-01' ORDER BY date""",
            [[str(p) for p in benchmarks]],
            output / "benchmarks_daily.parquet",
            BENCHMARK_COLUMNS,
            "date",
        )
        rows = con.execute(
            """SELECT ticker, permno, count(*), min(date), max(date)
            FROM read_parquet(?) GROUP BY ticker, permno ORDER BY ticker""",
            [str(output / "etf_daily.parquet")],
        ).fetchall()
        if {r[0] for r in rows} != set(TICKERS):
            raise ValueError("Missing requested ETFs in output")
        source_metadata = input_dir / "data/metadata.json"
        summary = {
            "extracted_at_utc": datetime.now(UTC).isoformat(),
            "source_metadata_sha256": hashlib.sha256(
                source_metadata.read_bytes()
            ).hexdigest()
            if source_metadata.exists()
            else None,
            "input_dir": str(input_dir),
            "years": [p.stem for p in daily],
            "dispersion_start": str(DISPERSION_START),
            "threads": threads,
            "job_id": os.environ.get("SLURM_JOB_ID"),
            "etfs": rows,
        }
        for row in rows:
            CONSOLE.log(
                f"ticker={row[0]} permno={row[1]} rows={row[2]} first={row[3]} last={row[4]}"
            )
        (output / "extraction.json").write_text(
            json.dumps(summary, default=str, indent=2) + "\n"
        )
        return summary


def make_demo(root: Path) -> None:
    """Small fixture: two years, reused ticker, excluded stocks, and null return."""
    with duckdb.connect() as con:
        con.execute("""CREATE TABLE history (ticker VARCHAR, permno BIGINT,
            secinfostartdt DATE, secinfoenddt DATE, securitytype VARCHAR, securitysubtype VARCHAR)""")
        con.executemany(
            "INSERT INTO history VALUES (?, ?, '1997-09-10', '1998-12-31', 'FUND', 'ETF')",
            [(ticker, 100 + i) for i, ticker in enumerate(TICKERS)],
        )
        con.execute(
            "INSERT INTO history VALUES ('SPY', 999, '1962-01-01', '1998-12-31', 'EQTY', 'COM')"
        )
        history = root / "security_history/security_info.parquet"
        history.parent.mkdir(parents=True)
        con.execute("COPY history TO ? (FORMAT PARQUET)", [str(history)])
        for year, day in [(1997, "1997-09-10"), (1998, "1998-01-02")]:
            # pandas is not needed: fixture values and expected SD are independent.
            con.execute(
                """CREATE OR REPLACE TABLE daily AS
                SELECT ?::DATE AS dlycaldt, i::BIGINT AS permno,
                    CASE WHEN i=1 THEN -0.01 WHEN i=2 THEN 0.02 WHEN i=3 THEN 0.03
                         WHEN i=4 THEN NULL ELSE 0.9 END::DOUBLE AS dlyret,
                    0.005::DOUBLE AS dlyretx, NULL::DOUBLE AS dlyprc, 0.0::DOUBLE AS dlyvol,
                    'NS' AS sharetype, 'EQTY' AS securitytype, 'COM' AS securitysubtype,
                    CASE WHEN i=5 THEN 'N' ELSE 'Y' END AS usincflg,
                    CASE WHEN i=6 THEN 'REIT' WHEN i=1 THEN 'ACOR' ELSE 'CORP' END AS issuertype,
                    CASE WHEN i=7 THEN 'X' ELSE 'Q' END AS primaryexch,
                    CASE WHEN i=8 THEN 'P1' ELSE 'D3' END AS dlyretdurflg
                FROM range(1,9) t(i)""",
                [day],
            )
            con.execute(
                """INSERT INTO daily SELECT ?::DATE, permno, 0.01, 0.005, 100.0, 50.0,
                'NS', securitytype, securitysubtype, 'Y', 'ACOR', 'N', 'D1' FROM history""",
                [day],
            )
            daily = root / f"data/daily/{year}.parquet"
            daily.parent.mkdir(parents=True, exist_ok=True)
            con.execute("COPY daily TO ? (FORMAT PARQUET)", [str(daily)])
            bench = root / f"data/benchmarks/{year}.parquet"
            bench.parent.mkdir(parents=True, exist_ok=True)
            con.execute(
                """COPY (SELECT ?::DATE AS dlycaldt, 0.01 AS vwretd,
                0.005 AS vwretx, 0.02 AS ewretd, 0.015 AS ewretx, 0.009 AS sprtrn)
                TO ? (FORMAT PARQUET)""",
                [day, str(bench)],
            )


def run_demo() -> None:
    with TemporaryDirectory(prefix="crsp-demo-") as directory:
        root = Path(directory)
        make_demo(root / "input")
        extract(root / "input", root / "output")
        with duckdb.connect() as con:
            rows = con.execute(
                "SELECT ivol FROM read_parquet(?) ORDER BY date",
                [str(root / "output/dispersion_daily.parquet")],
            ).fetchall()
            # Reused SPY is an eligible ordinary stock, but never an ETF observation.
            expected = stdev([-0.01, 0.02, 0.03, 0.01])
            if len(rows) != 2 or any(abs(r[0] - expected) > 1e-12 for r in rows):
                raise AssertionError(f"Demo SD mismatch: {rows}, expected {expected}")
        CONSOLE.log(
            "Demo passed: dated ETF joins, annual merge, hand-computed sample SD"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input-dir", type=Path, default=INPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_ROOT)
    parser.add_argument(
        "--threads", type=int, default=int(os.environ.get("SLURM_CPUS_PER_TASK", "4"))
    )
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--shard", default="1/1")
    parser.add_argument("--list-remaining", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    try:
        index, total = map(int, args.shard.split("/"))
        if not 1 <= index <= total or args.threads < 1:
            raise ValueError
    except ValueError:
        parser.error("Use --shard i/N with 1 <= i <= N and positive --threads")
    if args.demo:
        run_demo()
    else:
        if not os.environ.get("SLURM_JOB_ID") and not args.list_remaining:
            parser.error("Real extraction must run in a SLURM job; use --demo locally")
        extract(
            args.input_dir,
            args.output_dir,
            skip_existing=args.skip_existing,
            threads=args.threads,
            shard=(index, total),
            list_remaining=args.list_remaining,
        )


if __name__ == "__main__":
    main()
