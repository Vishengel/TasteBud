from libs.blend.adapters.base_adapter import BlendAdapter
from libs.blend.adapters.spotify_adapter import SpotifyAdapter
from libs.blend.data_models.enums import Platform


def make_adapter(user_id: str, platform: Platform) -> BlendAdapter:
    if platform == Platform.SPOTIFY:
        return SpotifyAdapter(user_id=user_id)
    raise ValueError(f"Unsupported platform: {platform!r}")
