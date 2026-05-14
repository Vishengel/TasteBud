from datetime import datetime

from domain.playlists.models import Playlist, Track
from infrastructure.spotify.client import SpotifyClient
from infrastructure.spotify.config import CONFIG
from infrastructure.spotify.models import SpotifyPlaylist, SpotifyTrack


def _mark_combined_playlist_name(combined_playlist_name: str) -> str:
    return f"[AUTO] {combined_playlist_name}"


def _create_default_combined_playlist_name() -> str:
    date = datetime.today().strftime("%Y-%m-%d")
    return _mark_combined_playlist_name(f"Combined Playlist {date}")


def _create_description(playlist_names: list[str]) -> str:
    if len(playlist_names) == 0:
        return CONFIG.tastebud_playlist_watermark
    return f"{' + '.join(playlist_names)}. {CONFIG.tastebud_playlist_watermark}"


def _to_domain_playlist(sp: SpotifyPlaylist) -> Playlist:
    return Playlist(
        id=sp.id,
        name=sp.name,
        external_url=sp.href,
        n_tracks=sp.n_tracks,
        owner_id=sp.owner_id,
        generated_by_tastebud=sp.generated_by_tastebud or False,
    )


def _to_domain_track(sp: SpotifyTrack) -> Track:
    return Track(uri=sp.uri)


class SpotifyPlaylistManager:
    def __init__(self, spotify_client: SpotifyClient, user_id: str | None = None):
        self.spotify_client = spotify_client
        self.main_user_id = user_id if user_id is not None else self.spotify_client.current_user_id
        self._playlists: dict[str, SpotifyPlaylist] = self._get_playlists_dict()
        self._name_to_id_map = {pl.name: pl.id for pl in self._playlists.values()}

    def get_all_playlists_for_user_id(self, user_id: str) -> list[Playlist]:
        raw_playlists = self.spotify_client.fetch_all_playlists(user_id)
        return [_to_domain_playlist(SpotifyPlaylist.from_spotify_playlist_dict(pl)) for pl in raw_playlists]

    def get_tracks_for_playlist_id(self, playlist_id: str) -> list[Track]:
        raw_tracks = self.spotify_client.fetch_tracks_for_playlist(playlist_id)
        return [_to_domain_track(SpotifyTrack.from_spotify_track_dict(t)) for t in raw_tracks]

    def create_combined_playlist(
        self,
        user_id: str,
        playlist_ids: list[str] | None = None,
        playlist_names: list[str] | None = None,
        combined_playlist_name: str | None = None,
    ) -> Playlist:
        if playlist_ids is not None:
            tracks = self._combine_playlists_by_id(playlist_ids)
        elif playlist_names is not None:
            tracks = self._combine_playlists_by_name(playlist_names)
        else:
            raise ValueError("Either playlist_ids or playlist_names must be provided")

        combined_playlist_name = (
            _mark_combined_playlist_name(combined_playlist_name)
            if combined_playlist_name
            else _create_default_combined_playlist_name()
        )

        if not self._playlist_exists(combined_playlist_name):
            description_source = []
            if playlist_names:
                description_source = playlist_names
            elif playlist_ids:
                description_source = [self._playlists[pid].name for pid in playlist_ids]
            self._create_spotify_playlist(user_id, combined_playlist_name, _create_description(description_source))

        combined_playlist_id = self._name_to_id_map[combined_playlist_name]
        self.spotify_client.replace_tracks_in_playlist(combined_playlist_id, [t.uri for t in tracks])
        updated = SpotifyPlaylist.from_spotify_playlist_dict(self.spotify_client.playlist(combined_playlist_id))
        self._playlists[combined_playlist_id] = updated
        return _to_domain_playlist(updated)

    def create_playlist(self, user_id: str, name: str, description: str = "") -> Playlist:
        return _to_domain_playlist(self._create_spotify_playlist(user_id, name, description))

    def _combine_playlists(self, playlists: list[SpotifyPlaylist]) -> list[Track]:
        return [track for pl in playlists for track in self.get_tracks_for_playlist_id(pl.id)]

    def _combine_playlists_by_id(self, playlist_ids: list[str]) -> list[Track]:
        return self._combine_playlists([self._find_by_id(pid) for pid in playlist_ids])

    def _combine_playlists_by_name(self, playlist_names: list[str]) -> list[Track]:
        ids = [self._name_to_id_map[name] for name in playlist_names if name in self._name_to_id_map]
        return self._combine_playlists_by_id(ids)

    def _find_by_id(self, playlist_id: str) -> SpotifyPlaylist:
        if playlist_id not in self._playlists:
            raise ValueError(f"Playlist with id {playlist_id} not found")
        return self._playlists[playlist_id]

    def _playlist_exists(self, name: str) -> bool:
        return name in self._name_to_id_map

    def _create_spotify_playlist(self, user_id: str, name: str, description: str) -> SpotifyPlaylist:
        playlist_dict = self.spotify_client.user_playlist_create(user=user_id, name=name, description=description)
        sp = SpotifyPlaylist.from_spotify_playlist_dict(playlist_dict)
        sp.generated_by_tastebud = True
        self._playlists[sp.id] = sp
        self._name_to_id_map[name] = sp.id
        return sp

    def _get_playlists_dict(self) -> dict[str, SpotifyPlaylist]:
        raw = self.spotify_client.fetch_all_playlists(self.main_user_id)
        return {pl["id"]: SpotifyPlaylist.from_spotify_playlist_dict(pl) for pl in raw}
