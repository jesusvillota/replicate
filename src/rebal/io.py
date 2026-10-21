"""Read the shared parquet contracts, or generate in-memory demo fixtures."""

import pandas as pd

from rebal.paths import processed_dir


def load_panel(demo: bool = False) -> pd.DataFrame:
    if demo:
        from rebal.demo import make_panel

        return make_panel()
    path = processed_dir() / "daily_panel.parquet"
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {path}. Run: uv run python3 -m rebal.panel --build"
        )
    return pd.read_parquet(path)


def load_signals(demo: bool = False, timing: str = "clean") -> pd.DataFrame:
    if not timing or not all(c.isalnum() or c in "_-" for c in timing):
        raise ValueError("timing must be a nonempty filename-safe name")
    if demo:
        from rebal.demo import make_signals

        return make_signals(load_panel(demo=True))
    path = processed_dir() / f"signals_{timing}.parquet"
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {path}. Run: uv run python3 -m rebal.signals --build --timing {timing}"
        )
    return pd.read_parquet(path)
