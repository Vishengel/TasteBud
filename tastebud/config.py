from pathlib import Path

from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    package_root: Path = Path(__file__).parent
    project_root: Path = package_root.parent
    cache_dir: Path = project_root / "cache"
    data_dir: Path = project_root / "data"

    cache_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)


CONFIG = _Config()
