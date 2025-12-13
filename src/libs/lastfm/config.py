from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from base_config import BaseConfig


class Config(BaseConfig):
    package_root: Path = Path(__file__).parent

    lastfm_api_key: str
    lastfm_shared_secret: SecretStr
    lastfm_username: str
    lastfm_password: SecretStr

    model_config = SettingsConfigDict(
        env_file=BaseConfig.project_root / ".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )


CONFIG = Config()
