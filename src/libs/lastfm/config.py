from base_config import BaseConfig


class Config(BaseConfig):
    lastfm_api_key: str
    lastfm_shared_secret: str
    lastfm_username: str
    lastfm_password: str


CONFIG = Config()
