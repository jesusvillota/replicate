"""Shared storage paths; licensed and processed data stay outside the repo."""

import os
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parents[2]


def _mkdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _data_root() -> Path:
    override = os.environ.get("REPLICATE_DATA_DIR")
    return (
        Path(override).expanduser() if override else Path.home() / "data" / "replicate"
    )


def _source(source: str) -> str:
    if not source or source in {".", ".."} or Path(source).name != source:
        raise ValueError("source must be one directory name")
    return source


def public_dir(source: str) -> Path:
    return _mkdir(REPO_ROOT / "data" / "public" / _source(source))


def licensed_dir(source: str) -> Path:
    return _mkdir(_data_root() / "licensed" / _source(source))


def processed_dir() -> Path:
    return _mkdir(_data_root() / "processed")


def output_dir(kind: Literal["tables", "figures", "demo"]) -> Path:
    if kind not in {"tables", "figures", "demo"}:
        raise ValueError("kind must be tables, figures or demo")
    return _mkdir(REPO_ROOT / "output" / kind)
