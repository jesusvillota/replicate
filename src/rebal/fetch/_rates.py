"""Shared validation for the small daily rate and stress downloads."""

from pathlib import Path

import numpy as np
import pandas as pd

from rebal.fetch.common import summarize

MAX_BYTES = 20_000_000


def validate(
    frame: pd.DataFrame,
    columns: list[str],
    coverage: dict[str, tuple[str, str]] | None = None,
) -> pd.DataFrame:
    """Normalize dates and missing markers; reject schema and coverage changes."""
    # pandas: small source-file parsing and validation, without analytical computation.
    if list(frame.columns) != ["date", *columns] or frame.empty:
        raise ValueError(f"Expected nonempty columns: {['date', *columns]}")
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame.date, errors="raise", format="mixed")
    if frame.date.isna().any() or frame.date.dt.tz is not None:
        raise ValueError("Dates must be present and timezone-naive")
    if not frame.date.eq(frame.date.dt.normalize()).all():
        raise ValueError("Expected daily dates without a time component")
    if frame.date.duplicated().any():
        raise ValueError("Duplicate dates")
    frame[columns] = frame[columns].apply(pd.to_numeric, errors="raise")
    values = frame[columns].to_numpy(dtype=float)
    if np.isinf(values).any() or frame[columns].isna().all().any():
        raise ValueError("Each series must have finite observed values")
    for column, (first, last) in (coverage or {}).items():
        observed = frame.loc[frame[column].notna(), "date"]
        if observed.min() > pd.Timestamp(first) or observed.max() < pd.Timestamp(last):
            raise ValueError(
                f"{column}: insufficient coverage for {first} through {last}"
            )
        for endpoint in (first, last):
            if not frame.loc[frame.date.eq(endpoint), column].notna().any():
                raise ValueError(
                    f"{column}: missing required observation on {endpoint}"
                )
    return frame.sort_values("date").reset_index(drop=True)


def check_size(path: Path) -> None:
    if path.stat().st_size >= MAX_BYTES:
        raise ValueError(f"{path}: must be under 20 MB")


def store(frame: pd.DataFrame, path: Path) -> None:
    """Write original units, then validate the stored file and print its coverage."""
    frame.to_csv(path, index=False, date_format="%Y-%m-%d")
    check_size(path)
    summarize(path, "date")
