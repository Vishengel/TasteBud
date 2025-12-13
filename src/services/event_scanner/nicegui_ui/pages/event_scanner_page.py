import datetime

from nicegui import ui

from libs.common.nicegui_ui.tastebud_nicegui_layout import NiceGUIPage
from services.event_scanner.server.app import find_events, get_event_source_info
from services.event_scanner.server.data_model import (
    EventSourceOverview,
    EventSourceType,
    FindEventsRequest,
    PodiuminfoSearchParams,
)


class EventScannerPage(NiceGUIPage):
    def __init__(self):
        self.use_podiuminfo: bool = False
        self.start_date = datetime.date.today()
        self.dropdown_value = None
        self.event_sources: dict[EventSourceType, EventSourceOverview] = {}
        self.loading_events: bool = False
        self.events_loaded: bool = False

    async def create_page(self):
        await self._get_event_source_info()
        podiuminfo_input_genres = self.event_sources[EventSourceType.PODIUMINFO].genres

        with ui.row().classes("justify-center items-start w-full mt-10"):
            with ui.column().classes("w-2/3 p-6 bg-gray-100 dark:bg-gray-800 rounded-lg shadow-lg gap-4"):
                with ui.row().classes("gap-4 items-center"):
                    ui.checkbox("Podiuminfo").bind_value(self, "use_podiuminfo")
                    ui.date_input("Start date", value=self.start_date.isoformat()).bind_value(self, "start_date")
                    ui.select(label="Select genre", options=podiuminfo_input_genres).bind_value(self, "dropdown_value")

                with ui.row().classes("items-center gap-2"):
                    self.scan_button = ui.button("Scan for events", on_click=self._scan_podiuminfo_events)
                    self.scan_button.bind_enabled_from(self, "loading_events", backward=lambda x: not x)
                    self.spinner = ui.spinner("audio", size="sm", color="green").bind_visibility_from(
                        self, "loading_events"
                    )

                columns = [
                    {
                        "name": "artist",
                        "label": "Artist",
                        "field": "artist",
                        "sortable": True,
                        "align": "left",
                        "style": "text-wrap: wrap",
                    },
                    {"name": "city", "label": "City", "field": "city", "sortable": True, "align": "left"},
                    {"name": "venue", "label": "Venue", "field": "venue", "sortable": True, "align": "left"},
                    {"name": "date", "label": "Date", "field": "date", "sortable": True, "align": "left"},
                    {"name": "url", "label": "URL", "field": "url", "sortable": True, "align": "left"},
                ]
                self.table = ui.table(columns=columns, rows=[], row_key="playlist_name").bind_visibility_from(
                    self, "events_loaded"
                )

    async def _scan_podiuminfo_events(self):
        self.loading_events = True
        find_events_request = FindEventsRequest(
            podiuminfo_params=PodiuminfoSearchParams(start_date=self.start_date, genre=self.dropdown_value)
        )
        events_response = await find_events(find_events_request)

        rows = []
        for event in events_response.events:
            rows.append(
                {
                    "artist": ", ".join([artist.name for artist in event.artists]),
                    "city": event.venue.location.city,
                    "venue": event.venue.name,
                    "date": event.date,
                    "url": event.url,
                }
            )

        self.table.rows = rows
        self.table.add_slot(
            "body-cell-url",
            """
            <q-td :props="props">
                <a :href="props.value">{{ props.value }}</a>
            </q-td>
        """,
        )
        self.table.update()
        self.loading_events = False
        self.events_loaded = True

    async def _get_event_source_info(self):
        event_info_response = await get_event_source_info()
        self.event_sources = {
            overview.event_source_type: overview for overview in event_info_response.event_source_overviews
        }
