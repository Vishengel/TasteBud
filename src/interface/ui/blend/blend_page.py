from datetime import datetime

from nicegui import ui

from application.blend.adapter_factory import make_adapter
from application.blend.blend_engine import BlendEngine
from common.ui.layout import NiceGUIPage
from domain.blend.models import BlendConfig, Platform


def _default_playlist_name(user_ids: list[str]) -> str:
    date = datetime.today().strftime("%Y-%m-%d")
    return f"[BLEND] {' + '.join(user_ids)} {date}"


class BlendPage(NiceGUIPage):
    def __init__(self):
        self.initiator_user_id: str = ""
        self.participant_inputs: list[ui.input] = []
        self.playlist_name_input: ui.input | None = None
        self.target_size_slider: ui.slider | None = None
        self.result_label: ui.label | None = None
        self.result_link: ui.link | None = None

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
        self.result_label.set_text(f"Created: {playlist.name} ({playlist.n_tracks} tracks)")
        self.result_link.set_target(playlist.external_url)
        self.result_link.set_text("Open on Spotify")
        self.result_label.set_visibility(True)
        self.result_link.set_visibility(True)

    async def create_page(self):
        ui.label("Blend").classes("text-h2").style("color: #6E93D6")

        with ui.card().classes("w-full max-w-lg"):
            ui.label("Users").classes("text-h6")

            initiator_input = ui.input("Your Spotify user ID", placeholder="e.g. jelle").classes("w-full")
            initiator_input.on("change", lambda e: setattr(self, "initiator_user_id", e.sender.value))

            participant_container = ui.column().classes("w-full gap-2")

            def add_participant():
                with participant_container:
                    inp = ui.input(f"Participant {len(self.participant_inputs) + 1} user ID").classes("w-full")
                    self.participant_inputs.append(inp)

            ui.button("+ Add participant", on_click=add_participant).classes("mt-2")

            ui.separator()
            ui.label("Playlist settings").classes("text-h6")

            self.playlist_name_input = ui.input("Playlist name").classes("w-full")
            ui.label("Target size")
            self.target_size_slider = ui.slider(min=20, max=100, value=50).classes("w-full")
            ui.label().bind_text_from(self.target_size_slider, "value", lambda v: f"{int(v)} tracks")

            ui.button("Generate Blend", on_click=self._run_blend).classes("mt-4 w-full")

        self.result_label = ui.label("").classes("text-h6 mt-4")
        self.result_label.set_visibility(False)
        self.result_link = ui.link("", target="").classes("mt-2")
        self.result_link.set_visibility(False)
