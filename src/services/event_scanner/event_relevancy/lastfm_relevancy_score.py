import asyncio
import logging
from asyncio import CancelledError
from enum import Enum
from typing import ClassVar

from libs.common.data_models.artist import Artist
from libs.common.data_models.event import Event
from libs.lastfm.lastfm_client import LastFMClient, Period
from services.event_scanner.event_relevancy.relevancy_score import RelevancyScore, RelevancyScoreSource

logger = logging.getLogger(__name__)


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
        self.period = LastFMPeriodOption.TWELVE_MONTHS
        self.username = None
        self.top_artists: list[Artist] = []
        self.top_artists_map: dict[str, Artist] = {}
        self.artists_loaded = False
        self._load_top_artists_task: asyncio.Task | None = None

    def prepare_top_artists(self):
        if self.active:
            if not self.artists_loaded and (self._load_top_artists_task is None or self._load_top_artists_task.done()):
                # Only load the first time the LastFM scoring checkbox is clicked
                self._load_top_artists_task = asyncio.create_task(self._load_lastfm_top_artists())
        else:
            # Cancel loading if unchecked while still collecting top artists
            if self._load_top_artists_task and not self._load_top_artists_task.done():
                self._load_top_artists_task.cancel()

    def get_score(self, event: Event) -> float:
        if not self.username:
            logger.warning("No username set for the LastFM relevancy scorer. Returning score of 0.0")
            return 0.0

        if not self.artists_loaded or len(self.top_artists) == 0:
            logger.warning("LastFM top artists have not been loaded yet. Returning score of 0.0")
            return 0.0

        for artist in event.artists:
            lastfm_artist = self.top_artists_map.get(artist.name, None)
            artist.playcount = lastfm_artist.playcount if lastfm_artist else 0

        top_artist_playcount = self.top_artist_playcount
        if top_artist_playcount == 0:
            raise ValueError(f"{top_artist_playcount} should not be 0")

        return 100 * sum(artist.playcount for artist in event.artists if artist.playcount) / top_artist_playcount

    @classmethod
    def to_api_period(cls, period: LastFMPeriodOption) -> Period:
        return cls.PERIOD_MAPPING[period]

    @property
    def top_artist_playcount(self) -> int:
        if not self.artists_loaded or len(self.top_artists) == 0:
            logger.warning("LastFM top artists have not been loaded yet. Returning top artist playcount of 0")
            return 0

        playcount = self.top_artists[0].playcount
        return playcount if playcount else 0

    @property
    def loading_top_artists(self) -> bool:
        return self._load_top_artists_task is not None and not self._load_top_artists_task.done()

    async def _load_lastfm_top_artists(self):
        self.artists_loaded = False
        try:
            logger.info("Loading top artists for user %s in period %s...", self.username, self.period)
            self.top_artists = await asyncio.to_thread(
                self.lastfm_client.get_top_artists_for_user,
                username=self.username,
                period=self.to_api_period(self.period),
            )
            self.top_artists_map = {artist.name: artist for artist in self.top_artists}
            self.artists_loaded = True
            logger.info("Finished loading top artists for user %s in period %s", self.username, self.period)
        except CancelledError:
            self.artists_loaded = False
