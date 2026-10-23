"""uv run python3 -m rebal.exhibits.robustness_extra --demo
uv run python3 -m rebal.exhibits.robustness_extra --d4-signals futures --end latest

CLI Arguments:
--demo: use synthetic fixtures and output/demo/.
--d4-signals: index (default) rebuilds D.4 signals; futures retains core signals.
--d14-lag: extra signal lag, 1 (default) or 0 for a timing check.
--end: sample endpoint, 2023-03-17 (default) or latest.
--timing: clean (default) or literal signal timing.
--se: hc1 (default), hc0 or hac; --hac-lags overrides the HAC lag count.

Reads the panel and signal contracts. Writes three regression CSVs and
robustness_extra.metadata.json. Demo response effects are planted locally,
after constructing each design. No real outputs belong in this task's commit.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console

from rebal.io import load_panel, load_signals
from rebal.paths import output_dir
from rebal.regress import DEFAULT_SAMPLE, TABLE_COLUMNS, dated, predictive
from rebal.signals import build

EXHIBITS = ["table_D4", "table_D9", "table_D14"]
BASE = ["threshold", "calendar", "week4", "calendar:week4", "momentum", "ret"]
D9_CONTROLS = {"1": "ra_bex", "2": "unc_bex", "4": "ara"}
SKIPPED = {"table_D9": {"3": "FEARS: authors' private full-sample data unavailable"}}


def index_signals(panel: pd.DataFrame, timing: str = "clean") -> pd.DataFrame:
    """Rebuild on the observed index-pair span; never fill missing returns."""
    # pandas: small date-aligned series are inputs to the existing signal engine.
    p = dated(panel)
    valid = np.isfinite(p[["r_sp500tr", "r_agg"]]).all(axis=1)
    if not valid.any():
        raise ValueError("D.4 has no observed index-pair returns")
    span = p.loc[valid[valid].index.min() : valid[valid].index.max()]
    if not valid.loc[span.index].all():
        raise ValueError("D.4 index-pair history has internal gaps; cannot simulate")
    return build(span.r_sp500tr, span.r_agg, timing=timing, r_sp500tr=span.r_sp500tr)


def prepare_designs(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    d4_signals: str = "index",
    d14_lag: int = 1,
    timing: str = "clean",
) -> dict[str, tuple[pd.DataFrame, pd.DataFrame, list[str], str]]:
    """Construct designs on the full calendar before any sample filtering."""
    if d4_signals not in {"index", "futures"}:
        raise ValueError("d4_signals must be index or futures")
    if d14_lag not in {0, 1}:
        raise ValueError("d14_lag must be 0 or 1")
    # pandas: small named statsmodels designs, date alignment and rolling control.
    p = dated(panel)
    s = dated(signals).reindex(p.index)
    d4 = dated(index_signals(panel, timing)) if d4_signals == "index" else s.copy()
    d4 = d4.reindex(p.index)
    d4["ret"] = p.r_sp500tr - p.r_agg
    d14 = s.copy()
    d14[["threshold", "calendar"]] = s[["threshold", "calendar"]].shift(d14_lag)
    # Week4 refers to t; Calendar refers to t-1 when the extra lag is enabled.
    p["sp500_trailing_2d"] = (1 + p.r_sp500tr).rolling(2, min_periods=2).apply(
        np.prod, raw=True
    ) - 1
    p["international_excess"] = (p.r_acwxus - p.rf_3m).where(
        p.index >= pd.Timestamp("2000-12-29")
    )
    # Do not extend the paper's attention sample with upstream forward fills.
    p["ara"] = p.ara.where(
        (p.index >= pd.Timestamp("2004-07-01"))
        & (p.index <= pd.Timestamp("2019-12-31"))
    )
    return {
        "table_D4": (d4, p.copy(), BASE, "ret"),
        "table_D9": (s, p.copy(), BASE, "ret"),
        "table_D14": (
            d14,
            p.copy(),
            BASE[:-1] + ["sp500_trailing_2d"],
            "international_excess",
        ),
    }


def _plant_demo(
    designs: dict[str, tuple[pd.DataFrame, pd.DataFrame, list[str], str]],
    betas: tuple[float, float],
) -> None:
    """Replace only demo responses; preserve predictor construction and timing."""
    rng = np.random.default_rng(26)
    for s, p, _, outcome in designs.values():
        response = (
            betas[0] * s.threshold
            + betas[1] * s.calendar * s.week4
            + rng.normal(0, 0.0002, len(s))
        ).shift(1)
        if outcome == "ret":
            s[outcome] = response
        else:
            p[outcome] = response.where(p[outcome].notna())


def build_tables(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    end: str = DEFAULT_SAMPLE[1],
    d4_signals: str = "index",
    d14_lag: int = 1,
    timing: str = "clean",
    se: str = "hc1",
    hac_lags: int | None = None,
    demo_betas: tuple[float, float] | None = None,
) -> dict[str, pd.DataFrame]:
    """Fit D.4/D.14 column 1 and the three available D.9 columns."""
    designs = prepare_designs(
        signals, panel, d4_signals=d4_signals, d14_lag=d14_lag, timing=timing
    )
    if demo_betas is not None:
        _plant_demo(designs, demo_betas)
    tables = {}
    # pandas: final tidy display tables from small statsmodels designs.
    for exhibit, (s, p, base, outcome) in designs.items():
        columns = D9_CONTROLS if exhibit == "table_D9" else {"1": None}
        rows = []
        for column, control in columns.items():
            result = predictive(
                s.reset_index(),
                p.reset_index(),
                base + ([control] if control else []),
                y=outcome,
                sample=(DEFAULT_SAMPLE[0], end),
                se=se,
                hac_lags=hac_lags,
            )
            tidy = result.tidy.copy()
            tidy["exhibit"], tidy["column"] = exhibit, column
            rows.append(tidy)
        tables[exhibit] = pd.concat(rows, ignore_index=True)[TABLE_COLUMNS]
    return tables


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    d4_signals: str = "index",
    d14_lag: int = 1,
    timing: str = "clean",
    se: str = "hc1",
    hac_lags: int | None = None,
) -> list[Path]:
    """Write only this module's artifacts, using shared path and input helpers."""
    parameters = {
        "end": end,
        "d4_signals": d4_signals,
        "d14_lag": d14_lag,
        "timing": timing,
        "se": se,
        "hac_lags": hac_lags,
    }
    tables = build_tables(
        load_signals(demo=demo, timing=timing),
        load_panel(demo=demo),
        **parameters,
        demo_betas=(-0.4, -0.3) if demo else None,
    )
    destination = output_dir("demo" if demo else "tables")
    outputs = []
    for exhibit, table in tables.items():
        path = destination / f"{exhibit}.csv"
        table.to_csv(path, index=False)
        outputs.append(path)
    samples = {
        exhibit: table.groupby("column")[["nobs", "sample_start", "sample_end"]]
        .first()
        .to_dict(orient="index")
        for exhibit, table in tables.items()
    }
    metadata = destination / "robustness_extra.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "parameters": parameters,
                "sample": [DEFAULT_SAMPLE[0], end],
                "samples": samples,
                "inputs": ["rebal.demo"]
                if demo
                else ["daily_panel.parquet", f"signals_{timing}.parquet"],
                "control_scaling": {
                    name: "published level; multiplier 1"
                    for name in D9_CONTROLS.values()
                },
                "d14_control": "(1+r_sp500tr[t])*(1+r_sp500tr[t-1])-1",
                "d14_interaction": "calendar[t-d14_lag] * week4[t]",
                "demo_betas": [-0.4, -0.3] if demo else None,
                "skipped": SKIPPED,
                "outputs": [path.name for path in outputs],
            },
            indent=2,
        )
        + "\n"
    )
    return outputs + [metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build extra robustness tables.")
    parser.add_argument("--demo", action="store_true", help="Use synthetic fixtures.")
    parser.add_argument("--d4-signals", choices=["index", "futures"], default="index")
    parser.add_argument("--d14-lag", type=int, choices=[0, 1], default=1)
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="ISO endpoint or latest."
    )
    parser.add_argument("--timing", choices=["clean", "literal"], default="clean")
    parser.add_argument("--se", choices=["hc0", "hc1", "hac"], default="hc1")
    parser.add_argument("--hac-lags", type=int, help="Nonnegative HAC lag override.")
    args = parser.parse_args()
    if args.hac_lags is not None and args.hac_lags < 0:
        parser.error("--hac-lags must be nonnegative")
    if args.end != "latest":
        try:
            if pd.isna(pd.Timestamp(args.end)) or pd.Timestamp(args.end) < pd.Timestamp(
                DEFAULT_SAMPLE[0]
            ):
                raise ValueError("invalid endpoint or endpoint precedes sample start")
        except ValueError as exc:
            parser.error(str(exc))
    return args


def main() -> None:
    console = Console()
    for path in run(**vars(parse_args())):
        console.print(str(path), markup=False)


if __name__ == "__main__":
    main()
