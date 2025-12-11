from typing import Protocol

from libs.common.data_models.event import Event
from services.event_scanner.server.data_model import EventSourceType, FindEventsRequest


class EventSource(Protocol):
    event_source_type: EventSourceType

    async def find_events(self, find_events_request: FindEventsRequest) -> list[Event]: ...

    def get_genres(self) -> list[str]: ...
