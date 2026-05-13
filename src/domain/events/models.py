import datetime
from typing import Any

from pydantic import BaseModel, model_validator


class Artist(BaseModel):
    name: str
    playcount: int | None = None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Artist) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Location(BaseModel):
    city: str
    country: str | None = None


class Venue(BaseModel):
    name: str | None = None
    location: Location | None = None

    @model_validator(mode="after")
    def validate_venue(self):
        if self.name is self.location is None:
            raise ValueError("Either a venue name or a location must be specified")
        return self


class Event(BaseModel):
    artists: list[Artist]
    date: datetime.date
    venue: Venue
    url: str | None = None


class Playlist(BaseModel):
    id: str
    name: str
    external_url: str
    n_tracks: int
