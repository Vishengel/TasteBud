from dataclasses import dataclass

import polars as pl


@dataclass
class GraphSchema:
    nodes: pl.DataFrame
    edges: pl.DataFrame
