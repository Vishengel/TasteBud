from fastapi import HTTPException
from nicegui import ui
from nicegui.events import GenericEventArguments

from libs.spotify.data_model.playlist import Playlist
from services.playlist_manager.nicegui_ui.components.playlists_table import PlaylistTable
from services.playlist_manager.server.app import combine_playlists, get_playlists
from services.playlist_manager.server.data_model import CombinePlaylistsRequest


class PlaylistsPage:
    def __init__(self):
        self.user_id: str | None = None
        self.selected = []
        self.table: PlaylistTable | None = None

    async def load_playlists(self) -> list[dict]:
        try:
            response = await get_playlists(self.user_id)
        except HTTPException:
            ui.notify(f'No playlists found for user "{self.user_id}"', type="negative", icon="warning", timeout=3000)
            return []
        return [
            {
                "idx": idx,
                "playlist_name": pl.name,
                "n_tracks": pl.n_tracks,
                "owner": pl.owner_id,
                "_playlist_object": pl.model_dump(),
                "_selected": False,
            }
            for idx, pl in enumerate(response.playlists)
        ]

    async def update_playlists(self, e: GenericEventArguments):
        self.user_id = e.sender.value
        if self.user_id:
            rows = await self.load_playlists()
            self.table.set_rows(rows)

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

        for row in self.table.rows:
            row["_selected"] = False
        self.table.update()

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
            on_change=lambda e: self.table.filter_by_owner(e.value, self.user_id),
        )

        self.table = PlaylistTable([], self.on_select_changed)
        (
            showing_playlists_label.bind_text_from(
                self, "user_id", lambda user_id: f"Showing all playlists for user {user_id}"
            ).bind_visibility_from(self.table, "has_rows")
        )
