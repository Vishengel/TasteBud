from pathlib import Path

from base_config import BaseConfig


class Config(BaseConfig):
    package_root: Path = Path(__file__).parent

    tastedive_api_key: str


CONFIG = Config()
