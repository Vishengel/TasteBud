import datetime
from typing import Any

from pydantic import BaseModel, field_validator, model_validator


class Artist(BaseModel):
    name: str
    playcount: int | None = None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Artist) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class Coordinates(BaseModel):
    lat: float
    lon: float

    model_config = {"frozen": True}


class Location(BaseModel):
    country: str | None = None
    country_code: str | None = None
    state: str | None = None
    city: str | None = None
    street: str | None = None
    street_number: str | None = None
    postal_code: str | None = None
    coordinates: Coordinates | None = None

    @field_validator("*", mode="before")
    @classmethod
    def _strip_strings(cls, v):
        if isinstance(v, str):
            v = v.strip()
            return v or None
        return v

    def to_address_string(self) -> str:
        street_part = " ".join(part for part in [self.street, self.street_number] if part) or None
        city_part = " ".join(part for part in [self.postal_code, self.city] if part) or None
        parts = [street_part, self.state, city_part, self.country]
        return ", ".join(part for part in parts if part)

    def __hash__(self):
        return hash(
            (
                self.country,
                self.country_code,
                self.state,
                self.city,
                self.street,
                self.street_number,
                self.postal_code,
                self.coordinates,
            )
        )


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
