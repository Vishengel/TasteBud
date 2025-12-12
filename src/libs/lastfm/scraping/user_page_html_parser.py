from bs4 import BeautifulSoup


def extract_artist_count_from_user_page(page_html: str, username: str) -> int:
    soup = BeautifulSoup(page_html, "html.parser")

    artist_link_element = soup.find("a", href=f"/user/{username}/library/artists")
    return int(artist_link_element.text.replace(",", "_"))
