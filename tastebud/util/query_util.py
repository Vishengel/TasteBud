import logging
import sys

import httpx

logger = logging.getLogger(__name__)

TOO_MANY_REQUESTS_ERROR_CODE = 429

class TooManyRequestsError(Exception):
    pass

def httpx_get_request(url: str, params: dict) -> dict | None:
    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    except httpx.RequestError as e:
        logger.error(f"An error occurred while making the request: {e}")
        return None
    except httpx.HTTPStatusError as e:
        if e.response.status_code == TOO_MANY_REQUESTS_ERROR_CODE:
            raise TooManyRequestsError()
        logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None

    return data
