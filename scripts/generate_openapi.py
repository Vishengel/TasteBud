#!/usr/bin/env python
import argparse
import importlib
import json
from pathlib import Path
from pkgutil import iter_modules

from dotenv import dotenv_values

from src import services


def projects_with_server(base_dir: str) -> list[str]:
    base = Path(base_dir)
    return [m.name for m in iter_modules([base_dir]) if (base / m.name / "server").exists()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--disable", action="store_true")
    args = parser.parse_args()
    if args.disable:
        return

    services_module = services.__path__[0]

    for name in projects_with_server(services_module):
        mod = importlib.import_module(f"{services.__name__}.{name}.server.app")
        app = getattr(mod, "app", None)

        if app is None or not hasattr(app, "openapi"):
            continue

        schema = app.openapi()
        schema.setdefault("servers", [{"url": "/"}])

        release_conf = Path(services_module) / name / "release.conf"
        if release_conf.exists():
            ver = dotenv_values(release_conf).get("RELEASE_VERSION")
            if ver:
                schema.setdefault("info", {}).update({"version": ver})

        out = Path(services_module) / name / "server" / "openapi.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
