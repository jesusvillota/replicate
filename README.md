# Rebalancing replication

This repo replicates Harvey, Mazzoleni and Melone (2026), *The Unintended Consequences of Rebalancing*.
The paper tests whether portfolio rebalancing predicts next-day stock-minus-bond returns.

1. Install the package: `uv sync`.
2. Run the source fetchers: `uv run python3 -m rebal.fetch.<source>`.
3. Build the daily panel: `uv run python3 -m rebal.panel --build`.
4. Build signals: `uv run python3 -m rebal.signals --build`.
5. Build exhibits: `uv run python3 -m rebal.exhibits --all`.

TASK-001 provides the scaffold. Fetchers, panel construction, signals and exhibit modules arrive in later tasks.

Check the synthetic fixtures with `uv run python3 -m rebal.demo --check`.
Run the empty exhibit runner with `uv run python3 -m rebal.exhibits --all --demo`.
Run tests with `uv run pytest`.

The [source map](docs/data/sources.md) records public and licensed storage rules.
Set `REPLICATE_DATA_DIR` to change the external data root (default: `~/data/replicate`).
Licensed data and processed files stay there. Public source files live in `data/public/`.
Demo outputs go to the ignored `output/demo/` directory.
The package reads the environment variable; it does not load `.env` automatically.

Read the [daily panel](docs/contracts/daily_panel.md), [signals](docs/contracts/signals.md),
and [exhibits](docs/contracts/exhibits.md) contracts before adding a module.
Each fetch task adds a [source card](docs/data/cards/TEMPLATE.md).
See the [goal plan](goals/hmm-rebalancing/README.md) for task ownership and the paper notes.
