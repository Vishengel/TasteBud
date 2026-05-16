import logging

from nicegui import ui

from infrastructure.spotify.client import SpotifyClient
from interface.ui.layout import NiceGUIPage

logger = logging.getLogger(__name__)


class SuccessPage(NiceGUIPage):
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def create_page(self):
        display_name: str | None = None
        try:
            client = SpotifyClient(user_id=self.user_id)
            profile = client.current_user()
            if profile["id"] != self.user_id:
                raise ValueError(f"Token mismatch: expected {self.user_id!r}, got {profile['id']!r}")
            display_name = profile.get("display_name") or self.user_id
        except Exception:
            logger.warning("Could not fetch Spotify display name for user_id=%s", self.user_id, exc_info=True)

        with ui.column().classes("items-center w-full mt-10 gap-6"):
            with ui.card().classes("tb-card w-full max-w-md p-6 gap-4"):
                ui.label("Connected!").style("color: var(--accent); font-size: 1.5rem; font-weight: 700;")
                if display_name:
                    ui.label(f"Logged in as: {display_name}").style("color: var(--text);")
                else:
                    ui.label("Connected! (couldn't fetch display name — but your token is saved)").style(
                        "color: var(--muted);"
                    )
                ui.label("You can close this tab. Ask the blend host to add your Spotify user ID.").style(
                    "color: var(--muted); font-size: 0.9rem;"
                )
                ui.link("Go to Blend", "/blend").style("color: var(--accent); text-decoration: underline;")
