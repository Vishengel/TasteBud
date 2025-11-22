from typing import Any, Protocol

from src.libs.graph.graph_dataclass import GraphSchema


class GraphBuilder(Protocol):
    graph: Any

    def build_graph(self, graph_schema: GraphSchema) -> None: ...
