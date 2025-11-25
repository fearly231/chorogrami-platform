# 1. Providers Configuration
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"          
    storage_account_name = "chorogramitfstate"     
    container_name       = "tfstate"          
    key                  = "prod.terraform.tfstate" 
  }
}

provider "azurerm" {
  features {}
}

# 2. Resorce group
resource "azurerm_resource_group" "rg" {
  name     = "devops-final-rg"
  location = "Poland Central"
}

# 3. Random string generator
resource "random_string" "acr_suffix" {
  length  = 6
  special = false
  upper   = false
}

# 4. Creating Azure Container Registry (ACR)
resource "azurerm_container_registry" "acr" {
  name                = "acr${random_string.acr_suffix.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# 5. Log Analytics 
resource "azurerm_log_analytics_workspace" "logs" {
  name                = "devops-logs-ws"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# 6.  Container Apps Enviroment
resource "azurerm_container_app_environment" "env" {
  name                       = "devops-aca-env"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.logs.id
}

# 7.  BACKEND App
resource "azurerm_container_app" "backend" {
  name                         = "backend-app"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "backend"
      image = "${azurerm_container_registry.acr.login_server}/backend:latest"
      cpu    = 0.25
      memory = "0.5Gi"
      
      env {
        name  = "WEBSITES_PORT"
        value = "8000"
      }
    }
    min_replicas = 0
    max_replicas = 1
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 8000
    transport                  = "auto"
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }
  
  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }
}

# 8.  FRONTEND App
resource "azurerm_container_app" "frontend" {
  name                         = "frontend-app"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = "frontend"
      image = "${azurerm_container_registry.acr.login_server}/frontend:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name  = "BACKEND_URL"
        value = "https://${azurerm_container_app.backend.latest_revision_fqdn}"
      }
    }
    min_replicas = 0
    max_replicas = 1
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 8501
    transport                  = "auto"
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = azurerm_container_registry.acr.login_server
    username             = azurerm_container_registry.acr.admin_username
    password_secret_name = "acr-password"
  }
  
  secret {
    name  = "acr-password"
    value = azurerm_container_registry.acr.admin_password
  }
}

# --- OUTPUTS ---


output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "acr_admin_username" {
  value = azurerm_container_registry.acr.admin_username
}

output "acr_admin_password" {
  value     = azurerm_container_registry.acr.admin_password
  sensitive = true
}

output "backend_url" {
  value = "https://${azurerm_container_app.backend.latest_revision_fqdn}/docs"
}

output "frontend_url" {
  value = "https://${azurerm_container_app.frontend.latest_revision_fqdn}"
}
