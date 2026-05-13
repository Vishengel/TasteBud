from spotipy import SpotifyException

from services.blend.server.data_model import ErrorResponse


async def spotify_exception_handler(_, exc: SpotifyException):
    return ErrorResponse(
        code=exc.code,
        reason=exc.reason,
    )
