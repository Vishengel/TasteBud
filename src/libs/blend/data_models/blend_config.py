from pydantic import BaseModel


class BlendConfig(BaseModel):
    playlist_name: str
    target_size: int = 50
    time_weights: dict[str, float] = {"long": 0.5, "medium": 0.3, "short": 0.2}
