from abc import ABC, abstractmethod

from libs.blend.data_models.scored_track import ScoredTrack
from libs.blend.data_models.user_taste_profile import UserTasteProfile
from libs.common.data_models.playlist import Playlist


class BlendAdapter(ABC):
    @abstractmethod
    def get_taste_profile(self, user_id: str, time_weights: dict[str, float]) -> UserTasteProfile: ...

    @abstractmethod
    def get_artist_top_tracks(self, artist_id: str) -> list[ScoredTrack]: ...

    @abstractmethod
    def create_playlist(self, user_id: str, name: str, track_uris: list[str]) -> Playlist: ...
