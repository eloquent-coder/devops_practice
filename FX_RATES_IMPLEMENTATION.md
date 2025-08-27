# FX Rates Implementation - Offline Baking Strategy

## Overview
Bake daily FX rates offline in CI and surface them in seeded banking data without runtime API calls.

## CI Pipeline Integration
```yaml
- name: Fetch FX Rates
  run: |
    curl "https://api.exchangerate-api.com/v4/latest/USD" > docker-assets/fx_rates.json
    jq '. + {"generated_at": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' docker-assets/fx_rates.json
```

## Dockerfile
```dockerfile
COPY docker-assets/fx_rates.json /app/fx_rates.json
```

## Python Integration
```python
def load_fx_rates():
    with open("fx_rates.json") as f:
        return json.load(f)

def generate_transactions(count=8):
    fx_rates = load_fx_rates()
    for txn in transactions:
        currency = random.choice(["USD", "EUR", "GBP"])
        fx_rate = fx_rates["rates"].get(currency, 1.0)
        txn.update({
            "currency": currency,
            "fx_rate": fx_rate,
            "usd_amount": round(txn["amount"] * fx_rate, 2)
        })
```

**Benefits**: No runtime API calls, deterministic FX rates, offline capability, realistic multi-currency data.