"""Download helpers. Every fetcher must summarize every file it writes."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from time import sleep

import pandas as pd
import requests
from rich.console import Console

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36"
)


def download(url: str, dest: Path, *, retries: int = 3) -> Path:
    """Download atomically; retries counts attempts after the initial request."""
    if retries < 0:
        raise ValueError("retries must be nonnegative")
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(retries + 1):
        temporary = None
        try:
            with requests.get(
                url, headers={"User-Agent": USER_AGENT}, timeout=60, stream=True
            ) as response:
                response.raise_for_status()
                with NamedTemporaryFile(dir=dest.parent, delete=False) as handle:
                    temporary = Path(handle.name)
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        handle.write(chunk)
                temporary.replace(dest)
            return dest
        except requests.RequestException:
            if attempt == retries:
                raise
            sleep(min(2**attempt, 8))
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    raise AssertionError("unreachable")


def summarize(path: Path, date_col: str) -> None:
    """Validate CSV, parquet or Excel data and emit exactly one summary line."""
    # pandas: file validation only; no analytical query or per-group computation.
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path)
    elif path.suffix.lower() in {".xls", ".xlsx"}:
        frame = pd.read_excel(path)
    else:
        frame = pd.read_csv(path)
    if frame.empty:
        raise ValueError(f"{path}: expected at least one row")
    if date_col not in frame:
        raise ValueError(f"{path}: missing date column {date_col!r}")
    dates = pd.to_datetime(frame[date_col], errors="raise")
    if dates.isna().any() or dates.dt.tz is not None:
        raise ValueError(f"{path}: dates must be nonmissing and timezone-naive")
    dates = dates.dt.normalize()
    if dates.duplicated().any():
        raise ValueError(f"{path}: duplicate dates")
    Console().print(
        f"OK {path} rows={len(frame)} first={dates.min():%Y-%m-%d} "
        f"last={dates.max():%Y-%m-%d}",
        markup=False,
        highlight=False,
        soft_wrap=True,
    )
