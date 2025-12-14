from pydantic import BaseModel, field_validator


class Coordinates(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    country: str | None = None
    country_code: str | None = None
    state: str | None = None
    city: str | None = None
    street: str | None = None
    street_number: str | None = None
    postal_code: str | None = None
    coordinates: Coordinates | None = None

    @field_validator("*", mode="before")
    @classmethod
    def _strip_strings(cls, v):
        if isinstance(v, str):
            v = v.strip()
            return v or None  # Returns "" as None
        return v

    def to_address_string(self) -> str:
        street_part = " ".join(part for part in [self.street, self.street_number] if part) or None

        city_part = " ".join(part for part in [self.postal_code, self.city] if part) or None

        parts = [street_part, self.state, city_part, self.country]
        return ", ".join(part for part in parts if part)
