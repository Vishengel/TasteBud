import datetime

from pydantic import BaseModel, model_validator

from libs.common.data_models.artist import Artist
from libs.common.data_models.location import Location


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
