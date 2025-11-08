import pylast


class LastFMClient:
    def __init__(self, api_key: str, api_secret: str, username: str, password: str):
        self.network = pylast.LastFMNetwork(
            api_key=api_key, api_secret=api_secret, username=username, password_hash=pylast.md5(password)
        )

    def get_similar_artists(self, artist_name: str, limit: int | None = None) -> list[str]:
        artist = self.network.get_artist(artist_name)
        similar_artists = artist.get_similar(limit=limit)
        return [artist.name for artist in similar_artists]
