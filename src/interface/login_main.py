import logging
import re

from nicegui import ui
from spotipy import CacheFileHandler, SpotifyException, SpotifyOAuth
from starlette.requests import Request

from infrastructure.spotify.config import CONFIG
from interface.ui.layout import common_layout
from interface.ui.login.login_page import LoginPage
from interface.ui.login.success_page import SuccessPage

logger = logging.getLogger(__name__)

_SAFE_USER_ID = re.compile(r"^[\w-]+$")  # \w = [a-zA-Z0-9_]


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
        logger.warning("OAuth callback missing required params: code=%r state=%r error=%r", code, state, error)
        ui.navigate.to("/login?error=auth_failed")
        return

    # Sanitize state param to prevent path traversal
    if not _SAFE_USER_ID.match(state):
        logger.warning("Rejected unsafe state param: %r", state)
        ui.navigate.to("/login?error=auth_failed")
        return
    user_id = state

    # Attempt token exchange
    cache_filename = f"credentials_{user_id}"
    try:
        oauth = SpotifyOAuth(
            client_id=CONFIG.spotipy_client_id,
            client_secret=CONFIG.spotipy_client_secret.get_secret_value(),
            redirect_uri=CONFIG.spotipy_redirect_uri,
            cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / cache_filename),
        )
        token = oauth.get_access_token(code, as_dict=False)
        if not token:
            logger.error("Token exchange returned no token for user_id=%s", user_id)
            ui.navigate.to("/login?error=auth_failed")
            return
    except SpotifyException as exc:
        logger.exception("Spotify OAuth error for user_id=%s: %s", user_id, exc)
        ui.navigate.to("/login?error=auth_failed")
        return
    except Exception:
        logger.exception("Unexpected error during token exchange for user_id=%s", user_id)
        ui.navigate.to("/login?error=auth_failed")
        return

    # Success: redirect to login/success page
    ui.navigate.to(f"/login/success?user_id={user_id}")


@ui.page("/login")
async def login_page(request: Request):
    """Login page. Reads ?error query param to show inline error messages."""
    error = request.query_params.get("error")
    page = LoginPage(error=error)
    await common_layout(page, active_route="/login")


@ui.page("/login/success")
async def login_success_page(request: Request):
    """Login success page. Reads user_id from query params and displays Spotify profile."""
    user_id = request.query_params.get("user_id", "")
    page = SuccessPage(user_id=user_id)
    await common_layout(page, active_route="/login")
