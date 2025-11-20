from typing import Any

from pydantic import BaseModel


class Track(BaseModel):
    uri: str

    @classmethod
    def from_spotify_track_dict(cls, spotify_track_dict: dict[str, Any]):
        return cls(
            uri=spotify_track_dict["track"]["uri"],
        )
