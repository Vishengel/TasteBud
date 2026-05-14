import asyncio
import datetime

from nicegui import ui

from application.event_scanner.event_sources.event_source_base import EventSourceType
from application.event_scanner.event_sources.event_source_factory import event_source_factory
from application.event_scanner.relevancy.relevancy_score_registry import RelevancyScoreRegistry
from infrastructure.lastfm.relevancy_score import LastFMPeriodOption
from interface.ui.layout import NiceGUIPage


class EventScannerPage(NiceGUIPage):
    def __init__(self):
        self.start_date = datetime.date.today()
        self.loading_events: bool = False
        self.events_loaded: bool = False
        self.relevancy_score_registry = RelevancyScoreRegistry()
        self._event_source_map = event_source_factory(set(EventSourceType))
        self._source_enabled: dict[EventSourceType, bool] = dict.fromkeys(self._event_source_map, True)
        self._source_genre: dict[EventSourceType, str | None] = dict.fromkeys(self._event_source_map)

    async def create_page(self):
        with ui.row().classes("justify-center items-start w-full mt-10"):
            with ui.column().classes("w-2/3 p-6 bg-gray-100 dark:bg-gray-800 rounded-lg shadow-lg gap-4"):
                with ui.row().classes("gap-4 items-center"):
                    ui.date_input("Start date", value=self.start_date.isoformat()).bind_value(self, "start_date")

                    for source_type, source in self._event_source_map.items():
                        label = source_type.value.capitalize()
                        ui.checkbox(label).bind_value(self._source_enabled, source_type)
                        genres = source.get_genres()
                        if genres:
                            ui.select(
                                label=f"{label} genre",
                                options=genres,
                            ).bind_value(self._source_genre, source_type).bind_visibility_from(
                                self._source_enabled, source_type
                            )

                    self.last_fm_checkbox = ui.checkbox("LastFM scoring").bind_value(
                        self.relevancy_score_registry.lastfm_score, "active"
                    )

                    (
                        ui.input("LastFM username")
                        .on("blur", self.relevancy_score_registry.lastfm_score.prepare_top_artists)
                        .on("keydown.enter", self.relevancy_score_registry.lastfm_score.prepare_top_artists)
                        .bind_value(self.relevancy_score_registry.lastfm_score, "username")
                        .bind_visibility_from(self.relevancy_score_registry.lastfm_score, "active")
                    )

                    ui.select(
                        label="Period",
                        options=[p.value for p in LastFMPeriodOption],
                        value=self.relevancy_score_registry.lastfm_score.period,
                    ).bind_visibility_from(self.relevancy_score_registry.lastfm_score, "active")

                    self.spinner = ui.spinner(size="sm", color="red").bind_visibility_from(
                        self.relevancy_score_registry.lastfm_score, "loading_top_artists"
                    )

                with ui.row().classes("items-center gap-2"):
                    self.scan_button = ui.button("Scan for events", on_click=self._scan_events)
                    self.scan_button.bind_enabled_from(self, "block_scan_button", backward=lambda x: not x)
                    self.spinner = ui.spinner("audio", size="sm", color="green").bind_visibility_from(
                        self, "loading_events"
                    )

                columns = [
                    {"name": "hype", "label": "HYPE", "field": "hype", "sortable": True, "align": "left"},
                    {
                        "name": "distance",
                        "label": "Distance (km)",
                        "field": "distance",
                        "sortable": True,
                        "align": "left",
                    },
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
                self.table = (
                    ui.table(columns=columns, rows=[], row_key="playlist_name")
                    .bind_visibility_from(self, "events_loaded")
                    .props("sort-by='hype' sort-descending")
                )

    @property
    def block_scan_button(self):
        return self.loading_events or self.relevancy_score_registry.lastfm_score.loading_top_artists

    async def _scan_events(self):
        self.loading_events = True
        enabled_sources = [
            (source, self._source_genre.get(source_type))
            for source_type, source in self._event_source_map.items()
            if self._source_enabled.get(source_type)
        ]
        results = await asyncio.gather(
            *[source.find_events(start_date=self.start_date, genre=genre) for source, genre in enabled_sources]
        )
        events = [event for result in results for event in result]

        rows = []
        for event in events:
            rows.append(
                {
                    "hype": round(self.relevancy_score_registry.lastfm_score.get_score(event)),
                    "distance": round(self.relevancy_score_registry.distance_score.get_score(event)),
                    "artist": ", ".join(artist.name for artist in event.artists),
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
