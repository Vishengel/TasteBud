import json

from bs4 import BeautifulSoup, Comment

from libs.common.scrape.exceptions import ElementNotFound

AGENDA_COMMENT = "agenda main"
NO_ITEMS_COMMENT = "geen resultaten"


def extract_events_from_html(page_html: str) -> list[str]:
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

    return event_jsons
