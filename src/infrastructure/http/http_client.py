from typing import Any, Protocol


class HttpResponse(Protocol):
    status_code: int
    text: str

    def json(self, **kwargs: Any) -> Any: ...


class SyncHttpClient(Protocol):
    def get(
        self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None
    ) -> HttpResponse | None: ...

    def close(self) -> None: ...


class AsyncHttpClient(Protocol):
    async def get(
        self, url: str, params: dict | None = None, headers: dict | None = None, cookies: dict | None = None
    ) -> HttpResponse | None: ...

    async def close(self) -> None: ...
