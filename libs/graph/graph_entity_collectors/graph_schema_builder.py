from polars import concat

from libs.graph.graph_dataclass import GraphSchema
from libs.graph.graph_entity_collectors.graph_entity_collector import GraphEntityCollector


class GraphSchemaBuilder:
    def __init__(self, builders: list[GraphEntityCollector]):
        self.builders = builders

    def create_schema(self, unique_artists: set[str]) -> GraphSchema:
        all_nodes = []
        all_edges = []

        for builder in self.builders:
            nodes_df, edges_df = builder.create_schema(unique_artists)
            all_nodes.append(nodes_df)
            all_edges.append(edges_df)

        return GraphSchema(concat(all_nodes, how="vertical"), concat(all_edges, how="vertical"))
