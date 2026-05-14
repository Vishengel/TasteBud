from enum import Enum
from typing import ClassVar, Protocol

from domain.events.models import Event


class RelevancyScoreSource(str, Enum):
    LASTFM = "lastfm"
    DISTANCE = "distance"


class RelevancyScore(Protocol):
    source: RelevancyScoreSource
    active: bool
    weight: ClassVar[float]

    def get_score(self, event: Event) -> float: ...
