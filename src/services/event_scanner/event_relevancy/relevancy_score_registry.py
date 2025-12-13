from dataclasses import dataclass, field

from libs.common.data_models.event import Event
from services.event_scanner.event_relevancy.lastfm_relevancy_score import LastFMRelevancyScore
from services.event_scanner.event_relevancy.relevancy_score import RelevancyScore


@dataclass
class RelevancyScoreRegistry:
    lastfm_score: LastFMRelevancyScore = field(default_factory=LastFMRelevancyScore)

    def active_scorers(self) -> list[RelevancyScore]:
        return [score for score in self.__dict__.values() if getattr(score, "active", False)]

    def get_combined_score(self, event: Event) -> float:
        return sum(round(scorer.weight * scorer.get_score(event), 1) for scorer in self.active_scorers())
