from pydantic import BaseModel


class Playlist(BaseModel):
    id: str
    name: str
    external_url: str
    n_tracks: int
    owner_id: str
    generated_by_tastebud: bool = False

    def __hash__(self):
        return hash(self.id)


class Track(BaseModel):
    uri: str
