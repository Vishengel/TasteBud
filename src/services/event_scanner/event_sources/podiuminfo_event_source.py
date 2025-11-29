from libs.common.data_models.event import Event
from services.event_scanner.event_sources.event_source_base import EventSource, EventSourceType


class PodiumInfoEventSource(EventSource):
    event_source_type = EventSourceType.PODIUMINFO

    def get_events(self) -> list[Event]:
        return []
