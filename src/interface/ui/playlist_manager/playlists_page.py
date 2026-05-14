from nicegui import ui
from nicegui.events import GenericEventArguments

from application.playlist_manager.playlist_manager import PlaylistManager
from application.playlist_manager.service import make_playlist_manager
from domain.playlists.models import Playlist
from interface.ui.layout import NiceGUIPage
from interface.ui.playlist_manager.components.playlists_table import PlaylistTable


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


class PlaylistsPage(NiceGUIPage):
    def __init__(self):
        self.user_id: str | None = None
        self.selected: list[Playlist] = []
        self.main_table: PlaylistTable | None = None
        self.combined_playlist_table: PlaylistTable | None = None
        self._playlist_manager: PlaylistManager | None = None

    def _get_manager(self) -> PlaylistManager:
        if self._playlist_manager is None:
            self._playlist_manager = make_playlist_manager()
        return self._playlist_manager

    async def load_playlists(self) -> list[Playlist]:
        assert self.user_id
        try:
            return self._get_manager().get_all_playlists_for_user_id(self.user_id)
        except Exception:
            ui.notify(f'No playlists found for user "{self.user_id}"', type="negative", icon="warning", timeout=3000)
            return []

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
        assert self.user_id
        result = self._get_manager().create_combined_playlist(self.user_id, [pl.id for pl in self.selected])
        self.selected.clear()

        for row in self.main_table.rows:
            row["_selected"] = False
        self.main_table.update()

        self.combined_playlist_table.rows.append(_playlist_to_row(len(self.combined_playlist_table.rows) + 1, result))
        self.combined_playlist_table.update()
        return result

    async def create_page(self):
        with ui.column().classes("w-full p-6 gap-4"):
            ui.label("Playlist Manager").style("color: var(--accent); font-size: 1.5rem; font-weight: 700;")

            with ui.row().classes("items-center gap-4 flex-wrap"):
                (
                    ui.input("Username", placeholder="Enter username")
                    .props("outlined")
                    .on("blur", self.update_playlists)
                    .on("keydown.enter", self.update_playlists)
                    .classes("tb-input")
                )
                ui.checkbox(
                    "User-owned only",
                    on_change=lambda e: self.main_table.filter_by_owner(e.value, self.user_id),
                )
                ui.button("Combine selected", on_click=self.combine).classes("tb-btn")

            showing_playlists_label = ui.label().style("color: var(--muted); font-size: 0.85rem;")

            with ui.row().classes("w-full gap-4").style("flex-wrap: nowrap;"):
                with ui.column().classes("gap-2").style("flex: 2; min-width: 0;"):
                    ui.label("User-managed Playlists").style("color: var(--muted);")
                    self.main_table = PlaylistTable([], self.on_select_changed)
                    self.main_table.table.classes("tb-table h-[65vh] overflow-y-auto w-full")

                with ui.column().classes("gap-2").style("flex: 1; min-width: 0;"):
                    ui.label("Tastebud-managed Playlists").style("color: var(--muted);")
                    self.combined_playlist_table = PlaylistTable([], self.on_select_changed)
                    self.combined_playlist_table.table.classes("tb-table h-[65vh] overflow-y-auto w-full")

            (
                showing_playlists_label.bind_text_from(
                    self, "user_id", lambda user_id: f"Showing playlists for {user_id}"
                ).bind_visibility_from(self.main_table, "has_rows")
            )
