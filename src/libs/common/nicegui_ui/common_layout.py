from nicegui import ui

from libs.common.nicegui_ui.tastebud_nicegui_layout import NiceGUIPage


async def common_layout(nicegui_page: NiceGUIPage):
    """Apply shared UI (drawer, header, theme) and inject page content."""
    dark = ui.dark_mode(True)

    with ui.header().classes("items-center justify-between bg-gray-800 text-white p-3"):
        ui.label("Tastebud").classes("text-h5")
        ui.switch("Dark mode", value=True).bind_value(dark, "value")

    with ui.column().classes("p-6"):
        await nicegui_page.create_page()
