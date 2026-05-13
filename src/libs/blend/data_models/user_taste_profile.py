from pydantic import BaseModel

from libs.blend.data_models.scored_track import ScoredTrack


class UserTasteProfile(BaseModel):
    user_id: str
    platform: str
    scored_tracks: list[ScoredTrack]
    top_artist_ids: list[str]
