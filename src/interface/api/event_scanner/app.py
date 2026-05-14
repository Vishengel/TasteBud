import datetime
import logging

import uvicorn
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field

from application.event_scanner.event_sources.event_source_base import EventSourceType
from application.event_scanner.event_sources.event_source_factory import event_source_factory
from domain.events.models import Event

logger = logging.getLogger(__name__)
router = APIRouter()


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


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")


def make_service():
    app_service = FastAPI(title="Event Scanner Service")
    logger.info("Starting %s...", app_service.title)
    app_service.state.event_source_overviews = event_source_factory({EventSourceType.PODIUMINFO})
    app_service.include_router(router)
    logger.info("Startup done.")
    return app_service


@router.get("/api/v1/events/find")
async def get_event_source_info() -> GetEventSourceInfoResponse:
    event_source_overviews = []
    for event_source_type in list(EventSourceType):
        event_source = app.state.event_source_overviews[event_source_type]
        event_source_overviews.append(
            EventSourceOverview(event_source_type=event_source.event_source_type, genres=event_source.get_genres())
        )
    return GetEventSourceInfoResponse(event_source_overviews=event_source_overviews)


@router.post("/api/v1/events/find")
async def find_events(find_events_request: FindEventsRequest) -> FindEventsResponse:
    logger.info("Received request to get all events with parameters: %s", find_events_request)
    events = []

    if find_events_request.podiuminfo_params:
        params = find_events_request.podiuminfo_params
        new_events = await app.state.event_source_overviews[EventSourceType.PODIUMINFO].find_events(
            start_date=params.start_date,
            genre=params.genre,
        )
        events.extend(new_events)

    return FindEventsResponse(events=events)


@router.get("/health")
def health_check() -> HealthResponse:
    return HealthResponse()


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
