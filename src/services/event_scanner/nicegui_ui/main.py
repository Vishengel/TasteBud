from nicegui import ui
from starlette.responses import RedirectResponse

from libs.common.nicegui_ui.common_layout import common_layout
from services.event_scanner.nicegui_ui.pages.event_scanner_page import EventScannerPage
from src.services.playlist_manager.server.app import app


@ui.page("/event-scanner")
async def page():
    event_scanner_page = EventScannerPage()
    await common_layout(event_scanner_page)


if __name__ in {"__main__", "__mp_main__"}:
    # Only attach event-scanner to root if it's being launched as the main app
    @ui.page("/")
    async def root():
        return RedirectResponse("/event-scanner")

    ui.run_with(app)
    ui.run(host="0.0.0.0", port=8000, reload=True)
