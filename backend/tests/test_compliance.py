from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from app.services.compliance_engine import build_summary, evaluate_device, recommended_actions


@dataclass
class DemoDevice:
    id: str = "test-device"
    hostname: str = "TEST-001"
    os_family: str = "Windows"
    last_checkin: datetime = datetime(2026, 5, 25, tzinfo=UTC)
    encryption_enabled: bool = True
    antivirus_enabled: bool = True
    firewall_enabled: bool = True
    patch_status: str = "updated"


def test_compliant_device() -> None:
    state, failed_rules = evaluate_device(DemoDevice(), now=datetime(2026, 5, 25, tzinfo=UTC))

    assert state == "compliant"
    assert failed_rules == []


def test_non_compliant_device() -> None:
    device = DemoDevice(encryption_enabled=False)

    state, failed_rules = evaluate_device(device, now=datetime(2026, 5, 25, tzinfo=UTC))

    assert state == "non_compliant"
    assert "disk_encryption_disabled" in failed_rules


def test_linux_device_antivirus_exception() -> None:
    device = DemoDevice(os_family="Linux", antivirus_enabled=False)

    state, failed_rules = evaluate_device(device, now=datetime(2026, 5, 25, tzinfo=UTC))

    assert state == "compliant"
    assert "antivirus_disabled" not in failed_rules


def test_outdated_patch_failure() -> None:
    device = DemoDevice(patch_status="outdated")

    state, failed_rules = evaluate_device(device, now=datetime(2026, 5, 25, tzinfo=UTC))

    assert state == "non_compliant"
    assert "patch_status_not_updated" in failed_rules


def test_old_checkin_failure() -> None:
    now = datetime(2026, 5, 25, tzinfo=UTC)
    device = DemoDevice(last_checkin=now - timedelta(days=8))

    state, failed_rules = evaluate_device(device, now=now)

    assert state == "non_compliant"
    assert "last_checkin_older_than_7_days" in failed_rules


def test_checkin_exactly_seven_days_old_is_allowed() -> None:
    now = datetime(2026, 5, 25, tzinfo=UTC)
    device = DemoDevice(last_checkin=now - timedelta(days=7))

    state, failed_rules = evaluate_device(device, now=now)

    assert state == "compliant"
    assert "last_checkin_older_than_7_days" not in failed_rules


def test_multiple_failed_rules_are_returned() -> None:
    device = DemoDevice(
        encryption_enabled=False,
        antivirus_enabled=False,
        firewall_enabled=False,
        patch_status="unknown",
    )

    state, failed_rules = evaluate_device(device, now=datetime(2026, 5, 25, tzinfo=UTC))

    assert state == "non_compliant"
    assert failed_rules == [
        "disk_encryption_disabled",
        "firewall_disabled",
        "antivirus_disabled",
        "patch_status_not_updated",
    ]


def test_compliance_summary_counts_and_failed_rules() -> None:
    now = datetime(2026, 5, 25, tzinfo=UTC)
    devices = [
        DemoDevice(id="ok-1", hostname="OK-1"),
        DemoDevice(id="bad-1", hostname="BAD-1", encryption_enabled=False),
        DemoDevice(id="bad-2", hostname="BAD-2", encryption_enabled=False, firewall_enabled=False),
    ]

    summary = build_summary(devices, now=now)

    assert summary["total_devices"] == 3
    assert summary["compliant_devices"] == 1
    assert summary["non_compliant_devices"] == 2
    assert summary["compliance_percentage"] == 33.33
    assert summary["top_failed_rules"][0] == {"rule": "disk_encryption_disabled", "count": 2}


def test_recommended_actions_are_mapped_from_failed_rules() -> None:
    actions = recommended_actions(["firewall_disabled", "patch_status_not_updated"])

    assert actions == [
        "Enable host firewall using the platform baseline.",
        "Install pending operating system security updates.",
    ]
