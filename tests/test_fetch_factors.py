"""Offline parser, stored-data and CLI checks for the two factor libraries."""

import csv
import hashlib
import json
import shutil
import sys
from io import StringIO
from zipfile import ZipFile

import numpy as np
import pandas as pd
import pytest

from rebal.fetch import french, hxz
from rebal.paths import REPO_ROOT

PUBLIC = REPO_ROOT / "data/public"


def assert_daily(frame, columns, first):
    assert list(frame.columns) == ["date", *columns]
    assert len(frame) > 0
    assert frame.date.notna().all()
    assert frame.date.is_unique and frame.date.is_monotonic_increasing
    assert frame.date.dt.tz is None
    assert np.isfinite(frame[columns].to_numpy(dtype=float)).all()
    assert frame.date.min() <= pd.Timestamp(first)
    assert frame.date.max() >= pd.Timestamp("2023-03-17")
    for endpoint in (first, "2023-03-17"):
        assert frame.loc[frame.date.eq(endpoint), columns].notna().all().all()
        assert frame.date.eq(endpoint).sum() == 1


@pytest.mark.parametrize("name,columns", french.FILES.items())
def test_stored_french_original_values_and_coverage(name, columns):
    raw = PUBLIC / "french" / f"{name}_CSV.zip"
    tidy = PUBLIC / "french" / f"{name}.csv"
    assert raw.stat().st_size < 20_000_000
    assert tidy.stat().st_size < 20_000_000
    frame = pd.read_csv(tidy, parse_dates=["date"])
    first = "1961-06-16" if name == "F-F_Research_Data_Factors_daily" else "1997-09-10"
    assert_daily(frame, columns, first)
    # Independent oracle: select only eight-digit dates from the published CSV.
    with ZipFile(raw) as archive:
        text = archive.read(archive.namelist()[0]).decode("utf-8-sig")
    records = [
        row
        for row in csv.reader(StringIO(text))
        if row and len(row[0].strip()) == 8 and row[0].strip().isdigit()
    ]
    assert frame.date.dt.strftime("%Y%m%d").tolist() == [r[0].strip() for r in records]
    np.testing.assert_allclose(
        frame[columns], [[float(v) for v in r[1:]] for r in records], rtol=0, atol=0
    )


def test_stored_hxz_original_values_and_coverage():
    directory = PUBLIC / "hxz"
    raw_path = directory / "q5_factors_daily.raw.csv"
    tidy_path = directory / "q5_factors_daily.csv"
    assert raw_path.stat().st_size < 20_000_000
    assert tidy_path.stat().st_size < 20_000_000
    raw = pd.read_csv(raw_path, parse_dates=["date"])
    tidy = pd.read_csv(tidy_path, parse_dates=["date"])
    assert_daily(tidy, hxz.COLUMNS, "1997-09-10")
    pd.testing.assert_frame_equal(tidy, raw)
    metadata = json.loads((directory / "source.json").read_text())
    assert metadata["sha256"] == hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert metadata["data_url"] == hxz.latest_daily_url(
        f'<a href="{metadata["data_url"]}">Daily</a>'
    )
    assert set(metadata) == {"data_url", "sha256"}


def french_fixture(tmp_path, rows, header=",Mom"):
    path = tmp_path / "factors.zip"
    with ZipFile(path, "w") as archive:
        archive.writestr("factors.csv", f"Publisher notes\n\n{header}\n{rows}")
    return path


def test_french_daily_block_and_missing_markers(tmp_path):
    path = french_fixture(
        tmp_path,
        "19970910, 1.25\n19970911,-99.99\n19970912,-999\n20230317,-2.5\n"
        "\nAnnual Factors\n1997,99\n20230318,99\nCopyright publisher\n",
    )
    frame, header = french.read_factors(path, ["Mom"])
    assert header == 2
    assert len(frame) == 4
    assert frame.Mom.iloc[0] == 1.25
    assert frame.Mom.iloc[1:3].isna().all()
    assert frame.Mom.iloc[-1] == -2.5


@pytest.mark.parametrize(
    "rows,header,message",
    [
        ("19970910,1\n20230317,2\n", ",Other", "missing daily header"),
        ("19970910,1\n19970910,2\n20230317,3\n", ",Mom", "Duplicate dates"),
        ("19970910,1\n20230230,2\n", ",Mom", "day is out of range"),
        ("19970910,1,2\n", ",Mom", "wrong number"),
        ("19970910,bad\n", ",Mom", "could not convert"),
        ("19970910,inf\n20230317,2\n", ",Mom", "finite observed"),
        ("19970911,1\n20230317,2\n", ",Mom", "insufficient coverage"),
        ("19970909,1\n19970911,1\n20230317,2\n", ",Mom", "missing required"),
        ("19970910,1\n20230316,2\n20230318,3\n", ",Mom", "missing required"),
        ("19970910,1\n2023031,2\n", ",Mom", "invalid daily date"),
        ("", ",Mom", "nonempty columns"),
    ],
)
def test_french_rejects_invalid_inputs(tmp_path, rows, header, message):
    with pytest.raises(ValueError, match=message):
        french.read_factors(french_fixture(tmp_path, rows, header), ["Mom"])


def test_french_rejects_ambiguous_archive(tmp_path):
    path = french_fixture(tmp_path, "19970910,1\n20230317,2\n")
    with ZipFile(path, "a") as archive:
        archive.writestr("other.csv", "")
    with pytest.raises(ValueError, match="exactly one CSV"):
        french.read_factors(path, ["Mom"])


def test_hxz_selects_newest_daily_q5():
    html = """<a href="/uploads/q5_factors_daily_2024.csv">old</a>
    <a href="https://global-q.org/uploads/q5_factors_monthly_2030.csv">monthly</a>
    <a href="http://global-q.org/uploads/q5_factors_daily_2025.csv">new</a>
    <a href="/uploads/benportf_me_eg_daily_2030.csv">portfolios</a>
    <a href="https://example.com/q5_factors_daily_2031.csv">unofficial</a>"""
    assert (
        hxz.latest_daily_url(html)
        == "https://global-q.org/uploads/q5_factors_daily_2025.csv"
    )


def test_hxz_missing_link_fails():
    with pytest.raises(ValueError, match="no q5 daily CSV"):
        hxz.latest_daily_url('<a href="q5_factors_monthly_2025.csv">monthly</a>')


@pytest.mark.parametrize(
    "change,message",
    [
        ("schema", "nonempty columns"),
        ("duplicate", "Duplicate dates"),
        ("endpoint", "missing required"),
        ("infinity", "finite observed"),
        ("date", "month must be in"),
    ],
)
def test_hxz_rejects_invalid_inputs(tmp_path, change, message):
    frame = pd.DataFrame(
        {
            "date": ["1997-09-09", "1997-09-10", "2023-03-17"],
            **{c: [0.01, 0.02, -0.03] for c in hxz.COLUMNS},
        }
    )
    if change == "schema":
        frame = frame.drop(columns="R_EG")
    elif change == "duplicate":
        frame.loc[0, "date"] = "1997-09-10"
    elif change == "endpoint":
        frame.loc[1, "R_EG"] = np.nan
    elif change == "infinity":
        frame.loc[1, "R_EG"] = np.inf
    else:
        frame.loc[1, "date"] = "1997-13-10"
    path = tmp_path / "q5.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError, match=message):
        hxz.read_factors(path)


@pytest.mark.parametrize("module", [french, hxz])
def test_cli_is_idempotent_offline(tmp_path, monkeypatch, capsys, module):
    source = "french" if module is french else "hxz"
    monkeypatch.setattr(sys, "argv", [f"rebal.fetch.{source}"])
    monkeypatch.setattr(module, "public_dir", lambda name: tmp_path)

    def fake_download(url, dest):
        if url == hxz.PAGE_URL:
            dest.write_text('<a href="/uploads/q5_factors_daily_2025.csv">daily</a>')
        else:
            shutil.copyfile(PUBLIC / source / dest.name, dest)
        return dest

    monkeypatch.setattr(module, "download", fake_download)
    module.main()
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    module.main()
    after = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    assert before == after
    assert capsys.readouterr().out.count("OK ") == (20 if module is french else 4)


@pytest.mark.parametrize("source", ["french", "hxz"])
def test_source_card_exists(source):
    assert (REPO_ROOT / "docs/data/cards" / f"{source}.md").is_file()
