output "resource_group_name" {
  value = azurerm_resource_group.main.name
}

output "storage_account_name" {
  value = module.storage.storage_account_name
}

output "compliance_container_name" {
  value = module.storage.compliance_container_name
}

output "application_insights_connection_string" {
  value     = module.monitoring.application_insights_connection_string
  sensitive = true
}

output "entra_application_client_id" {
  value = module.identity.entra_application_client_id
}
