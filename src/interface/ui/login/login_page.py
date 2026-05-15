from nicegui import ui
from spotipy import CacheFileHandler, SpotifyOAuth

from infrastructure.spotify.client import SpotifyClient
from infrastructure.spotify.config import CONFIG
from interface.ui.layout import NiceGUIPage


def _build_oauth(user_id: str) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=CONFIG.spotipy_client_id,
        client_secret=CONFIG.spotipy_client_secret.get_secret_value(),
        redirect_uri=CONFIG.spotipy_redirect_uri,
        scope=" ".join(SpotifyClient.SCOPE),
        cache_handler=CacheFileHandler(cache_path=CONFIG.cache_dir / f"credentials_{user_id}"),
        state=user_id,
    )


class LoginPage(NiceGUIPage):
    def __init__(self, error: str | None = None):
        self.error = error
        self.user_id_input: ui.input | None = None

    def _connect(self):
        user_id = (self.user_id_input.value or "").strip()
        if not user_id:
            ui.notify("Enter your Spotify user ID", type="negative")
            return
        oauth = _build_oauth(user_id)
        url = oauth.get_authorize_url()
        ui.navigate.to(url)

    async def create_page(self):
        with ui.column().classes("items-center w-full mt-10 gap-6"):
            with ui.card().classes("tb-card w-full max-w-md p-6 gap-4"):
                ui.label("Connect Spotify").style("color: var(--accent); font-size: 1.5rem; font-weight: 700;")
                ui.label(
                    "Enter your Spotify user ID to authorise TasteBud. "
                    "You'll be redirected to Spotify to approve access."
                ).style("color: var(--muted); font-size: 0.9rem;")

                if self.error == "auth_failed":
                    ui.label("Authentication failed. Please try again.").style("color: #f87171;")
                elif self.error == "cancelled":
                    ui.label("You cancelled the Spotify login.").style("color: var(--muted);")

                self.user_id_input = ui.input("Spotify user ID").props("outlined").classes("tb-input w-full")
                ui.button("Connect with Spotify", on_click=self._connect).classes("tb-btn w-full mt-2")
