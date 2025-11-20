import argparse

from libs.spotify.playlist_management.playlist_manager import PlaylistManager
from libs.spotify.spotify_client.spotify_client import SpotifyClient


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_names", nargs="+", type=str)
    return parser.parse_args()


def main():
    args = get_args()
    spotify_client = SpotifyClient()
    playlist_manager = PlaylistManager(spotify_client)
    playlist_manager.create_combined_playlist(
        "test",
        playlist_names=args.playlist_names,
    )


if __name__ == "__main__":
    main()
