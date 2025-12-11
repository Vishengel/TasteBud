import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, field_validator

from libs.common.data_models.event import Event
from libs.podiuminfo.data_model import PodiuminfoInputGenre


class EventSourceType(str, Enum):
    PODIUMINFO = "podiuminfo"


class EventSourceOverview(BaseModel):
    event_source_type: EventSourceType
    genres: list[str]


class GetEventSourceInfoResponse(BaseModel):
    event_source_overviews: list[EventSourceOverview]


class PodiuminfoSearchParams(BaseModel):
    start_date: datetime.date | None = datetime.date.today()
    genre: PodiuminfoInputGenre | None = None

    @field_validator("genre", mode="before")
    @classmethod
    def parse_enum_name(cls, value):
        if isinstance(value, str):
            value = value.upper()
            try:
                return PodiuminfoInputGenre[value]
            except KeyError as exc:
                raise ValidationError(f"Unknown genre '{value}'") from exc
        return value


class FindEventsRequest(BaseModel):
    podiuminfo_params: PodiuminfoSearchParams | None = None


class FindEventsResponse(BaseModel):
    events: list[Event]


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")
