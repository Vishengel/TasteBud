import json
import logging
from glob import glob
from pathlib import Path

logger = logging.getLogger()


def load_json_from_file(json_path: Path) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_files_in_dir(dir_path: Path, file_pattern: str) -> list[Path]:
    return [Path(str_path) for str_path in glob(str(dir_path / file_pattern))]
