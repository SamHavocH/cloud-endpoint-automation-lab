# Screenshots

This page explains the screenshots used in the README and what each one demonstrates.

## Dashboard Overview

![Endpoint Compliance Dashboard](Endpoint_Compliance_Dashboard.png)

Shows the Streamlit dashboard running locally with fleet-level compliance metrics, operating system filters, compliance-state filters, and the top failed rules chart.

## Filtered Non-Compliant Devices

![Endpoint Compliance Dashboard filtered by non-compliant devices](Endpoint_Compliance_Dashboard_filtrado.png)

Shows the dashboard filtered to non-compliant devices, highlighting how failed compliance rules can be reviewed operationally.

## Remediation Dry Run

![Generate remediation recommendations for a selected device](Generate_remediation_device_based.png)

Shows the dry-run remediation workflow. The backend generates recommended actions without making device changes.

## Device Sync Simulation

![Simulate an Intune-style device sync](Simulate_sync.png)

Shows the simulated Intune-style device sync action and reinforces that the project does not require a real Microsoft Graph or Intune tenant.

## FastAPI Swagger UI

![FastAPI Swagger UI](FastAPI_Swagger.png)

Shows the API surface exposed by the FastAPI backend, including inventory, compliance, sync, and remediation endpoints.

## Compliance Report JSON

![Compliance report JSON response](Compliance_report_JSON.png)

Shows the structured `/compliance/report` response with fleet totals, compliance percentage, and top failed rules.

## GitHub Actions Validation

![GitHub Actions validation workflow](GitHub_Actions.png)

Shows the CI workflow validating backend tests, dashboard syntax, Docker Compose, Terraform, and simulated deployment readiness.
