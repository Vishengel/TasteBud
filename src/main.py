from fastapi import FastAPI
from nicegui import ui
from starlette.responses import RedirectResponse

# isort: off
import interface.event_scanner_main
import interface.playlist_manager_main
import interface.blend_main
import interface.login_main  # noqa: F401

# isort: on
from interface.api.blend.app import app as blend_app
from interface.api.event_scanner.app import app as event_scanner_app
from interface.api.playlist_manager.app import app as playlist_manager_app

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
