#!/usr/bin/env python3
import json, random, os, pandas as pd
import pandera.pandas as pa
from datetime import datetime, timedelta

# Fixed seed for deterministic output
random.seed(42)

# Schema validation for fail-fast approach
schema = pa.DataFrameSchema({
    "id": pa.Column(str, checks=pa.Check.str_startswith("txn-")),
    "account_id": pa.Column(str, checks=pa.Check.str_startswith("acc-")),
    "amount": pa.Column(float, checks=pa.Check.in_range(-10000, 10000)),
    "category": pa.Column(str, checks=pa.Check.isin(["GROCERIES", "FUEL", "SHOPPING", "DINING", "TRANSFER", "SALARY"]))
})

def generate_transactions(count=8):    
    # Load and validate accounts
    if not os.path.exists("bundle/products/accounts.json"):
        raise FileNotFoundError("Missing accounts.json")
    
    with open("bundle/products/accounts.json") as f:
        accounts = json.load(f)
    
    account_ids = [acc["id"] for acc in accounts if acc.get("id", "").startswith("acc-")]
    if len(account_ids) < 2:
        raise ValueError("Need at least 2 accounts")
    
    # Generate transactions
    transactions = []
    base_date = datetime(2025, 8, 26)
    categories = ["GROCERIES", "FUEL", "SHOPPING", "DINING", "TRANSFER", "SALARY"]
    
    for i in range(count):
        amount = round(random.uniform(-200, 2000), 2)        
        txn = {
            "id": f"txn-{random.randint(100000000000, 999999999999)}",
            "account_id": random.choice(account_ids),
            "amount": amount,
            "category": random.choice(categories),
            "transaction_date": (base_date - timedelta(days=random.randint(5, 85))).isoformat() + "Z",
            "status": "completed"
        }
        transactions.append(txn)
    
    # Pandera schema validation
    df = pd.DataFrame(transactions)
    schema.validate(df[["id", "account_id", "amount", "category"]])
    return transactions

if __name__ == "__main__":
    try:
        count = int(os.getenv("TXN_COUNT", "8"))
        dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        
        txns = generate_transactions(count)
        print(f"✅ Generated {len(txns)} valid transactions")
        
        if not dry_run:
            os.makedirs("bundle/transactions", exist_ok=True)
            with open("bundle/transactions/transactions.json", "w") as f:
                json.dump(txns, f, indent=2)
            print("✅ Saved successfully!")
        else:
            print("🔄 DRY RUN mode - no files written")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        exit(1)