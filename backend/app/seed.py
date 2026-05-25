from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models import Device
from app.services.compliance_engine import evaluate_device
from app.services.graph_client import GraphClient


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def seed_devices(db: Session) -> None:
    existing_count = len(db.scalars(select(Device.id)).all())
    if existing_count:
        return

    for item in GraphClient().list_managed_devices():
        item["last_checkin"] = datetime.fromisoformat(item["last_checkin"])
        device = Device(**item)
        device.compliance_state, _ = evaluate_device(device)
        db.add(device)
    db.commit()
