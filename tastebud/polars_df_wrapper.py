import logging
from pathlib import Path

import polars

logger = logging.getLogger()


class PolarsDfWrapper:
    def __init__(self, df: polars.DataFrame):
        self.df = df

    def print_df_info(self):
        logger.info("Rows: %s", self.df.shape[0])
        logger.info("Columns: %s", self.df.shape[1])
        logger.info("Columns: %s", self.df.columns)
        logger.info("Top 10 rows: %s", self.df.head(10))
        logger.info("Bottom 10 rows: %s", self.df.tail(10))

    @classmethod
    def from_parquet(cls, parquet_path: str | Path) -> "PolarsDfWrapper":
        return cls(polars.read_parquet(parquet_path))

    def to_parquet(self, parquet_path: str | Path) -> None:
        self.df.write_parquet(parquet_path)
