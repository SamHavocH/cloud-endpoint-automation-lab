from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ActionResponse, DeviceRead
from app.services.automation_service import AutomationService
from app.services.device_service import get_device_or_404, list_devices

router = APIRouter(prefix="/devices", tags=["devices"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[DeviceRead])
def get_devices(db: DbSession) -> list[DeviceRead]:
    return list_devices(db)


@router.get("/{device_id}", response_model=DeviceRead)
def get_device(device_id: str, db: DbSession) -> DeviceRead:
    return get_device_or_404(db, device_id)


@router.post("/{device_id}/sync", response_model=ActionResponse)
def sync_device(device_id: str, db: DbSession) -> dict[str, object]:
    device = get_device_or_404(db, device_id)
    return AutomationService().sync_device(device)


@router.post("/{device_id}/remediate", response_model=ActionResponse)
def remediate_device(device_id: str, db: DbSession) -> dict[str, object]:
    device = get_device_or_404(db, device_id)
    return AutomationService().remediate_device(device)
