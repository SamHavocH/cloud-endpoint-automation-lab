output "storage_account_name" {
  value = azurerm_storage_account.main.name
}

output "compliance_container_name" {
  value = azurerm_storage_container.reports.name
}
