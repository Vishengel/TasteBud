from fastapi import Request
from fastapi.responses import JSONResponse
from spotipy import SpotifyException


async def spotify_exception_handler(_request: Request, exc: SpotifyException) -> JSONResponse:
    return JSONResponse(status_code=exc.code, content={"reason": exc.reason})
