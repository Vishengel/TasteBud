import asyncio
import logging

from httpx import AsyncClient, HTTPStatusError, RequestError

from libs.common.http.exceptions import TOO_MANY_REQUESTS_ERROR_CODE, TooManyRequestsError
from src.libs.common.http.http_client import AsyncHttpClient, HttpResponse

logger = logging.getLogger(__name__)


class AsyncHTTPXClient(AsyncHttpClient):
    def __init__(self, concurrency: int = 5, timeout: int = 10):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.client = AsyncClient(timeout=timeout)

    async def get(
        self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None
    ) -> HttpResponse | None:
        async with self.semaphore:
            try:
                response = await self.client.get(url=url, params=params, headers=headers, cookies=cookies)
                response.raise_for_status()
            except RequestError as e:
                logger.error(f"An error occurred while making the request: {e}")
                return None
            except HTTPStatusError as e:
                if e.response.status_code == TOO_MANY_REQUESTS_ERROR_CODE:
                    raise TooManyRequestsError() from e
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                return None

            return response

    async def close(self):
        await self.client.aclose()
