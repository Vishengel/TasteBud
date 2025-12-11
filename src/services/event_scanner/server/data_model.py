import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from libs.common.data_models.event import Event
from libs.podiuminfo.scraping.event_scraper import PodiuminfoInputGenre


class EventSourceType(str, Enum):
    PODIUMINFO = "podiuminfo"


class GetEventSourcesResponse(BaseModel):
    event_sources: list[EventSourceType]


class PodiuminfoSearchParams(BaseModel):
    start_date: datetime.date | None = datetime.date.today()
    genre: PodiuminfoInputGenre | None = None

    @field_validator("genre", mode="before")
    @classmethod
    def parse_enum_name(cls, v):
        if isinstance(v, str):
            v = v.upper()
            try:
                return PodiuminfoInputGenre[v]
            except KeyError as exc:
                raise ValueError(f"Unknown genre '{v}'") from exc
        return v


class FindEventsRequest(BaseModel):
    podiuminfo_params: PodiuminfoSearchParams | None = None


class FindEventsResponse(BaseModel):
    events: list[Event]


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")
