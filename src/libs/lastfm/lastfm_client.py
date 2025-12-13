import logging
from enum import Enum

from diskcache import Cache
from pydantic_settings import BaseSettings
from pylast import (
    PERIOD_1MONTH,
    PERIOD_3MONTHS,
    PERIOD_6MONTHS,
    PERIOD_7DAYS,
    PERIOD_12MONTHS,
    PERIOD_OVERALL,
    LastFMNetwork,
    MalformedResponseError,
    NetworkError,
    WSError,
    md5,
)

from libs.common.data_models.artist import Artist
from libs.lastfm.config import CONFIG

logger = logging.getLogger(__name__)


class Period(str, Enum):
    OVERALL = PERIOD_OVERALL
    SEVENDAYS = PERIOD_7DAYS
    ONEMONTH = PERIOD_1MONTH
    THREEMONTHS = PERIOD_3MONTHS
    SIXMONTHS = PERIOD_6MONTHS
    TWELVEMONTHS = PERIOD_12MONTHS


class LastFMClient:
    artist_cache = Cache(CONFIG.cache_dir / "lastfm_similar_artists")

    def __init__(self, api_key: str, api_secret: str, username: str, password: str):
        self.network = LastFMNetwork(
            api_key=api_key, api_secret=api_secret, username=username, password_hash=md5(password)
        )

    def get_similar_artists(self, artist_name: str, limit: int | None = 10) -> list[str]:
        cache_key = f"{artist_name}{limit}" if limit is not None else artist_name
        cached_response = self.artist_cache.get(cache_key)
        if cached_response is not None:
            return cached_response

        artist = self.network.get_artist(artist_name)

        try:
            similar_artists = artist.get_similar(limit=limit)
        except (MalformedResponseError, WSError, NetworkError) as e:
            logger.error(f"Error fetching similar artists for {artist_name}: {e}")
            return []

        similar_artist_names = [similar_artist.item.name for similar_artist in similar_artists]
        self.artist_cache.set(cache_key, similar_artist_names)

        return similar_artist_names

    def get_top_artists_for_user(
        self, username: str | None, period: Period = Period.OVERALL, limit: int | None = None
    ) -> list[Artist]:
        if username is None:
            username = self.network.username
        user = self.network.get_user(username=username)

        if period == Period.OVERALL and ((limit is None) or (limit is not None and limit > 1000)):
            # A top_artists request is limited to 1000 items. If limit > 1000 or set to None (== all artists),
            # we retrieve the user library and get the artists from there. This might take a while.
            library = user.get_library()
            items = library.get_artists(limit=limit)
            return [Artist(name=item.item.name, playcount=item.playcount) for item in items]

        if limit is None:
            limit = 1000

        items = user.get_top_artists(period=period.value, limit=limit)
        return [Artist(name=top_item.item.name, playcount=top_item.weight) for top_item in items]

    @classmethod
    def from_config(cls, config: BaseSettings = CONFIG) -> "LastFMClient":
        return cls(
            config.lastfm_api_key,
            config.lastfm_shared_secret.get_secret_value(),
            config.lastfm_username,
            config.lastfm_password.get_secret_value(),
        )
