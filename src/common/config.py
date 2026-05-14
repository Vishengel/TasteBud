from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    project_root: ClassVar[Path] = Path(__file__).parent.parent.parent
    cache_dir: ClassVar[Path] = project_root / "cache"
    data_dir: ClassVar[Path] = project_root / "data"

    model_config = SettingsConfigDict(
        env_file=project_root / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
    )

    @classmethod
    def ensure_dirs(cls) -> None:
        cls.cache_dir.mkdir(parents=True, exist_ok=True)
        cls.data_dir.mkdir(parents=True, exist_ok=True)
