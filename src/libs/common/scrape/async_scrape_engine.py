import asyncio
import time
from asyncio import Semaphore, create_task, gather
from collections.abc import Iterable
from dataclasses import dataclass

from libs.common.http.async_httpx_client import AsyncHTTPXClient
from libs.common.http.http_client import AsyncHttpClient, HttpResponse


@dataclass
class ScrapeTask:
    url: str
    params: dict | None = None
    headers: dict | None = None
    cookies: dict | None = None


class AsyncScrapeEngine:
    def __init__(
        self,
        http_client: AsyncHttpClient | None = None,
        concurrency: int = 1,
        per_batch_crawl_delay: float | None = None,
    ):
        if http_client is None:
            self.http_client: AsyncHttpClient = AsyncHTTPXClient()
        else:
            self.http_client = http_client

        self.concurrency = concurrency
        self.semaphore = Semaphore(concurrency)
        self.per_batch_crawl_delay = per_batch_crawl_delay

    async def scrape(self, scrape_task: ScrapeTask) -> HttpResponse | None:
        async with self.semaphore:
            return await self.http_client.get(
                url=scrape_task.url, params=scrape_task.params, headers=scrape_task.headers, cookies=scrape_task.cookies
            )

    async def scrape_multiple(self, scrape_tasks: Iterable[ScrapeTask]) -> Iterable[HttpResponse | None]:
        start_time = time.time()
        tasks = [create_task(self.scrape(task)) for task in scrape_tasks]
        results = await gather(*tasks)
        elapsed = time.time() - start_time

        if self.per_batch_crawl_delay is not None:
            wait = self.per_batch_crawl_delay - elapsed
            if wait > 0:
                await asyncio.sleep(wait)

        return results
