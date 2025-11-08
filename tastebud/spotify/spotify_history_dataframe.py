import logging
from pathlib import Path

import polars
from polars import count

logger = logging.getLogger(__name__)


class SpotifyHistoryDataFrame:
    TIMESTAMP_COL_NAME = "ts"
    ARTIST_COL_NAME = "artist"
    ARTIST_URI_COL_NAME = "artist_uri"
    TRACK_COL_NAME = "track"
    TRACK_URI_COL_NAME = "track_uri"
    PLAY_COUNT_COL_NAME = "play_count"

    history_df: polars.DataFrame
    play_count_per_artist: polars.DataFrame
    play_count_per_track: polars.DataFrame

    def __init__(self, history_df: polars.DataFrame):
        self.history_df = history_df.with_columns(polars.col(self.TIMESTAMP_COL_NAME).str.to_datetime()).sort(
            self.TIMESTAMP_COL_NAME, descending=False
        )
        self._compute_aggregates()
        self.print_df_info()

    def get_eligible_artists(self, min_duration_ms: int = 60000, min_play_count: int = 50) -> polars.Series:
        # Step 1: Filter tracks with sufficient duration
        filtered_tracks = self.history_df.filter(polars.col("ms_played") > min_duration_ms)

        # Step 2: Group by artist and calculate play count
        eligible_artists_df = (
            filtered_tracks.group_by(self.ARTIST_COL_NAME)
            .agg(polars.count().alias("play_count"))
            .filter(polars.col("play_count") >= min_play_count)
        )

        # Step 3: Extract unique artist names
        return (
            eligible_artists_df.select(self.ARTIST_COL_NAME)
            .drop_nans()
            .filter(polars.col(self.ARTIST_COL_NAME).is_not_null())
            .unique()
            .to_series()
        )

    @property
    def history_start_date(self):
        return self.history_df.item(0, self.TIMESTAMP_COL_NAME)

    @property
    def history_end_date(self):
        return self.history_df.item(-1, self.TIMESTAMP_COL_NAME)

    @property
    def unique_artists(self) -> polars.Series:
        return (
            self.history_df.select(self.ARTIST_COL_NAME)
            .drop_nans()
            .filter(polars.col(self.ARTIST_COL_NAME).is_not_null())
            .unique()
            .to_series()
        )

    def print_df_info(self):
        logger.info("Created Spotify History DataFrame:")
        logger.info("N Rows: %s", self.history_df.shape[0])
        logger.info("Columns: %s", self.history_df.columns)
        logger.info("Timespan: [%s, %s]", self.history_start_date, self.history_end_date)
        logger.debug("Top 10 rows: %s", self.history_df.head(10))
        logger.debug("Bottom 10 rows: %s", self.history_df.tail(10))

    @classmethod
    def from_parquet(cls, parquet_path: str | Path) -> "SpotifyHistoryDataFrame":
        return cls(polars.read_parquet(parquet_path))

    def to_parquet(self, parquet_path: str | Path) -> None:
        self.history_df.write_parquet(parquet_path)

    def _compute_aggregates(self):
        self.play_count_per_artist = self._aggregate_by_col_names(self.ARTIST_COL_NAME)
        self.play_count_per_track = self._aggregate_by_col_names(
            [self.TRACK_URI_COL_NAME, self.TRACK_COL_NAME, self.ARTIST_COL_NAME]
        )

    def _aggregate_by_col_names(self, col_names: str | list[str]):
        aggregate_df = (
            self.history_df.group_by(col_names)
            .agg(count().alias(self.PLAY_COUNT_COL_NAME))
            .sort(self.PLAY_COUNT_COL_NAME, descending=True)
        )
        return aggregate_df
