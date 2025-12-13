from enum import Enum
from typing import ClassVar

from libs.lastfm.lastfm_client import LastFMClient, Period
from services.event_scanner.event_relevancy.relevancy_score import RelevancyScore, RelevancyScoreSource


class LastFMPeriodOption(str, Enum):
    OVERALL = "Overall"
    SEVEN_DAYS = "7 days"
    ONE_MONTH = "1 month"
    THREE_MONTHS = "3 months"
    SIX_MONTHS = "6 months"
    TWELVE_MONTHS = "12 months"


class LastFMRelevancyScore(RelevancyScore):
    PERIOD_MAPPING: ClassVar[dict[LastFMPeriodOption, Period]] = {
        LastFMPeriodOption.OVERALL: Period.OVERALL,
        LastFMPeriodOption.SEVEN_DAYS: Period.SEVENDAYS,
        LastFMPeriodOption.ONE_MONTH: Period.ONEMONTH,
        LastFMPeriodOption.THREE_MONTHS: Period.THREEMONTHS,
        LastFMPeriodOption.SIX_MONTHS: Period.SIXMONTHS,
        LastFMPeriodOption.TWELVE_MONTHS: Period.TWELVEMONTHS,
    }

    source = RelevancyScoreSource.LASTFM
    active: bool
    weight: ClassVar[float] = 1.0

    def __init__(self, lastfm_client: LastFMClient | None = None):
        self.lastfm_client = lastfm_client or LastFMClient.from_config()
        self.active = False
        self.period = LastFMPeriodOption.OVERALL

    def get_score(self) -> float:
        return 0.0

    @classmethod
    def to_api_period(cls, period: LastFMPeriodOption) -> Period:
        return cls.PERIOD_MAPPING[period]
