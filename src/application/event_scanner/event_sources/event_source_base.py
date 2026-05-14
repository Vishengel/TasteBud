import datetime
from enum import Enum
from typing import Protocol

from domain.events.models import Event


class EventSourceType(str, Enum):
    PODIUMINFO = "podiuminfo"


class EventSource(Protocol):
    event_source_type: EventSourceType

    async def find_events(
        self,
        start_date: datetime.date | None = None,
        genre: str | None = None,
    ) -> list[Event]: ...

    def get_genres(self) -> list[str]: ...
