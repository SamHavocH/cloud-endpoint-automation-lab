resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  sanitized_project = substr(replace(lower(var.project_name), "/[^a-z0-9]/", ""), 0, 16)
  storage_name      = substr("${local.sanitized_project}${var.environment}${random_id.suffix.hex}", 0, 24)
}

resource "azurerm_storage_account" "main" {
  name                            = local.storage_name
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_kind                    = "StorageV2"
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = true
  tags                            = var.tags
}

resource "azurerm_storage_container" "reports" {
  name                  = "compliance-reports"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}
