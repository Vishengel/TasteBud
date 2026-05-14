from pydantic import BaseModel


class PlaylistRef(BaseModel):
    id: str
    name: str
    external_url: str
    n_tracks: int
    owner_id: str
    generated_by_tastebud: bool = False


class GetPlaylistsResponse(BaseModel):
    user_id: str
    playlists: list[PlaylistRef]


class CombinePlaylistsRequest(BaseModel):
    playlist_ids: list[str]


class CombinePlaylistsResponse(BaseModel):
    combined_playlist: PlaylistRef


class ErrorResponse(BaseModel):
    code: int
    reason: str
