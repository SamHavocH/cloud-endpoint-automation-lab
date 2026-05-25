# Compliance Rules

The demo compliance engine marks a device compliant only when all applicable rules pass.

## Common Rules

- Disk encryption must be enabled.
- Firewall must be enabled.
- Patch status must be `updated`.
- Last check-in must be within 7 days.

## Windows Rule

- Antivirus must be enabled for Windows devices.

## Linux Exception

- Antivirus is optional for Linux devices in this demo.
- Linux devices still require disk encryption, firewall, updated patch status, and recent check-in.

## Failed Rule Identifiers

| Rule ID | Meaning |
| --- | --- |
| `disk_encryption_disabled` | Disk encryption is not enabled |
| `firewall_disabled` | Host firewall is not enabled |
| `antivirus_disabled` | Windows antivirus is not enabled |
| `patch_status_not_updated` | Patch status is not `updated` |
| `last_checkin_older_than_7_days` | Device has not checked in within 7 days |
