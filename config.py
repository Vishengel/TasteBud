from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class _Config(BaseSettings):
    package_root: Path = Path(__file__).parent
    project_root: Path = package_root.parent
    cache_dir: Path = project_root / "cache"
    data_dir: Path = project_root / "data"

    spotipy_client_id: str
    spotipy_client_secret: str
    spotipy_redirect_uri: str
    tastedive_api_key: str
    lastfm_api_key: str
    lastfm_shared_secret: str
    lastfm_username: str
    lastfm_password: str

    cache_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


CONFIG = _Config()
