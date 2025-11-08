from ensmallen import Graph

from tastebud.graph.graph_dataclass import GraphSchema


class GrapeGraphBuilder:
    graph: Graph

    def build_graph(self, graph: GraphSchema) -> Graph:
        self.graph = Graph.from_pd(
            edges_df=graph.edges.to_pandas(),
            nodes_df=graph.nodes.to_pandas(),
            node_name_column="name",
            node_type_column="type",
            edge_src_column="subject",
            edge_dst_column="object",
            edge_weight_column="weight",
            edge_type_column="predicate",
            node_types_separator="|",
            directed=True,
            name="Spotify History Graph",
        )
