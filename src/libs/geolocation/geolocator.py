import logging

from geopy.distance import distance
from geopy.geocoders import Nominatim
from geopy.geocoders.base import Geocoder

from libs.common.data_models.location import Coordinates, Location

logger = logging.getLogger(__name__)


class Geolocator:
    def __init__(self, geolocation_provider: Geocoder | None = None):
        self.geolocator = geolocation_provider or Nominatim(user_agent="tastebud")

    def find_coordinates_for_location(
        self, location: Location, include_address_details: bool = True, language: str = "en"
    ) -> Location:
        geopy_location = self.geolocator.geocode(
            location.to_address_string(), addressdetails=include_address_details, language=language
        )
        location.coordinates = Coordinates(lat=geopy_location.latitude, lon=geopy_location.longitude)
        return location

    @staticmethod
    def get_distance(coords1: Coordinates, coords2: Coordinates) -> float:
        return distance(coords1, coords2).kilometers

    def get_distance_between_locations(self, loc1: Location, loc2: Location) -> float:
        location1 = self.find_coordinates_for_location(loc1)
        location2 = self.find_coordinates_for_location(loc2)

        if location1.coordinates is None:
            raise ValueError(f"Unable to retrieve coordinates for {location1}")

        if location2.coordinates is None:
            raise ValueError(f"Unable to retrieve coordinates for {location2}")

        return self.get_distance(location1.coordinates, location2.coordinates)


loc = Geolocator()
location = loc.get_distance_between_locations(Location(city="groningen"), Location(city="amsterdam"))
print(location)
