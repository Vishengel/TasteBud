from application.playlist_manager.playlist_manager import PlaylistManager
from infrastructure.spotify.client import SpotifyClient


def make_playlist_manager() -> PlaylistManager:
    return PlaylistManager(SpotifyClient())
