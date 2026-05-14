#!/usr/bin/env python
import argparse
import importlib
import json
from pathlib import Path
from pkgutil import iter_modules

from src.interface import api as services


def projects_with_app(base_dir: str) -> list[str]:
    base = Path(base_dir)
    return [m.name for m in iter_modules([base_dir]) if (base / m.name / "app.py").exists()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disable", action="store_true")
    args = parser.parse_args()
    if args.disable:
        return

    services_module = services.__path__[0]

    for name in projects_with_app(services_module):
        mod = importlib.import_module(f"{services.__name__}.{name}.app")
        app = getattr(mod, "app", None)

        if app is None or not hasattr(app, "openapi"):
            continue

        schema = app.openapi()
        schema.setdefault("servers", [{"url": "/"}])

        out = Path(services_module) / name / "openapi.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
