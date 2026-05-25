import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

RULE_LABELS = {
    "antivirus_disabled": "Disabled antivirus",
    "disk_encryption_disabled": "Disabled disk encryption",
    "firewall_disabled": "Disabled firewall",
    "last_checkin_older_than_7_days": "Check-in older than 7 days",
    "patch_status_not_updated": "Patch status not updated",
}

STATE_LABELS = {
    "compliant": "Compliant",
    "non_compliant": "Non-compliant",
    "unknown": "Unknown",
}

PATCH_LABELS = {
    "updated": "Updated",
    "pending": "Pending",
    "outdated": "Outdated",
    "unknown": "Unknown",
}


def api_get(path: str) -> dict | list:
    response = requests.get(f"{API_URL}{path}", timeout=10)
    response.raise_for_status()
    return response.json()


def api_post(path: str) -> dict:
    response = requests.post(f"{API_URL}{path}", timeout=10)
    response.raise_for_status()
    return response.json()


def humanize_rule(rule: str) -> str:
    return RULE_LABELS.get(rule, rule.replace("_", " ").capitalize())


def humanize_state(state: str) -> str:
    return STATE_LABELS.get(state, state.replace("_", " ").capitalize())


def humanize_patch_status(status: str) -> str:
    return PATCH_LABELS.get(status, status.replace("_", " ").capitalize())


def humanize_rules(rules: list[str]) -> str:
    if not rules:
        return "None"
    return ", ".join(humanize_rule(rule) for rule in rules)


def render_action_result(result: dict[str, Any]) -> None:
    st.info(result["message"])
    st.caption(f"Status: {result['status']} | Dry run: {result.get('dry_run', True)}")
    if result.get("recommended_actions"):
        st.write("Recommended actions")
        for action in result["recommended_actions"]:
            st.write(f"- {action}")


st.set_page_config(page_title="Endpoint Compliance Dashboard", layout="wide")
st.title("Endpoint Compliance Dashboard")
st.caption("Local demo mode. The backend uses fake Intune-style data and does not call Microsoft Graph.")

try:
    report = api_get("/compliance/report")
    devices = api_get("/devices")
    compliance_devices = api_get("/compliance/devices")
except requests.RequestException as exc:
    st.error(f"Unable to reach backend API at {API_URL}: {exc}")
    st.stop()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total devices", report["total_devices"])
col2.metric("Compliance", f"{report['compliance_percentage']}%")
col3.metric("Compliant", report["compliant_devices"])
col4.metric("Non-compliant", report["non_compliant_devices"])
col5.metric("Unknown", report["unknown_devices"])

device_df = pd.DataFrame(devices)
compliance_df = pd.DataFrame(compliance_devices)
inventory_df = device_df.drop(columns=["compliance_state"], errors="ignore").merge(
    compliance_df[["device_id", "compliance_state", "failed_rules"]],
    left_on="id",
    right_on="device_id",
    how="left",
)
inventory_df["compliance_state_label"] = inventory_df["compliance_state"].map(humanize_state)
inventory_df["patch_status_label"] = inventory_df["patch_status"].map(humanize_patch_status)
inventory_df["failed_rules_label"] = inventory_df["failed_rules"].map(humanize_rules)
compliance_df["compliance_state_label"] = compliance_df["compliance_state"].map(humanize_state)
compliance_df["failed_rules_label"] = compliance_df["failed_rules"].map(humanize_rules)

filter_col1, filter_col2 = st.columns(2)
os_filter = filter_col1.multiselect(
    "OS family",
    sorted(device_df["os_family"].unique()),
    default=sorted(device_df["os_family"].unique()),
)
state_filter = filter_col2.multiselect(
    "Compliance state",
    sorted(compliance_df["compliance_state_label"].unique()),
    default=sorted(compliance_df["compliance_state_label"].unique()),
)

filtered_devices = inventory_df[inventory_df["os_family"].isin(os_filter)]
filtered_compliance = compliance_df[
    (compliance_df["device_id"].isin(filtered_devices["id"]))
    & (compliance_df["compliance_state_label"].isin(state_filter))
]
filtered_devices = filtered_devices[filtered_devices["compliance_state_label"].isin(state_filter)]

top_failed_rules = pd.DataFrame(report["top_failed_rules"])
if not top_failed_rules.empty:
    top_failed_rules["rule_label"] = top_failed_rules["rule"].map(humanize_rule)
    st.subheader("Top Failed Rules")
    st.bar_chart(top_failed_rules.set_index("rule_label")["count"])

st.subheader("Device Inventory")
st.dataframe(
    filtered_devices[
        [
            "id",
            "hostname",
            "assigned_user",
            "os_family",
            "os_version",
            "ip_address",
            "last_checkin",
            "patch_status_label",
            "compliance_state_label",
            "failed_rules_label",
        ]
    ].rename(
        columns={
            "id": "Device ID",
            "hostname": "Hostname",
            "assigned_user": "Assigned user",
            "os_family": "OS family",
            "os_version": "OS version",
            "ip_address": "IP address",
            "last_checkin": "Last check-in",
            "patch_status_label": "Patch status",
            "compliance_state_label": "Compliance state",
            "failed_rules_label": "Failed rules",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Failed Rules")
failed_rows = filtered_compliance[filtered_compliance["failed_rules"].map(len) > 0]
if failed_rows.empty:
    st.success("No failed rules for the selected filters.")
else:
    st.dataframe(
        failed_rows[
            [
                "device_id",
                "hostname",
                "os_family",
                "compliance_state_label",
                "failed_rules_label",
            ]
        ].rename(
            columns={
                "device_id": "Device ID",
                "hostname": "Hostname",
                "os_family": "OS family",
                "compliance_state_label": "Compliance state",
                "failed_rules_label": "Failed rules",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

st.subheader("Sync and Remediation Simulation")
if filtered_devices.empty:
    st.warning("No devices match the selected filters.")
else:
    selected_device = st.selectbox(
        "Device",
        filtered_devices["id"].tolist(),
        format_func=lambda value: (
            f"{value} - {device_df.loc[device_df['id'] == value, 'hostname'].iloc[0]}"
        ),
    )

    action_col1, action_col2 = st.columns(2)
    if action_col1.button("Simulate sync"):
        render_action_result(api_post(f"/devices/{selected_device}/sync"))

    if action_col2.button("Generate remediation"):
        render_action_result(api_post(f"/devices/{selected_device}/remediate"))

if st.button("Refresh data"):
    st.rerun()
