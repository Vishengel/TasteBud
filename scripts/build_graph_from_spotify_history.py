import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv
from embiggen import GraphVisualizer

from libs.graph.graph_builders.grape_graph_builder import GrapeGraphBuilder
from libs.graph.graph_builders.graph_builder_pipeline import GraphBuilderPipeline
from libs.graph.graph_entity_collectors.graph_entity_collector import GraphEntityCollector
from libs.graph.graph_entity_collectors.graph_schema_builder import GraphSchemaBuilder
from libs.graph.graph_entity_collectors.lastfm_entity_source import LastFMEntitySource
from libs.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("pylast").setLevel(logging.WARNING)
logging.getLogger("embiggen").setLevel(logging.DEBUG)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("parquet_file", type=Path)
    return parser.parse_args()


def build_graph_from_spotify_history(spotify_history_df: SpotifyHistoryDataFrame):
    lastfm_builder = GraphEntityCollector(LastFMEntitySource())

    schema_builder = GraphSchemaBuilder([lastfm_builder])

    pipeline = GraphBuilderPipeline(schema_builder, GrapeGraphBuilder)
    graph = pipeline.build(spotify_history_df)

    return graph


if __name__ == "__main__":
    args = get_args()
    load_dotenv()
    spotify_history_df = SpotifyHistoryDataFrame.from_parquet(args.parquet_file)
    graph = build_graph_from_spotify_history(spotify_history_df)
    visualization = GraphVisualizer(graph).plot_dot()
    visualization.engine = "fdp"
    visualization.render()
