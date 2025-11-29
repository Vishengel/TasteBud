from fastapi import HTTPException
from nicegui import ui
from nicegui.events import GenericEventArguments

from src.libs.spotify.data_model.playlist import Playlist
from src.services.playlist_manager.nicegui_ui.components.playlists_table import PlaylistTable
from src.services.playlist_manager.server.app import combine_playlists, get_playlists
from src.services.playlist_manager.server.data_model import CombinePlaylistsRequest


def _playlist_to_row(idx: int, playlist: Playlist):
    return {
        "idx": idx,
        "playlist_name": playlist.name,
        "n_tracks": playlist.n_tracks,
        "owner": playlist.owner_id,
        "_playlist_object": playlist.model_dump(),
        "_selected": False,
    }


def _get_table_rows(playlists: list[Playlist], return_tastebud_playlists: bool = False):
    filtered_playlists = [pl for pl in playlists if pl.generated_by_tastebud == return_tastebud_playlists]
    return [_playlist_to_row(idx, pl) for idx, pl in enumerate(filtered_playlists, start=1)]


class PlaylistsPage:
    def __init__(self):
        self.user_id: str | None = None
        self.selected = []
        self.main_table: PlaylistTable | None = None
        self.combined_playlist_table: PlaylistTable | None = None

    async def load_playlists(self) -> list[Playlist]:
        try:
            response = await get_playlists(self.user_id)
        except HTTPException:
            ui.notify(f'No playlists found for user "{self.user_id}"', type="negative", icon="warning", timeout=3000)
            return []
        return response.playlists

    async def update_playlists(self, e: GenericEventArguments):
        self.user_id = e.sender.value
        if self.user_id:
            playlists = await self.load_playlists()
            self.main_table.set_rows(_get_table_rows(playlists, return_tastebud_playlists=False))
            self.combined_playlist_table.set_rows(_get_table_rows(playlists, return_tastebud_playlists=True))

    def on_select_changed(self, e: GenericEventArguments):
        pl_dict = e.args["_playlist_object"]
        playlist = Playlist.model_validate(pl_dict)

        if e.args["_selected"]:
            self.selected.append(playlist)
        else:
            self.selected.remove(playlist)

    async def combine(self):
        result = await combine_playlists(self.user_id, CombinePlaylistsRequest(playlists=self.selected))
        self.selected.clear()

        for row in self.main_table.rows:
            row["_selected"] = False
        self.main_table.update()

        self.combined_playlist_table.rows.append(
            _playlist_to_row(len(self.combined_playlist_table.rows) + 1, result.combined_playlist)
        )
        self.combined_playlist_table.update()

        return result

    async def create(self):
        dark = ui.dark_mode(True)
        ui.switch("Dark mode", value=True).bind_value(dark, target_name="value")

        with ui.left_drawer():
            ui.label("Actions").classes("text-h6")
            ui.button("Combine selected", on_click=self.combine)

        ui.label("Playlist Manager").classes("text-h2").style("color: #6E93D6")
        (
            ui.input("Username", placeholder="Enter username")
            .on("blur", self.update_playlists)
            .on("keydown.enter", self.update_playlists)
        )
        showing_playlists_label = ui.label()

        ui.checkbox(
            "User-owned only",
            on_change=lambda e: self.main_table.filter_by_owner(e.value, self.user_id),
        )
        with ui.row().classes("w-full h-full no-wrap gap-4"):
            with ui.column().classes("w-2/3 h-[70vh] overflow-hidden"):
                ui.label("User-managed Playlists")
                self.main_table = PlaylistTable([], self.on_select_changed)
                self.main_table.table.classes("h-full overflow-y-auto whitespace-normal break-words")

            with ui.column().classes("w-1/3 h-[70vh] overflow-hidden"):
                ui.label("Tastebud-managed Playlists")
                self.combined_playlist_table = PlaylistTable([], self.on_select_changed)
                self.combined_playlist_table.table.classes("h-full overflow-y-auto whitespace-normal break-words")

        (
            showing_playlists_label.bind_text_from(
                self, "user_id", lambda user_id: f"Showing all playlists for user {user_id}"
            ).bind_visibility_from(self.main_table, "has_rows")
        )
