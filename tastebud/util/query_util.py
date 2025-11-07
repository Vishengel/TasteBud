import httpx


def httpx_get_request(url: str, params: dict) -> dict | None:
    try:
        response = httpx.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except httpx.RequestError as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        return None

    return data
