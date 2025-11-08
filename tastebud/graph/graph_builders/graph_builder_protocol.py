from typing import Protocol


class GraphBuilder(Protocol):
    def build_graph(self) -> None: ...
