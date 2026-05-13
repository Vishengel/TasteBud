from pydantic import BaseModel


class BlendConfig(BaseModel):
    playlist_name: str
    target_size: int = 50
    time_weights: dict[str, float] = {"long_term": 0.5, "medium_term": 0.3, "short_term": 0.2}
