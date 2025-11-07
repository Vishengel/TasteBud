import polars as pl


class GrapeGraphConstructor:
    def __init__(self, nodes_df: pl.DataFrame, edges_df: pl.DataFrame):
        self.nodes_df = nodes_df
        self.edges_df = edges_df

    def construct_graph(self) -> None:
        self.graph = None
