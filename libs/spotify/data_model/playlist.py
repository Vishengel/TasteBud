from typing import Any

from pydantic import BaseModel


class Playlist(BaseModel):
    name: str
    href: str
    id: str
    tracks_url: str
    n_tracks: int
    collaborative: bool
    owner_id: str

    @classmethod
    def from_spotify_playlist_dict(cls, spotify_playlist_dict: dict[str, Any]):
        return cls(
            name=spotify_playlist_dict["name"],
            href=spotify_playlist_dict["href"],
            id=spotify_playlist_dict["id"],
            tracks_url=spotify_playlist_dict["tracks"]["href"],
            n_tracks=spotify_playlist_dict["tracks"]["total"],
            collaborative=spotify_playlist_dict["collaborative"],
            owner_id=spotify_playlist_dict["owner"]["id"],
        )
