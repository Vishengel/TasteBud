from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    name: str
    external_url: str
    n_tracks: int
