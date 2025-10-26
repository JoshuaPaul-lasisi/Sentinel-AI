import random
import uuid
from faker import Faker
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime, timedelta

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

# Parameters
N_TX = 10000
N_CUSTOMERS = 2000
N_DEVICES = 3000
N_AGENTS = 150
N_BENEF = 2500
N_GRAPH_EDGES = 5000

start_time = datetime.now() - timedelta(days=365)
end_time = datetime.now()

# 1) Generate fraud_labels table
fraud_labels = pd.DataFrame([
    {"fraud_label_id": 1, "label": "Legit", "description": "No fraud detected"},
    {"fraud_label_id": 2, "label": "Suspicious", "description": "Needs review"},
    {"fraud_label_id": 3, "label": "Fraud", "description": "Confirmed fraud"}
])

# 2) Customers
cust_ids = np.arange(1, N_CUSTOMERS+1)
cust_rows = []
for cid in cust_ids:
    signup = fake.date_between(start_date='-5y', end_date='today')
    risk_level = np.random.choice([1,2,3,4,5], p=[0.6,0.2,0.12,0.06,0.02])  # most low-risk
    avg_amount = float(np.round(10**np.random.normal(2.0 + 0.2*(risk_level-1), 0.8),2))
    cust_rows.append({
        "customer_id": int(cid),
        "name": fake.name(),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "gender": np.random.choice(["M","F","Other"], p=[0.48,0.48,0.04]),
        "phone": fake.phone_number(),
        "email": fake.email(),
        "signup_date": signup,
        "country": fake.country(),
        "customer_risk_level": int(risk_level),
        "avg_txn_amount": avg_amount
    })
customers = pd.DataFrame(cust_rows)

# 3) Devices
device_rows = []
for did in range(1, N_DEVICES+1):
    os = np.random.choice(["Windows","macOS","Linux","Android","iOS"], p=[0.25,0.15,0.05,0.35,0.20])
    browser = np.random.choice(["Chrome","Safari","Firefox","Edge","Other"], p=[0.5,0.2,0.15,0.1,0.05])
    first_seen = start_time + timedelta(days=random.randint(0, 300))
    last_seen = first_seen + timedelta(days=random.randint(0, 365))
    ip_pref = ".".join(map(str, np.random.randint(1,255,size=3)))
    # randomly associate device to a customer (but many devices not owned exclusively; set 70% mapped)
    owner = int(np.random.choice(cust_ids)) if random.random() < 0.7 else None
    device_rows.append({
        "device_id": did,
        "device_fingerprint": str(uuid.uuid4()),
        "os": os,
        "browser": browser,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "ip_prefix": ip_pref,
        "owner_customer_id": owner
    })
devices = pd.DataFrame(device_rows)

# 4) Agents
agent_rows = []
regions = ["North","South","East","West","Central"]
for aid in range(1, N_AGENTS+1):
    agent_rows.append({
        "agent_id": aid,
        "agent_name": fake.name(),
        "region": random.choice(regions),
        "branch_code": f"BR{random.randint(100,999)}"
    })
agents = pd.DataFrame(agent_rows)

# 5) Beneficiaries
benef_rows = []
for bid in range(1, N_BENEF+1):
    created = start_time + timedelta(days=random.randint(0,365))
    benef_rows.append({
        "beneficiary_id": bid,
        "name": fake.name(),
        "country": fake.country(),
        "account_id": f"ACC{random.randint(10000000,99999999)}",
        "created_at": created
    })
beneficiaries = pd.DataFrame(benef_rows)

# 6) Graph relationships - edges representing sharing and relationships
# We'll create edges of types: customer-device (ownership/sharing), device-device (shared ip), customer-customer (same beneficiary, or referral), customer-beneficiary
G = nx.Graph()
# Add nodes for identification with prefix
for cid in cust_ids:
    G.add_node(("customer", int(cid)))
for did in range(1, N_DEVICES+1):
    G.add_node(("device", int(did)))
for bid in range(1, N_BENEF+1):
    G.add_node(("beneficiary", int(bid)))
# Create some edges
edges = []
# customer-device edges: if device.owner_customer_id set, create owner edge; and add additional sharing edges
for _, d in devices.iterrows():
    did = int(d.device_id)
    owner = d.owner_customer_id
    if owner:
        edges.append((("customer", int(owner)), ("device", did), "owns", 1.0))
# add sharing edges: choose some devices to be used by multiple customers
for _ in range(int(N_DEVICES * 0.2)):
    did = random.randint(1, N_DEVICES)
    c1 = random.randint(1, N_CUSTOMERS)
    c2 = random.randint(1, N_CUSTOMERS)
    if c1 != c2:
        edges.append((("customer", c1), ("device", did), "uses", 0.6))
        edges.append((("customer", c2), ("device", did), "uses", 0.6))
# customer-beneficiary edges (customers using benefs)
for _ in range(int(N_TX * 0.2)):
    c = random.randint(1, N_CUSTOMERS)
    b = random.randint(1, N_BENEF)
    edges.append((("customer", c), ("beneficiary", b), "transfers_to", 0.8))
# customer-customer referral / same phone family
for _ in range(int(N_CUSTOMERS * 0.05)):
    a = random.randint(1, N_CUSTOMERS)
    b = random.randint(1, N_CUSTOMERS)
    if a != b:
        edges.append((("customer", a), ("customer", b), "known_to", 0.4))

# dedupe and create relationships dataframe
rel_rows = []
seen = set()
rid = 1
for (s, t, rtype, w) in edges:
    key = (s, t, rtype)
    if key in seen: 
        continue
    seen.add(key)
    s_type, s_id = s
    t_type, t_id = t
    rel_rows.append({
        "relationship_id": rid,
        "source_type": s_type,
        "source_id": int(s_id),
        "target_type": t_type,
        "target_id": int(t_id),
        "relationship_type": rtype,
        "weight": float(w),
        "created_at": fake.date_time_between(start_date='-2y', end_date='now')
    })
    rid += 1
graph_relationships = pd.DataFrame(rel_rows)

# 7) Transactions
txn_rows = []
channels = ["web","mobile","agent","atm"]
statuses = ["completed","failed","pending","reversed"]
tx_types = ["transfer","payout","payment","cash_in","cash_out"]
currency = ["USD","EUR","GBP","NGN","KES","GHS"]

for txid in range(1, N_TX+1):
    # pick a customer, weighted by risk (higher risk customers slightly more transactions)
    # give higher-risk customers a slightly elevated transaction count
    cust = np.random.choice(customers['customer_id'],
                            p=(customers['customer_risk_level'] / customers['customer_risk_level'].sum()))
    # pick device either owned by this customer (most), or random (some anomalies)
    cust_devices = devices[devices['owner_customer_id']==cust]
    if len(cust_devices) > 0 and random.random() < 0.85:
        device = int(cust_devices.sample(1).iloc[0]['device_id'])
    else:
        device = int(np.random.randint(1, N_DEVICES+1))
    # agent
    agent = int(np.random.randint(1, N_AGENTS+1))
    # beneficiary
    benef = int(np.random.randint(1, N_BENEF+1))
    # amount based on customer's avg_txn_amount with log-normal noise
    cust_avg = customers.loc[customers['customer_id']==cust,'avg_txn_amount'].iloc[0]
    amt = float(np.round(np.random.lognormal(mean=np.log(max(1,cust_avg)), sigma=0.9),2))
    # timestamp: skew by signup date (but here broadly across 1 year)
    ts = fake.date_time_between(start_date='-1y', end_date='now')
    ch = random.choice(channels)
    st = np.random.choice(statuses, p=[0.85,0.05,0.08,0.02])
    ip = f"{devices.loc[devices['device_id']==device,'ip_prefix'].iloc[0]}.{random.randint(1,254)}"
    ctry = fake.country()
    city = fake.city()
    txn_type = random.choice(tx_types)
    # risk_score: combine customer risk level, unusual device use (device owner mismatch), high amount, time-of-day anomaly
    cust_risk = customers.loc[customers['customer_id']==cust,'customer_risk_level'].iloc[0]
    device_owner = devices.loc[devices['device_id']==device,'owner_customer_id'].iloc[0]
    device_mismatch = 1 if (pd.isnull(device_owner) or device_owner!=cust) else 0
    high_amount = 1 if amt > cust_avg * 5 else 0
    hour = ts.hour
    odd_hour = 1 if hour < 6 or hour > 23 else 0
    base_score = 0.05 * cust_risk + 0.3 * device_mismatch + 0.4 * high_amount + 0.2 * odd_hour
    # scale and add noise
    risk_score = min(0.99, max(0.0, base_score + np.random.normal(0,0.05)))
    # assign fraud label probabilistically
    # e.g., risk_score < 0.15 => Legit, 0.15-0.5 => Suspicious, >0.5 => Fraud with some noise
    if random.random() < 0.005:  # a tiny random hit to add some outliers
        label = 3
    else:
        if risk_score < 0.15:
            label = 1
        elif risk_score < 0.5:
            label = 2
        else:
            label = 3
    txn_rows.append({
        "transaction_id": txid,
        "customer_id": int(cust),
        "device_id": int(device),
        "agent_id": int(agent),
        "beneficiary_id": int(benef),
        "fraud_label_id": int(label),
        "amount": amt,
        "currency": random.choice(currency),
        "timestamp": ts,
        "channel": ch,
        "status": st,
        "ip_address": ip,
        "country": ctry,
        "city": city,
        "risk_score": float(round(risk_score,3)),
        "txn_type": txn_type
    })

transactions = pd.DataFrame(txn_rows)

# Inspect ratios
print("Transactions by fraud label:")
print(transactions['fraud_label_id'].value_counts(normalize=True))

# Save to CSV
customers.to_csv("../data/synthetic/customers.csv", index=False)
devices.to_csv("../data/synthetic/devices.csv", index=False)
agents.to_csv("../data/synthetic/agents.csv", index=False)
beneficiaries.to_csv("../data/synthetic/beneficiaries.csv", index=False)
fraud_labels.to_csv("../data/synthetic/fraud_labels.csv", index=False)
graph_relationships.to_csv("../data/synthetic/graph_relationships.csv", index=False)
transactions.to_csv("../data/synthetic/transactions.csv", index=False)

print("CSV files written.")