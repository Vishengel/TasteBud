import uvicorn
from nicegui import ui

from libs.common.nicegui_ui.common_layout import common_layout
from src.services.playlist_manager.nicegui_ui.pages.playlists_page import PlaylistsPage
from src.services.playlist_manager.server.app import app


@ui.page("/playlist-manager")
async def page():
    playlists_page = PlaylistsPage()
    await common_layout(playlists_page)


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload=True)
