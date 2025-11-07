import polars as pl

from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame
from tastebud.util.query_util import httpx_get_request


class TastediveGraphDataExtractor:
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

        for artist in unique_artists:
            recommendations = self._get_tastedive_recommendations(artist)

            for rec_artist in recommendations:
                if rec_artist not in unique_artists:
                    nodes.append({"name": rec_artist, "type": "artist|unknown"})

                edges.append({"subject": artist, "object": rec_artist, "weight": 1.0, "predicate": "similar_to"})

        self.nodes_df = pl.DataFrame(nodes)
        self.edges_df = pl.DataFrame(edges)

    def _get_tastedive_recommendations(self, artist: str) -> list[str]:
        url = "https://tastedive.com/api/similar"
        params = {
            "k": self.tastedive_api_key,
            "q": artist,
            "type": "music",
        }
        response = httpx_get_request(url, params)
        print(response)
