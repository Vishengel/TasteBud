from nicegui import ui
from starlette.responses import RedirectResponse

from interface.api.playlist_manager.app import app
from interface.ui.layout import common_layout
from interface.ui.playlist_manager.playlists_page import PlaylistsPage


@ui.page("/playlist-manager")
async def page():
    playlists_page = PlaylistsPage()
    await common_layout(playlists_page, active_route="/playlist-manager")


if __name__ in {"__main__", "__mp_main__"}:
    import interface.blend_main
    import interface.event_scanner_main  # noqa: F401 — registers /event-scanner

    @ui.page("/")
    async def root():
        return RedirectResponse("/playlist-manager")

    ui.run_with(app)
    ui.run(host="0.0.0.0", port=8003, reload=True)
