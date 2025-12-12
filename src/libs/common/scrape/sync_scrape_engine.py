from dataclasses import dataclass

from libs.common.http.http_client import HttpResponse, SyncHttpClient
from libs.common.http.sync_httpx_client import SyncHTTPXClient


@dataclass
class ScrapeTask:
    url: str
    params: dict | None = None
    headers: dict | None = None
    cookies: dict | None = None


class SyncScrapeEngine:
    def __init__(
        self,
        http_client: SyncHttpClient | None = None,
    ):
        if http_client is None:
            self.http_client: SyncHttpClient = SyncHTTPXClient()
        else:
            self.http_client = http_client

    def scrape(self, scrape_task: ScrapeTask) -> HttpResponse | None:
        return self.http_client.get(
            url=scrape_task.url, params=scrape_task.params, headers=scrape_task.headers, cookies=scrape_task.cookies
        )
