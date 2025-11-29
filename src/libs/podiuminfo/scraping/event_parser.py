import json

from bs4 import BeautifulSoup, Comment

AGENDA_COMMENT = "agenda main"


def extract_events(page_html: str) -> list[str]:
    soup = BeautifulSoup(page_html, "html.parser")

    comment = soup.find(string=lambda text: isinstance(text, Comment) and AGENDA_COMMENT in text.strip().lower())

    event_json_tags = comment.find_all_next("script", type="application/ld+json")
    event_jsons = [json.loads(tag.contents[0]) for tag in event_json_tags]

    return event_jsons
