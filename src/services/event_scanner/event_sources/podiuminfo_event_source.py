from libs.common.data_models.event import Event
from services.event_scanner.event_sources.event_source_base import EventSource


class PodiumInfoEventSource(EventSource):
    def get_events(self) -> list[Event]:
        return []
