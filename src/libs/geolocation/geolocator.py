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
        self._cached_geocoder_method = make_cached_geocoder(self.geolocator)
        self.supported_countries = tuple(supported_countries) if supported_countries else None

    @staticmethod
    def get_distance(coords1: Coordinates, coords2: Coordinates) -> float:
        return distance((coords1.lat, coords1.lon), (coords2.lat, coords2.lon)).kilometers

    def _get_coordinates(self, location: Location) -> Coordinates:
        city = location.city
        country = location.country

        coords = self._cached_geocoder_method(city, country, self.supported_countries)

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
def make_cached_geocoder(provider: GeocodingProvider):
    @lru_cache(maxsize=512)
    def _cached(
        city: str | None,
        country: str | None,
        supported_countries: tuple[str, ...] | None,
    ) -> Coordinates | None:
        location = Location(city=city, country=country)

        return provider.geocode_location(
            location,
            list(supported_countries) if supported_countries else None,
        )

    return _cached
