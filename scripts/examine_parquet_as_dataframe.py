import argparse
import logging
from pathlib import Path

from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("parquet_file", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    polars_wrapper = SpotifyHistoryDataFrame.from_parquet(args.parquet_file)
    polars_wrapper.print_df_info()
