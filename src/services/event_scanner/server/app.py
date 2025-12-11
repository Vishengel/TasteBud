import logging.config

import uvicorn
from fastapi import APIRouter, FastAPI

from services.event_scanner.event_sources.event_source_factory import event_source_factory
from services.event_scanner.server.data_model import (
    EventSourceOverview,
    EventSourceType,
    FindEventsRequest,
    FindEventsResponse,
    GetEventSourceInfoResponse,
    HealthResponse,
)
from src.services.playlist_manager.server.log_config import LOG_CONFIG

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_CONFIG)
router = APIRouter()


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

    # ToDo: make async
    if find_events_request.podiuminfo_params:
        new_events = await app.state.event_source_overviews[EventSourceType.PODIUMINFO].find_events(find_events_request)
        events.extend(new_events)

    return FindEventsResponse(events=events)


@router.get("/health")
def health_check() -> HealthResponse:
    return HealthResponse()


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
