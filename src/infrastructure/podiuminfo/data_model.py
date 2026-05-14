from enum import IntEnum

from pydantic import BaseModel, PrivateAttr, field_serializer


class PodiuminfoInputGenre(IntEnum):
    """Genres get represented by integers in the Podiuminfo query parameters."""

    METAL = 100
    ROCK = 200
    PUNK = 300
    DANCE = 400
    SOUL_RNB_HIPHOP = 500
    REGGAE = 600
    ROOTS_AMERICANA = 700
    FOLK_WERELDMUZIEK = 800
    NEDERLANDSTALIG = 900
    POP = 1000
    EXPERIMENTEEL = 1100
    COVERS_TRIBUTE = 1200
    GAMES = 1300
    OVERIG = 1400
    MUSICAL = 1500
    CABARET = 1600
    KLASSIEK = 1700

    @classmethod
    def get_genres_as_strings(cls) -> list[str]:
        return [genre.name.title().replace("_", "/") for genre in cls]


class PodiuminfoInputProvince(IntEnum):
    """Provinces get represented by integers in the Podiuminfo query parameters."""

    GRONINGEN = 8  # The only relevant province
    # ToDo: expand this with less relevant provinces


class PodiuminfoQueryParams(BaseModel):
    input_zoek: str | None = None
    Date_Day: int | None = None
    Date_Month: int | None = None
    Date_Year: int | None = None
    input_genre: PodiuminfoInputGenre | None = None
    input_podium: str | None = None
    input_provincie: str | None = None
    input_plaats: str | None = None

    _page: int = PrivateAttr(default=1)  # internal page counter

    @field_serializer("input_genre")
    def serialize_enum(self, value: IntEnum) -> int:
        return value.value

    def to_dict(self) -> dict[str, str | int]:
        params = self.model_dump(exclude_none=True)
        params["page"] = self._page
        return params
