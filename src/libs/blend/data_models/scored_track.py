from pydantic import BaseModel


class ScoredTrack(BaseModel):
    uri: str
    platform: str
    score: float
    artist_ids: list[str]
