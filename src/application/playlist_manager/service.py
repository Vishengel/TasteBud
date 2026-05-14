from application.playlist_manager.playlist_manager import PlaylistManager
from infrastructure.spotify.client import SpotifyClient
from infrastructure.spotify.playlist_management import SpotifyPlaylistManager


def make_playlist_manager() -> PlaylistManager:
    return SpotifyPlaylistManager(SpotifyClient())
