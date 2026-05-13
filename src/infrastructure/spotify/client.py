from collections.abc import Callable
from typing import ClassVar

from spotipy import CacheFileHandler, Spotify, SpotifyOAuth

from infrastructure.spotify.config import CONFIG
from infrastructure.spotify.time_range import TimeRange
from libs.common.util.data_util import chunk_generator


class SpotifyClient(Spotify):
    SCOPE: ClassVar[list[str]] = [
        "user-library-read",
        "user-library-modify",
        "playlist-modify-public",
        "playlist-modify-private",
        "user-top-read",
    ]
    GET_ITEM_LIMIT: ClassVar[int] = 50  # Spotify API allows up to 50 items per get request
    PUT_ITEM_LIMIT: ClassVar[int] = 100  # Spotify API allows up to 100 items per put request

    def __init__(self, user_id: str | None = None):
        cache_filename = f"credentials_{user_id}" if user_id else "credentials"
        super().__init__(
            auth_manager=SpotifyOAuth(
                client_id=CONFIG.spotipy_client_id,
                client_secret=CONFIG.spotipy_client_secret.get_secret_value(),
                redirect_uri=CONFIG.spotipy_redirect_uri,
                scope=self.SCOPE,
                cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / cache_filename),
            )
        )

    @property
    def current_user_id(self) -> str:
        return self.current_user()["id"]

    def fetch_all_playlists(self, user_id: str) -> list[dict]:
        return self._fetch_paginated_items(self.user_playlists, user_id, limit=self.GET_ITEM_LIMIT)

    def fetch_tracks_for_playlist(self, playlist_id: str) -> list[dict]:
        return self._fetch_paginated_items(self.playlist_items, playlist_id, limit=self.GET_ITEM_LIMIT)

    def replace_tracks_in_playlist(self, playlist_id: str, track_uris: list[str]):
        self.playlist_replace_items(playlist_id, [])
        for chunk in chunk_generator(iterable=track_uris, n=self.PUT_ITEM_LIMIT):
            self.playlist_add_items(playlist_id, chunk)

    def fetch_top_tracks(self, time_range: TimeRange, limit: int = 50) -> list[dict]:
        result = self.current_user_top_tracks(limit=limit, time_range=time_range)
        return result["items"]

    def fetch_artist_top_tracks(self, artist_id: str, country: str = "US") -> list[dict]:
        result = self.artist_top_tracks(artist_id, country=country)
        return result["tracks"]

    def _fetch_paginated_items(self, fetch_function: Callable, *args, **kwargs) -> list[dict]:
        items = []
        result = fetch_function(*args, **kwargs)
        items.extend(result["items"])
        while result := self.next(result):
            items.extend(result["items"])
        return items
