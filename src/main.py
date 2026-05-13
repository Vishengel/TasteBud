from fastapi import FastAPI
from nicegui import ui
from starlette.responses import RedirectResponse

import services.blend.nicegui_ui.main
import services.event_scanner.nicegui_ui.main
import services.playlist_manager.nicegui_ui.main  # noqa: F401 — registers /playlist-manager page
from services.blend.server.app import app as blend_app
from services.event_scanner.server.app import app as event_scanner_app
from services.playlist_manager.server.app import app as playlist_manager_app

combined = FastAPI(title="TasteBud")
combined.mount("/event-scanner-api", event_scanner_app)
combined.mount("/playlist-manager-api", playlist_manager_app)
combined.mount("/blend-api", blend_app)


@ui.page("/")
async def root():
    return RedirectResponse("/event-scanner")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run_with(combined, title="TasteBud")
    ui.run(host="0.0.0.0", port=8000, reload=False)
