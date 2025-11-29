from typing import Protocol


class HttpResponse(Protocol):
    status_code: int
    text: str


class SyncHttpClient(Protocol):
    def get(self, url: str) -> HttpResponse | None: ...

    def close(self) -> None: ...


class AsyncHttpClient(Protocol):
    async def get(self, url: str) -> HttpResponse | None: ...

    async def close(self) -> None: ...
