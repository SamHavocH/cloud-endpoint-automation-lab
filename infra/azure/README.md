# Azure Terraform Foundation

This Terraform configuration creates a low-cost Azure foundation for the endpoint automation lab.

It provisions:

- Resource group
- Storage account and blob container for compliance reports
- Log Analytics Workspace
- Application Insights
- Entra ID application registration
- Service principal

No AKS, virtual machines, or other expensive compute resources are created by default.

## Layout

```text
main.tf                 Root orchestration, naming, tags, and module wiring
modules/storage/        Storage account and compliance reports container
modules/monitoring/     Log Analytics Workspace and Application Insights
modules/identity/       Entra ID app registration and service principal
```

## Usage

```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

Environment-specific examples are available under `environments/`:

```bash
terraform plan -var-file=environments/development.tfvars
terraform plan -var-file=environments/production.tfvars
```

## Notes

- The storage account is private by default and intended for generated compliance reports.
- Application Insights is connected to Log Analytics for a modern workspace-based setup.
- The Entra application is a placeholder for a future Microsoft Graph integration.
