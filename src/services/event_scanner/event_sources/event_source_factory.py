from services.event_scanner.event_sources.event_source_base import EventSource
from services.event_scanner.event_sources.podiuminfo_event_source import PodiuminfoEventSource
from services.event_scanner.server.data_model import EventSourceType


def event_source_factory(source_types: set[EventSourceType]) -> dict[EventSourceType, EventSource]:
    event_sources = {}
    for source_type in source_types:
        if source_type == EventSourceType.PODIUMINFO:
            event_sources[source_type] = PodiuminfoEventSource()
    return event_sources
