from fastapi import APIRouter
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    message: str = Field("This is a static response indicating the server is responsive.")


health_router = APIRouter()


@health_router.get("/health")
def health_check() -> HealthResponse:
    return HealthResponse()
