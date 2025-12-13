import datetime

from pydantic import BaseModel, model_validator

from libs.common.data_models.artist import Artist


class Coordinates(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    country: str | None = None
    country_code: str | None = None
    state: str | None = None
    city: str | None = None
    street: str | None = None
    street_number: str | None = None
    postal_code: str | None = None
    coordinates: Coordinates | None = None


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
