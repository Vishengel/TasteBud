from pathlib import Path
from typing import Literal

import polars as pl

from tastebud.config import CONFIG
from tastebud.util.file_util import get_files_in_dir, load_json_from_file, logger


def get_spotify_history_files_in_dir(
    dir_path: Path, history_type: Literal["audio", "video", "all"] = "all"
) -> list[Path]:
    if history_type == "audio":
        logger.info("Getting audio history files.")
        file_pattern = "*Audio*.json"
    elif history_type == "video":
        logger.info("Getting video history files.")
        file_pattern = "*Video*.json"
    else:
        logger.info("Getting all .json files.")
        file_pattern = "*.json"
    return get_files_in_dir(dir_path, file_pattern=file_pattern)


def _get_year_range_from_json_file_names(json_files: list[Path]) -> str:
    if len(json_files) == 1:
        return json_files[0].stem.split("_")[-2]

    first_year_range = json_files[0].stem.split("_")[-2]
    last_year_range = json_files[-1].stem.split("_")[-2]

    return f"{first_year_range.split('-')[0]}-{last_year_range.split('-')[-1]}"


def _get_records_from_json(json_path: Path) -> list[dict]:
    track_records: list[dict] = []
    json_dict = load_json_from_file(json_path=json_path)
    for track_record in json_dict:
        track_records.append(
            {
                "ts": track_record["ts"],
                "ms_played": track_record["ms_played"],
                "artist": track_record["master_metadata_album_artist_name"],
                "track": track_record["master_metadata_track_name"],
                "track_uri": track_record["spotify_track_uri"],
                "skipped": track_record["skipped"],
            }
        )
    return track_records


def convert_streaming_history_to_dataframe(streaming_history_dir: Path, user_name: str) -> None:
    json_files = get_spotify_history_files_in_dir(dir_path=streaming_history_dir, history_type="audio")
    year_range = _get_year_range_from_json_file_names(json_files=json_files)

    output_file_name = f"Streaming_History_Audio_{user_name}_{year_range}.parquet"

    track_records: list[dict] = []
    for json_file in json_files:
        track_records.extend(_get_records_from_json(json_path=json_file))

    df = pl.from_dicts(track_records)
    df.write_parquet(CONFIG.data_dir / output_file_name)
