from typing import Any

from libs.spotify.data_model.playlist import Playlist
from libs.spotify.data_model.track import Track
from libs.spotify.spotify_client.spotify_client import SpotifyClient


class PlaylistManager:
    def __init__(self, spotify_client: SpotifyClient, user_id: str | None = None):
        self.spotify_client = spotify_client
        self.user_id = user_id if user_id is not None else self.spotify_client.current_user_id
        self.playlists = self._get_playlists()
        self.name_to_id_map = {playlist.name: playlist.id for playlist in self.playlists.values()}

    def create_combined_playlist(
        self,
        combined_playlist_name: str,
        playlist_ids: list[str] | list[str] | None = None,
        playlist_names: list[str] | None = None,
    ):
        if playlist_ids is None and playlist_names is None:
            raise ValueError("Either playlist_ids or playlist_names must be provided")

        if playlist_ids is not None:
            tracks = self._combine_playlists_by_id(playlist_ids)
        else:
            tracks = self._combine_playlists_by_name(playlist_names)

        if not self._playlist_exists(combined_playlist_name):
            playlist_dict = self.spotify_client.user_playlist_create(self.user_id, combined_playlist_name)
            playlist = Playlist.from_spotify_playlist_dict(playlist_dict)
            self.playlists[playlist.id] = playlist
            self.name_to_id_map[combined_playlist_name] = playlist.id

        self.spotify_client.playlist_replace_items(
            self.name_to_id_map[combined_playlist_name], [track.uri for track in tracks]
        )

    def _create_playlist(self, name: str) -> None:
        playlist = self.spotify_client.user_playlist_create(self.user_id, name)
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
        playlists = []
        user_playlists_result = self.spotify_client.user_playlists(self.user_id, limit=100)
        playlists.extend(self._get_playlist_from_results(user_playlists_result))

        while user_playlists_result := self.spotify_client.next(user_playlists_result):
            playlists.extend(self._get_playlist_from_results(user_playlists_result))

        return {playlist.id: playlist for playlist in playlists}

    def _get_tracks_for_playlist(self, playlist: Playlist) -> list[Track]:
        tracks = []
        tracks_for_playlist = self.spotify_client.playlist_items(playlist.id, limit=100)
        tracks.extend(self._get_tracks_from_track_dict(tracks_for_playlist))

        while tracks_for_playlist := self.spotify_client.next(tracks_for_playlist):
            tracks.extend(self._get_tracks_from_track_dict(tracks_for_playlist))

        return tracks

    @staticmethod
    def _get_playlist_from_results(user_playlists_result: dict[str, Any]):
        return [Playlist.from_spotify_playlist_dict(playlist) for playlist in user_playlists_result["items"]]

    @staticmethod
    def _get_tracks_from_track_dict(tracks_for_playlist: dict[str, Any]):
        return [Track.from_spotify_track_dict(track_dict) for track_dict in tracks_for_playlist["items"]]
