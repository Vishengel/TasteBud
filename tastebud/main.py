import os

from dotenv import load_dotenv

from tastebud.spotify_client.request_handlers.access_token_handler import get_access_token

if __name__ == "__main__":
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    access_token_response = get_access_token(client_id, client_secret)
    print(access_token_response)
