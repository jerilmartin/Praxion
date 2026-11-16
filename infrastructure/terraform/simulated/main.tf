# Praxion – Simulated Cloud Infrastructure
# Terraform configuration for local development / testing (no real AWS account needed)
# Uses localstack or null_resource providers to simulate cloud resources.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    # Use the null provider + local files to simulate resources without cloud credentials.
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# ── Variables ────────────────────────────────────────────────────────────────

variable "environment" {
  default = "simulated"
}

variable "region" {
  default = "us-east-1"
}

# ── Simulated Compute Resource ───────────────────────────────────────────────

resource "null_resource" "web_server" {
  triggers = {
    name        = "web-server-01"
    type        = "compute"
    environment = var.environment
  }

  # Checkov finding: CKV_AWS_8 – no IMDSv2 enforcement (intentional for demo)
}

# ── Simulated Storage Bucket (misconfigured) ─────────────────────────────────

resource "null_resource" "public_storage" {
  triggers = {
    name        = "data-bucket-public"
    type        = "storage"
    public      = "true"      # intentional misconfiguration for scanning demo
    encryption  = "none"      # intentional misconfiguration
  }
}

# ── Simulated IAM Role (overly permissive) ───────────────────────────────────

resource "null_resource" "admin_role" {
  triggers = {
    name        = "app-admin-role"
    type        = "iam"
    policy      = "AdministratorAccess"   # intentional over-privilege for demo
  }
}

# ── Simulated Database ───────────────────────────────────────────────────────

resource "null_resource" "primary_database" {
  triggers = {
    name             = "app-database-01"
    type             = "database"
    publicly_exposed = "false"
    encrypted        = "true"
  }
}

# ── Simulated Network ────────────────────────────────────────────────────────

resource "null_resource" "main_vpc" {
  triggers = {
    name = "main-vpc"
    type = "network"
    cidr = "10.0.0.0/16"
  }
}

# ── Local state output for Praxion discovery agent ───────────────────────────

output "simulated_resources" {
  value = {
    web_server       = null_resource.web_server.triggers
    public_storage   = null_resource.public_storage.triggers
    admin_role       = null_resource.admin_role.triggers
    primary_database = null_resource.primary_database.triggers
    main_vpc         = null_resource.main_vpc.triggers
  }
}
