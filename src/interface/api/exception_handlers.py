import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from spotipy import SpotifyException

logger = logging.getLogger(__name__)


async def spotify_exception_handler(_request: Request, exc: SpotifyException) -> JSONResponse:
    logger.error("Spotify error: %s", exc)
    return JSONResponse(status_code=exc.code, content={"reason": exc.reason})
