from config import CONFIG
from src.libs.tastedive.tastedive_client import TastediveClient


class TastediveEntitySource:
    def __init__(self, tastedive_api_client: TastediveClient | None = None):
        if tastedive_api_client is None:
            self.tastedive_api_client = TastediveClient(CONFIG.tastedive_api_key)
        else:
            self.tastedive_api_client = tastedive_api_client

    def get_related_entities(self, entities: list[str]) -> list[str]:
        return self.tastedive_api_client.fetch_recommendations_for_artists(entities)
