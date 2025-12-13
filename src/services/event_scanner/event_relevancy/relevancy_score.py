from enum import Enum
from typing import ClassVar, Protocol


class RelevancyScoreSource(str, Enum):
    LASTFM = "lastfm"


class RelevancyScore(Protocol):
    source: RelevancyScoreSource
    active: bool
    weight: ClassVar[float]

    def get_score(self) -> float: ...
