from typing import Any

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from config import CONFIG


class Playlist(BaseModel):
    name: str
    href: str
    id: str
    description: str
    tracks_url: str
    n_tracks: int
    collaborative: bool
    owner_id: str
    generated_by_tastebud: bool | None = None

    @classmethod
    def from_spotify_playlist_dict(cls, spotify_playlist_dict: dict[str, Any]):
        return cls(
            name=spotify_playlist_dict["name"],
            href=spotify_playlist_dict["href"],
            id=spotify_playlist_dict["id"],
            description=spotify_playlist_dict["description"],
            tracks_url=spotify_playlist_dict["tracks"]["href"],
            n_tracks=spotify_playlist_dict["tracks"]["total"],
            collaborative=spotify_playlist_dict["collaborative"],
            owner_id=spotify_playlist_dict["owner"]["id"],
        )

    @field_validator("generated_by_tastebud", mode="after")
    @classmethod
    def set_generated_by_tastebud(cls, value: bool | None, info: ValidationInfo):
        if value is None:
            return CONFIG.tastebud_playlist_watermark in info.data["description"]
        return value
