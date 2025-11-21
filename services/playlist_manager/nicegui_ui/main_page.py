import uvicorn
from nicegui import ui
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments

from libs.spotify.data_model.playlist import Playlist
from services.playlist_manager.server.app import app, combine_playlists, get_playlists
from services.playlist_manager.server.data_model import CombinePlaylistsRequest

selected_playlists = []


def _update_table(own_playlists_only: bool, table: Table, all_rows: list[dict], user_id: str):
    if own_playlists_only:
        filtered_rows = [row for row in all_rows if row["owner"] == user_id]
    else:
        filtered_rows = all_rows

    table.rows = filtered_rows


async def _combine_playlists(user_id: str, playlists: list[Playlist]):
    response = await combine_playlists(user_id, CombinePlaylistsRequest(playlists=playlists))
    return response.combined_playlist


def get_selected(table):
    return [row for row in table.rows if row.get("_selected")]


def update_selected_playlists(e: GenericEventArguments):
    playlist = Playlist.model_validate(e.args["_playlist_object"])
    if e.args["_selected"]:
        selected_playlists.append(playlist)
    else:
        selected_playlists.remove(playlist)
    print(selected_playlists)


@ui.page("/")
async def page():
    ui.page_title("Playlist Manager")

    dark = ui.dark_mode(True)
    ui.switch("Dark mode", value=True).bind_value(dark, target_name="value")

    user_id = "vissert"
    ui.input("Enter Spotify user name", value=user_id)
    playlists_response = await get_playlists(user_id)
    playlists = playlists_response.playlists

    ui.label("Playlist Manager").style("color: #6E93D6; font-size: 200%; font-weight: 300")
    ui.label(f"All playlists for user {user_id}:")

    ui.checkbox("User-owned only", on_change=lambda e: _update_table(e.value, table, rows, user_id))

    columns = [
        {"name": "idx", "label": "Index", "field": "idx", "required": True, "align": "left", "sortable": True},
        {
            "name": "playlist_name",
            "label": "Playlist Name",
            "field": "playlist_name",
            "required": True,
            "align": "left",
        },
        {"name": "n_tracks", "label": "No. of Tracks", "field": "n_tracks", "sortable": True},
        {"name": "owner", "label": "Owner", "field": "owner", "sortable": True},
        {"name": "combine", "label": "Combine", "field": "combine"},
    ]
    rows = [
        {
            "idx": idx,
            "playlist_name": playlist.name,
            "n_tracks": playlist.n_tracks,
            "owner": playlist.owner_id,
            "_playlist_object": playlist.model_dump(),
        }
        for idx, playlist in enumerate(playlists)
    ]
    table = ui.table(columns=columns, rows=rows, row_key="playlist_name", pagination=10)
    table.add_slot(
        "body",
        r"""
            <q-tr :props="props">
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    
                    <template v-if="col.name !== 'combine'">
                        {{ props.row[col.field] }}
                    </template>
                    
                    <template v-else>
                          <q-checkbox
                            v-model="props.row._selected"
                            size="xs"
                            class="no-padding no-margin"
                            toggle-order="tf"
                            @update:model-value="(val) => $parent.$emit('row_selected_changed', props.row)"
                          />
                    </template>
                </q-td>
            </q-tr>
        """,
    )

    table.on("row_selected_changed", update_selected_playlists)
    ui.button("Combine selected playlists", on_click=lambda: _combine_playlists(user_id, selected_playlists))


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main_page:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
