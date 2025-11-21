from datetime import datetime

from config import CONFIG
from libs.spotify.data_model.playlist import Playlist
from libs.spotify.data_model.track import Track
from libs.spotify.spotify_client.spotify_client import SpotifyClient


def _mark_combined_playlist_name(combined_playlist_name: str) -> str:
    return f"[AUTO] {combined_playlist_name}"


def _create_default_combined_playlist_name(playlist_names: list[str]) -> str:
    date = datetime.today().strftime("%Y-%m-%d")
    return _mark_combined_playlist_name(f"Combined Playlist {date}")


def _create_description(playlist_names: list[str]) -> str:
    return f"{' + '.join(playlist_names)}. {CONFIG.tastebud_playlist_watermark}"


class PlaylistManager:
    def __init__(self, spotify_client: SpotifyClient, user_id: str | None = None):
        self.spotify_client = spotify_client
        self.user_id = user_id if user_id is not None else self.spotify_client.current_user_id
        self.playlists = self._get_playlists()
        self.name_to_id_map = {playlist.name: playlist.id for playlist in self.playlists.values()}

    def create_combined_playlist(
        self,
        playlist_ids: list[str] | None = None,
        playlist_names: list[str] | None = None,
        combined_playlist_name: str | None = None,
    ):
        if playlist_ids is not None:
            tracks = self._combine_playlists_by_id(playlist_ids)
        elif playlist_names is not None:
            tracks = self._combine_playlists_by_name(playlist_names)
        else:
            raise ValueError("Either playlist_ids or playlist_names must be provided")

        # ToDo: this silently fails if multiple playlists are created on the same date without providing a name
        combined_playlist_name = (
            _mark_combined_playlist_name(combined_playlist_name)
            if combined_playlist_name
            else _create_default_combined_playlist_name(playlist_names)
        )

        if not self._playlist_exists(combined_playlist_name):
            self.create_playlist(combined_playlist_name, _create_description(playlist_names))

        self.spotify_client.playlist_replace_items(
            self.name_to_id_map[combined_playlist_name], [track.uri for track in tracks]
        )

    def create_playlist(self, name: str, description: str = "") -> None:
        playlist_dict = self.spotify_client.user_playlist_create(user=self.user_id, name=name, description=description)
        playlist = Playlist.from_spotify_playlist_dict(playlist_dict)
        playlist.generated_by_tastebud = True
        self.playlists[playlist.id] = playlist
        self.name_to_id_map[name] = playlist.id

    def _combine_playlists(self, playlists: list[Playlist]) -> list[Track]:
        return [track for playlist in playlists for track in self._get_tracks_for_playlist(playlist)]

    def _combine_playlists_by_id(self, playlist_ids: list[str]) -> list[Track]:
        return self._combine_playlists([self._find_playlist_by_id(playlist_id) for playlist_id in playlist_ids])

    def _combine_playlists_by_name(self, playlist_names: list[str]) -> list[Track]:
        ids = [self.name_to_id_map[name] for name in playlist_names if name in self.name_to_id_map]
        return self._combine_playlists_by_id(ids)

    def _find_playlist_by_id(self, playlist_id: str) -> Playlist:
        if playlist_id not in self.playlists:
            raise ValueError(f"Playlist with id {playlist_id} not found")
        return self.playlists[playlist_id]

    def _find_playlist_by_name(self, name: str) -> Playlist:
        if name not in self.name_to_id_map:
            raise ValueError(f"Playlist with name {name} not found")
        return self.playlists[self.name_to_id_map[name]]

    def _playlist_exists(self, name: str) -> bool:
        return name in self.name_to_id_map

    def _get_playlists(self) -> dict[str, Playlist]:
        raw_playlists = self.spotify_client.fetch_all_playlists(self.user_id)
        return {playlist["id"]: Playlist.from_spotify_playlist_dict(playlist) for playlist in raw_playlists}

    def _get_tracks_for_playlist(self, playlist: Playlist) -> list[Track]:
        raw_tracks = self.spotify_client.fetch_tracks_for_playlist(playlist.id)
        return [Track.from_spotify_track_dict(track_dict) for track_dict in raw_tracks]
