from services.event_scanner.event_sources.event_source_base import EventSource, EventSourceType
from services.event_scanner.event_sources.podiuminfo_event_source import PodiumInfoEventSource


def event_source_factory(source_types: set[EventSourceType]) -> dict[EventSourceType, EventSource]:
    event_sources = {}
    for source_type in source_types:
        if source_type == EventSourceType.PODIUMINFO:
            event_sources[source_type] = PodiumInfoEventSource()
    return event_sources
