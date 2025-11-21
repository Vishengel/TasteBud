from pydantic import BaseModel

from libs.spotify.data_model.playlist import Playlist


class GetPlaylistsResponse(BaseModel):
    user_id: str
    playlists: list[Playlist]


class CombinePlaylistsRequest(BaseModel):
    playlists: list[Playlist]


class CombinePlaylistsResponse(BaseModel):
    combined_playlist: Playlist
