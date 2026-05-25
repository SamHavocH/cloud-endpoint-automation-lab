variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
  default     = "cloud-endpoint-automation-lab"

  validation {
    condition     = length(var.project_name) >= 3
    error_message = "project_name must be at least 3 characters."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "environment must be one of: dev, test, prod."
  }
}

variable "location" {
  description = "Azure region for regional resources."
  type        = string
  default     = "eastus"
}

variable "tags" {
  description = "Common resource tags."
  type        = map(string)
  default = {
    workload = "endpoint-automation"
  }
}
