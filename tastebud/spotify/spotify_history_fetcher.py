import logging
from pathlib import Path

from diskcache import Cache
from polars import DataFrame, col, read_parquet
from spotipy import Spotify
from tqdm import tqdm

from tastebud.config import CONFIG
from tastebud.util.data_util import chunk_generator

logger = logging.getLogger(__name__)


class SpotifyHistoryFetcher:
    artist_cache = Cache(CONFIG.cache_dir / "spotify_artist_meta")

    def __init__(self, sp_client: Spotify, parquet_path: Path):
        self.sp_client = sp_client
        self.history_df = read_parquet(parquet_path)
        logger.info(
            "Loaded Spotify history from %s with columns %s. History contains %d entries.",
            parquet_path.name,
            self.history_df.columns,
            self.history_df.shape[0],
        )
        self._get_artist_uris()
        logger.debug(self.history_df.head())

        output_path = parquet_path.with_name(parquet_path.name + "_enhanced.parquet")
        self.history_df.write_parquet(output_path)

    def _get_cached_artist_meta(self, batch: list[str]) -> tuple[list, list]:
        tracks_to_fetch = []
        cached_meta = []
        for track_uri in batch:
            artists_for_track = (
                self.history_df.filter(col("track_uri") == track_uri).select("artist").unique().to_series().to_list()
            )
            for artist_name in artists_for_track:
                cache_key = f"{track_uri}|{artist_name}"
                if cache_key in self.artist_cache:
                    cached_meta.append(self.artist_cache[cache_key])
                else:
                    tracks_to_fetch.append(track_uri)

        return cached_meta, tracks_to_fetch

    def _get_artist_meta_for_track(self, track: dict) -> dict:
        track_uri = track["uri"]
        history_rows = (
            self.history_df.filter(col("track_uri") == track_uri).select(["artist"]).unique().to_series().to_list()
        )

        for artist in track["artists"]:
            if artist["name"] in history_rows:
                meta = {"artist": artist["name"], "track_uri": track_uri, "artist_uri": artist["uri"]}
                cache_key = f"{track_uri}|{artist['name']}"
                self.artist_cache[cache_key] = meta
                return meta

        raise ValueError(f"None of {track['artists']} are in {history_rows}.")

    def _get_artist_uris(self, batch_size: int = 50) -> None:
        unique_track_uris = self.history_df["track_uri"].unique().to_list()

        all_artist_meta = []

        for batch in tqdm(
            chunk_generator(unique_track_uris, batch_size), total=(len(unique_track_uris) // batch_size + 1)
        ):
            cached_meta, tracks_to_fetch = self._get_cached_artist_meta(batch)
            all_artist_meta.extend(cached_meta)
            tracks_to_fetch = list(set(tracks_to_fetch))

            if not tracks_to_fetch:
                continue

            tracks_data = self.sp_client.tracks(tracks_to_fetch)["tracks"]

            for track in tracks_data:
                try:
                    all_artist_meta.extend(self._get_artist_meta_for_track(track))
                except ValueError as exc:
                    logger.error(exc)

        artist_df = DataFrame(all_artist_meta).unique()
        self.history_df = self.history_df.join(artist_df, on=["artist", "track_uri"], how="left")

    def _get_artist_genres(self, batch_size: int = 50):
        unique_artists = self.history_df.select(["artist", "artist_uri"]).unique().to_dicts()

        all_artist_genres = []

        for batch in tqdm(chunk_generator(unique_artists, batch_size), total=(len(unique_artists) // batch_size + 1)):
            artist_ids_to_fetch = []
            cached = []

            for artist in batch:
                cache_key = f"genres|{artist['artist_uri']}"
                if cache_key in self.artist_cache:
                    cached.append(self.artist_cache[cache_key])
                else:
                    artist_ids_to_fetch.append(artist["artist_uri"])

            # Add cached genres
            all_artist_genres.extend(cached)

            if not artist_ids_to_fetch:
                continue

            results = self.sp_client.artists(artist_ids_to_fetch)["artists"]
            for artist in results:
                meta = {"artist": artist["name"], "artist_uri": artist["uri"], "genres": artist["genres"]}
                cache_key = f"genres|{artist['uri']}"
                self.artist_cache[cache_key] = meta
                all_artist_genres.append(meta)

        artist_genres_df = DataFrame(all_artist_genres).unique()

        # Join genres back into your history
        self.history_df = self.history_df.join(artist_genres_df, on=["artist", "artist_uri"], how="left")
