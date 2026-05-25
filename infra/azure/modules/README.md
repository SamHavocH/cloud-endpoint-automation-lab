# Terraform Modules

The modules are intentionally small and grouped by operational concern.

| Module | Purpose |
| --- | --- |
| `storage` | Compliance report storage account and private blob container |
| `monitoring` | Log Analytics Workspace and workspace-based Application Insights |
| `identity` | Entra ID application registration and service principal |

This layout is enough to show modular Terraform practice without adding remote-state orchestration, environment wrappers, or a private module registry.
