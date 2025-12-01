from libs.common.data_models.event import Event
from libs.podiuminfo.scraping.event_scraper import PodiuminfoEventScraper, PodiuminfoInputGenre, PodiuminfoQueryParams
from services.event_scanner.event_sources.event_source_base import EventSource
from services.event_scanner.server.data_model import EventSourceType, FindEventsRequest


class PodiuminfoEventSource(EventSource):
    event_source_type = EventSourceType.PODIUMINFO

    def __init__(self, event_scraper: PodiuminfoEventScraper | None = None):
        self.event_scraper = event_scraper or PodiuminfoEventScraper()

    async def find_events(self, find_events_request: FindEventsRequest) -> list[Event]:
        podiuminfo_params = find_events_request.podiuminfo_params
        start_date = podiuminfo_params.start_date
        # ToDo: TEMP - for now only METAL is supported as input genre
        genre = PodiuminfoInputGenre.METAL if podiuminfo_params.genre else None
        query_params = PodiuminfoQueryParams(
            Date_Year=start_date.year, Date_Month=start_date.month, Date_Day=start_date.day, input_genre=genre
        )
        events = await self.event_scraper.scrape_events(query_params)
        return events
