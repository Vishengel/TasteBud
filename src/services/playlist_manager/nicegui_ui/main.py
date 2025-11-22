import uvicorn
from nicegui import ui

from src.services.playlist_manager.nicegui_ui.pages.playlists_page import PlaylistsPage
from src.services.playlist_manager.server.app import app


@ui.page("/playlist-manager")
async def page():
    manager = PlaylistsPage()
    await manager.create()


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
