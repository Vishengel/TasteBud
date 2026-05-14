from application.blend.blend_engine import BlendAdapter
from domain.blend.models import Platform
from infrastructure.spotify.blend_adapter import SpotifyAdapter


def make_adapter(user_id: str, platform: Platform) -> BlendAdapter:
    if platform == Platform.SPOTIFY:
        return SpotifyAdapter(user_id=user_id)
    raise ValueError(f"Unsupported platform: {platform!r}")
