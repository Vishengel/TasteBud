import datetime
import json
import logging

from bs4 import BeautifulSoup, Comment

from libs.common.data_models.event import Event
from libs.common.scrape.exceptions import ElementNotFound

logger = logging.getLogger(__name__)

AGENDA_COMMENT = "agenda main"
NO_ITEMS_COMMENT = "geen resultaten"


def _serialize_event_json(event_json: dict) -> Event | None:
    if "performer" not in event_json:
        logger.warning(
            "No artist found for event %s at url %s. This event will be excluded from the Event Scanner",
            event_json["name"],
            event_json["url"],
        )
        return None

    artists = [performer["name"] for performer in event_json["performer"]]
    event_datetime = datetime.datetime.fromisoformat(event_json["startDate"])
    return Event(artists=artists, date=event_datetime.date())


def extract_events_from_html(page_html: str) -> list[Event | None]:
    soup = BeautifulSoup(page_html, "html.parser")

    agenda_comment = soup.find(string=lambda text: isinstance(text, Comment) and AGENDA_COMMENT in text.strip().lower())

    if agenda_comment is None:
        # ToDo: implement better stop condition by looking for next page button on page
        no_items_comment = soup.find(
            string=lambda text: isinstance(text, Comment) and NO_ITEMS_COMMENT in text.strip().lower()
        )
        if no_items_comment is not None:
            return []
        raise ElementNotFound("Unknown page: HTML contains neither an event overview nor a 'No results' indicator")

    event_json_tags = agenda_comment.find_all_next("script", type="application/ld+json")
    event_jsons = [json.loads(tag.contents[0]) for tag in event_json_tags]

    return [_serialize_event_json(event_json) for event_json in event_jsons]
