from typing import ClassVar

from libs.common.data_models.event import Event
from libs.common.data_models.location import Location
from libs.geolocation.geolocator import Geolocator
from services.event_scanner.config import CONFIG
from services.event_scanner.event_relevancy.relevancy_score import RelevancyScore, RelevancyScoreSource


class DistanceRelevancyScore(RelevancyScore):
    source = RelevancyScoreSource.DISTANCE
    active: bool
    weight: ClassVar[float] = 1.0
    supported_countries: ClassVar[tuple[str, str]] = ("be", "nl")

    def __init__(self, geolocator: Geolocator | None = None):
        self.geolocator = geolocator or Geolocator(supported_countries=list(self.supported_countries))
        self.city_of_residence = Location(city=CONFIG.city_of_residence)

    def get_score(self, event: Event) -> float:
        full_event_location = event.venue.location
        # For now, just compute distance to the city center
        event_city = Location(city=full_event_location.city, country=full_event_location.country)
        distance = self.geolocator.get_distance_between_locations(self.city_of_residence, event_city)
        return distance
