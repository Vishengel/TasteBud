import datetime

from nicegui import ui

from libs.common.nicegui_ui.tastebud_nicegui_layout import NiceGUIPage
from services.event_scanner.server.app import get_event_source_info
from services.event_scanner.server.data_model import EventSourceOverview, EventSourceType


class EventScannerPage(NiceGUIPage):
    def __init__(self):
        self.use_podiuminfo: bool = False
        self.start_date = datetime.date.today()
        self.dropdown_value = None
        self.event_sources: dict[EventSourceType, EventSourceOverview] = {}

    async def create_page(self):
        await self._get_event_source_info()
        podiuminfo_input_genres = self.event_sources[EventSourceType.PODIUMINFO].genres

        with ui.row().classes("justify-center items-start w-full mt-10"):
            with ui.column().classes("w-1/2 p-6 bg-gray-100 dark:bg-gray-800 rounded-lg shadow-lg gap-4"):
                with ui.row().classes("gap-4 items-center"):
                    ui.checkbox("Podiuminfo").bind_value(self, "use_podiuminfo")
                    ui.date_input("Start date", value=self.start_date.isoformat()).bind_value(self, "start_date")
                    ui.select(label="Select genre", options=podiuminfo_input_genres).bind_value(self, "dropdown_value")

                ui.button("Scan for events", on_click=self.scan_events)

    async def scan_events(self):
        print("Podiuminfo:", self.use_podiuminfo)
        print("Start date:", self.start_date)
        print("Dropdown selection:", self.dropdown_value)
        ui.notify("Scan triggered!")

    async def _get_event_source_info(self):
        event_info_response = await get_event_source_info()
        self.event_sources = {
            overview.event_source_type: overview for overview in event_info_response.event_source_overviews
        }
