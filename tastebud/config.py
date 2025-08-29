from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    package_root: Path = Path(__file__).parent
    project_root: Path = package_root.parent
    data_dir: Path = project_root / "data"


CONFIG = _Config()
