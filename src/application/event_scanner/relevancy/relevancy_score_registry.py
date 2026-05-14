from dataclasses import dataclass, field

from application.event_scanner.relevancy.distance_relevancy_score import DistanceRelevancyScore
from application.event_scanner.relevancy.lastfm_relevancy_score import LastFMRelevancyScore
from application.event_scanner.relevancy.relevancy_score import RelevancyScore
from domain.events.models import Event


@dataclass
class RelevancyScoreRegistry:
    lastfm_score: LastFMRelevancyScore = field(default_factory=LastFMRelevancyScore)
    distance_score: DistanceRelevancyScore = field(default_factory=DistanceRelevancyScore)

    def active_scorers(self) -> list[RelevancyScore]:
        return [score for score in self.__dict__.values() if getattr(score, "active", False)]

    def get_combined_score(self, event: Event) -> float:
        return sum(round(scorer.weight * scorer.get_score(event), 1) for scorer in self.active_scorers())
