from typing import Any

from pydantic import BaseModel, model_validator

from libs.spotify.config import CONFIG


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

    @model_validator(mode="after")
    def set_generated_by_tastebud(self):
        if self.generated_by_tastebud is None:
            self.generated_by_tastebud = CONFIG.tastebud_playlist_watermark in self.description
        return self

    def __hash__(self):
        return hash(self.id)
