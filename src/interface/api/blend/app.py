import logging.config

import uvicorn
from fastapi import APIRouter, FastAPI
from spotipy import SpotifyException

from application.blend.adapter_factory import make_adapter
from application.blend.blend_engine import BlendEngine
from interface.api.blend.models import BlendRequest, BlendResponse
from interface.api.exception_handlers import spotify_exception_handler
from interface.api.health_check import health_router

logger = logging.getLogger(__name__)
router = APIRouter()


def make_service():
    app_service = FastAPI(title="Blend Service")
    logger.info("Starting %s...", app_service.title)
    app_service.include_router(router)
    app_service.include_router(health_router)
    app_service.add_exception_handler(SpotifyException, spotify_exception_handler)
    logger.info("Startup done.")
    return app_service


@router.post("/api/v1/blend")
async def create_blend(body: BlendRequest) -> BlendResponse:
    all_participants = [body.initiator, *body.participants]
    logger.info("Received blend request for users: %s", [p.user_id for p in all_participants])

    adapters = [make_adapter(p.user_id, p.platform) for p in all_participants]
    engine = BlendEngine(adapters)

    tracks = engine.create_blend([p.user_id for p in all_participants], body.config)
    playlist = adapters[0].create_playlist(
        user_id=body.initiator.user_id,
        name=body.config.playlist_name,
        track_uris=[t.uri for t in tracks],
    )
    return BlendResponse(playlist=playlist)


app: FastAPI = make_service()
__all__ = ["app"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
