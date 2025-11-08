from diskcache import Cache

from tastebud.config import CONFIG
from tastebud.graph.graph_dataclass import GraphSchema
from tastebud.graph.graph_entity_collectors.base_graph_entity_collector import BaseGraphEntityCollector
from tastebud.spotify.spotify_history_dataframe import SpotifyHistoryDataFrame


class LastFMGraphEntityCollector(BaseGraphEntityCollector):
    LASTFM_URL: str = "https://tastedive.com/api/similar"
    artist_cache = Cache(CONFIG.cache_dir / "lastfm_similar_artists")
    graph: GraphSchema

    def __init__(self, lastfm_api_key: str, spotify_history: SpotifyHistoryDataFrame, cache_dir: str):
        super().__init__(cache_dir)
        self.lastfm_api_key = lastfm_api_key
        self.spotify_history = spotify_history

    def _query_lastfm(self, params: dict) -> dict | None: ...

    def _fetch_related_artists(self, artists: list[str]) -> list[str]: ...
