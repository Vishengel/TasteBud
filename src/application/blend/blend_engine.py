from collections import Counter
from typing import Protocol

from domain.blend.models import BlendConfig, ScoredTrack, UserTasteProfile
from domain.events.models import Playlist


def build_blend_description(user_ids: list[str], config: BlendConfig) -> str:
    weights = ", ".join(f"{k}:{v}" for k, v in config.time_weights.items())
    return (
        f"TasteBud blend of {' + '.join(user_ids)}. "
        f"Scoring: rank-weighted top tracks (time weights: {weights}). "
        f"Target size: {config.target_size}. "
        "Expanded with shared artist top tracks when needed."
    )


class BlendAdapter(Protocol):
    def get_taste_profile(self, user_id: str, time_weights: dict[str, float]) -> UserTasteProfile: ...

    def get_artist_top_tracks(self, artist_id: str) -> list[ScoredTrack]: ...

    def create_playlist(self, user_id: str, name: str, track_uris: list[str], description: str = "") -> Playlist: ...


class BlendEngine:
    def __init__(self, adapters: list[BlendAdapter]):
        self._adapters = adapters

    def create_blend(self, user_ids: list[str], config: BlendConfig) -> list[ScoredTrack]:
        profiles = [
            adapter.get_taste_profile(user_id, config.time_weights)
            for adapter, user_id in zip(self._adapters, user_ids, strict=False)
        ]

        merged = self._merge_profiles(profiles)
        result = sorted(merged, key=lambda t: t.score, reverse=True)[: config.target_size]

        if len(result) < config.target_size:
            shared_artist_ids = self._find_shared_artist_ids(profiles)
            result = self._expand_with_artists(result, shared_artist_ids, config.target_size)

        return result

    def _merge_profiles(self, profiles: list[UserTasteProfile]) -> list[ScoredTrack]:
        scores: dict[str, float] = {}
        meta: dict[str, ScoredTrack] = {}

        for profile in profiles:
            for track in profile.scored_tracks:
                scores[track.uri] = scores.get(track.uri, 0.0) + track.score
                if track.uri not in meta:
                    meta[track.uri] = track

        return [meta[uri].model_copy(update={"score": score}) for uri, score in scores.items()]

    def _find_shared_artist_ids(self, profiles: list[UserTasteProfile]) -> list[str]:
        artist_counts = Counter(artist_id for profile in profiles for artist_id in profile.top_artist_ids)
        return [aid for aid, count in artist_counts.items() if count >= 2]

    def _expand_with_artists(
        self,
        current: list[ScoredTrack],
        shared_artist_ids: list[str],
        target_size: int,
    ) -> list[ScoredTrack]:
        existing_uris = {t.uri for t in current}
        expansion_adapter = self._adapters[0]
        result = list(current)

        for artist_id in shared_artist_ids:
            if len(result) >= target_size:
                break
            for track in expansion_adapter.get_artist_top_tracks(artist_id):
                if len(result) >= target_size:
                    break
                if track.uri not in existing_uris:
                    result.append(track)
                    existing_uris.add(track.uri)

        return result
