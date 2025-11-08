import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from tastebud.config import CONFIG
from tastebud.graph.graph_builders.grape_graph_builder import GrapeGraphBuilder
from tastebud.graph.graph_builders.graph_builder_pipeline import GraphBuilderPipeline
from tastebud.graph.graph_entity_collectors.graph_schema_builder import GraphSchemaBuilder
from tastebud.graph.graph_entity_collectors.tastedive_graph_entity_collector import TastediveGraphEntityCollector
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
    tastedive_builder = TastediveGraphEntityCollector(CONFIG.tastedive_api_key, spotify_history_df)

    schema_builder = GraphSchemaBuilder([tastedive_builder])

    pipeline = GraphBuilderPipeline(schema_builder, GrapeGraphBuilder)
    graph = pipeline.build(spotify_history_df)

    return graph


if __name__ == "__main__":
    args = get_args()
    load_dotenv()
    spotify_history_df = SpotifyHistoryDataFrame.from_parquet(args.parquet_file)
    build_graph_from_spotify_history(spotify_history_df)
