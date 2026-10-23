"""uv run python3 -m rebal.exhibits.long_sample --demo
uv run python3 -m rebal.exhibits.long_sample --pre-1971 dgs10

CLI Arguments:
--demo: use a synthetic long panel with a planted post-1997 effect.
--pre-1971 dgs10|omit: early yield proxy (default dgs10) or GSW only.
--end: inclusive outcome endpoint (default 2023-03-17), or latest.
--timing clean|literal: same-close or delayed signal resets (default clean).
--momentum medium-slow|all15: momentum aggregation (default medium-slow).
--se hc0|hc1|hac: covariance estimator (default hc1).
--hac-lags: optional nonnegative Newey-West lag count.

Reads public French, GSW and FRED sources, or rebal.demo fixtures. Writes
table_4.csv in the exhibits regression contract and table_4.metadata.json.
No main-panel files are read or changed. Processing only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from rich.console import Console

from rebal import proxies, signals
from rebal.demo import make_panel
from rebal.panel import read_source, trading_calendar
from rebal.paths import REPO_ROOT, output_dir
from rebal.regress import TABLE_COLUMNS, dated, predictive

EXHIBITS = ["table_4"]
START, END = "1961-06-16", "2023-03-17"
SPLIT, GSW_START = "1997-09-10", "1971-08-16"
TERMS = ["threshold", "calendar", "week4", "calendar:week4", "momentum", "ret"]
OMITTED_CONTROLS = ["vix", "move", "epu", "ads", "sentiment"]

# pandas: labeled Series/frames are required by the shared proxy, signal and
# statsmodels APIs. DuckDB projects source files; NumPy generates planted noise.


def long_returns(
    french: pd.DataFrame,
    curve: pd.DataFrame,
    dgs10: pd.Series,
    *,
    pre_1971: str = "dgs10",
) -> pd.DataFrame:
    """Align quotes before pricing; never splice different yield levels."""
    if pre_1971 not in {"dgs10", "omit"}:
        raise ValueError("pre_1971 must be dgs10 or omit")
    calendar = french.index
    rf = french.RF / 100
    curve = curve.reindex(calendar)
    bond = proxies.ty_zero_10(curve, rf)
    if pre_1971 == "dgs10":
        early = proxies.zero_coupon_return(dgs10.reindex(calendar), 10, rf)
        bond = bond.where(calendar >= pd.Timestamp(GSW_START), early)
    equity = (french["Mkt-RF"] + french.RF) / 100
    retained = trading_calendar(equity - rf, bond)
    return (
        pd.DataFrame(
            {
                "r_es": equity - rf,
                "r_ty": bond,
                "rf": rf,
                "r_mkt_french": equity,
                "r_10y_gsw": bond + rf,
            }
        )
        .loc[retained]
        .rename_axis("date")
        .reset_index()
    )


def load_long_panel(pre_1971: str = "dgs10") -> tuple[pd.DataFrame, list[Path]]:
    """Read only the three long-history public inputs with the shared reader."""
    paths: list[Path] = []
    public = REPO_ROOT / "data/public"
    # rebal has no DuckDB manager; the shared panel reader accepts a connection.
    with duckdb.connect() as con:
        french = read_source(
            con,
            public / "french/F-F_Research_Data_Factors_daily.csv",
            ("Mkt-RF", "RF"),
            paths,
        ).loc[START:]
        curve = read_source(
            con,
            public / "gsw/feds200628.csv",
            ("SVENY09", "SVENY10"),
            paths,
        )
        dgs10 = (
            read_source(
                con,
                public / "fred/DGS10.csv",
                ("DGS10",),
                paths,
            ).DGS10
            if pre_1971 == "dgs10"
            else pd.Series(dtype=float)
        )
    return long_returns(french, curve, dgs10, pre_1971=pre_1971), paths


def build_signals(
    panel: pd.DataFrame, *, timing: str = "clean", momentum: str = "medium-slow"
) -> pd.DataFrame:
    """Build on all available history, before applying any regression window."""
    history = dated(panel)
    return signals.build(history.r_es, history.r_ty, timing=timing, momentum=momentum)


def demo_inputs(
    *,
    beta_post: float = -0.4,
    beta_calendar_post: float = -0.3,
    seed: int = 24,
    timing: str = "clean",
    momentum: str = "medium-slow",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Use the real signal engine, then plant only the next-day demo response."""
    panel = make_panel(start="1960-01-04", end="2023-12-29", seed=seed)
    frame = build_signals(panel, timing=timing, momentum=momentum)
    rng = np.random.default_rng(seed + 1)
    response = rng.normal(0, 0.0008, len(frame))
    after_split = frame.date.iloc[1:].to_numpy() >= np.datetime64(SPLIT)
    response[1:] += after_split * (
        beta_post * frame.threshold.to_numpy()[:-1]
        + beta_calendar_post * (frame.calendar * frame.week4).to_numpy()[:-1]
    )
    frame["ret"] = response
    return panel, frame


def build_table(
    frame: pd.DataFrame,
    panel: pd.DataFrame,
    *,
    end: str = END,
    se: str = "hc1",
    hac_lags: int | None = None,
) -> pd.DataFrame:
    """Select both predictor and outcome dates inside each paper window."""
    rows = []
    for column, sample in enumerate(
        [(START, end), (START, "1997-09-09"), (SPLIT, end)], 1
    ):
        # The global endpoint also caps the early subperiod.
        stop = sample[1]
        if end != "latest":
            stop = min(pd.Timestamp(stop), pd.Timestamp(end)).date().isoformat()
        result = predictive(
            frame, panel, TERMS, sample=(sample[0], stop), se=se, hac_lags=hac_lags
        )
        tidy = result.tidy.copy()
        tidy["exhibit"], tidy["column"] = "table_4", str(column)
        rows.append(tidy)
    return pd.concat(rows, ignore_index=True)[TABLE_COLUMNS]


def run(
    demo: bool = False,
    *,
    pre_1971: str = "dgs10",
    end: str = END,
    timing: str = "clean",
    momentum: str = "medium-slow",
    se: str = "hc1",
    hac_lags: int | None = None,
) -> list[Path]:
    """Discoverable exhibit entry point; write only Table 4 artifacts."""
    paths: list[Path] = []
    if demo:
        panel, frame = demo_inputs(timing=timing, momentum=momentum)
    else:
        panel, paths = load_long_panel(pre_1971)
        frame = build_signals(panel, timing=timing, momentum=momentum)
    table = build_table(frame, panel, end=end, se=se, hac_lags=hac_lags)
    destination = output_dir("demo" if demo else "tables")
    path = destination / "table_4.csv"
    table.to_csv(path, index=False)
    metadata_path = destination / "table_4.metadata.json"
    samples = table.loc[
        table.term == "threshold", ["column", "nobs", "sample_start", "sample_end"]
    ]
    metadata_path.write_text(
        json.dumps(
            {
                "module": __name__,
                "created_utc": datetime.now(UTC).isoformat(),
                "demo": demo,
                "inputs": [str(p) for p in paths]
                if paths
                else ["rebal.demo.make_panel"],
                "sha256": {
                    str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
                },
                "parameters": {
                    "pre_1971": pre_1971,
                    "end": end,
                    "timing": timing,
                    "momentum": momentum,
                    "se": se,
                    "hac_lags": hac_lags,
                },
                "first_return_date": panel.date.min().date().isoformat(),
                "first_momentum_date": frame.loc[frame.momentum.notna(), "date"]
                .min()
                .date()
                .isoformat(),
                "samples": samples.to_dict(orient="records"),
                "terms": TERMS,
                "omitted_controls": OMITTED_CONTROLS,
                "outputs": [path.name],
            },
            indent=2,
        )
        + "\n"
    )
    return [path, metadata_path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Table 4 long-sample regressions."
    )
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--pre-1971", choices=["dgs10", "omit"], default="dgs10")
    parser.add_argument("--end", default=END, help="Inclusive outcome date or latest.")
    parser.add_argument("--timing", choices=["clean", "literal"], default="clean")
    parser.add_argument(
        "--momentum", choices=["medium-slow", "all15"], default="medium-slow"
    )
    parser.add_argument("--se", choices=["hc0", "hc1", "hac"], default="hc1")
    parser.add_argument("--hac-lags", type=int)
    args = parser.parse_args()
    if args.hac_lags is not None and args.hac_lags < 0:
        parser.error("--hac-lags must be nonnegative")
    if args.end != "latest":
        try:
            if pd.Timestamp(args.end) <= pd.Timestamp(SPLIT):
                raise ValueError("endpoint must follow the split date")
        except ValueError as exc:
            parser.error(str(exc))
    return args


def main() -> None:
    args = parse_args()
    for path in run(**vars(args)):
        Console().print(str(path), markup=False)


if __name__ == "__main__":
    main()
