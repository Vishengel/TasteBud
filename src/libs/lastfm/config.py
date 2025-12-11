from pathlib import Path

from base_config import BaseConfig


class Config(BaseConfig):
    package_root: Path = Path(__file__).parent

    lastfm_api_key: str
    lastfm_shared_secret: str
    lastfm_username: str
    lastfm_password: str


CONFIG = Config()
