from nicegui import ui
from starlette.responses import RedirectResponse

from common.ui.layout import common_layout
from interface.api.event_scanner.app import app
from interface.ui.event_scanner.event_scanner_page import EventScannerPage


@ui.page("/event-scanner")
async def page():
    event_scanner_page = EventScannerPage()
    await common_layout(event_scanner_page)


if __name__ in {"__main__", "__mp_main__"}:

    @ui.page("/")
    async def root():
        return RedirectResponse("/event-scanner")

    ui.run_with(app)
    ui.run(host="0.0.0.0", port=8001, reload=True)
