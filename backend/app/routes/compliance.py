from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ComplianceReport, ComplianceResult
from app.services.compliance_engine import build_summary, evaluate_devices
from app.services.device_service import list_devices

router = APIRouter(prefix="/compliance", tags=["compliance"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/report", response_model=ComplianceReport)
def compliance_report(db: DbSession) -> dict[str, object]:
    return build_summary(list_devices(db))


@router.get("/devices", response_model=list[ComplianceResult])
def compliance_devices(db: DbSession) -> list[dict[str, object]]:
    return evaluate_devices(list_devices(db))
