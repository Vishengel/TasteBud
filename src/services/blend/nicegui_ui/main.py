from nicegui import ui
from starlette.responses import RedirectResponse

from libs.common.nicegui_ui.common_layout import common_layout
from services.blend.nicegui_ui.pages.blend_page import BlendPage
from services.blend.server.app import app


@ui.page("/blend")
async def blend_page():
    page = BlendPage()
    await common_layout(page)


if __name__ in {"__main__", "__mp_main__"}:

    @ui.page("/")
    async def root():
        return RedirectResponse("/blend")

    ui.run_with(app, title="TasteBud")
    ui.run(host="0.0.0.0", port=8002, reload=True)
