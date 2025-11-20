import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv
from spotipy import CacheFileHandler, Spotify, SpotifyClientCredentials

from config import CONFIG
from libs.spotify.spotify_history_builder import SpotifyHistoryBuilder

logging.basicConfig(
    format="%(asctime)s,%(msecs)03d %(levelname)-1s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger("spotipy").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", required=True, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()
    args = get_args()
    sp_client = Spotify(
        auth_manager=SpotifyClientCredentials(
            cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / "credentials")
        )
    )
    spotify_history_analyzer = SpotifyHistoryBuilder(sp_client, args.history)
