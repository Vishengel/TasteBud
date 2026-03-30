from ensmallen import Graph

from libs.graph.graph_builders.graph_builder_protocol import GraphBuilder
from libs.graph.graph_dataclass import GraphSchema


class GrapeGraphBuilder(GraphBuilder):
    graph: Graph

    def build_graph(self, graph_schema: GraphSchema) -> Graph:
        self.graph = Graph.from_pd(
            edges_df=graph_schema.edges.drop(["weight", "predicate"]).to_pandas(),
            nodes_df=graph_schema.nodes.to_pandas(),
            node_name_column="name",
            node_type_column="type",
            edge_src_column="subject",
            edge_dst_column="object",
            # edge_weight_column="weight",
            # edge_type_column="predicate",
            node_types_separator="|",
            directed=False,
            name="Spotify History Graph",
        )
