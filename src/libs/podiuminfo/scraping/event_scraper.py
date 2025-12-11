import logging
from collections.abc import Iterable
from copy import copy
from typing import ClassVar

from libs.common.data_models.event import Event
from libs.common.http.http_client import HttpResponse
from libs.common.scrape.async_scrape_engine import AsyncScrapeEngine, ScrapeTask
from libs.podiuminfo.data_model import PodiuminfoQueryParams
from libs.podiuminfo.scraping.event_html_parser import extract_events_from_html

logger = logging.getLogger(__name__)


class PodiuminfoEventScraper:
    CONCERTAGENDA_URL: ClassVar[str] = "https://www.podiuminfo.nl/concertagenda/"
    # We safely stay below Podiuminfo's rate limit by making 1 request per 0.5 seconds
    SAFE_CRAWL_DELAY: ClassVar[float] = 1.0
    # To Do: we want to move the full rate limit functionality to the async scrape engine
    SAFE_N_CONCURRENT_REQUESTS: ClassVar[int] = 1

    def __init__(self, scrape_engine: AsyncScrapeEngine | None = None):
        self.scrape_engine = scrape_engine or AsyncScrapeEngine(
            per_batch_crawl_delay=self.SAFE_CRAWL_DELAY, concurrency=self.SAFE_N_CONCURRENT_REQUESTS
        )
        self._enforce_safe_crawl_delay()
        self.concurrent_requests = self.SAFE_N_CONCURRENT_REQUESTS

    async def scrape_events(self, query_params: PodiuminfoQueryParams) -> list[Event]:
        events = []
        end_of_results = False
        cursor = query_params._page

        while not end_of_results:
            concurrent_query_params: list[PodiuminfoQueryParams] = []
            for idx in range(cursor, cursor + self.concurrent_requests):
                concurrent_query_param = query_params.model_copy(update={"_page": idx})
                concurrent_query_params.append(concurrent_query_param)
                cursor += self.concurrent_requests

            scrape_tasks = [
                ScrapeTask(url=self.CONCERTAGENDA_URL, params=params.to_dict()) for params in concurrent_query_params
            ]
            html_results = await self.scrape_engine.scrape_multiple(scrape_tasks)
            # ToDo: parallelize this as well
            new_events = self._extract_all_events(html_results)

            if len(new_events) == 0:
                logger.info("End of results reached")
                end_of_results = True

            events.extend([event for event in new_events if event is not None])
            logger.info("Collected %s events in total", len(events))

        return events

    def _enforce_safe_crawl_delay(self) -> None:
        if (
            self.scrape_engine.per_batch_crawl_delay is None
            or self.scrape_engine.per_batch_crawl_delay < self.SAFE_CRAWL_DELAY
        ):
            logger.warning(
                "The provided scrape engine has no per_batch_crawl_delay set or "
                "has a per_batch_crawl_delay higher than %.1f seconds. "
                "Creating new engine with safe crawl delay",
                self.SAFE_CRAWL_DELAY,
            )
            new_engine = copy(self.scrape_engine)
            new_engine.per_batch_crawl_delay = self.SAFE_CRAWL_DELAY
            self.scrape_engine = new_engine

    def _extract_all_events(self, html_results: Iterable[HttpResponse | None]) -> list[Event | None]:
        new_events = []
        nested_events = [extract_events_from_html(result.text) for result in html_results]
        for event_list in nested_events:
            if len(event_list) > 0:
                new_events.extend(event_list)
        return new_events
