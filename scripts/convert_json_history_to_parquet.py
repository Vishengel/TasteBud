import argparse
from pathlib import Path

from src.libs.spotify.spotify_history.data_processing.streaming_history_to_dataframe_conversion import (
    convert_streaming_history_to_dataframe,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--streaming_history_dir", type=Path)
    parser.add_argument("--user_name", type=Path)
    args = parser.parse_args()
    convert_streaming_history_to_dataframe(args.streaming_history_dir, args.user_name)
