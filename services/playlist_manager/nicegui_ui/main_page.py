import uvicorn
from nicegui import ui

from services.playlist_manager.server.app import app


@ui.page("/")
def page():
    ui.page_title("Playlist Manager")
    ui.label("Hello World!")


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main_page:app", log_level="info", reload=True)
