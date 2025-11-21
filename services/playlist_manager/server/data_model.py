from pydantic import BaseModel

from libs.spotify.data_model.playlist import Playlist


class GetPlaylistsResponse(BaseModel):
    user_id: str
    playlists: list[Playlist]
