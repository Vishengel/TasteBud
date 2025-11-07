from abc import ABC
from typing import Protocol


class GraphConstructor(Protocol):
    def construct_graph(self) -> None:
        ...