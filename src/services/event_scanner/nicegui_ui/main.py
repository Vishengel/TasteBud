import uvicorn
from nicegui import ui

from libs.common.nicegui_ui.common_layout import common_layout
from services.event_scanner.nicegui_ui.pages.event_scanner_page import EventScannerPage
from src.services.playlist_manager.server.app import app


@ui.page("/event-scanner")
async def page():
    event_scanner_page = EventScannerPage()
    await common_layout(event_scanner_page)


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
