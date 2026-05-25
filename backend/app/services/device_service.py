from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Device
from app.services.compliance_engine import evaluate_device


def _refresh_compliance_state(db: Session, devices: list[Device]) -> None:
    changed = False
    for device in devices:
        state, _ = evaluate_device(device)
        if device.compliance_state != state:
            device.compliance_state = state
            changed = True
    if changed:
        db.commit()


def list_devices(db: Session) -> list[Device]:
    devices = list(db.scalars(select(Device).order_by(Device.hostname)).all())
    _refresh_compliance_state(db, devices)
    return devices


def get_device_or_404(db: Session, device_id: str) -> Device:
    device = db.get(Device, device_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{device_id}' was not found.",
        )
    _refresh_compliance_state(db, [device])
    return device
