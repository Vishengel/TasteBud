from abc import ABC, abstractmethod

from polars import DataFrame
from tqdm import tqdm


class BaseGraphEntityCollector(ABC):
    def create_schema(self, unique_artists: set[str]) -> tuple[DataFrame, DataFrame]:
        nodes = [{"name": artist, "type": "artist|known"} for artist in unique_artists]
        edges = []

        for artist in tqdm(unique_artists, desc="Collecting artists relationships"):
            related_artists = self._fetch_related_artists([artist])

            for rec_artist in related_artists:
                if rec_artist not in unique_artists:
                    nodes.append({"name": rec_artist, "type": "artist|unknown"})

                edges.append({"subject": artist, "object": rec_artist, "weight": 1.0, "predicate": "similar_to"})

        return DataFrame(nodes), DataFrame(edges)

    @abstractmethod
    def _fetch_related_artists(self, artists: list[str]) -> list[str]:
        pass
