from collections import Counter
from datetime import UTC, datetime, timedelta
from typing import Protocol, TypedDict

from app.schemas import ComplianceState

MAX_CHECKIN_AGE_DAYS = 7


class ComplianceDevice(Protocol):
    id: str
    hostname: str
    os_family: str
    last_checkin: datetime
    encryption_enabled: bool
    antivirus_enabled: bool
    firewall_enabled: bool
    patch_status: str


class ComplianceEvaluation(TypedDict):
    device_id: str
    hostname: str
    os_family: str
    compliance_state: str
    failed_rules: list[str]


def _as_aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def evaluate_device(device: ComplianceDevice, now: datetime | None = None) -> tuple[str, list[str]]:
    """Evaluate one device against demo compliance policy rules."""
    current_time = _as_aware(now or datetime.now(UTC))
    last_checkin = _as_aware(device.last_checkin)
    failed_rules: list[str] = []

    if not device.encryption_enabled:
        failed_rules.append("disk_encryption_disabled")

    if not device.firewall_enabled:
        failed_rules.append("firewall_disabled")

    if device.os_family.lower() == "windows" and not device.antivirus_enabled:
        failed_rules.append("antivirus_disabled")

    if device.patch_status != "updated":
        failed_rules.append("patch_status_not_updated")

    if current_time - last_checkin > timedelta(days=MAX_CHECKIN_AGE_DAYS):
        failed_rules.append("last_checkin_older_than_7_days")

    state = ComplianceState.COMPLIANT if not failed_rules else ComplianceState.NON_COMPLIANT
    return state.value, failed_rules


def evaluate_devices(
    devices: list[ComplianceDevice], now: datetime | None = None
) -> list[ComplianceEvaluation]:
    results: list[ComplianceEvaluation] = []
    for device in devices:
        state, failed_rules = evaluate_device(device, now=now)
        results.append(
            {
                "device_id": device.id,
                "hostname": device.hostname,
                "os_family": device.os_family,
                "compliance_state": state,
                "failed_rules": failed_rules,
            }
        )
    return results


def build_summary(
    devices: list[ComplianceDevice], now: datetime | None = None
) -> dict[str, object]:
    generated_at = _as_aware(now or datetime.now(UTC))
    results = evaluate_devices(devices, now=generated_at)
    total = len(results)
    compliant = sum(
        1 for item in results if item["compliance_state"] == ComplianceState.COMPLIANT.value
    )
    non_compliant = sum(
        1 for item in results if item["compliance_state"] == ComplianceState.NON_COMPLIANT.value
    )
    unknown = total - compliant - non_compliant
    percentage = round((compliant / total) * 100, 2) if total else 0.0

    failures = Counter(rule for item in results for rule in item["failed_rules"])

    return {
        "generated_at": generated_at,
        "total_devices": total,
        "compliant_devices": compliant,
        "non_compliant_devices": non_compliant,
        "unknown_devices": unknown,
        "compliance_percentage": percentage,
        "top_failed_rules": [
            {"rule": rule, "count": count} for rule, count in failures.most_common(5)
        ],
    }


def recommended_actions(failed_rules: list[str]) -> list[str]:
    action_map = {
        "disk_encryption_disabled": "Enable disk encryption and escrow recovery keys.",
        "firewall_disabled": "Enable host firewall using the platform baseline.",
        "antivirus_disabled": "Verify Microsoft Defender or approved antivirus is active.",
        "patch_status_not_updated": "Install pending operating system security updates.",
        "last_checkin_older_than_7_days": "Investigate stale check-in and trigger device sync.",
    }
    return [action_map[rule] for rule in failed_rules if rule in action_map]
