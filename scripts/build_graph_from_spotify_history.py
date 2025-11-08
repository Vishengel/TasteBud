import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from tastebud.config import CONFIG
from tastebud.graph.grape_graph_constructor import GrapeGraphConstructor
from tastebud.graph.tastedive_graph_data_extractor import TastediveGraphDataExtractor
from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("parquet_file", type=Path)
    return parser.parse_args()


def build_graph_from_spotify_history(spotify_history_df: SpotifyHistoryDataFrame):
    graph_data_extractor = TastediveGraphDataExtractor(CONFIG.tastedive_api_key, spotify_history_df)
    GrapeGraphConstructor(graph_data_extractor.nodes_df, graph_data_extractor.edges_df)


if __name__ == "__main__":
    args = get_args()
    load_dotenv()
    spotify_history_df = SpotifyHistoryDataFrame.from_parquet(args.parquet_file)
    build_graph_from_spotify_history(spotify_history_df)
