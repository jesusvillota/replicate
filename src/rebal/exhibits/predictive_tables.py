"""uv run python3 -m rebal.exhibits.predictive_tables --demo --end latest

CLI Arguments:
--demo: use planted fixtures and output/demo/.
--end: sample endpoint (default 2023-03-17); latest uses all available dates.
--se: hc0, hc1 (default), or hac; D1/D2 always use hac.
--hac-lags: nonnegative Newey–West lag override; otherwise automatic.
--timing: signal file suffix (default clean).

Reads the panel and signals contracts. Writes 15 long-format regression CSVs,
magnitudes/magnitudes.csv and predictive_tables.metadata.json. No figures.
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
from rebal.regress import (
    DEFAULT_SAMPLE,
    TABLE_COLUMNS,
    RegressionResult,
    dated,
    ols,
    predictive,
    predictive_data,
)

EXHIBITS = [
    "table_1",
    "table_2a",
    "table_2b",
    "table_3",
    "table_D1",
    "table_D2",
    "table_D3",
    "table_D5",
    "table_D6",
    "table_D7",
    "table_D8",
    "table_D10",
    "table_D11",
    "table_D12",
    "table_D13",
]
BASE = ["threshold", "calendar", "week4", "calendar:week4", "momentum", "ret"]
CONTROLS = ["vix", "move", "epu", "ads", "sentiment"]
CONTROL_SETS = [[], CONTROLS[:2], CONTROLS[2:4], CONTROLS[4:], CONTROLS]
HORIZONS = [1, 2, 3, 4, 5, 10, 15, 21, 42, 63, 126, 252]


def build_tables(
    signals: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
    hac_lags: int | None = None,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    """Build the paper column layouts and one-SD effects on estimation samples."""
    # pandas: small, named statsmodels designs and final tidy display tables.
    s = signals.copy()
    p = panel.copy()
    sample = (DEFAULT_SAMPLE[0], end)
    rows: dict[str, list[pd.DataFrame]] = {name: [] for name in EXHIBITS}
    magnitudes: list[dict] = []

    def fit(
        exhibit: str,
        column: int | str,
        terms: list[str],
        *,
        y: str = "ret",
        source: pd.DataFrame | None = None,
        subset: pd.Series | None = None,
        covariance: str | None = None,
    ) -> RegressionResult:
        source = s if source is None else source
        result = predictive(
            source,
            p,
            terms,
            y=y,
            sample=sample,
            subset=subset,
            se=covariance or se,
            hac_lags=hac_lags,
        )
        tidy = result.tidy.copy()
        tidy["exhibit"], tidy["column"] = exhibit, str(column)
        rows[exhibit].append(tidy)
        if exhibit in {"table_1", "table_3"}:
            for term in terms:
                sd = float(result.design[term].std(ddof=1))
                magnitudes.append(
                    {
                        "exhibit": exhibit,
                        "column": str(column),
                        "outcome": y,
                        "term": term,
                        "coef": result.coef[term],
                        "sd": sd,
                        "magnitude": result.coef[term] * sd,
                        "magnitude_bps": result.coef[term] * sd * 10000,
                        "nobs": result.nobs,
                        "sd_ddof": 1,
                    }
                )
        return result

    for col, controls in enumerate(CONTROL_SETS, 1):
        fit("table_1", col, BASE + controls)
        fit("table_D2", col, BASE + controls, covariance="hac")
        fit(
            "table_D3",
            col,
            [
                name
                for term in BASE
                for name in (
                    ["mom_fast", "mom_medium", "mom_slow"]
                    if term == "momentum"
                    else [term]
                )
            ]
            + controls,
        )
    fit("table_2a", 1, [t for t in BASE if t != "calendar:week4"])
    fit("table_2a", 2, BASE)
    fit("table_2a", 3, BASE + ["threshold:week4"])
    for month in range(1, 4):
        subset = (pd.DatetimeIndex(s.date).month - 1) % 3 + 1 == month
        fit(
            "table_2b",
            month,
            BASE,
            subset=pd.Series(subset, index=pd.DatetimeIndex(s.date)),
        )
    for leg, outcome in enumerate(["r_es", "r_ty"]):
        for with_controls in range(2):
            fit(
                "table_3",
                2 * leg + with_controls + 1,
                BASE + (CONTROLS if with_controls else []),
                y=outcome,
            )
        for col, controls in enumerate(CONTROL_SETS, 1):
            fit(
                "table_D13",
                f"{'A' if leg == 0 else 'B'}{col}",
                BASE + controls,
                y=outcome,
            )

    # D1 is contemporaneous; compute trailing sums before cutting the sample.
    history = dated(s)
    trailing = pd.DataFrame(
        {f"ret_{h}": history.ret.rolling(h, min_periods=h).sum() for h in HORIZONS}
    )
    end_date = history.index.max() if end == "latest" else pd.Timestamp(end)
    mask = (history.index >= pd.Timestamp(sample[0])) & (history.index <= end_date)
    for col, outcome in enumerate(["threshold", "calendar"], 1):
        result = ols(history.loc[mask, outcome], trailing.loc[mask], "hac", hac_lags)
        tidy = pd.concat(
            [result.tidy, result.contrast(list(trailing), "coefficient_sum")],
            ignore_index=True,
        )
        tidy["exhibit"], tidy["column"] = "table_D1", str(col)
        rows["table_D1"].append(tidy)

    differences = dated(p)[CONTROLS].diff()
    for control in CONTROLS:
        p[f"d_{control}"] = differences[control].to_numpy()
    for col, controls in enumerate(CONTROL_SETS[1:], 1):
        fit("table_D5", col, BASE + [f"d_{control}" for control in controls])
    for variant, (lower, upper) in enumerate([(0, 20), (1, 25)]):
        alternate = s.copy()
        alternate["threshold"] = alternate[
            [f"thr_{i:03d}" for i in range(lower, upper + 1)]
        ].mean(axis=1, skipna=False)
        for with_controls in range(2):
            fit(
                "table_D6",
                2 * variant + with_controls + 1,
                BASE + (CONTROLS if with_controls else []),
                source=alternate,
            )
    for col, target in enumerate(["t86", "t50", "t70"], 1):
        alternate = s.copy()
        for name in ["threshold", "calendar"]:
            alternate[name] = alternate[f"{name}_{target}"]
        fit("table_D7", col, BASE, source=alternate)

    # Fit each residualization on exactly its complete regression sample.
    _, baseline_design, _ = predictive_data(s, p, BASE, sample=sample)
    median = float(baseline_design.threshold.abs().median())
    s["threshold_small"] = s.threshold.where(s.threshold.abs() <= median, 0.0).where(
        s.threshold.notna()
    )
    s["threshold_large"] = s.threshold.where(s.threshold.abs() > median, 0.0).where(
        s.threshold.notna()
    )
    for with_controls in range(2):
        terms = BASE + (CONTROLS if with_controls else [])
        fit(
            "table_D8",
            with_controls + 1,
            ["threshold_small", "threshold_large"] + terms[1:],
        )
        response, design, _ = predictive_data(s, p, terms, sample=sample)
        projection = ols(design.threshold, design[["momentum"]])
        residual = design.threshold - projection.design @ projection.coef
        alternate = s.copy()
        alternate["threshold_perp"] = alternate.date.map(residual)
        original = predictive(s, p, terms, sample=sample, se=se, hac_lags=hac_lags)
        result = fit(
            "table_D8",
            with_controls + 3,
            ["threshold_perp"] + terms[1:],
            source=alternate,
        )
        if not np.isclose(
            result.coef["threshold_perp"],
            original.coef["threshold"],
            rtol=0,
            atol=1e-10,
        ):
            raise AssertionError("D8 FWL coefficient identity failed (tolerance 1e-10)")
        if result.nobs != len(response):
            raise AssertionError("D8 FWL estimation samples differ")

    reversal_base = BASE[:-1]
    reversal_terms = [
        ["rev_st"],
        reversal_base + ["rev_st"],
        ["rev_lt"],
        reversal_base + ["rev_lt"],
        reversal_base + ["rev_st", "rev_lt"],
    ]
    for col, terms in enumerate(reversal_terms, 1):
        fit("table_D10", col, terms)
    available_eom = pd.Series(
        s.eom_rev.notna().to_numpy(), index=pd.DatetimeIndex(s.date)
    )
    for col, (terms, outcome) in enumerate(
        [
            (["eom_rev"], "ret"),
            (BASE, "ret"),
            (BASE + ["eom_rev"], "ret"),
            (BASE + ["eom_rev"], "r_es"),
            (BASE + ["eom_rev"], "r_ty"),
        ],
        1,
    ):
        fit("table_D11", col, terms, y=outcome, subset=available_eom)
    for with_week4 in range(2):
        for week in range(1, 4):
            terms = [
                "threshold",
                "calendar",
                f"week{week}",
                f"calendar:week{week}",
                "momentum",
                "ret",
            ]
            if with_week4:
                terms += ["week4", "calendar:week4"]
            fit("table_D12", 3 * with_week4 + week, terms)
    return (
        {
            name: pd.concat(parts, ignore_index=True)[TABLE_COLUMNS]
            for name, parts in rows.items()
        },
        pd.DataFrame(magnitudes),
    )


def run(
    demo: bool = False,
    *,
    end: str = DEFAULT_SAMPLE[1],
    se: str = "hc1",
    hac_lags: int | None = None,
    timing: str = "clean",
) -> list[Path]:
    """Runner entry point; write only this module's artifacts."""
    panel, signals = load_panel(demo=demo), load_signals(demo=demo, timing=timing)
    tables, magnitudes = build_tables(signals, panel, end=end, se=se, hac_lags=hac_lags)
    destination = output_dir("demo" if demo else "tables")
    outputs = []
    for exhibit, table in tables.items():
        path = destination / f"{exhibit}.csv"
        table.to_csv(path, index=False)
        outputs.append(path)
    magnitude_path = (
        destination / "magnitudes" / "magnitudes.csv"
        if demo
        else destination / "magnitudes.csv"
    )
    magnitude_path.parent.mkdir(parents=True, exist_ok=True)
    magnitudes.to_csv(magnitude_path, index=False)
    outputs.append(magnitude_path)
    metadata_path = destination / "predictive_tables.metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "sample": [DEFAULT_SAMPLE[0], end],
                "se": se,
                "hac_lags": hac_lags,
                "timing": timing,
                "inputs": [
                    "rebal.demo" if demo else "daily_panel.parquet",
                    "rebal.demo" if demo else f"signals_{timing}.parquet",
                ],
                "outputs": [str(path.relative_to(destination)) for path in outputs],
                "table_3_outcomes": {
                    "1": "r_es",
                    "2": "r_es",
                    "3": "r_ty",
                    "4": "r_ty",
                },
                "table_D13_panels": {"A": "r_es", "B": "r_ty"},
            },
            indent=2,
        )
        + "\n"
    )
    return outputs + [metadata_path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build predictive-regression tables.")
    parser.add_argument("--demo", action="store_true", help="Use synthetic fixtures.")
    parser.add_argument(
        "--end", default=DEFAULT_SAMPLE[1], help="ISO endpoint or latest."
    )
    parser.add_argument("--se", choices=["hc0", "hc1", "hac"], default="hc1")
    parser.add_argument("--hac-lags", type=int, help="Newey–West lag override.")
    parser.add_argument("--timing", default="clean", help="Signal file suffix.")
    args = parser.parse_args()
    if args.hac_lags is not None and args.hac_lags < 0:
        parser.error("--hac-lags must be nonnegative")
    if args.end != "latest":
        try:
            if pd.Timestamp(args.end) < pd.Timestamp(DEFAULT_SAMPLE[0]):
                raise ValueError("endpoint precedes sample start")
        except ValueError as exc:
            parser.error(str(exc))
    return args


def main() -> None:
    args = parse_args()
    console = Console()
    for path in run(**vars(args)):
        console.print(str(path), markup=False)


if __name__ == "__main__":
    main()
