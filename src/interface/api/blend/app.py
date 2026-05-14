import logging.config

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field
from spotipy import SpotifyException

from application.blend.adapter_factory import make_adapter
from application.blend.blend_engine import BlendEngine
from common.spotify_exception_handler import spotify_exception_handler
from domain.blend.models import BlendConfig, Platform
from domain.events.models import Playlist

logger = logging.getLogger(__name__)
router = APIRouter()


class BlendParticipant(BaseModel):
    user_id: str
    platform: Platform = Platform.SPOTIFY


class BlendRequest(BaseModel):
    initiator: BlendParticipant
    participants: list[BlendParticipant]
    config: BlendConfig


class BlendResponse(BaseModel):
    playlist: Playlist


class ErrorResponse(BaseModel):
    code: int
    reason: str


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")


def make_service():
    app_service = FastAPI(title="Blend Service")
    logger.info("Starting %s...", app_service.title)
    app_service.include_router(router)
    app_service.add_exception_handler(SpotifyException, spotify_exception_handler)
    logger.info("Startup done.")
    return app_service


@router.post("/api/v1/blend")
async def create_blend(body: BlendRequest) -> BlendResponse:
    all_participants = [body.initiator, *body.participants]
    logger.info("Received blend request for users: %s", [p.user_id for p in all_participants])

    adapters = [make_adapter(p.user_id, p.platform) for p in all_participants]
    engine = BlendEngine(adapters)

    try:
        tracks = engine.create_blend([p.user_id for p in all_participants], body.config)
    except SpotifyException as exc:
        logger.error("Error during blend: %s", exc)
        raise HTTPException(status_code=exc.code, detail=exc.reason) from exc

    try:
        playlist = adapters[0].create_playlist(
            user_id=body.initiator.user_id,
            name=body.config.playlist_name,
            track_uris=[t.uri for t in tracks],
        )
    except SpotifyException as exc:
        logger.error("Error creating playlist: %s", exc)
        raise HTTPException(status_code=exc.code, detail=exc.reason) from exc

    return BlendResponse(playlist=playlist)


@router.get("/health")
def health_check() -> HealthResponse:
    return HealthResponse()


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
