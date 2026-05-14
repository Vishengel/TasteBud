from typing import Protocol

from nicegui import ui


class NiceGUIPage(Protocol):
    async def create_page(self) -> None: ...


async def common_layout(nicegui_page: NiceGUIPage):
    dark = ui.dark_mode(True)
    ui.add_css("""
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus {
            -webkit-box-shadow: 0 0 0px 1000px #f3f4f6 inset !important;
            -webkit-text-fill-color: black !important;
        }
        body.body--dark input:-webkit-autofill,
        body.body--dark input:-webkit-autofill:hover,
        body.body--dark input:-webkit-autofill:focus {
            -webkit-box-shadow: 0 0 0px 1000px #1f2937 inset !important;
            -webkit-text-fill-color: white !important;
        }
        body.body--dark input {
            color: white !important;
        }
    """)

    with ui.header().classes("items-center justify-between bg-gray-800 text-white p-3"):
        ui.label("Tastebud").classes("text-h5")
        ui.switch("Dark mode", value=True).bind_value(dark, "value")

    await nicegui_page.create_page()
