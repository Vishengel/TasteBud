from typing import Protocol

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import GeoNames, Nominatim

from libs.common.data_models.location import Coordinates, Location


class GeocodingProvider(Protocol):
    def geocode_location(
        self, location: Location, supported_countries: list[str] | None = None
    ) -> Coordinates | None: ...


class GeoNamesProvider:
    RATE_LIMIT_SECONDS: float = 1 / 20

    def __init__(self, username: str, user_agent: str = "tastebud"):
        self.client = GeoNames(username=username, user_agent=user_agent)
        self.rate_limited_geocode = RateLimiter(self.client.geocode, min_delay_seconds=self.RATE_LIMIT_SECONDS)

    def geocode_location(self, location: Location, supported_countries: list[str] | None = None) -> Coordinates | None:
        result = self.rate_limited_geocode(location.to_address_string(), country=supported_countries, exactly_one=True)

        if not result:
            return None

        return Coordinates(lat=result.latitude, lon=result.longitude)


class NominatimProvider:
    RATE_LIMIT_SECONDS: float = 1.0

    def __init__(self, user_agent: str = "tastebud"):
        self.client = Nominatim(user_agent=user_agent)
        self.rate_limited_geocode = RateLimiter(self.client.geocode, min_delay_seconds=self.RATE_LIMIT_SECONDS)

    def geocode_location(self, location: Location, supported_countries: list[str] | None = None) -> Coordinates | None:
        result = self.rate_limited_geocode(
            location.to_address_string(),
            country_codes=supported_countries,
            addressdetails=True,
            language="en",
        )

        if not result:
            return None

        return Coordinates(lat=result.latitude, lon=result.longitude)
