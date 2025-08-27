# Banking Demo Data Initializer

Synthetic data generator for banking demo environments with deterministic, idempotent data seeding using Kubernetes Jobs.

## Project Structure

```
├── src/
│   └── generate_transactions.py    # Python generator with Pandera validation
├── bundle/                         # Sample banking data
│   ├── org/users.json             # User identity data
│   ├── products/accounts.json     # Banking accounts  
│   ├── access/cards.json          # Payment cards
│   └── transactions/              # Generated transactions
├── docker-assets/                 # Container configuration
├── kubernetes/                    # AKS deployment specs
├── .github/workflows/             # CI/CD pipeline
└── docs/                          # Design and implementation notes
```

## Quick Start

### Local Development
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r docker-assets/requirements.txt

# Generate data
python3 src/generate_transactions.py

# Docker
cd docker-assets && docker-compose up
```

### Production Deployment
```bash
# Build and deploy to AKS
kubectl apply -f kubernetes/banking-data-seeder-job.yaml
```

## Key Features

- **Deterministic**: Fixed seed (42) ensures identical output across runs
- **Validated**: Pandera schema validation for data quality
- **Configurable**: Environment variables (`TXN_COUNT`, `DRY_RUN`)
- **Azure-Ready**: Kubernetes Job with OIDC authentication
- **Safe**: DRY_RUN mode prevents accidental data modification

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TXN_COUNT` | 8 | Number of transactions to generate |
| `DRY_RUN` | true | Skip file writes for testing |

## Documentation

- **[Design Note](DESIGN_NOTE.md)** - Architecture and key decisions
- **[Risks & Trade-offs](RISKS_AND_TRADEOFFS.md)** - Implementation considerations  
- **[FX Rates Strategy](FX_RATES_IMPLEMENTATION.md)** - Multi-currency enhancement approach
- **[CI/CD Guide](.github/README-cicd.md)** - GitHub Actions workflow setup

## Assignment Deliverables

✅ **Design Note** (≤2 pages) - Data model, determinism, flow, Azure integration  
✅ **Sample Data Bundle** - 4 JSON files with realistic banking data  
✅ **Python Generator** (~70 lines) - Deterministic script with validation  
✅ **Kubernetes Job** - AKS-ready deployment specification  
✅ **CI/CD Pipeline** - GitHub Actions with Azure OIDC  
✅ **Risk Analysis** (½ page) - Trade-offs and implementation considerations  
