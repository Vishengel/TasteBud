from collections.abc import Callable

from nicegui import ui
from nicegui.elements.table import Table
from nicegui.events import GenericEventArguments


class PlaylistTable:
    def __init__(self, rows: list[dict], on_select_changed: Callable[[GenericEventArguments], None]):
        self.rows = rows
        self.on_select_changed = on_select_changed

        columns = [
            {"name": "idx", "label": "Index", "field": "idx", "required": True, "align": "left", "sortable": True},
            {
                "name": "playlist_name",
                "label": "Playlist Name",
                "field": "playlist_name",
                "required": True,
                "align": "left",
                "text-wrap": "wrap",
            },
            {"name": "n_tracks", "label": "No. of Tracks", "field": "n_tracks", "sortable": True},
            {"name": "owner", "label": "Owner", "field": "owner", "sortable": True},
            {"name": "combine", "label": "Combine", "field": "combine", "align": "center"},
        ]

        self.table: Table = ui.table(columns=columns, rows=self.rows, row_key="playlist_name")
        self._install_body_slot()
        self.table.on("row_selected_changed", self.on_select_changed)

    def update(self):
        self.table.update()

    def filter_by_owner(self, only_owned: bool, user_id: str):
        if only_owned:
            self.table.rows = [r for r in self.rows if r["owner"] == user_id]
        else:
            self.table.rows = self.rows
        self.table.update()

    def _install_body_slot(self):
        self.table.add_slot(
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
