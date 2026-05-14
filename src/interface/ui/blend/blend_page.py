from datetime import datetime

from nicegui import ui

from application.blend.adapter_factory import make_adapter
from application.blend.blend_engine import BlendEngine
from domain.blend.models import BlendConfig, Platform
from interface.ui.layout import NiceGUIPage


def _default_playlist_name(user_ids: list[str]) -> str:
    date = datetime.today().strftime("%Y-%m-%d")
    return f"[BLEND] {' + '.join(user_ids)} {date}"


class BlendPage(NiceGUIPage):
    def __init__(self):
        self.initiator_user_id: str = ""
        self.participant_inputs: list[ui.input] = []
        self.playlist_name_input: ui.input | None = None
        self.target_size_slider: ui.slider | None = None
        self.result_card: ui.card | None = None

    def _get_all_user_ids(self) -> list[str]:
        participants = [inp.value for inp in self.participant_inputs if inp.value.strip()]
        return [self.initiator_user_id, *participants]

    async def _run_blend(self):
        all_user_ids = self._get_all_user_ids()
        if len(all_user_ids) < 2:
            ui.notify("Need at least 2 users", type="negative")
            return

        playlist_name = self.playlist_name_input.value or _default_playlist_name(all_user_ids)
        target_size = int(self.target_size_slider.value)
        config = BlendConfig(playlist_name=playlist_name, target_size=target_size)

        try:
            adapters = [make_adapter(uid, Platform.SPOTIFY) for uid in all_user_ids]
            engine = BlendEngine(adapters)
            tracks = engine.create_blend(all_user_ids, config)
            playlist = adapters[0].create_playlist(
                user_id=all_user_ids[0],
                name=config.playlist_name,
                track_uris=[t.uri for t in tracks],
            )
        except Exception as exc:
            ui.notify(f"Blend failed: {exc}", type="negative")
            return

        result_card = self.result_card
        if result_card is None:
            return
        result_card.clear()
        with result_card:
            ui.label(playlist.name).style("color: var(--text); font-size: 1.1rem; font-weight: 600;")
            ui.label(f"{playlist.n_tracks} tracks").style("color: var(--muted);")
            ui.link("Open on Spotify", playlist.external_url).style("color: var(--accent); text-decoration: underline;")
        result_card.set_visibility(True)

    async def create_page(self):
        with ui.column().classes("items-center w-full mt-10 gap-6"):
            with ui.card().classes("tb-card w-full max-w-lg p-6 gap-4"):
                ui.label("Blend").style("color: var(--accent); font-size: 1.5rem; font-weight: 700;")

                ui.label("Users").style("color: var(--muted); font-size: 0.85rem; text-transform: uppercase;")

                initiator_input = ui.input("Your Spotify user ID", placeholder="e.g. jelle").classes("tb-input w-full")
                initiator_input.on("change", lambda e: setattr(self, "initiator_user_id", e.sender.value))

                participant_container = ui.column().classes("w-full gap-2")

                def add_participant():
                    with participant_container:
                        inp = ui.input(f"Participant {len(self.participant_inputs) + 1} user ID").classes(
                            "tb-input w-full"
                        )
                        self.participant_inputs.append(inp)

                ui.button("+ Add participant", on_click=add_participant).props("flat").style("color: var(--accent);")

                ui.separator().style("border-color: var(--border);")

                ui.label("Playlist settings").style(
                    "color: var(--muted); font-size: 0.85rem; text-transform: uppercase;"
                )

                self.playlist_name_input = ui.input("Playlist name").classes("tb-input w-full")

                with ui.column().classes("w-full gap-1"):
                    ui.label("Target size").style("color: var(--muted); font-size: 0.85rem;")
                    self.target_size_slider = (
                        ui.slider(min=20, max=100, value=50).classes("w-full").style("accent-color: var(--accent);")
                    )
                    ui.label().bind_text_from(self.target_size_slider, "value", lambda v: f"{int(v)} tracks").style(
                        "color: var(--muted); font-size: 0.8rem;"
                    )

                ui.button("Generate Blend", on_click=self._run_blend).classes("tb-btn w-full mt-2")

            self.result_card = ui.card().classes("tb-card w-full max-w-lg p-6 gap-2")
            self.result_card.set_visibility(False)
