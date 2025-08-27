# Banking Data Seeder - Production Mode

## Quick Start

### Generate Banking Demo Data
```bash
# From docker-assets directory
cd docker-assets
docker-compose up --build
```

### Custom Configuration
```bash
# From docker-assets directory
cd docker-assets

# Set custom transaction count
export TXN_COUNT=15
docker-compose up --build

# Or use .env file
cp env.example .env
# Edit .env file with your values
docker-compose up --build
```

## Production Configuration

### Default Settings
- **TXN_COUNT**: 10 transactions
- **DRY_RUN**: false (writes real data)
- **TXN_WINDOW_DAYS**: 60 days lookback
- **Output**: Data written to `../bundle/transactions/`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| TXN_COUNT | 10 | Number of transactions to generate (1-50) |
| DRY_RUN | false | Skip file writing if true |
| TXN_WINDOW_DAYS | 60 | Transaction date window (days) |

## Commands

```bash
# From docker-assets directory
cd docker-assets

# Build and run (one command)
docker-compose up --build

# Build only
docker-compose build

# Run without rebuild
docker-compose up

# Run one-time with custom config
docker-compose run --rm -e TXN_COUNT=20 banking-data-seeder

# View logs
docker-compose logs banking-data-seeder

# Clean up
docker-compose down
```

## Output

- **Location**: `bundle/transactions/transactions.json`
- **Format**: JSON array of transaction objects
- **Validation**: Schema validated before write
- **Deterministic**: Same seed produces same output

## Kubernetes Job Ready

This container is designed for Kubernetes Jobs:
- ✅ Non-zero exit codes on failure
- ✅ Environment variable configuration
- ✅ Fail-fast validation
- ✅ One-time execution pattern
