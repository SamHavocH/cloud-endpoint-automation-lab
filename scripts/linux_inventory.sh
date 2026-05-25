#!/usr/bin/env bash
set -euo pipefail

hostname_value="$(hostname)"
current_user="$(id -un)"
timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
os_version="unknown"
ip_address="unknown"
firewall_status="unknown"
encryption_status="unknown"

if [[ -r /etc/os-release ]]; then
  os_version="$(. /etc/os-release && echo "${PRETTY_NAME:-unknown}")"
fi

if command -v hostname >/dev/null 2>&1; then
  ip_address="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi

if command -v ufw >/dev/null 2>&1; then
  firewall_status="$(ufw status 2>/dev/null | head -n 1 | awk -F': ' '{print $2}')"
elif command -v firewall-cmd >/dev/null 2>&1; then
  firewall_status="$(firewall-cmd --state 2>/dev/null || true)"
fi

if command -v lsblk >/dev/null 2>&1; then
  if lsblk -o TYPE | grep -q "crypt"; then
    encryption_status="enabled"
  else
    encryption_status="not_detected"
  fi
fi

packages=""
if command -v dpkg-query >/dev/null 2>&1; then
  packages="$(dpkg-query -W -f='${binary:Package}\n' 2>/dev/null | head -n 10)"
elif command -v rpm >/dev/null 2>&1; then
  packages="$(rpm -qa 2>/dev/null | head -n 10)"
fi

export INVENTORY_HOSTNAME="$hostname_value"
export INVENTORY_OS_VERSION="$os_version"
export INVENTORY_CURRENT_USER="$current_user"
export INVENTORY_IP_ADDRESS="$ip_address"
export INVENTORY_FIREWALL_STATUS="$firewall_status"
export INVENTORY_ENCRYPTION_STATUS="$encryption_status"
export INVENTORY_TIMESTAMP="$timestamp"
export INVENTORY_PACKAGES="$packages"

python3 - <<'PY'
import json
import os

packages = [item for item in os.getenv("INVENTORY_PACKAGES", "").splitlines() if item]
print(json.dumps({
    "hostname": os.getenv("INVENTORY_HOSTNAME", "unknown"),
    "os_family": "Linux",
    "os_version": os.getenv("INVENTORY_OS_VERSION", "unknown"),
    "current_user": os.getenv("INVENTORY_CURRENT_USER", "unknown"),
    "ip_address": os.getenv("INVENTORY_IP_ADDRESS", "unknown"),
    "firewall_status": os.getenv("INVENTORY_FIREWALL_STATUS", "unknown"),
    "disk_encryption_status": os.getenv("INVENTORY_ENCRYPTION_STATUS", "unknown"),
    "installed_packages_sample": packages,
    "timestamp": os.getenv("INVENTORY_TIMESTAMP", "unknown"),
}, indent=2))
PY
