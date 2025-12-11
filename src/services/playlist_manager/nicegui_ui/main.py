from nicegui import ui
from starlette.responses import RedirectResponse

from libs.common.nicegui_ui.common_layout import common_layout
from src.services.playlist_manager.nicegui_ui.pages.playlists_page import PlaylistsPage
from src.services.playlist_manager.server.app import app


@ui.page("/")
async def root():
    return RedirectResponse("/playlist-manager")


@ui.page("/playlist-manager")
async def playlist_manager_page():
    playlists_page = PlaylistsPage()
    await common_layout(playlists_page)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run_with(app, title="TasteBud")
    ui.run(host="0.0.0.0", port=8001, reload=True)
