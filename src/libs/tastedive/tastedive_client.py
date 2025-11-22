import sys
from urllib.parse import quote

from diskcache import Cache

from config import CONFIG
from src.libs.common.query_util import TooManyRequestsError, httpx_get_request


class TastediveClient:
    TASTEDIVE_URL: str = "https://tastedive.com/api/similar"
    artist_cache = Cache(CONFIG.cache_dir / "tastedive_recommendations")

    def __init__(self, tastedive_api_key: str):
        self.tastedive_api_key = tastedive_api_key

    def _query_tastedive(self, params: dict) -> dict | None:
        try:
            response = httpx_get_request(self.TASTEDIVE_URL, params)
        except TooManyRequestsError:
            sys.exit("Tastedive API is limited to 300 requests per hour. Exiting.")

        return response

    def fetch_recommendations_for_artists(self, artists: list[str]) -> list[str]:
        query = ",".join([f"music:{quote(artist)}" for artist in artists])
        # ToDo: generalize cache implementations
        cached_response = self.artist_cache.get(query)
        if cached_response is not None:
            return cached_response

        params = {"k": self.tastedive_api_key, "q": query, "type": "music", "slimit": 2, "limit": 20}

        response = self._query_tastedive(params)

        if response is None:
            return []

        results = response["similar"]["results"]
        recommendations = [artist["name"] for artist in results]
        self.artist_cache.set(query, recommendations)

        return recommendations
