locals {
  display_name = "${var.project_name}-${var.environment}-graph-demo"
}

resource "azuread_application" "main" {
  display_name = local.display_name
}

resource "azuread_service_principal" "main" {
  client_id = azuread_application.main.client_id
}
