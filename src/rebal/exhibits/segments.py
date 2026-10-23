"""uv run python3 -m rebal.exhibits.segments --demo
uv run python3 -m rebal.exhibits.segments --value-weight 0.5 --controls all

CLI Arguments:
--demo: use synthetic segment returns and output/demo/.
--value-weight: Value target, 0.9 (default) or 0.5.
--controls: baseline (Table 1 column 1, default) or all external controls.
--end: ISO sample endpoint (default 2023-03-17), or latest.
--timing: clean (default) or literal reset; --momentum: medium-slow or all15.
--se: hc1 (default), hc0 or hac; --hac-lags: optional nonnegative lag count.

Reads the daily panel contract. Builds signals from each equity pair and writes
table_5.csv in the regression contract layout, plus segments.metadata.json.
See docs/methods/segments.md. No figures or shared signal files are written.
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
from rich.console import Console

from rebal.io import load_panel
from rebal.paths import output_dir, processed_dir
from rebal.regress import TABLE_COLUMNS, dated, predictive
from rebal.signals import build

EXHIBITS = ["table_5"]
SAMPLE = ("2006-08-17", "2023-03-17")
PAIRS = {"1": ("r_r1k", "r_r2k"), "2": ("r_r1kv", "r_r1kg")}
BASE = ["threshold", "calendar", "week4", "calendar:week4", "momentum", "ret"]
EXTERNAL = ["vix", "move", "epu", "ads", "sentiment"]


def make_demo_panel(
    *, beta_threshold: float = -0.4, beta_calweek4: float = -0.3, seed: int = 25
) -> pd.DataFrame:
    """Plant next-day effects through returns, before building any regressors.

    Value/Growth has zero effects. The local recursion supplies causal returns;
    estimation independently rebuilds the full signals via rebal.signals.build.
    """
    # pandas: small synthetic fixture and calendar construction, not data scans.
    panel = load_panel(demo=True).copy()
    dates = pd.DatetimeIndex(panel.date)
    days_left = panel.date.groupby(dates.to_period("M")).cumcount(ascending=False) + 1
    rng = np.random.default_rng(seed)
    for column, (large, small) in PAIRS.items():
        weight = 0.9
        previous = np.full(26, weight)
        calendar_post = weight
        threshold = calendar_week4 = 0.0
        spreads = np.empty(len(panel))
        for t in range(len(panel)):
            spread = rng.normal(0, 0.004)
            if column == "1":
                spread += beta_threshold * threshold + beta_calweek4 * calendar_week4
            spreads[t] = spread
            common = float(panel.r_es.iloc[t])
            eq, bd = common + spread / 2, common - spread / 2
            pre = previous * (1 + eq)
            pre /= pre + (1 - previous) * (1 + bd)
            threshold = float(np.mean(pre - weight))
            previous = np.where(
                np.abs(pre - weight) >= np.arange(26) / 1000, weight, pre
            )
            cal_pre = calendar_post * (1 + eq)
            cal_pre /= cal_pre + (1 - calendar_post) * (1 + bd)
            calendar_week4 = (cal_pre - weight) * (days_left.iloc[t] <= 5)
            calendar_post = weight if days_left.iloc[t] == 1 else cal_pre
        common_total = panel.r_es.to_numpy() + panel.rf_3m.to_numpy()
        panel[large] = common_total + spreads / 2
        panel[small] = common_total - spreads / 2
    return panel


def segment_signals(
    panel: pd.DataFrame,
    large: str,
    small: str,
    *,
    target: float = 0.9,
    timing: str = "clean",
    momentum: str = "medium-slow",
) -> pd.DataFrame:
    """Use the contiguous available history; never fill or bridge missing returns."""
    # pandas: small labeled inputs to the sequential simulation and statsmodels.
    history = dated(panel)[[large, small, "rf_3m"]]
    valid = np.isfinite(history).all(axis=1)
    if not valid.any():
        raise ValueError(f"no complete history for {large}/{small} and rf_3m")
    history = history.loc[valid[valid].index[0] : valid[valid].index[-1]]
    if not np.isfinite(history).all().all():
        raise ValueError(f"interior missing return or cash rate for {large}/{small}")
    return build(
        history[large] - history.rf_3m,
        history[small] - history.rf_3m,
        target=target,
        timing=timing,
        momentum=momentum,
    )


def build_table(
    panel: pd.DataFrame,
    *,
    value_weight: float = 0.9,
    controls: str = "baseline",
    end: str = SAMPLE[1],
    timing: str = "clean",
    momentum: str = "medium-slow",
    se: str = "hc1",
    hac_lags: int | None = None,
) -> pd.DataFrame:
    """Fit segment-specific next-day spreads using the shared timing convention."""
    if value_weight not in {0.9, 0.5}:
        raise ValueError("value_weight must be 0.9 or 0.5")
    if controls not in {"baseline", "all"}:
        raise ValueError("controls must be baseline or all")
    terms = BASE + (EXTERNAL if controls == "all" else [])
    rows = []
    for column, (large, small) in PAIRS.items():
        signals = segment_signals(
            panel,
            large,
            small,
            target=0.9 if column == "1" else value_weight,
            timing=timing,
            momentum=momentum,
        )
        result = predictive(
            signals, panel, terms, sample=(SAMPLE[0], end), se=se, hac_lags=hac_lags
        )
        tidy = result.tidy.copy()
        tidy["exhibit"], tidy["column"] = "table_5", column
        rows.append(tidy)
    # pandas: final tidy regression output only.
    return pd.concat(rows, ignore_index=True)[TABLE_COLUMNS]


def run(demo: bool = False, **options) -> list[Path]:
    """Exhibit discovery entry point; write only this module's two artifacts."""
    panel = make_demo_panel() if demo else load_panel()
    table = build_table(panel, **options)
    destination = output_dir("demo" if demo else "tables")
    path = destination / "table_5.csv"
    table.to_csv(path, index=False)
    metadata = destination / "segments.metadata.json"
    metadata.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "input": "segments.make_demo_panel"
                if demo
                else str(processed_dir() / "daily_panel.parquet"),
                "requested_sample": [SAMPLE[0], options.get("end", SAMPLE[1])],
                "weights": {"1": 0.9, "2": options.get("value_weight", 0.9)},
                "terms": BASE + (EXTERNAL if options.get("controls") == "all" else []),
                "timing": options.get("timing", "clean"),
                "momentum": options.get("momentum", "medium-slow"),
                "se": options.get("se", "hc1"),
                "hac_lags": options.get("hac_lags"),
                "cash": "rf_3m subtracted from both ETF total returns",
                "estimation": table[["column", "nobs", "sample_start", "sample_end"]]
                .drop_duplicates()
                .to_dict("records"),
                "outputs": [path.name],
            },
            indent=2,
        )
        + "\n"
    )
    return [path, metadata]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Table 5 equity-segment regressions."
    )
    parser.add_argument(
        "--demo", action="store_true", help="Use synthetic segment returns."
    )
    parser.add_argument("--value-weight", type=float, choices=[0.9, 0.5], default=0.9)
    parser.add_argument("--controls", choices=["baseline", "all"], default="baseline")
    parser.add_argument("--end", default=SAMPLE[1], help="ISO endpoint or latest.")
    parser.add_argument("--timing", choices=["clean", "literal"], default="clean")
    parser.add_argument(
        "--momentum", choices=["medium-slow", "all15"], default="medium-slow"
    )
    parser.add_argument("--se", choices=["hc0", "hc1", "hac"], default="hc1")
    parser.add_argument(
        "--hac-lags", type=int, help="Nonnegative Newey–West lag count."
    )
    args = parser.parse_args()
    if args.hac_lags is not None and args.hac_lags < 0:
        parser.error("--hac-lags must be nonnegative")
    if args.end != "latest":
        try:
            if pd.Timestamp(args.end) < pd.Timestamp(SAMPLE[0]):
                raise ValueError("endpoint precedes sample start")
        except ValueError as exc:
            parser.error(str(exc))
    return args


def main() -> None:
    console = Console()
    for path in run(**vars(parse_args())):
        console.print(str(path), markup=False)


if __name__ == "__main__":
    main()
