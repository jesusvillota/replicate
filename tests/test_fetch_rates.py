"""Stored-file contracts and failure checks; no network calls during pytest.

Run the four fetchers first. HPW stays under REPLICATE_DATA_DIR/licensed/hpw.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from rebal.fetch import fred, gsw, hpw, ofr
from rebal.fetch._rates import validate
from rebal.paths import REPO_ROOT, licensed_dir

PUBLIC = REPO_ROOT / "data" / "public"


def stored(path: Path) -> pd.DataFrame:
    assert path.is_file(), f"Missing {path}; run the four rebal.fetch modules first"
    assert path.stat().st_size < 20_000_000
    frame = pd.read_csv(path, parse_dates=["date"])
    assert frame.date.notna().all()
    assert frame.date.is_unique and frame.date.is_monotonic_increasing
    assert frame.date.dt.tz is None
    assert not np.isinf(frame.iloc[:, 1:].to_numpy(dtype=float)).any()
    assert frame.iloc[:, 1:].notna().any().all()
    return frame


def covers(frame: pd.DataFrame, column: str, first: str, last: str) -> None:
    observed = frame.loc[frame[column].notna(), "date"]
    assert observed.min() <= pd.Timestamp(first)
    assert observed.max() >= pd.Timestamp(last)
    for endpoint in (first, last):
        assert frame.loc[frame.date.eq(endpoint), column].notna().any()


@pytest.mark.parametrize("series", ["DTB3", "DGS10", "VIXCLS"])
def test_stored_fred(series):
    directory = PUBLIC / "fred"
    frame = stored(directory / f"{series}.csv")
    assert list(frame.columns) == ["date", series]
    covers(frame, series, "1997-09-10", "2023-03-17")
    raw = pd.read_csv(directory / f"{series}.raw.csv", na_values=["."])
    raw = raw.rename(columns={"observation_date": "date"})
    raw["date"] = pd.to_datetime(raw.date)
    pd.testing.assert_frame_equal(frame, raw)


def test_stored_gsw():
    frame = stored(PUBLIC / "gsw/feds200628.csv")
    expected = (
        [f"SVENY{i:02}" for i in range(1, 31)]
        + [f"SVENPY{i:02}" for i in range(1, 31)]
        + [f"BETA{i}" for i in range(4)]
        + ["TAU1", "TAU2"]
    )
    short = [c for c in expected if c not in {f"SVENPY{i:02}" for i in range(11, 31)}]
    assert list(frame.columns) in [["date", *expected], ["date", *short]]
    for column in ("SVENY10", "SVENPY10"):
        covers(frame, column, "1997-09-10", "2023-03-17")
        first = frame.loc[frame[column].notna(), "date"].min()
        assert pd.Timestamp("1970-01-01") <= first <= pd.Timestamp("1972-01-01")
    raw = PUBLIC / "gsw/feds200628.raw.csv"
    assert raw.stat().st_size < 20_000_000
    parsed, _ = gsw.read_curve(raw)
    pd.testing.assert_frame_equal(frame, parsed[list(frame.columns)])


def test_stored_ofr():
    frame = stored(PUBLIC / "ofr/fsi.csv")
    assert list(frame.columns) == [
        "date",
        "OFR FSI",
        "Credit",
        "Equity valuation",
        "Safe assets",
        "Funding",
        "Volatility",
        "United States",
        "Other advanced economies",
        "Emerging markets",
    ]
    for column in frame.columns[1:]:
        covers(frame, column, "2000-01-03", "2023-03-17")
    pd.testing.assert_frame_equal(frame, ofr.read_index(PUBLIC / "ofr/fsi.raw.csv"))
    # Published values round to three decimals: five categories plus the total
    # permit a sum discrepancy of at most 6 * 0.0005 index points.
    np.testing.assert_allclose(
        frame.iloc[:, 2:7].sum(axis=1), frame["OFR FSI"], rtol=0, atol=0.00301
    )


def test_stored_hpw():
    directory = licensed_dir("hpw")
    assert not (PUBLIC / "hpw").exists(), "HPW must not be redistributed"
    frame = stored(directory / "noise.csv")
    assert list(frame.columns) == ["date", "Noise_bp"]
    covers(frame, "Noise_bp", "1987-01-02", "2025-12-31")
    pd.testing.assert_frame_equal(
        frame, hpw.read_noise(directory / "Noise_Measure_2025.xlsx")
    )


def test_fred_maintenance_fallback_preserves_raw(monkeypatch, tmp_path, capsys):
    published = b"observation_date,DTB3\n1997-09-10,5.1\n1997-09-11,.\n2023-03-17,4.5\n"
    calls = []

    def download(url, path):
        calls.append(url)
        path.write_bytes(
            published if "web.archive.org" in url else b"<html>maintenance</html>"
        )

    monkeypatch.setattr(fred, "download", download)
    fred.fetch("DTB3", tmp_path)
    assert len(calls) == 2 and calls[1].startswith("https://web.archive.org/")
    assert (tmp_path / "DTB3.raw.csv").read_bytes() == published
    assert pd.read_csv(tmp_path / "DTB3.csv").DTB3.isna().sum() == 1
    assert (
        len([s for s in capsys.readouterr().out.splitlines() if s.startswith("OK ")])
        == 2
    )


@pytest.mark.parametrize(
    "dates,values,error",
    [
        (["2020-01-02", "2020-01-02"], [1, 2], "Duplicate dates"),
        ([None, "2020-01-02"], [1, 2], "Dates must be present"),
        (["2020-01-02", "2020-01-03"], [1, np.inf], "finite observed"),
        (["2020-01-02", "2020-01-03"], [np.nan, np.nan], "finite observed"),
    ],
)
def test_reject_invalid_download(dates, values, error):
    with pytest.raises(ValueError, match=error):
        validate(pd.DataFrame({"date": dates, "rate": values}), ["rate"])


def test_reject_truncated_history_and_missing_endpoint():
    frame = pd.DataFrame({"date": ["1997-09-10", "2023-03-17"], "rate": [1, 2]})
    with pytest.raises(ValueError, match="insufficient coverage"):
        validate(frame, ["rate"], {"rate": ("1971-01-01", "2023-03-17")})
    with pytest.raises(ValueError, match="missing required observation"):
        validate(frame, ["rate"], {"rate": ("2000-01-03", "2023-03-17")})


@pytest.mark.parametrize("source", ["fred", "gsw", "ofr", "hpw"])
def test_cards_record_coverage(source):
    card = (REPO_ROOT / f"docs/data/cards/{source}.md").read_text()
    assert "## Coverage" in card
    if source in {"ofr", "hpw"}:
        directory = PUBLIC / source if source == "ofr" else licensed_dir("hpw")
        frame = stored(directory / ("fsi.csv" if source == "ofr" else "noise.csv"))
        assert f"{frame.date.min():%Y-%m-%d}" in card
        assert f"{frame.date.max():%Y-%m-%d}" in card
