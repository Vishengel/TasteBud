import logging

from nicegui import ui
from spotipy import CacheFileHandler, SpotifyOAuth
from starlette.requests import Request

from infrastructure.spotify.config import CONFIG

logger = logging.getLogger(__name__)


@ui.page("/auth/spotify/callback")
async def spotify_callback(request: Request):
    """
    Spotify OAuth callback handler. Reads query params, exchanges auth code for token,
    then redirects to /login/success or /login?error=auth_failed.
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    error = request.query_params.get("error")

    # Check for OAuth errors or missing required params
    if error or not code or not state:
        ui.navigate.to("/login?error=auth_failed")
        return

    # Attempt token exchange
    user_id = state
    cache_filename = f"credentials_{user_id}"
    try:
        oauth = SpotifyOAuth(
            client_id=CONFIG.spotipy_client_id,
            client_secret=CONFIG.spotipy_client_secret.get_secret_value(),
            redirect_uri=CONFIG.spotipy_redirect_uri,
            cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / cache_filename),
        )
        oauth.get_access_token(code, as_dict=False)
    except Exception:
        logger.exception("Spotify token exchange failed for user_id=%s", user_id)
        ui.navigate.to("/login?error=auth_failed")
        return

    # Success: redirect to login/success page
    ui.navigate.to(f"/login/success?user_id={user_id}")


@ui.page("/login")
async def login_page():
    """Login page. Stub for Task 3."""
    ui.label("Login page (stub)")


@ui.page("/login/success")
async def login_success_page():
    """Login success page. Stub for Task 4."""
    ui.label("Login success page (stub)")
