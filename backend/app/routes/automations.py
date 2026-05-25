from fastapi import APIRouter

router = APIRouter(prefix="/automations", tags=["automations"])


@router.get("/catalog")
def automation_catalog() -> list[dict[str, str]]:
    return [
        {
            "name": "sync_device",
            "description": "Queue a demo Intune-style device sync request.",
        },
        {
            "name": "remediate_device",
            "description": "Generate remediation recommendations from failed compliance rules.",
        },
    ]
