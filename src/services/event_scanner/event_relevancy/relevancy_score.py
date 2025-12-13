from enum import Enum
from typing import ClassVar, Protocol

from libs.common.data_models.event import Event


class RelevancyScoreSource(str, Enum):
    LASTFM = "lastfm"


class RelevancyScore(Protocol):
    source: RelevancyScoreSource
    active: bool
    weight: ClassVar[float]

    def get_score(self, event: Event) -> float: ...
