from tastebud.graph.graph_dataclass import GraphSchema


class GrapeGraphBuilder:
    def __init__(self, graph: GraphSchema):
        self.graph_schema = graph

    def build_graph(self) -> None:
        self.graph = None
