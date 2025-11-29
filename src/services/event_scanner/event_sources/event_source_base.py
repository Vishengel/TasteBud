from enum import Enum
from typing import Protocol

from libs.common.data_models.event import Event


class EventSourceType(str, Enum):
    PODIUMINFO = "podiuminfo"


class EventSource(Protocol):
    def get_events(self) -> list[Event]: ...
