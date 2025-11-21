import uvicorn
from nicegui import ui
from nicegui.elements.table import Table

from services.playlist_manager.server.app import app, get_playlists


def _update_table(own_playlists_only: bool, table: Table, all_rows: list[dict], user_id: str):
    if own_playlists_only:
        filtered_rows = [row for row in all_rows if row["owner"] == user_id]
    else:
        filtered_rows = all_rows

    table.rows = filtered_rows


@ui.page("/")
async def page():
    ui.page_title("Playlist Manager")

    dark = ui.dark_mode(True)
    ui.switch("Dark mode", value=True).bind_value(dark, target_name="value")

    user_id = "vissert"
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
    ]
    rows = [
        {"idx": idx, "playlist_name": playlist.name, "n_tracks": playlist.n_tracks, "owner": playlist.owner_id}
        for idx, playlist in enumerate(playlists)
    ]
    table = ui.table(columns=columns, rows=rows, row_key="playlist_name")


ui.run_with(app)


if __name__ == "__main__":
    uvicorn.run("main_page:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
