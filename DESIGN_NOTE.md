# Banking Demo Data Initializer - Design Note

**Project**: Synthetic-Data Initializer for Banking Demo Environment  
**Implementation**: Kubernetes Job with Azure Integration  
**Author**: Usman Ashraf  

## Executive Summary

This design implements a deterministic banking data seeder for demo environments using Kubernetes Jobs with Azure integration. The solution focuses on deterministic data generation, schema validation, and safe deployment practices.

## Data Model Architecture

### Three-Tier Organization

The data is organized into three logical tiers:

- **Org Tier** (`bundle/org/`): User identity data (2 users with basic profile information)
- **Products/Access Tier** (`bundle/products/`, `bundle/access/`): Financial accounts (3 accounts: CURRENT, SAVINGS, LOAN) and payment cards (2 DEBIT, 1 CREDIT)  
- **Facts Tier** (`bundle/transactions/`): Transaction history (configurable count, default 8 transactions spanning 5-85 days)

**Rationale**: Separating identity from products from behavioral data makes the structure easier to understand and maintain during demo scenarios.

## Determinism & Idempotency Strategy

### Fixed Seed Approach
- **Seed Value**: 42 (hardcoded for consistent results)
- **ID Generation**: Prefixed random integers (`txn-` + 12-digit number)
- **Benefit**: Same input parameters produce identical output every time

### Validation Strategy
- **Account Validation**: Checks `accounts.json` exists and contains properly formatted account IDs
- **Schema Validation**: Pandera validation ensures ID formats, amount ranges, and valid categories
- **Input Validation**: Count range (1-50) and environment parameter validation

## Initializer Flow

1. **Validate Inputs**: Check count range and environment variables
2. **Validate References**: Ensure account file exists and contains valid account IDs
3. **Generate Data**: Create deterministic transactions using seeded random values  
4. **Validate Output**: Apply Pandera schema validation to generated transactions
5. **Write Files**: Save JSON files (or skip in DRY_RUN mode)
6. **Report Status**: Exit with appropriate code for Kubernetes Job handling

### Current Implementation
- **Production Mode**: Generates and saves transaction files
- **DRY_RUN Mode**: Validates generation without writing files
- **Error Handling**: Fails fast on validation errors or missing dependencies

## Kubernetes Job Design

### Job Configuration
- **Restart Policy**: Never (fail fast, don't retry automatically)
- **Backoff Limit**: 3 (allow some retries for transient issues)
- **TTL**: 24 hours (automatic cleanup)

**Rationale**: Data initialization should fail visibly rather than retry silently. Backoff provides safety for network issues while preventing infinite loops.

### Environment Variables
- `DRY_RUN`: Safe testing mode (default: true)
- `TXN_COUNT`: Number of transactions to generate (default: 8)
- `DISABLE_PANDERA_IMPORT_WARNING`: Suppress Pandera deprecation warnings

## Azure Integration

### Container & Security
- **Image Storage**: Azure Container Registry (ACR) for private image hosting
- **Authentication**: Workload Identity/OIDC (no long-lived secrets)
- **Secret Management**: Key Vault CSI for runtime secret injection

### CI/CD Pipeline
- **Build Trigger**: Push to main/develop branches
- **Authentication**: OIDC with federated credentials  
- **Deployment**: Commented ACR push for safety (dry-run mode)
- **Artifacts**: Bundle files published for deployment stages

## Safety & Rollback Strategy

### Environment Protection
- **Namespace Isolation**: `banking-demo` namespace prevents cross-environment issues
- **Default Safety**: DRY_RUN=true prevents accidental data modification
- **Resource Limits**: Prevents runaway resource consumption

### Rollback Capabilities
- **Deterministic Regeneration**: Same seed produces identical baseline data
- **CI/CD Artifacts**: Bundle files preserved for each build
- **Easy Cleanup**: Namespace deletion removes all components

## Validation Implementation

### Pre-flight Checks
- Account file existence and format validation
- Account ID format and sufficiency validation (minimum 2 accounts)

### Schema Validation (Pandera)
- **ID Format**: Transaction IDs must start with "txn-" 
- **Account References**: Account IDs must start with "acc-"
- **Amount Range**: Transactions between -10,000 and 10,000
- **Category Validation**: Must be one of 6 valid categories (GROCERIES, FUEL, SHOPPING, DINING, TRANSFER, SALARY)

### Error Handling
- Pandera schema validation on generated DataFrame
- Immediate termination on validation failures
- Exit code 1 for Kubernetes Job failure detection

## Key Design Decisions

### Why Deterministic Generation?
**Decision**: Use fixed seed (42) for all random values
**Rationale**: Demo environments need consistent, reproducible data for testing and demonstrations

### Why Schema Validation?
**Decision**: Use Pandera for comprehensive data validation  
**Rationale**: Ensures data quality and prevents malformed data from entering the system

### Why Fail-Fast Validation?
**Decision**: Terminate immediately on validation failures
**Rationale**: Prevents partial state scenarios that could confuse demo scenarios

### Why DRY_RUN Default?
**Decision**: Safe mode enabled by default, production mode explicit
**Rationale**: Prevents accidental data modification in shared demo environments

This design provides a reliable, maintainable solution for seeding banking demo environments with consistent, validated data while following Azure and Kubernetes best practices.