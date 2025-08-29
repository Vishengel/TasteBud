import json
from glob import glob
from pathlib import Path
from typing import Literal


def load_json_from_file(json_path: Path) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_json_files_in_dir(json_path: Path, history_type: Literal["audio", "video", "all"] = "all") -> list[Path]:
    if history_type == "audio":
        file_pattern = "*Audio*.json"
    elif history_type == "video":
        file_pattern = "*Video*.json"
    else:
        file_pattern = "*.json"
    return [Path(str_path) for str_path in glob(str(json_path / file_pattern))]
