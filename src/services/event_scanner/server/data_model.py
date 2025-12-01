import datetime
from enum import Enum

from pydantic import BaseModel, Field

from libs.common.data_models.event import Event


class EventSourceType(str, Enum):
    PODIUMINFO = "podiuminfo"


class GetEventSourcesResponse(BaseModel):
    event_sources: list[EventSourceType]


class FindEventsRequest(BaseModel):
    sources: list[EventSourceType]
    start_date: datetime.date | None = datetime.date.today()


class FindEventsResponse(BaseModel):
    events: list[Event]


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")
