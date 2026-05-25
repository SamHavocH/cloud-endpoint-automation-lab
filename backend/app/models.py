from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    hostname: Mapped[str] = mapped_column(String, index=True)
    assigned_user: Mapped[str] = mapped_column(String)
    os_family: Mapped[str] = mapped_column(String, index=True)
    os_version: Mapped[str] = mapped_column(String)
    serial_number: Mapped[str] = mapped_column(String, unique=True, index=True)
    ip_address: Mapped[str] = mapped_column(String)
    last_checkin: Mapped[DateTime] = mapped_column(DateTime)
    encryption_enabled: Mapped[bool] = mapped_column(Boolean)
    antivirus_enabled: Mapped[bool] = mapped_column(Boolean)
    firewall_enabled: Mapped[bool] = mapped_column(Boolean)
    patch_status: Mapped[str] = mapped_column(String)
    compliance_state: Mapped[str] = mapped_column(String, index=True)
    installed_apps: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
