"""uv run python3 -m rebal.exhibits --all --demo

CLI Arguments:
--all: run all discovered exhibit modules.
--demo: use synthetic inputs and output/demo/.
--only ID ...: restrict execution to modules which own the given IDs.

Discovers exhibit modules with pkgutil. Each module reads its own inputs and
returns its output paths; this runner reads and writes no data itself.
"""

from __future__ import annotations

import argparse
import importlib
import pkgutil
from types import ModuleType

from rich.console import Console

import rebal.exhibits


def discover() -> list[ModuleType]:
    modules = []
    for info in sorted(
        pkgutil.iter_modules(rebal.exhibits.__path__), key=lambda item: item.name
    ):
        if info.name.startswith("_"):
            continue
        module = importlib.import_module(f"rebal.exhibits.{info.name}")
        if hasattr(module, "EXHIBITS") and callable(getattr(module, "run", None)):
            modules.append(module)
    return modules


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run automatically discovered exhibits."
    )
    parser.add_argument(
        "--all", action="store_true", help="Run all modules (the default)."
    )
    parser.add_argument("--demo", action="store_true", help="Use synthetic fixtures.")
    parser.add_argument(
        "--only", nargs="+", metavar="ID", help="Run modules owning these exhibit IDs."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    modules = discover()
    if args.only:
        known = {exhibit for module in modules for exhibit in module.EXHIBITS}
        unknown = set(args.only) - known
        if unknown:
            raise SystemExit(f"Unknown exhibit IDs: {', '.join(sorted(unknown))}")
        modules = [
            module for module in modules if set(args.only).intersection(module.EXHIBITS)
        ]
    console = Console()
    console.print(f"{len(modules)} exhibit modules")
    for module in modules:
        for path in module.run(demo=args.demo):
            console.print(str(path), markup=False)


if __name__ == "__main__":
    main()
