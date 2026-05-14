import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from application.event_scanner.event_sources.event_source_base import EventSourceType
from application.event_scanner.event_sources.event_source_factory import event_source_factory
from interface.api.event_scanner.models import (
    EventSourceOverview,
    FindEventsRequest,
    FindEventsResponse,
    GetEventSourceInfoResponse,
)
from interface.api.health_check import health_router

logger = logging.getLogger(__name__)
router = APIRouter()


def make_service():
    app_service = FastAPI(title="Event Scanner Service")
    logger.info("Starting %s...", app_service.title)
    app_service.state.event_source_overviews = event_source_factory({EventSourceType.PODIUMINFO})
    app_service.include_router(router)
    app_service.include_router(health_router)
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


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
