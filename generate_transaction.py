import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)

print("=" * 60)
print("FraudShield Bank — Dataset Generator")
print("=" * 60)

# ── Constants ────────────────────────────────────────────────
N_CUSTOMERS     = 100_000
N_ACCOUNTS      = 150_000
N_TRANSACTIONS  = 5_000_000
FRAUD_RATE      = 0.021
START_DATE      = datetime(2023, 1, 1)
END_DATE        = datetime(2024, 12, 31)
DATE_RANGE_DAYS = (END_DATE - START_DATE).days

# ── Segments ─────────────────────────────────────────────────
SEGMENTS        = ['young_adult', 'working_adult', 'established', 'retired']
SEG_WEIGHTS     = [0.25, 0.40, 0.25, 0.10]

SEG_AGE         = {'young_adult': (18, 30), 'working_adult': (31, 50),
                   'established': (51, 65), 'retired':       (66, 85)}
SEG_INCOME      = {'young_adult': (18000, 35000), 'working_adult': (35000, 85000),
                   'established': (45000, 120000),'retired':       (12000, 35000)}
SEG_CREDIT      = {'young_adult': (550, 720),  'working_adult': (650, 850),
                   'established': (700, 900),  'retired':       (700, 880)}

UK_REGIONS = ['London', 'South East', 'North West', 'Yorkshire',
              'West Midlands', 'East of England', 'South West',
              'East Midlands', 'North East', 'Wales', 'Scotland', 'Northern Ireland']
REGION_W   = [0.20, 0.14, 0.11, 0.08, 0.08, 0.08, 0.07, 0.07, 0.04, 0.04, 0.07, 0.02]

OCCUPATIONS = ['Employed', 'Self-Employed', 'Student', 'Retired', 'Unemployed', 'Part-Time']
OCC_BY_SEG  = {
    'young_adult':    [0.40, 0.10, 0.35, 0.00, 0.10, 0.05],
    'working_adult':  [0.65, 0.20, 0.00, 0.00, 0.08, 0.07],
    'established':    [0.55, 0.25, 0.00, 0.05, 0.08, 0.07],
    'retired':        [0.00, 0.05, 0.00, 0.85, 0.05, 0.05],
}

# ── CUSTOMERS ────────────────────────────────────────────────
print("\n[1/3] Generating customers.csv ...")

segments = np.random.choice(SEGMENTS, size=N_CUSTOMERS, p=SEG_WEIGHTS)

ages, incomes, credit_scores, occupations = [], [], [], []
for seg in segments:
    lo, hi = SEG_AGE[seg];    ages.append(np.random.randint(lo, hi + 1))
    lo, hi = SEG_INCOME[seg]; incomes.append(np.random.randint(lo, hi))
    lo, hi = SEG_CREDIT[seg]; credit_scores.append(np.random.randint(lo, hi + 1))
    occupations.append(np.random.choice(OCCUPATIONS, p=OCC_BY_SEG[seg]))

customer_since_days = np.random.randint(180, 365 * 15, size=N_CUSTOMERS)
customer_since      = [
    (START_DATE - timedelta(days=int(d))).strftime('%Y-%m-%d')
    for d in customer_since_days
]

customers = pd.DataFrame({
    'customer_id':     [f'CUST{str(i).zfill(6)}' for i in range(1, N_CUSTOMERS + 1)],
    'segment':         segments,
    'customer_age':    ages,
    'annual_income':   incomes,
    'credit_score':    credit_scores,
    'occupation':      occupations,
    'region':          np.random.choice(UK_REGIONS, size=N_CUSTOMERS, p=REGION_W),
    'customer_since':  customer_since,
})

# Introduce ~1% nulls in customer_age (realistic missing data)
null_idx = np.random.choice(N_CUSTOMERS, size=int(N_CUSTOMERS * 0.01), replace=False)
customers.loc[null_idx, 'customer_age'] = np.nan

customers.to_csv('/Users/gokulsathyan/Desktop/Bank fraud detection/customers.csv', index=False)
print(f"   customers.csv saved — {len(customers):,} rows")

# ── ACCOUNTS ─────────────────────────────────────────────────
print("\n[2/3] Generating accounts.csv ...")

# Assign accounts: 60% have 1, 30% have 2, 10% have 3
n1 = int(N_CUSTOMERS * 0.60)
n2 = int(N_CUSTOMERS * 0.30)
n3 = N_CUSTOMERS - n1 - n2

account_rows = []
account_counter = 1

# Map customer → segment for account logic
seg_map = dict(zip(customers['customer_id'], customers['segment']))
inc_map = dict(zip(customers['customer_id'], customers['annual_income']))

for i, cust_id in enumerate(customers['customer_id']):
    seg = seg_map[cust_id]
    inc = inc_map[cust_id]

    if i < n1:
        n_accs = 1
    elif i < n1 + n2:
        n_accs = 2
    else:
        n_accs = 3

    acc_types = []
    if n_accs == 1:
        acc_types = ['Current']
    elif n_accs == 2:
        acc_types = ['Current', 'Savings']
    else:
        acc_types = ['Current', 'Savings', 'Business']

    for acc_type in acc_types:
        # Realistic balance by segment and account type
        if seg == 'young_adult':
            balance = np.random.uniform(200, 3000)
        elif seg == 'working_adult':
            balance = np.random.uniform(1000, 25000)
        elif seg == 'established':
            balance = np.random.uniform(5000, 80000)
        else:
            balance = np.random.uniform(8000, 150000)

        if acc_type == 'Savings':
            balance *= np.random.uniform(1.5, 4.0)
        elif acc_type == 'Business':
            balance *= np.random.uniform(2.0, 8.0)

        # Account open date — before start of transaction period
        open_days_ago = np.random.randint(30, 365 * 15)
        open_date     = (START_DATE - timedelta(days=open_days_ago)).strftime('%Y-%m-%d')

        # Small % of accounts frozen or closed
        status_r = np.random.random()
        if status_r < 0.015:
            status = 'Frozen'
        elif status_r < 0.03:
            status = 'Closed'
        else:
            status = 'Active'

        account_rows.append({
            'account_id':        f'ACC{str(account_counter).zfill(7)}',
            'customer_id':       cust_id,
            'account_type':      acc_type,
            'account_open_date': open_date,
            'account_balance':   round(balance, 2),
            'account_status':    status,
        })
        account_counter += 1

accounts = pd.DataFrame(account_rows)
accounts.to_csv('/Users/gokulsathyan/Desktop/Bank fraud detection/accounts.csv', index=False)
print(f"   accounts.csv saved — {len(accounts):,} rows")

# ── TRANSACTIONS ─────────────────────────────────────────────
print("\n[3/3] Generating transactions.csv ...")
print("   This will take a few minutes — generating 5M rows in batches ...\n")

# Pre-build lookup maps
acc_ids      = accounts['account_id'].values
acc_cust     = accounts.set_index('account_id')['customer_id'].to_dict()
acc_type_map = accounts.set_index('account_id')['account_type'].to_dict()
acc_open_map = accounts.set_index('account_id')['account_open_date'].to_dict()
acc_status   = accounts.set_index('account_id')['account_status'].to_dict()
cust_seg_map = customers.set_index('customer_id')['segment'].to_dict()
cust_inc_map = customers.set_index('customer_id')['annual_income'].to_dict()
cust_reg_map = customers.set_index('customer_id')['region'].to_dict()

# Active accounts only for transactions
active_accs = accounts[accounts['account_status'] == 'Active']['account_id'].values
print(f"   Active accounts: {len(active_accs):,}")

# Transaction type distribution
TX_TYPES   = ['POS', 'Online', 'ATM', 'Mobile', 'Transfer']
TX_WEIGHTS = [0.40, 0.30, 0.12, 0.10, 0.08]

# Merchant categories with realistic amount ranges [min, max, distribution]
MERCHANT_CATS = {
    'Supermarket':      (5,    150,   'low'),
    'Restaurant/Cafe':  (3,    80,    'low'),
    'Online Retail':    (5,    500,   'medium'),
    'Utilities/Bills':  (30,   300,   'medium'),
    'Transport/Fuel':   (10,   120,   'low'),
    'Entertainment':    (5,    200,   'medium'),
    'Travel/Hotels':    (50,   2000,  'high'),
    'Healthcare':       (5,    300,   'medium'),
    'ATM Withdrawal':   (20,   300,   'low'),
    'Crypto/Gaming':    (10,   5000,  'high'),
    'Transfer':         (50,   10000, 'high'),
    'Other':            (5,    500,   'medium'),
}
CAT_NAMES    = list(MERCHANT_CATS.keys())
CAT_WEIGHTS  = [0.22, 0.15, 0.12, 0.10, 0.08, 0.07, 0.05, 0.05, 0.08, 0.03, 0.03, 0.02]

CURRENCIES   = ['GBP', 'USD', 'EUR', 'AED', 'AUD', 'CAD']
CURR_WEIGHTS = [0.94, 0.03, 0.02, 0.003, 0.004, 0.003]

# Hour-of-day probability weights (24 hours)
HOUR_WEIGHTS = np.array([
    0.3, 0.2, 0.15, 0.15, 0.2, 0.5,   # 0-5 (very low, night)
    1.0, 2.0, 2.5, 2.0, 2.0, 2.5,     # 6-11 (morning ramp)
    3.5, 3.5, 2.5, 2.5, 3.0, 4.5,     # 12-17 (lunch + afternoon)
    5.0, 4.5, 3.5, 2.5, 1.5, 0.8,     # 18-23 (evening peak)
])
HOUR_WEIGHTS = HOUR_WEIGHTS / HOUR_WEIGHTS.sum()

def generate_amount(cat, rng=np.random):
    lo, hi, dist = MERCHANT_CATS[cat]
    if cat == 'ATM Withdrawal':
        val = rng.choice(np.arange(lo, hi + 10, 10))
        return float(val)
    if dist == 'low':
        val = np.abs(rng.normal((lo + hi * 0.3) / 2, (hi - lo) * 0.2)) + lo
    elif dist == 'medium':
        val = np.abs(rng.normal((lo + hi) / 3, (hi - lo) * 0.25)) + lo
    else:
        val = np.abs(rng.exponential((hi - lo) * 0.15)) + lo
    return round(min(max(val, lo), hi), 2)

# Generate in batches
BATCH_SIZE = 500_000
N_BATCHES  = N_TRANSACTIONS // BATCH_SIZE
rng        = np.random.default_rng(SEED)

first_batch = True
total_fraud  = 0

for batch_num in range(N_BATCHES):
    n = BATCH_SIZE

    # Sample accounts (weighted toward current accounts for more transactions)
    sampled_accs = rng.choice(active_accs, size=n, replace=True)

    # Timestamps — random seconds within date range
    seconds      = rng.integers(0, DATE_RANGE_DAYS * 86400, size=n)
    timestamps   = [START_DATE + timedelta(seconds=int(s)) for s in seconds]
    hours        = np.array([t.hour for t in timestamps])
    days_of_week = np.array([t.weekday() for t in timestamps])  # 0=Mon, 6=Sun
    is_weekend   = (days_of_week >= 5).astype(int)

    # Override some hours with realistic distribution
    sampled_hours = rng.choice(24, size=n, p=HOUR_WEIGHTS)
    # Mix: 70% use realistic hour distribution, 30% truly random
    use_realistic = rng.random(n) < 0.70
    hours         = np.where(use_realistic, sampled_hours, hours)

    # Transaction types
    tx_types = rng.choice(TX_TYPES, size=n, p=TX_WEIGHTS)

    # Merchant categories
    merchant_cats = rng.choice(CAT_NAMES, size=n, p=CAT_WEIGHTS)

    # Amounts
    amounts = np.array([generate_amount(cat, np.random) for cat in merchant_cats])

    # Currencies
    currencies = rng.choice(CURRENCIES, size=n, p=CURR_WEIGHTS)
    is_foreign = (currencies != 'GBP').astype(int)

    # Merchant IDs
    merchant_ids = np.array([f'MER{str(rng.integers(1, 50000)):>05}' for _ in range(n)])

    # Behavioural signals
    days_since_last = rng.integers(0, 30, size=n)
    prev_tx_amount  = np.abs(rng.normal(100, 80, size=n)).round(2)
    login_attempts  = rng.choice([1, 1, 1, 1, 2, 2, 3, 4, 5], size=n)
    device_change   = (rng.random(n) < 0.04).astype(int)   # 4% base rate
    location_change = (rng.random(n) < 0.05).astype(int)   # 5% base rate
    ip_mismatch     = (rng.random(n) < 0.02).astype(int)   # 2% base rate
    failed_pin      = rng.choice([0, 0, 0, 0, 0, 1, 2, 3], size=n)

    # ── FRAUD LABELLING ──────────────────────────────────────
    fraud_prob = np.full(n, 0.005)  # base rate

    # Pattern 1: Velocity — late night + high login attempts
    p1 = ((hours >= 1) & (hours <= 4) & (login_attempts >= 3))
    fraud_prob = np.where(p1, fraud_prob + 0.25, fraud_prob)

    # Pattern 2: Account takeover — device change + IP mismatch + high amount
    p2 = ((device_change == 1) & (ip_mismatch == 1) & (amounts > 500))
    fraud_prob = np.where(p2, fraud_prob + 0.45, fraud_prob)

    # Pattern 3: Foreign + crypto/gaming + night
    p3 = ((is_foreign == 1) & (np.isin(merchant_cats, ['Crypto/Gaming'])) & (hours >= 22))
    fraud_prob = np.where(p3, fraud_prob + 0.40, fraud_prob)

    # Pattern 4: Failed PIN + device change + transfer
    p4 = ((failed_pin >= 2) & (device_change == 1) & (np.isin(tx_types, ['Transfer'])))
    fraud_prob = np.where(p4, fraud_prob + 0.50, fraud_prob)

    # Pattern 5: High amount transfer + IP mismatch
    p5 = ((amounts > 2000) & (ip_mismatch == 1) & (np.isin(tx_types, ['Transfer', 'Online'])))
    fraud_prob = np.where(p5, fraud_prob + 0.35, fraud_prob)

    # Pattern 6: location change + high amount + foreign currency
    p6 = ((location_change == 1) & (is_foreign == 1) & (amounts > 300))
    fraud_prob = np.where(p6, fraud_prob + 0.30, fraud_prob)

    fraud_prob = np.clip(fraud_prob, 0, 0.95)
    is_fraud   = (rng.random(n) < fraud_prob).astype(int)

    # ── DATA QUALITY ISSUES ──────────────────────────────────
    # ~2% null amounts
    null_amt = rng.choice(n, size=int(n * 0.02), replace=False)
    amounts_series = amounts.astype(object)
    amounts_series[null_amt] = np.nan

    # ~1% null merchant category
    null_cat = rng.choice(n, size=int(n * 0.01), replace=False)
    merchant_cats = np.array(merchant_cats, dtype=object)
    merchant_cats[null_cat] = np.nan

    # ~0.5% inconsistent currency formatting
    bad_curr = rng.choice(n, size=int(n * 0.005), replace=False)
    curr_replacements = {'GBP': 'gbp', 'USD': 'usd', 'EUR': 'Eur'}
    currencies = np.array(currencies, dtype=object)
    for idx in bad_curr:
        c = str(currencies[idx])
        currencies[idx] = curr_replacements.get(c, c.lower())

    total_fraud += is_fraud.sum()

    batch_df = pd.DataFrame({
        'transaction_id':             [f'TXN{str(batch_num * BATCH_SIZE + i + 1).zfill(8)}' for i in range(n)],
        'account_id':                 sampled_accs,
        'timestamp':                  [t.strftime('%Y-%m-%d %H:%M:%S') for t in timestamps],
        'amount':                     amounts_series,
        'transaction_type':           tx_types,
        'merchant_category':          merchant_cats,
        'merchant_id':                merchant_ids,
        'currency':                   currencies,
        'is_foreign_currency':        is_foreign,
        'hour_of_day':                hours,
        'day_of_week':                days_of_week,
        'is_weekend':                 is_weekend,
        'days_since_last_transaction':days_since_last,
        'previous_transaction_amount':prev_tx_amount,
        'login_attempts':             login_attempts,
        'device_change_flag':         device_change,
        'location_change_flag':       location_change,
        'ip_country_mismatch':        ip_mismatch,
        'failed_pin_attempts':        failed_pin,
        'is_fraud':                   is_fraud,
    })

    mode = 'w' if first_batch else 'a'
    batch_df.to_csv('/Users/gokulsathyan/Desktop/Bank fraud detection/transactions.csv', mode=mode,
                    header=first_batch, index=False)
    first_batch = False

    pct = (batch_num + 1) / N_BATCHES * 100
    print(f"   Batch {batch_num + 1}/{N_BATCHES} complete — {(batch_num+1)*BATCH_SIZE:,} rows written ({pct:.0f}%)")

print(f"\n   Total fraud transactions: {total_fraud:,}")
print(f"   Fraud rate: {total_fraud / N_TRANSACTIONS * 100:.2f}%")

print("\n" + "=" * 60)
print("All files generated successfully!")
print("=" * 60)
print(f"\n  customers.csv    — {N_CUSTOMERS:,} rows")
print(f"  accounts.csv     — {N_ACCOUNTS:,} rows")
print(f"  transactions.csv — {N_TRANSACTIONS:,} rows")