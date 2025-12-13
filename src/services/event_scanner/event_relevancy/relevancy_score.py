from enum import Enum
from typing import Protocol


class RelevancyScoreSource(str, Enum):
    LASTFM = "lastfm"


class RelevancyScore(Protocol):
    source: RelevancyScoreSource
