from base_config import BASE_CONFIG
from src.libs.lastfm.lastfm_client import LastFMClient


class LastFMEntitySource:
    def __init__(self, lastfm_api_client: LastFMClient | None = None):
        if lastfm_api_client is None:
            self.lastfm_api_client = LastFMClient(
                BASE_CONFIG.lastfm_api_key,
                BASE_CONFIG.lastfm_shared_secret,
                BASE_CONFIG.lastfm_username,
                BASE_CONFIG.lastfm_password,
            )
        else:
            self.lastfm_api_client = lastfm_api_client

    def get_related_entities(self, entities: list[str]) -> list[str]:
        similar_artists = [
            artist for entity in entities for artist in self.lastfm_api_client.get_similar_artists(entity)
        ]
        return similar_artists
