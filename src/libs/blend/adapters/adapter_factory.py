from libs.blend.adapters.base_adapter import BlendAdapter
from libs.blend.adapters.spotify_adapter import SpotifyAdapter


def make_adapter(user_id: str, platform: str) -> BlendAdapter:
    if platform == "spotify":
        return SpotifyAdapter(user_id=user_id)
    raise ValueError(f"Unsupported platform: {platform!r}")
