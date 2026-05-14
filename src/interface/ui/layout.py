from typing import Protocol

from nicegui import ui


class NiceGUIPage(Protocol):
    async def create_page(self) -> None: ...


async def common_layout(nicegui_page: NiceGUIPage):
    dark = ui.dark_mode(True)

    with ui.header().classes("items-center justify-between bg-gray-800 text-white p-3"):
        ui.label("Tastebud").classes("text-h5")
        ui.switch("Dark mode", value=True).bind_value(dark, "value")

    await nicegui_page.create_page()
