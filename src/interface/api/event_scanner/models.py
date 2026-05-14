import datetime

from pydantic import BaseModel

from application.event_scanner.event_sources.event_source_base import EventSourceType
from domain.events.models import Event


class EventSourceOverview(BaseModel):
    event_source_type: EventSourceType
    genres: list[str]


class GetEventSourceInfoResponse(BaseModel):
    event_source_overviews: list[EventSourceOverview]


class PodiuminfoSearchParams(BaseModel):
    start_date: datetime.date | None = datetime.date.today()
    genre: str | None = None


class FindEventsRequest(BaseModel):
    podiuminfo_params: PodiuminfoSearchParams | None = None


class FindEventsResponse(BaseModel):
    events: list[Event]
