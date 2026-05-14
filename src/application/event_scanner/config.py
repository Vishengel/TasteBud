from pydantic_settings import SettingsConfigDict

from common.config import BaseConfig


class Config(BaseConfig):
    city_of_residence: str

    model_config = SettingsConfigDict(
        env_file=BaseConfig.project_root / ".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )


CONFIG = Config()
