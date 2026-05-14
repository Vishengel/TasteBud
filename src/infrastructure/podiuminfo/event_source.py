import datetime

from application.event_scanner.event_sources.event_source_base import EventSource, EventSourceType
from domain.events.models import Event
from infrastructure.podiuminfo.data_model import PodiuminfoInputGenre, PodiuminfoQueryParams
from infrastructure.podiuminfo.scraping.event_scraper import PodiuminfoEventScraper


class PodiuminfoEventSource(EventSource):
    event_source_type = EventSourceType.PODIUMINFO

    def __init__(self, event_scraper: PodiuminfoEventScraper | None = None):
        self.event_scraper = event_scraper or PodiuminfoEventScraper()

    async def find_events(
        self,
        start_date: datetime.date | None = None,
        genre: str | None = None,
    ) -> list[Event]:
        start_date = start_date or datetime.date.today()
        genre_enum = PodiuminfoInputGenre[genre.upper()] if genre else None
        query_params = PodiuminfoQueryParams(
            Date_Year=start_date.year,
            Date_Month=start_date.month,
            Date_Day=start_date.day,
            input_genre=genre_enum,
        )
        return await self.event_scraper.scrape_events(query_params)

    def get_genres(self) -> list[str]:
        return PodiuminfoInputGenre.get_genres_as_strings()
