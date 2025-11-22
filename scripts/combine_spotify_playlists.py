import argparse

from src.libs.spotify.playlist_management.playlist_manager import PlaylistManager
from src.libs.spotify.spotify_client.spotify_client import SpotifyClient


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_names", nargs="+", type=str)
    parser.add_argument("-u", "--user_name", type=str)
    parser.add_argument("-n", "--combined_playlist_name", type=str, required=False)
    return parser.parse_args()


def main():
    args = get_args()
    spotify_client = SpotifyClient()
    playlist_manager = PlaylistManager(spotify_client)
    playlist_manager.create_combined_playlist(
        user_id=args.user_name,
        playlist_names=args.playlist_names,
        combined_playlist_name=args.combined_playlist_name,
    )


if __name__ == "__main__":
    main()
