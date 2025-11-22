from nicegui import ui
from nicegui.events import GenericEventArguments

from libs.spotify.data_model.playlist import Playlist
from services.playlist_manager.nicegui_ui.components.playlists_table import PlaylistTable
from services.playlist_manager.server.app import combine_playlists, get_playlists
from services.playlist_manager.server.data_model import CombinePlaylistsRequest


class PlaylistsPage:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.selected = []
        self.all_rows = []
        self.table: PlaylistTable | None = None

    async def load_playlists(self):
        response = await get_playlists(self.user_id)
        self.all_rows = [
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
        await self.load_playlists()

        dark = ui.dark_mode(True)
        ui.switch("Dark mode", value=True).bind_value(dark, target_name="value")

        ui.label("Playlist Manager").classes("text-h4").style("color: #6E93D6; font-size: 200%; font-weight: 300")
        ui.label(f"All playlists for user {self.user_id}")

        ui.checkbox(
            "User-owned only",
            on_change=lambda e: self.table.filter_by_owner(e.value, self.user_id),
        )

        self.table = PlaylistTable(self.all_rows, self.on_select_changed)

        ui.button("Combine selected", on_click=self.combine)
