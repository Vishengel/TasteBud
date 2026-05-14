import logging

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from spotipy import SpotifyException

from application.playlist_manager.service import make_playlist_manager
from infrastructure.spotify.exception_handler import spotify_exception_handler
from interface.api.health_check import health_router
from interface.api.playlist_manager.models import (
    CombinePlaylistsRequest,
    CombinePlaylistsResponse,
    GetPlaylistsResponse,
    PlaylistRef,
)

logger = logging.getLogger(__name__)
router = APIRouter()


def make_service():
    app_service = FastAPI(title="Playlist Manager Service")
    logger.info("Starting %s...", app_service.title)
    app_service.state.playlist_manager = make_playlist_manager()
    app_service.include_router(router)
    app_service.include_router(health_router)
    app_service.add_exception_handler(SpotifyException, spotify_exception_handler)
    logger.info("Startup done.")
    return app_service


@router.get("/api/v1/playlists/{user_id}")
async def get_playlists(user_id: str) -> GetPlaylistsResponse:
    logger.info("Received request to get all playlists for user %s", user_id)
    try:
        playlists = app.state.playlist_manager.get_all_playlists_for_user_id(user_id)
    except SpotifyException as exc:
        logger.error("Error fetching playlists for user %s: %s", user_id, exc)
        raise HTTPException(
            status_code=exc.code, detail=f"Error fetching playlists for user {user_id}: {exc.reason}"
        ) from exc
    return GetPlaylistsResponse(
        user_id=user_id,
        playlists=[PlaylistRef.model_validate(pl.model_dump()) for pl in playlists],
    )


@router.post("/api/v1/playlists/{user_id}/combine")
async def combine_playlists(user_id: str, body: CombinePlaylistsRequest) -> CombinePlaylistsResponse:
    logger.info("Received combine request for user %s to combine %d playlists", user_id, len(body.playlist_ids))
    try:
        combined_playlist = app.state.playlist_manager.create_combined_playlist(user_id, body.playlist_ids)
    except SpotifyException as exc:
        logger.error("Error combining playlists for user %s: %s", user_id, exc)
        raise HTTPException(
            status_code=exc.code, detail=f"Error combining playlists for user {user_id}: {exc.reason}"
        ) from exc
    return CombinePlaylistsResponse(combined_playlist=PlaylistRef.model_validate(combined_playlist.model_dump()))


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
