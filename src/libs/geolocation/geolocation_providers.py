from typing import Protocol

from geopy.geocoders import GeoNames, Nominatim

from libs.common.data_models.location import Coordinates, Location


class GeocodingProvider(Protocol):
    def geocode_location(
        self, location: Location, supported_countries: list[str] | None = None
    ) -> Coordinates | None: ...


class GeoNamesProvider:
    def __init__(self, username: str, user_agent: str = "tastebud"):
        self.client = GeoNames(username=username, user_agent=user_agent)

    def geocode_location(self, location: Location, supported_countries: list[str] | None = None) -> Coordinates | None:
        result = self.client.geocode(location.to_address_string(), country=supported_countries, exactly_one=True)

        if not result:
            return None

        return Coordinates(lat=result.latitude, lon=result.longitude)


class NominatimProvider:
    def __init__(self, user_agent: str = "tastebud"):
        self.client = Nominatim(user_agent=user_agent)

    def geocode_location(self, location: Location, supported_countries: list[str] | None = None) -> Coordinates | None:
        result = self.client.geocode(
            location.to_address_string(),
            country_codes=supported_countries,
            addressdetails=True,
            language="en",
        )

        if not result:
            return None

        return Coordinates(lat=result.latitude, lon=result.longitude)
