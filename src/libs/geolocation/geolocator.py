import logging
from functools import lru_cache

from geopy.distance import distance

from libs.common.data_models.location import Coordinates, Location
from libs.geolocation.config import CONFIG
from libs.geolocation.geolocation_providers import GeocodingProvider, GeoNamesProvider

logger = logging.getLogger(__name__)


class Geolocator:
    def __init__(
        self, geolocation_provider: GeocodingProvider | None = None, supported_countries: list[str] | None = None
    ):
        self.geolocator = geolocation_provider or GeoNamesProvider(username=CONFIG.geonames_username)
        self.supported_countries = supported_countries

    @staticmethod
    def get_distance(coords1: Coordinates, coords2: Coordinates) -> float:
        return distance((coords1.lat, coords1.lon), (coords2.lat, coords2.lon)).kilometers

    def _get_coordinates(self, location: Location) -> Coordinates:
        city = location.city
        country = location.country

        coords = _get_cached_coordinates(city, country)

        if coords is None:
            raise ValueError(f"Unable to retrieve coordinates for {location}")

        location.coordinates = coords
        return coords

    def get_distance_between_locations(
        self,
        loc1: Location,
        loc2: Location,
    ) -> float:
        coords1 = self._get_coordinates(loc1)
        coords2 = self._get_coordinates(loc2)

        return self.get_distance(coords1, coords2)


# Moved outside of Geolocator class to prevent functools cache-related memory leaks
@lru_cache(maxsize=512)
def _get_cached_coordinates(
    geolocator: Geolocator,
    city: str,
    country: str,
) -> Coordinates | None:
    location = Location(city=city, country=country)
    return geolocator.geolocator.geocode_location(
        location,
        geolocator.supported_countries,
    )
