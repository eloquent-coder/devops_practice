# CI/CD Pipeline - Banking Data Seeder

## Overview

GitHub Actions workflow for building and deploying the banking data seeder using Azure OIDC authentication and Azure Container Registry.

## Pipeline Features

### **GitHub Actions Workflow** (`build-and-push.yml`)
- **Azure OIDC Login**: Secure authentication without long-lived secrets
- **Docker Build**: Container image build with proper context
- **ACR Integration**: Push to Azure Container Registry (dry-run mode for safety)
- **Artifact Upload**: Bundle files published for deployment stages
- **Trigger**: Push to main/develop branches

## OIDC Setup (No Secrets Required)

### Azure Configuration
```bash
# Create App Registration
az ad app create --display-name "banking-seeder-github-oidc"

# Create Service Principal 
az ad sp create --id <app-id>

# Add federated credential for GitHub
az ad app federated-credential create \
  --id <app-id> \
  --parameters @federated-credential.json
```

### GitHub Secrets (Repository Settings)
```
AZURE_CLIENT_ID: <app-id>
AZURE_TENANT_ID: <tenant-id>  
AZURE_SUBSCRIPTION_ID: <subscription-id>
```

## Workflow Execution

### **Automatic Triggers**
- Push to `main` branch → Full build and push
- Push to `develop` branch → Build and artifact upload
- Pull requests → Build validation only

### **Manual Execution**
```bash
# Trigger workflow manually
gh workflow run build-and-push.yml
```

## Security Features

### **Zero Secrets Architecture**
- **OIDC Authentication**: Short-lived tokens replace permanent secrets
- **Workload Identity**: Azure AD integration for Kubernetes
- **Dry-run Mode**: ACR push commented out for safety during development

### **Access Controls**
- **Minimal Permissions**: Service principal with limited ACR and storage access
- **Branch Protection**: Main branch requires PR approval
- **Environment Isolation**: Separate registries for staging/production

## Deployment Flow

1. **Code Push** → GitHub Actions triggered
2. **Build Image** → Docker container created with banking seeder
3. **Publish Artifacts** → Bundle files uploaded for deployment
4. **Deploy to AKS** → (Manual step using published artifacts)

## Local Testing

```bash
# Build locally
docker build -f docker-assets/Dockerfile -t banking-seeder:local .

# Test with Docker Compose
cd docker-assets && docker-compose up
```

This CI/CD approach provides secure, automated building and deployment of the banking data seeder with Azure integration and proper security practices.