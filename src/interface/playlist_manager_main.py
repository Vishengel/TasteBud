from nicegui import ui
from starlette.responses import RedirectResponse

from interface.api.playlist_manager.app import app
from interface.ui.layout import common_layout
from interface.ui.playlist_manager.playlists_page import PlaylistsPage


@ui.page("/playlist-manager")
async def playlist_manager_page():
    playlists_page = PlaylistsPage()
    await common_layout(playlists_page)


if __name__ in {"__main__", "__mp_main__"}:

    @ui.page("/")
    async def root():
        return RedirectResponse("/playlist-manager")

    ui.run_with(app, title="TasteBud")
    ui.run(host="0.0.0.0", port=8000, reload=True)
