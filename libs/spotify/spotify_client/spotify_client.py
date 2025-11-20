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
        self.current_user_id = self.current_user()["id"]
