from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_LEVELS = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_")
    LEVEL: str | None = Field("INFO")

    @field_validator("LEVEL")
    @classmethod
    def validate_level(cls, value):
        return value if value in LOG_LEVELS else "DEBUG"


LOG_SETTINGS = LogSettings()

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "[%(asctime)s] [%(process)s] [%(name)s] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
    },
    "handlers": {
        "std_out_handler": {
            "formatter": "app",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["std_out_handler"],
        "level": LOG_SETTINGS.LEVEL,
    },
}
