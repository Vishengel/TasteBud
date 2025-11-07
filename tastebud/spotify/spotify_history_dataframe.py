import logging
from pathlib import Path

import polars
from polars import count

logger = logging.getLogger()


class SpotifyHistoryDataFrame:
    history_df: polars.DataFrame
    play_count_per_artist: polars.DataFrame
    play_count_per_track: polars.DataFrame

    def __init__(self, history_df: polars.DataFrame):
        self.history_df = history_df
        self._compute_aggregates()

    def print_df_info(self):
        logger.info("Rows: %s", self.history_df.shape[0])
        logger.info("Columns: %s", self.history_df.shape[1])
        logger.info("Columns: %s", self.history_df.columns)
        logger.info("Top 10 rows: %s", self.history_df.head(10))
        logger.info("Bottom 10 rows: %s", self.history_df.tail(10))

    @classmethod
    def from_parquet(cls, parquet_path: str | Path) -> "SpotifyHistoryDataFrame":
        return cls(polars.read_parquet(parquet_path))

    def to_parquet(self, parquet_path: str | Path) -> None:
        self.history_df.write_parquet(parquet_path)

    def _compute_aggregates(self):
        self.play_count_per_artist = self._aggregate_by_col_names("artist")
        self.play_count_per_track = self._aggregate_by_col_names(["track_uri", "track", "artist"])

    def _aggregate_by_col_names(self, col_names: str | list[str]):
        aggregate_df = (
            self.history_df.group_by(col_names).agg(count().alias("play_count")).sort("play_count", descending=True)
        )
        return aggregate_df
