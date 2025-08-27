# Kubernetes Job Spec - Banking Data Seeder

## Overview

This Kubernetes Job spec demonstrates how to safely deploy the banking data seeder in an Azure Kubernetes Service (AKS) environment with proper security, retry logic, and Azure integrations.

## Key Features

### ✅ **Job Execution Safety**
- `restartPolicy: Never` - Fail fast, don't restart on failure
- `backoffLimit: 3` - Retry up to 3 times with exponential backoff
- `ttlSecondsAfterFinished: 86400` - Auto-cleanup after 24 hours

### ✅ **Azure Integration**
- **ACR Image**: Placeholder for Azure Container Registry
- **Workload Identity**: No long-lived secrets via OIDC
- **Key Vault CSI**: Secure secret mounting
- **Premium Storage**: Fast, reliable data persistence

### ✅ **Security & Isolation**
- **Namespace isolation**: `banking-demo` namespace
- **Resource limits**: Prevents resource exhaustion
- **Read-only secrets**: Immutable secret mounting
- **Service account**: Scoped permissions via RBAC

### ✅ **Configuration Management**
- **Environment variables**: Runtime configuration
- **ConfigMap**: Non-sensitive settings
- **PVC**: Persistent data storage
- **DRY_RUN**: Safe testing mode by default

## Usage

### Prerequisites
```bash
# Create namespace
kubectl create namespace banking-demo

# Apply RBAC (not shown - would include Role/RoleBinding)
kubectl apply -f rbac.yaml

# Create Secret Provider Class for Key Vault
kubectl apply -f secret-provider-class.yaml
```

### Deploy the Job
```bash
# Deploy the complete stack
kubectl apply -f banking-data-seeder-job.yaml

# Check job status
kubectl get jobs -n banking-demo

# View logs
kubectl logs -n banking-demo job/banking-data-seeder

# Check generated data
kubectl exec -n banking-demo deployment/banking-api -- \
  ls -la /data/bundle/transactions/
```

### Environment Configuration
```bash
# For production data generation
kubectl patch job banking-data-seeder -n banking-demo -p '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "data-seeder",
          "env": [
            {"name": "DRY_RUN", "value": "false"},
            {"name": "TXN_COUNT", "value": "50"}
          ]
        }]
      }
    }
  }
}'
```

## Retry & Backoff Behavior

### How It Works
1. **First Failure**: Immediate retry
2. **Second Failure**: ~10 second delay
3. **Third Failure**: ~20 second delay  
4. **Final Failure**: Job marked as failed

### Why This Is Safe
- **Idempotent**: Same data generated on retry
- **Deterministic**: Fixed seed ensures consistency
- **Fail Fast**: Validation catches issues early
- **No Side Effects**: DRY_RUN prevents pollution

## Monitoring & Debugging

### Job Status
```bash
# Check overall status
kubectl describe job banking-data-seeder -n banking-demo

# Pod status and events
kubectl get pods -n banking-demo -l job-name=banking-data-seeder

# Detailed pod information
kubectl describe pod -n banking-demo -l job-name=banking-data-seeder
```

### Logs & Troubleshooting
```bash
# Current logs
kubectl logs -n banking-demo -l job-name=banking-data-seeder

# Previous run logs (if pod restarted)
kubectl logs -n banking-demo -l job-name=banking-data-seeder --previous

# Events for debugging
kubectl get events -n banking-demo --sort-by='.lastTimestamp'
```

## Production Considerations

### Security
- Replace `CLIENT_ID_PLACEHOLDER` with actual Azure Workload Identity client ID
- Configure proper RBAC with minimal required permissions
- Use Azure Key Vault for sensitive configuration
- Enable Pod Security Standards/Pod Security Policies

### Scalability
- Consider using CronJob for periodic data refresh
- Implement data validation webhooks for quality assurance
- Add monitoring/alerting for job success/failure rates
- Use Init Containers for dependency checks

### Data Management
- Implement backup strategy for generated data
- Consider data retention policies
- Add data validation post-generation
- Implement rollback procedures for bad data

## Helm Values Fragment

For Helm-based deployments:

```yaml
# values.yaml
job:
  image:
    repository: myregistry.azurecr.io/banking-data-seeder
    tag: latest
  
  env:
    dryRun: true
    txnCount: 15
    txnWindowDays: 60
  
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 512Mi
      cpu: 500m

azure:
  workloadIdentity:
    clientId: "your-client-id"
  keyVault:
    name: "your-keyvault"
```
