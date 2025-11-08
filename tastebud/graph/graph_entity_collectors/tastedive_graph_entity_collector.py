import sys
from urllib.parse import quote

import httpx
import polars as pl
from diskcache import Cache

from tastebud.config import CONFIG
from tastebud.graph.graph_entity_collectors.base_graph_entity_collector import BaseGraphEntityCollector
from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame
from tastebud.util.query_util import httpx_get_request


class TastediveGraphEntityCollector(BaseGraphEntityCollector):
    TASTEDIVE_URL: str = "https://tastedive.com/api/similar"
    artist_cache = Cache(CONFIG.cache_dir / "tastedive_recommendations")
    nodes_df: pl.DataFrame
    edges_df: pl.DataFrame

    def __init__(self, tastedive_api_key: str, spotify_history: SpotifyHistoryDataFrame):
        super().__init__()
        self.tastedive_api_key = tastedive_api_key
        self.spotify_history = spotify_history

    def _query_tastedive(self, params: dict) -> dict | None:
        try:
            response = httpx_get_request(self.TASTEDIVE_URL, params)
        except httpx.HTTPStatusError:
            sys.exit("Tastedive API is limited to 300 requests per hour. Exiting.")

        return response

    def _fetch_related_artists(self, artists: list[str]) -> list[str]:
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
