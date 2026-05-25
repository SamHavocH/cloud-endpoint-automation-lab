variable "project_name" {
  description = "Project name used for naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
}

variable "resource_group_name" {
  description = "Resource group where storage resources are created."
  type        = string
}

variable "tags" {
  description = "Tags applied to storage resources."
  type        = map(string)
}
