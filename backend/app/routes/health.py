import os
from datetime import UTC, datetime

from fastapi import APIRouter

from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=os.getenv("APP_NAME", "Cloud Endpoint Automation Lab"),
        demo_mode=os.getenv("DEMO_MODE", "true").lower() == "true",
        timestamp=datetime.now(UTC),
    )
