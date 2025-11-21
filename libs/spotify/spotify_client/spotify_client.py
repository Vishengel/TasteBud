from collections.abc import Callable
from typing import ClassVar

from spotipy import CacheFileHandler, Spotify, SpotifyOAuth

from config import CONFIG


class SpotifyClient(Spotify):
    SCOPE: ClassVar[list[str]] = [
        "user-library-read",
        "user-library-modify",
        "playlist-modify-public",
        "playlist-modify-private",
    ]

    def __init__(self):
        super().__init__(
            auth_manager=SpotifyOAuth(
                scope=self.SCOPE, cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / "credentials")
            )
        )

    @property
    def current_user_id(self) -> str:
        return self.current_user()["id"]

    def fetch_all_playlists(self, user_id: str) -> list[dict]:
        return self._fetch_paginated_items(self.user_playlists, user_id, limit=100)

    def fetch_tracks_for_playlist(self, playlist_id: str) -> list[dict]:
        return self._fetch_paginated_items(self.playlist_tracks, playlist_id, limit=100)

    def _fetch_paginated_items(self, fetch_function: Callable, *args, **kwargs) -> list[dict]:
        items = []
        result = fetch_function(*args, **kwargs)
        items.extend(result["items"])
        while result := self.next(result):
            items.extend(result["items"])
        return items
