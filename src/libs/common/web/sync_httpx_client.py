import logging

import httpx
from httpx import Client, HTTPStatusError, RequestError

from src.libs.common.exceptions.http_exceptions import TOO_MANY_REQUESTS_ERROR_CODE, TooManyRequestsError
from src.libs.common.web.http_client import HttpResponse, SyncHttpClient

logger = logging.getLogger(__name__)


class SyncHTTPXClient(SyncHttpClient):
    def __init__(self, timeout: int = 10):
        self.client = Client(timeout=timeout)

    def get(self, url: str) -> HttpResponse | None:
        try:
            response = self.client.get(url)
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

    def close(self):
        self.client.close()


def httpx_get_request(url: str, params: dict | None = None) -> HttpResponse | None:
    try:
        response = httpx.get(url, params=params)
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


def get_html_document(url: str) -> str:
    response = httpx_get_request(url)
    return response.text
