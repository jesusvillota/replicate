"""Check published public files and source-specific parsing without network calls."""

from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

import numpy as np
import pandas as pd
import pytest

from rebal.fetch import ads, ara, bex, epu, fears, sentiment
from rebal.fetch.common import summarize
from rebal.paths import REPO_ROOT

PUBLIC = REPO_ROOT / "data/public"


@pytest.mark.parametrize(
    "source,filename",
    [
        (epu, "All_Daily_Policy_Data.raw.csv"),
        (ads, "ADS_Index_Most_Current_Vintage.xlsx"),
        (sentiment, "news_sentiment_data.xlsx"),
    ],
)
def test_public_data_match_published_files(source, filename):
    name = source.__name__.split(".")[-1]
    directory = PUBLIC / name
    raw = directory / filename
    tidy = directory / f"{name}.csv"
    assert raw.stat().st_size < 20_000_000
    assert tidy.stat().st_size < 20_000_000
    frame = pd.read_csv(tidy, parse_dates=["date"])
    assert list(frame.columns) == ["date", name]
    assert frame.date.is_unique and frame.date.is_monotonic_increasing
    assert frame.date.dt.tz is None
    assert np.isfinite(frame[name]).all()
    for endpoint in ["1997-09-10", "2023-03-17"]:
        assert frame.loc[frame.date.eq(endpoint), name].notna().any()
    pd.testing.assert_frame_equal(frame, source.read_index(raw))


def test_epu_keeps_published_index_units():
    raw = pd.read_csv(PUBLIC / "epu/All_Daily_Policy_Data.raw.csv")
    tidy = pd.read_csv(PUBLIC / "epu/epu.csv")
    np.testing.assert_array_equal(raw.daily_policy_index, tidy.epu)


def test_sentiment_does_not_fill_published_gaps():
    frame = sentiment.read_index(PUBLIC / "sentiment/news_sentiment_data.xlsx")
    # The publisher has no observation for this early date.
    assert not frame.date.eq("1980-01-04").any()


def test_ads_preserves_latest_vintage_values():
    raw = pd.read_excel(PUBLIC / "ads/ADS_Index_Most_Current_Vintage.xlsx")
    tidy = ads.read_index(PUBLIC / "ads/ADS_Index_Most_Current_Vintage.xlsx")
    np.testing.assert_array_equal(raw.ADS_Index, tidy.ads)


def bex_workbook(path: Path) -> None:
    pd.DataFrame(
        {
            "yyyymmdd": [19970910, 20230317],
            "ra_bex_PAPER": [2.7, 3.1],
            "unc_bex_PAPER": [0.000025, 0.00003],
            "unc_bex_AnnualVolPercentage": [1.73, 1.9],
        }
    ).to_excel(path, sheet_name=bex.SHEET, index=False)


def test_bex_uses_original_variance_not_annual_volatility(tmp_path):
    raw = tmp_path / "bex.xlsx"
    bex_workbook(raw)
    frame = bex.read_index(raw)
    assert list(frame.columns) == ["date", "ra", "unc"]
    np.testing.assert_array_equal(frame.ra, [2.7, 3.1])
    np.testing.assert_array_equal(frame.unc, [0.000025, 0.00003])
    assert frame.date.dt.strftime("%Y-%m-%d").tolist() == ["1997-09-10", "2023-03-17"]


def test_bex_keeps_raw_bytes_in_licensed_storage(monkeypatch, tmp_path):
    published = tmp_path / "published.xlsx"
    bex_workbook(published)
    payload = published.read_bytes()
    destination = tmp_path / "licensed/bex"
    destination.mkdir(parents=True)

    def download(url, path):
        assert url == "https://example.org/current.xlsx"
        path.write_bytes(payload)
        return path

    monkeypatch.setattr(bex, "workbook_url", lambda: "https://example.org/current.xlsx")
    monkeypatch.setattr(bex, "licensed_dir", lambda source: destination)
    monkeypatch.setattr(bex, "download", download)
    monkeypatch.setattr("sys.argv", ["bex"])
    bex.main()
    assert (destination / "bex.raw.xlsx").read_bytes() == payload
    assert (destination / "bex.csv").is_file()
    assert not (PUBLIC / "bex").exists()


def test_bex_resolves_current_official_link(monkeypatch):
    url = "https://www.nancyxu.net/_files/ugd/current.xlsx?dn=BEX_Indices_20300101.xlsx"
    response = SimpleNamespace(
        text=f'<a href="{url}">Data</a>', raise_for_status=lambda: None
    )
    monkeypatch.setattr(bex.requests, "get", lambda *args, **kwargs: response)
    assert bex.workbook_url() == url
    response.text = "<html>File removed</html>"
    with pytest.raises(ValueError, match="one current BEX workbook"):
        bex.workbook_url()


@pytest.mark.parametrize("problem", ["duplicate", "short", "missing", "infinite"])
def test_epu_rejects_unusable_source_data(tmp_path, problem):
    frame = pd.DataFrame(
        {
            "day": [10, 17],
            "month": [9, 3],
            "year": [1997, 2023],
            "daily_policy_index": [100.0, 200.0],
        }
    )
    if problem == "duplicate":
        frame = pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
    elif problem == "short":
        frame.loc[0, "year"] = 2000
    elif problem == "missing":
        frame.loc[0, "daily_policy_index"] = np.nan
    else:
        frame.loc[0, "daily_policy_index"] = np.inf
    path = tmp_path / "epu.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError):
        epu.read_index(path)


def test_raw_split_dates_summary(tmp_path, capsys):
    path = tmp_path / "raw.csv"
    path.write_text("year,month,day,value\n1997,9,10,100\n2023,3,17,200\n")
    summarize(path, ["year", "month", "day"])
    output = capsys.readouterr().out
    assert "OK " in output
    assert "first=1997-09-10 last=2023-03-17" in output
    path.write_text("year,month,day,value\n1997,9,10,100\n1997,9,10,200\n")
    with pytest.raises(ValueError, match="duplicate dates"):
        summarize(path, ["year", "month", "day"])


def test_ara_reads_csv_from_zip_with_other_documents(tmp_path, capsys):
    raw = tmp_path / "ara.zip"
    with ZipFile(raw, "w") as archive:
        archive.writestr("ARA.csv", "date,ara\n01jul2004,0.016\n31dec2019,0.017\n")
        archive.writestr("Readme.pdf", b"published companion document")
    frame = ara.read_index(raw)
    np.testing.assert_array_equal(frame.ara, [0.016, 0.017])
    summarize(
        raw,
        "date",
        archive_member="ARA.csv",
        parse_dates=["date"],
        date_format="%d%b%Y",
    )
    assert "first=2004-07-01 last=2019-12-31" in capsys.readouterr().out


def test_fears_preserves_all_public_variants_and_short_history(tmp_path):
    raw = tmp_path / "fears.csv"
    raw.write_text(
        "date,fears25,fears30,fears35\n"
        "7/1/2004,-0.08,-0.10,-0.21\n12/30/2011,0.34,0.29,0.35\n"
    )
    frame = fears.read_index(raw)
    assert list(frame.columns) == ["date", "fears25", "fears30", "fears35"]
    assert frame.date.max() == pd.Timestamp("2011-12-30")
    np.testing.assert_array_equal(frame.fears35, [-0.21, 0.35])


def test_ara_download_requests_zip_and_keeps_published_archive(monkeypatch, tmp_path):
    published = tmp_path / "published.zip"
    with ZipFile(published, "w") as archive:
        archive.writestr("ARA.csv", "date,ara\n01jul2004,0.016\n31dec2019,0.017\n")
        archive.writestr("Readme.pdf", b"published companion document")
    payload = published.read_bytes()
    destination = tmp_path / "licensed/ara"
    destination.mkdir(parents=True)

    def download(url, path):
        assert url == ara.URL
        assert "&raw=1" in url
        path.write_bytes(payload)
        return path

    monkeypatch.setattr(ara, "download", download)
    monkeypatch.setattr(ara, "licensed_dir", lambda source: destination)
    monkeypatch.setattr("sys.argv", ["ara"])
    ara.main()
    assert (destination / "ara.raw.zip").read_bytes() == payload
    assert (destination / "ara.csv").is_file()
    assert not (PUBLIC / "ara").exists()


@pytest.mark.parametrize("source", ["epu", "ads", "sentiment", "bex", "ara", "fears"])
def test_source_card_has_status(source):
    card = (REPO_ROOT / f"docs/data/cards/{source}.md").read_text()
    assert any(line.startswith("Status: ") for line in card.splitlines())
    for heading in [
        "## Source",
        "## License class",
        "## Coverage",
        "## Known problems",
    ]:
        assert heading in card
