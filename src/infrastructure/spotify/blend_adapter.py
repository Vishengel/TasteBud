from __future__ import annotations

from domain.blend.models import Platform, ScoredTrack, UserTasteProfile
from domain.events.models import Playlist
from infrastructure.spotify.client import SpotifyClient
from infrastructure.spotify.time_range import TimeRange

_TIME_WEIGHT_KEY_TO_RANGE: dict[str, TimeRange] = {
    "long": TimeRange.LONG,
    "medium": TimeRange.MEDIUM,
    "short": TimeRange.SHORT,
}


def _extract_artist_ids(track_dict: dict) -> list[str]:
    return [artist["id"] for artist in track_dict["artists"]]


class SpotifyAdapter:
    PLATFORM = Platform.SPOTIFY

    def __init__(self, user_id: str):
        self._client = SpotifyClient(user_id=user_id)

    def get_taste_profile(self, user_id: str, time_weights: dict[str, float]) -> UserTasteProfile:
        scores: dict[str, float] = {}
        artist_ids_by_uri: dict[str, list[str]] = {}

        for key, weight in time_weights.items():
            time_range = _TIME_WEIGHT_KEY_TO_RANGE[key]
            self._score_time_range(time_range, weight, scores, artist_ids_by_uri)

        scored_tracks = [
            ScoredTrack(
                uri=uri,
                platform=self.PLATFORM,
                score=score,
                artist_ids=artist_ids_by_uri[uri],
            )
            for uri, score in scores.items()
        ]

        top_artist_ids = list({artist_id for track in scored_tracks for artist_id in track.artist_ids})

        return UserTasteProfile(
            user_id=user_id,
            platform=self.PLATFORM,
            scored_tracks=scored_tracks,
            top_artist_ids=top_artist_ids,
        )

    def _score_time_range(
        self,
        time_range: TimeRange,
        weight: float,
        scores: dict[str, float],
        artist_ids_by_uri: dict[str, list[str]],
    ) -> None:
        tracks = self._client.fetch_top_tracks(time_range=time_range)
        for rank, track_dict in enumerate(tracks, start=1):
            uri = track_dict["uri"]
            scores[uri] = scores.get(uri, 0.0) + (1.0 / rank) * weight
            if uri not in artist_ids_by_uri:
                artist_ids_by_uri[uri] = _extract_artist_ids(track_dict)

    def get_artist_top_tracks(self, artist_id: str) -> list[ScoredTrack]:
        tracks = self._client.fetch_artist_top_tracks(artist_id)
        return [
            ScoredTrack(
                uri=t["uri"],
                platform=self.PLATFORM,
                score=0.0,
                artist_ids=_extract_artist_ids(t),
            )
            for t in tracks
        ]

    def create_playlist(self, user_id: str, name: str, track_uris: list[str], description: str = "") -> Playlist:
        playlist_dict = self._client.user_playlist_create(
            user=user_id, name=name, public=False, description=description
        )
        playlist_id = playlist_dict["id"]
        self._client.replace_tracks_in_playlist(playlist_id, track_uris)
        return Playlist(
            id=playlist_id,
            name=playlist_dict["name"],
            external_url=playlist_dict["external_urls"]["spotify"],
            n_tracks=len(track_uris),
        )
