import argparse
from pathlib import Path

from tastebud.spotify.data_processing.streaming_history_to_parquet_conversion import (
    convert_streaming_history_to_parquet,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--streaming_history_dir", type=Path)
    parser.add_argument("--user_name", type=Path)
    args = parser.parse_args()
    convert_streaming_history_to_parquet(args.streaming_history_dir, args.user_name)
