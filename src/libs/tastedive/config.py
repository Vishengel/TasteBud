from pathlib import Path

from pydantic_settings import SettingsConfigDict

from base_config import BaseConfig


class Config(BaseConfig):
    package_root: Path = Path(__file__).parent

    tastedive_api_key: str

    model_config = SettingsConfigDict(
        env_file=BaseConfig.project_root / ".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )


CONFIG = Config()
