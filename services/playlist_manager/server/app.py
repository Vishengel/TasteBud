import logging
import logging.config

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from spotipy import SpotifyException

from libs.spotify.playlist_management.playlist_manager import PlaylistManager
from libs.spotify.spotify_client.spotify_client import SpotifyClient
from services.playlist_manager.server.data_model import (
    CombinePlaylistsRequest,
    CombinePlaylistsResponse,
    GetPlaylistsResponse,
    HealthResponse,
)
from services.playlist_manager.server.exception_handlers import spotify_exception_handler
from services.playlist_manager.server.log_config import LOG_CONFIG

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOG_CONFIG)
router = APIRouter()


def make_service():
    app_service = FastAPI(title="Playlist Manager Service")
    logger.info("Starting %s...", app_service.title)

    spotify_client = SpotifyClient()
    app_service.state.playlist_manager = PlaylistManager(spotify_client)
    app_service.include_router(router)

    app_service.add_exception_handler(SpotifyException, spotify_exception_handler)

    logger.info("Startup done.")
    return app_service


@router.get("/api/v1/playlists/{user_id}")
async def get_playlists(user_id: str) -> GetPlaylistsResponse:
    logger.info("Received request to get all playlists for user %s", user_id)
    try:
        playlists = app.state.playlist_manager.get_all_playlists_for_user_id(user_id)
    except SpotifyException as exc:
        logger.error(f"Error fetching playlists for user {user_id}: {exc}")
        raise HTTPException(
            status_code=exc.code, detail=f"Error fetching playlists for user {user_id}: {exc.reason}"
        ) from exc
    return GetPlaylistsResponse(user_id=user_id, playlists=playlists)


@router.post("/api/v1/playlists/{user_id}/combine")
async def combine_playlists(user_id: str, body: CombinePlaylistsRequest) -> CombinePlaylistsResponse:
    logger.info("Received combine request for user %s to combine %d playlists", user_id, len(body.playlists))
    try:
        combined_playlist = app.state.playlist_manager.create_combined_playlist(
            user_id, [playlist.id for playlist in body.playlists]
        )
    except SpotifyException as exc:
        logger.error(f"Error combining playlists for user {user_id}: {exc}")
        raise HTTPException(
            status_code=exc.code, detail=f"Error fetching playlists for user {user_id}: {exc.reason}"
        ) from exc
    return CombinePlaylistsResponse(combined_playlist=combined_playlist)


@router.get("/health")
def health_check() -> HealthResponse:
    return HealthResponse()


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
