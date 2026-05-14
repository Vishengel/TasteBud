from nicegui import ui
from starlette.responses import RedirectResponse

from common.ui.layout import common_layout
from interface.api.blend.app import app
from interface.ui.blend.blend_page import BlendPage


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
