import logging

import pylast
from diskcache import Cache
from pylast import MalformedResponseError, NetworkError, WSError

from tastebud.config import CONFIG

logger = logging.getLogger(__name__)


class LastFMClient:
    artist_cache = Cache(CONFIG.cache_dir / "lastfm_similar_artists")

    def __init__(self, api_key: str, api_secret: str, username: str, password: str):
        self.network = pylast.LastFMNetwork(
            api_key=api_key, api_secret=api_secret, username=username, password_hash=pylast.md5(password)
        )

    def get_similar_artists(self, artist_name: str, limit: int | None = 10) -> list[str]:
        cache_key = f"{artist_name}{limit}" if limit is not None else artist_name
        cached_response = self.artist_cache.get(cache_key)
        if cached_response is not None:
            return cached_response

        artist = self.network.get_artist(artist_name)

        try:
            similar_artists = artist.get_similar(limit=limit)
        except (MalformedResponseError, WSError, NetworkError) as e:
            logger.error(f"Error fetching similar artists for {artist_name}: {e}")
            return []

        similar_artist_names = [similar_artist.item.name for similar_artist in similar_artists]
        self.artist_cache.set(cache_key, similar_artist_names)

        return similar_artist_names
