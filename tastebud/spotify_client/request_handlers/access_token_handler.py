import requests
from pydantic import BaseModel

TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"


class AccessTokenRequest(BaseModel):
    grant_type: str
    client_id: str
    client_secret: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


def get_access_token(client_id: str, client_secret: str) -> AccessTokenResponse:
    request = AccessTokenRequest(grant_type="client_credentials", client_id=client_id, client_secret=client_secret)
    response = requests.post(url=TOKEN_ENDPOINT, data=request.model_dump())
    return AccessTokenResponse(**response.json())
