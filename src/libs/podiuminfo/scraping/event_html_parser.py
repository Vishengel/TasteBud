import datetime
import json
import logging

from bs4 import BeautifulSoup, Comment

from libs.common.data_models.event import Event, Location, Venue
from libs.common.scrape.exceptions import ElementNotFound

logger = logging.getLogger(__name__)

AGENDA_COMMENT = "agenda main"
NO_ITEMS_COMMENT = "geen resultaten"
ERROR_STRING_START = "Het is niet mogelijk meer dan"


def _venue_from_location_field(event_json: dict) -> Venue:
    location = event_json.get("location", None)
    name = location.get("name", None)
    address = location.get("address", None)

    if address:
        full_street_address = address.get("streetAddress", None)
        street = " ".join(full_street_address.split(" ")[:-1]) if full_street_address else None
        street_number = full_street_address.split(" ")[-1] if full_street_address else None
        location = Location(
            country_code=address.get("addressCountry", None),
            state=address.get("addressRegion", None),
            city=address.get("addressLocality", None),
            street=street,
            street_number=street_number,
            postal_code=address.get("postalCode", None),
        )

    return Venue(name=name, location=location)


def _serialize_event_json(event_json: dict) -> Event | None:
    if "performer" not in event_json:
        logger.warning(
            "No artist found for event %s at url %s. This event will be excluded from the Event Scanner",
            event_json["name"],
            event_json["url"],
        )
        return None

    artists = [performer["name"] for performer in event_json["performer"]]

    try:
        venue = _venue_from_location_field(event_json)
    except ValueError:
        logger.warning(
            "No location info found for event %s at url %s. This event will be excluded from the Event Scanner",
            event_json["name"],
            event_json["url"],
        )
        return None

    event_datetime = datetime.datetime.fromisoformat(event_json["startDate"])
    return Event(artists=artists, date=event_datetime.date(), venue=venue, url=event_json.get("url", None))


def extract_events_from_html(page_html: str) -> list[Event | None]:
    soup = BeautifulSoup(page_html, "html.parser")

    agenda_comment = soup.find(string=lambda text: isinstance(text, Comment) and AGENDA_COMMENT in text.strip().lower())

    if agenda_comment is None:
        no_items_comment = soup.find(
            string=lambda text: isinstance(text, Comment) and NO_ITEMS_COMMENT in text.strip().lower()
        )
        if no_items_comment is not None:
            return []
        raise ElementNotFound("Unknown page: HTML contains neither an event overview nor a 'No results' indicator")

    page_limit_error = soup.find(name="span", attrs={"class": "error"})

    if page_limit_error is not None:
        logger.info("Podiuminfo page limit reached")
        return []

    event_json_tags = agenda_comment.find_all_next("script", type="application/ld+json")
    event_jsons = [json.loads(tag.contents[0]) for tag in event_json_tags]

    return [_serialize_event_json(event_json) for event_json in event_jsons]
