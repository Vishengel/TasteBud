from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    project_root: ClassVar[Path] = Path(__file__).parent
    cache_dir: ClassVar[Path] = project_root / "cache"
    data_dir: ClassVar[Path] = project_root / "data"

    cache_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    model_config = SettingsConfigDict(
        env_file=project_root / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )
