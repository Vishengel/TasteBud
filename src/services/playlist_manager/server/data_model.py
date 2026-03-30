from pydantic import BaseModel, Field

from libs.spotify.data_model.playlist import Playlist


class GetPlaylistsResponse(BaseModel):
    user_id: str
    playlists: list[Playlist]


class CombinePlaylistsRequest(BaseModel):
    playlists: list[Playlist]


class CombinePlaylistsResponse(BaseModel):
    combined_playlist: Playlist


class ErrorResponse(BaseModel):
    code: int
    reason: str


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")
