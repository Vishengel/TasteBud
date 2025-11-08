from tastebud.config import CONFIG
from tastebud.lastfm.lastfm_client import LastFMClient


class LastFMEntitySource:
    def __init__(self, lastfm_api_client: LastFMClient | None = None):
        if lastfm_api_client is None:
            self.lastfm_api_client = LastFMClient(
                CONFIG.lastfm_api_key, CONFIG.lastfm_shared_secret, CONFIG.lastfm_username, CONFIG.lastfm_password
            )
        else:
            self.lastfm_api_client = lastfm_api_client

    def get_related_entities(self, entities: list[str]) -> list[str]:
        similar_artists = []
        similar_artists.extend(self.lastfm_api_client.get_similar_artists(artist) for artist in entities)
        return similar_artists
