from typing import Any

from pydantic import BaseModel


class Artist(BaseModel):
    name: str
    playcount: int | None = None

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Artist) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
