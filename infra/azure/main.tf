locals {
  name_prefix = lower(replace("${var.project_name}-${var.environment}", "_", "-"))
  common_tags = merge(var.tags, {
    project     = var.project_name
    environment = var.environment
    managed_by  = "terraform"
  })
}

resource "azurerm_resource_group" "main" {
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}

module "storage" {
  source              = "./modules/storage"
  project_name        = var.project_name
  environment         = var.environment
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

module "monitoring" {
  source              = "./modules/monitoring"
  project_name        = var.project_name
  environment         = var.environment
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = local.common_tags
}

module "identity" {
  source       = "./modules/identity"
  project_name = var.project_name
  environment  = var.environment
}
