from pydantic import BaseModel, Field

from libs.blend.data_models.blend_config import BlendConfig
from libs.common.data_models.playlist import Playlist


class BlendParticipant(BaseModel):
    user_id: str
    platform: str = "spotify"


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
