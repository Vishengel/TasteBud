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
    --bg:         #0f0f0f;
    --surface:    #1a1a2e;
    --border:     #2d2d4e;
    --accent:     #8B5CF6;
    --accent-dim: #6D28D9;
    --text:       #ffffff;
    --muted:      #a0a0a0;
    --accent-hover: rgba(139, 92, 246, 0.08);
}

body {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* autofill fix */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px var(--surface) inset !important;
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
}

/* primary button */
.tb-btn {
    background: var(--accent) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.tb-btn:hover {
    background: var(--accent-dim) !important;
}

/* inputs */
.tb-input .q-field__control {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
.tb-input .q-field__label,
.tb-input input {
    color: var(--text) !important;
}

/* tables */
.tb-table .q-table {
    background: var(--surface) !important;
    color: var(--text) !important;
}
.tb-table thead tr th {
    background: var(--surface) !important;
    color: var(--accent) !important;
    border-bottom: 1px solid var(--border) !important;
}
.tb-table tbody tr:hover td {
    background: var(--accent-hover) !important;
}
"""


async def common_layout(nicegui_page: NiceGUIPage, active_route: str = ""):
    ui.dark_mode(True)
    ui.add_css(CSS_VARS)

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
        ui.html(nav_html)

    await nicegui_page.create_page()
