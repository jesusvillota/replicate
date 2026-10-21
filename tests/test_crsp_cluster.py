"""Independent numerical and identity checks on the synthetic CRSP archive."""

import subprocess
import sys
from datetime import date
from statistics import stdev

import duckdb
import pytest

from rebal.fetch.crsp_cluster import (
    TICKERS,
    extract,
    make_demo,
    resolve_etfs,
)


@pytest.fixture
def archive(tmp_path):
    source, output = tmp_path / "input", tmp_path / "output"
    make_demo(source)
    extract(source, output, threads=2)
    return source, output


def test_demo_cli():
    result = subprocess.run(
        [sys.executable, "-m", "rebal.fetch.crsp_cluster", "--demo"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "Demo passed" in result.stdout


def test_identity_and_year_merge(archive):
    _, output = archive
    with duckdb.connect() as con:
        rows = con.execute(
            """SELECT ticker, permno, count(*), min(date), max(date)
            FROM read_parquet(?) GROUP BY ALL ORDER BY ticker""",
            [str(output / "etf_daily.parquet")],
        ).fetchall()
        assert rows == sorted(
            (ticker, 100 + i, 2, date(1997, 9, 10), date(1998, 1, 2))
            for i, ticker in enumerate(TICKERS)
        )
        assert (
            con.execute(
                "SELECT count(*) FROM read_parquet(?)",
                [str(output / "benchmarks_daily.parquet")],
            ).fetchone()[0]
            == 2
        )
        assert con.execute(
            "SELECT ret, retx, prc, vol FROM read_parquet(?) LIMIT 1",
            [str(output / "etf_daily.parquet")],
        ).fetchone() == (0.01, 0.005, 100.0, 50.0)


def test_sd_winsorization_and_filters(archive):
    _, output = archive
    with duckdb.connect() as con:
        rows = con.execute(
            "SELECT ivol, ivol_w, n_stocks FROM read_parquet(?)",
            [str(output / "dispersion_daily.parquet")],
        ).fetchall()
    # Includes ACOR, zero volume, and null prices; excludes foreign, REIT,
    # off-exchange, multi-period and missing returns. Reused SPY is a stock.
    returns = [-0.01, 0.01, 0.02, 0.03]
    lo = returns[0] + 0.03 * (returns[1] - returns[0])
    hi = returns[2] + 0.97 * (returns[3] - returns[2])
    for raw, winsorized, count in rows:
        assert count == 4
        assert raw == pytest.approx(stdev(returns))
        assert winsorized == pytest.approx(stdev([lo, 0.01, 0.02, hi]))


def test_resume_and_repair(archive):
    source, output = archive
    part = output / "parts/1997.parquet"
    unchanged = part.stat().st_mtime_ns
    extract(source, output, skip_existing=True)
    assert part.stat().st_mtime_ns == unchanged
    (output / "parts/etf/1997.parquet").write_bytes(b"interrupted write")
    extract(source, output, skip_existing=True)
    with duckdb.connect() as con:
        assert (
            con.execute(
                "SELECT count(*) FROM read_parquet(?)",
                [str(output / "parts/etf/1997.parquet")],
            ).fetchone()[0]
            == 12
        )


def test_shards_do_not_publish_partial_merge(tmp_path):
    source, output = tmp_path / "input", tmp_path / "output"
    make_demo(source)
    extract(source, output, shard=(1, 2))
    assert not (output / "etf_daily.parquet").exists()
    extract(source, output, shard=(2, 2))
    assert (output / "etf_daily.parquet").exists()


def test_ambiguous_etf_fails(tmp_path):
    make_demo(tmp_path)
    history = tmp_path / "security_history/security_info.parquet"
    with duckdb.connect() as con:
        con.execute("CREATE TABLE h AS SELECT * FROM read_parquet(?)", [str(history)])
        con.execute(
            "INSERT INTO h VALUES ('SPY', 555, '1997-01-01', '1998-12-31', 'FUND', 'ETF')"
        )
        con.execute("COPY h TO ? (FORMAT PARQUET)", [str(history)])
        with pytest.raises(ValueError, match="one ETF PERMNO"):
            resolve_etfs(con, history)


def test_duplicate_daily_key_fails(tmp_path):
    source, output = tmp_path / "input", tmp_path / "output"
    make_demo(source)
    path = source / "data/daily/1997.parquet"
    with duckdb.connect() as con:
        con.execute("CREATE TABLE d AS SELECT * FROM read_parquet(?)", [str(path)])
        con.execute("INSERT INTO d SELECT * FROM d WHERE permno=100")
        con.execute("COPY d TO ? (FORMAT PARQUET)", [str(path)])
    with pytest.raises(ValueError, match="invalid rows/keys"):
        extract(source, output)


def test_dry_run_writes_nothing(tmp_path):
    source, output = tmp_path / "input", tmp_path / "output"
    make_demo(source)
    assert extract(source, output, list_remaining=True) == {}
    assert not output.exists()


def test_dated_history_excludes_prior_observations(archive):
    source, output = archive
    path = source / "data/daily/1997.parquet"
    with duckdb.connect() as con:
        con.execute("CREATE TABLE d AS SELECT * FROM read_parquet(?)", [str(path)])
        con.execute("""INSERT INTO d SELECT * REPLACE (DATE '1997-09-09' AS dlycaldt)
            FROM d WHERE permno=100""")
        con.execute("COPY d TO ? (FORMAT PARQUET)", [str(path)])
    extract(source, output)
    with duckdb.connect() as con:
        assert con.execute(
            """SELECT count(*), min(date) FROM read_parquet(?)
            WHERE permno=100""",
            [str(output / "etf_daily.parquet")],
        ).fetchone() == (2, date(1997, 9, 10))
