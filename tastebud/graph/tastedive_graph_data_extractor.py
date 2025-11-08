import sys

import httpx
import polars as pl
from diskcache import Cache
from tqdm import tqdm
from urllib.parse import quote

from tastebud.config import CONFIG
from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame
from tastebud.util.query_util import httpx_get_request


class TastediveGraphDataExtractor:
    TASTEDIVE_URL: str = "https://tastedive.com/api/similar"
    artist_cache = Cache(CONFIG.cache_dir / "tastedive_recommendations")
    nodes_df: pl.DataFrame
    edges_df: pl.DataFrame

    def __init__(self, tastedive_api_key: str, spotify_history: SpotifyHistoryDataFrame):
        self.tastedive_api_key = tastedive_api_key
        self.spotify_history = spotify_history
        self.extract_graph()

    def extract_graph(self) -> None:
        unique_artists = set(self.spotify_history.unique_artists.to_list())

        nodes = [{"name": artist, "type": "artist|known"} for artist in unique_artists]
        edges = []

        for artist in tqdm(unique_artists):
            recommendations = self._get_tastedive_recommendations([artist])

            for rec_artist in recommendations:
                if rec_artist not in unique_artists:
                    nodes.append({"name": rec_artist, "type": "artist|unknown"})

                edges.append({"subject": artist, "object": rec_artist, "weight": 1.0, "predicate": "similar_to"})

        self.nodes_df = pl.DataFrame(nodes)
        self.edges_df = pl.DataFrame(edges)

    def _query_tastedive(self, params: dict) -> dict | None:
        try:
            response = httpx_get_request(self.TASTEDIVE_URL, params)
        except httpx.HTTPStatusError as e:
            sys.exit("Tastedive API is limited to 300 requests per hour. Exiting.")

        return response

    def _get_tastedive_recommendations(self, artists: list[str]) -> list[str]:
        query = ",".join([f"music:{quote(artist)}" for artist in artists])
        # ToDo: generalize cache implementations
        cached_response = self.artist_cache.get(query)
        if cached_response is not None:
            return cached_response
        
        params = {
            "k": self.tastedive_api_key,
            "q": query,
            "type": "music",
            "slimit": 2,
            "limit": 20
        }

        response = self._query_tastedive(params)

        if response is None:
            return []

        results = response["similar"]["results"]
        recommendations = [artist["name"] for artist in results]
        self.artist_cache.set(query, recommendations)

        return recommendations
