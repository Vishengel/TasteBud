from enum import Enum

from pydantic import BaseModel


class Platform(str, Enum):
    SPOTIFY = "spotify"


class ScoredTrack(BaseModel):
    uri: str
    platform: str
    score: float
    artist_ids: list[str]


class BlendConfig(BaseModel):
    playlist_name: str
    target_size: int = 50
    time_weights: dict[str, float] = {"long": 0.5, "medium": 0.3, "short": 0.2}


class UserTasteProfile(BaseModel):
    user_id: str
    platform: str
    scored_tracks: list[ScoredTrack]
    top_artist_ids: list[str]

    def merge(self, other: "UserTasteProfile") -> "UserTasteProfile":
        scores: dict[str, float] = {}
        meta: dict[str, ScoredTrack] = {}

        for track in [*self.scored_tracks, *other.scored_tracks]:
            scores[track.uri] = scores.get(track.uri, 0.0) + track.score
            if track.uri not in meta:
                meta[track.uri] = track

        merged_tracks = [meta[uri].model_copy(update={"score": score}) for uri, score in scores.items()]
        merged_artist_ids = list({*self.top_artist_ids, *other.top_artist_ids})

        return UserTasteProfile(
            user_id=f"{self.user_id}+{other.user_id}",
            platform=self.platform,
            scored_tracks=merged_tracks,
            top_artist_ids=merged_artist_ids,
        )
