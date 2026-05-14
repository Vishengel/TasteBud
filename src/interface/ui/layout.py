from typing import Protocol

from nicegui import ui


class NiceGUIPage(Protocol):
    async def create_page(self) -> None: ...


NAV_LINKS = [
    ("/event-scanner", "Events"),
    ("/playlist-manager", "Playlists"),
    ("/blend", "Blend"),
]

CSS_VARS = """
:root {
    --bg:           #070b18;
    --surface:      #0d1630;
    --border:       #16213a;
    --accent:       #818CF8;
    --accent-dim:   #6366F1;
    --text:         #e8eaf6;
    --muted:        #6878a0;
    --accent-hover: rgba(129, 140, 248, 0.08);

    /* override Quasar's primary so buttons/focus rings use our accent */
    --q-primary: #818CF8;
}

body {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* autofill fix */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px var(--bg) inset !important;
    -webkit-text-fill-color: var(--text) !important;
}

/* nav links */
.tb-nav a {
    color: var(--muted);
    text-decoration: none;
    padding-bottom: 2px;
    font-size: 0.95rem;
    transition: color 0.15s;
}
.tb-nav a:hover {
    color: var(--text);
}
.tb-nav a.active {
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
}

/* cards */
.tb-card {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
}

/* primary button — target the inner Quasar element */
.tb-btn.q-btn {
    background: var(--accent) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.tb-btn.q-btn:hover {
    background: var(--accent-dim) !important;
}
.tb-btn.q-btn .q-focus-helper {
    display: none !important;
}
.tb-btn.q-btn .q-btn__content {
    color: var(--text) !important;
}
/* catch Quasar's bg-primary utility class used internally */
.bg-primary { background: var(--accent) !important; }
.text-primary { color: var(--accent) !important; }

/* inputs — outlined variant */
.tb-input .q-field__control {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.tb-input.q-field--outlined .q-field__control:before {
    border-color: var(--border) !important;
    border-radius: 8px !important;
}
.tb-input.q-field--outlined .q-field__control:hover:before {
    border-color: var(--accent) !important;
}
.tb-input.q-field--outlined.q-field--focused .q-field__control:after {
    border-color: var(--accent) !important;
    border-radius: 8px !important;
}
.tb-input .q-field__label {
    color: var(--muted) !important;
}
.tb-input.q-field--float .q-field__label {
    color: var(--accent) !important;
}
.tb-input input,
.tb-input textarea {
    color: var(--text) !important;
}

/* selects */
.tb-select .q-field__control {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 8px !important;
}
.tb-select.q-field--outlined .q-field__control:before {
    border-color: var(--border) !important;
    border-radius: 8px !important;
}
.tb-select.q-field--outlined .q-field__control:hover:before {
    border-color: var(--accent) !important;
}
.tb-select.q-field--outlined.q-field--focused .q-field__control:after {
    border-color: var(--accent) !important;
    border-radius: 8px !important;
}
.tb-select .q-field__label {
    color: var(--muted) !important;
}
.tb-select.q-field--float .q-field__label {
    color: var(--accent) !important;
}
.tb-select .q-field__native,
.tb-select .q-field__input {
    color: var(--text) !important;
}

/* dropdown menu */
.q-menu {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.q-item:hover {
    background: var(--accent-hover) !important;
}
.q-item__label {
    color: var(--text) !important;
}

/* tables */
.tb-table {
    width: 100% !important;
}
.tb-table .q-table {
    background: var(--surface) !important;
    color: var(--text) !important;
}
.tb-table thead tr th {
    background: var(--surface) !important;
    color: var(--accent) !important;
    border-bottom: 1px solid var(--border) !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
}
.tb-table tbody tr td {
    border-bottom: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.tb-table tbody tr:hover td {
    background: var(--accent-hover) !important;
}
"""


async def common_layout(nicegui_page: NiceGUIPage, active_route: str = ""):
    ui.dark_mode(True)
    ui.add_css(CSS_VARS)
    ui.add_body_html(
        '<script>document.addEventListener("DOMContentLoaded",()=>{'
        'if(window.Quasar){Quasar.setCssVar("primary","#818CF8");}'
        "});</script>"
    )

    with (
        ui.header()
        .style("background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 1.5rem;")
        .classes("items-center justify-between")
    ):
        ui.link("TasteBud", "/").style(
            "color: var(--accent); font-size: 1.25rem; font-weight: 700; text-decoration: none;"
        )

        # nav links rendered as raw HTML so CSS classes apply cleanly
        nav_html = '<div class="tb-nav" style="display:flex;gap:2rem;">'
        for route, label in NAV_LINKS:
            active_class = "active" if route == active_route else ""
            nav_html += f'<a href="{route}" class="{active_class}">{label}</a>'
        nav_html += "</div>"
        ui.html(nav_html, sanitize=False)

    await nicegui_page.create_page()
