from nicegui import ui
from starlette.responses import RedirectResponse

from interface.api.blend.app import app
from interface.ui.blend.blend_page import BlendPage
from interface.ui.layout import common_layout


@ui.page("/blend")
async def blend_page():
    page = BlendPage()
    await common_layout(page, active_route="/blend")


if __name__ in {"__main__", "__mp_main__"}:
    import interface.event_scanner_main
    import interface.playlist_manager_main  # noqa: F401 — registers /playlist-manager

    @ui.page("/")
    async def root():
        return RedirectResponse("/blend")

    ui.run_with(app, title="TasteBud")
    ui.run(host="0.0.0.0", port=8002, reload=True)
