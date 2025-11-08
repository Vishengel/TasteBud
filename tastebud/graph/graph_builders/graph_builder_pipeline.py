from tastebud.graph.graph_builders.graph_builder_protocol import GraphBuilder
from tastebud.graph.graph_entity_collectors.graph_schema_builder import GraphSchemaBuilder
from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame


class GraphBuilderPipeline:
    def __init__(self, schema_builder: GraphSchemaBuilder, graph_builder_class: type[GraphBuilder]):
        self.schema_builder = schema_builder
        self.graph_builder_class = graph_builder_class

    def build(self, spotify_history: SpotifyHistoryDataFrame):
        unique_artists = set(spotify_history.unique_artists.to_list())

        graph_schema = self.schema_builder.create_schema(unique_artists)

        graph_builder = self.graph_builder_class()
        graph_builder.build_graph(graph_schema)

        return graph_builder.graph
