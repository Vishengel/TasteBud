from pathlib import Path

from pydantic_settings import SettingsConfigDict

from common.config import BaseConfig


class GeolocationConfig(BaseConfig):
    package_root: Path = Path(__file__).parent

    geonames_username: str

    model_config = SettingsConfigDict(
        env_file=BaseConfig.project_root / ".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )


CONFIG = GeolocationConfig()
