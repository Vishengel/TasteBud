from typing import Protocol


class NiceGUIPage(Protocol):
    async def create_page(self) -> None: ...
