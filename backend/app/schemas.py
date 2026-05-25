from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class OSFamily(StrEnum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MACOS = "macOS"


class PatchStatus(StrEnum):
    UPDATED = "updated"
    PENDING = "pending"
    OUTDATED = "outdated"
    UNKNOWN = "unknown"


class ComplianceState(StrEnum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNKNOWN = "unknown"


class DeviceBase(BaseModel):
    id: str
    hostname: str
    assigned_user: str
    os_family: OSFamily
    os_version: str
    serial_number: str
    ip_address: str
    last_checkin: datetime
    encryption_enabled: bool
    antivirus_enabled: bool
    firewall_enabled: bool
    patch_status: PatchStatus
    compliance_state: ComplianceState
    installed_apps: list[str]
    tags: list[str]


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)


class ComplianceResult(BaseModel):
    device_id: str
    hostname: str
    os_family: OSFamily
    compliance_state: ComplianceState
    failed_rules: list[str]


class FailedRuleSummary(BaseModel):
    rule: str
    count: int


class ComplianceReport(BaseModel):
    generated_at: datetime
    total_devices: int
    compliant_devices: int
    non_compliant_devices: int
    unknown_devices: int
    compliance_percentage: float
    top_failed_rules: list[FailedRuleSummary]


class HealthResponse(BaseModel):
    status: str
    service: str
    demo_mode: bool
    timestamp: datetime


class ActionResponse(BaseModel):
    device_id: str
    status: str
    message: str
    dry_run: bool = True
    timestamp: datetime
    recommended_actions: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
