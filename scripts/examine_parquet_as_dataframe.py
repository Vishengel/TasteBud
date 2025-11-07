import argparse
import logging
from pathlib import Path

from tastebud.spotify.polars_df_wrapper import PolarsDfWrapper

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("parquet_file", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    polars_wrapper = PolarsDfWrapper.from_parquet(args.parquet_file)
    polars_wrapper.print_df_info()
