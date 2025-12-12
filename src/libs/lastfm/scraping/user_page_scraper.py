from typing import ClassVar

from libs.common.scrape.sync_scrape_engine import ScrapeTask, SyncScrapeEngine
from libs.lastfm.scraping.user_page_html_parser import extract_artist_count_from_user_page


class UserPageScraper:
    LASTFM_USER_BASE_URL: ClassVar[str] = "https://www.last.fm/user/"

    def __init__(self, scrape_engine: SyncScrapeEngine | None = None):
        self.scrape_engine = scrape_engine or SyncScrapeEngine()

    def get_artist_count(self, username: str) -> int:
        url = self.LASTFM_USER_BASE_URL + username
        html_result = self.scrape_engine.scrape(ScrapeTask(url=url))
        return extract_artist_count_from_user_page(html_result.text, username)
