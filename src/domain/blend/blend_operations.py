from collections import Counter
from functools import reduce

from domain.blend.models import BlendConfig, ScoredTrack, UserTasteProfile


def merge_profiles(profiles: list[UserTasteProfile]) -> UserTasteProfile:
    return reduce(lambda a, b: a.merge(b), profiles)


def top_tracks(profile: UserTasteProfile, config: BlendConfig) -> list[ScoredTrack]:
    return sorted(profile.scored_tracks, key=lambda t: t.score, reverse=True)[: config.target_size]


def find_shared_artist_ids(profiles: list[UserTasteProfile]) -> list[str]:
    artist_counts = Counter(artist_id for profile in profiles for artist_id in profile.top_artist_ids)
    return [aid for aid, count in artist_counts.items() if count >= 2]
