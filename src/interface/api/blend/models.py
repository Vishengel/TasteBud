from pydantic import BaseModel

from domain.blend.models import BlendConfig, Platform
from domain.events.models import Playlist


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
