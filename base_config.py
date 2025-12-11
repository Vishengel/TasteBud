from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class BaseConfig(BaseSettings):
    project_root: ClassVar[Path] = Path(__file__).parent
    cache_dir: ClassVar[Path] = project_root / "cache"
    data_dir: ClassVar[Path] = project_root / "data"

    cache_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)


BASE_CONFIG = BaseConfig()
