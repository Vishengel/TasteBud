from typing import Protocol

from domain.playlists.models import Playlist, Track


class PlaylistManager(Protocol):
    def get_all_playlists_for_user_id(self, user_id: str) -> list[Playlist]: ...

    def get_tracks_for_playlist_id(self, playlist_id: str) -> list[Track]: ...

    def create_combined_playlist(
        self,
        user_id: str,
        playlist_ids: list[str] | None = None,
        playlist_names: list[str] | None = None,
        combined_playlist_name: str | None = None,
    ) -> Playlist: ...

    def create_playlist(self, user_id: str, name: str, description: str = "") -> Playlist: ...
