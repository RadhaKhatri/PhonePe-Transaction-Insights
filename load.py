import os
import json
import pandas as pd
from sqlalchemy import create_engine

# ✅ MySQL connection
engine = create_engine("mysql+mysqlconnector://root:Radha%401474@localhost/phonepe", echo=True)

# ✅ Base directory
base_dir = "D:/Dhara/Phonepay/pulse/data/"

# Helper: Safe insert
def safe_insert(df, table_name):
    if not df.empty:
        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"✅ Inserted {len(df)} rows into `{table_name}`")

# ---------------------------
# 1. AGGREGATED TRANSACTION
# ---------------------------
print("\n📁 Loading: aggregated_transaction")
path = base_dir + "aggregated/transaction/country/india/state/"
for state in os.listdir(path):
    for year in os.listdir(os.path.join(path, state)):
        for file in os.listdir(os.path.join(path, state, year)):
            file_path = os.path.join(path, state, year, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
            qtr = int(file.replace(".json", ""))
            rows = [{
                "state": state.replace("-", " ").title(),
                "year": int(year),
                "quarter": qtr,
                "transaction_type": entry.get("name"),
                "transaction_count": entry["paymentInstruments"][0]["count"],
                "transaction_amount": entry["paymentInstruments"][0]["amount"]
            } for entry in data.get("data", {}).get("transactionData", [])]
            safe_insert(pd.DataFrame(rows), "aggregated_transaction")

# ---------------------------
# 2. AGGREGATED USER (Fixed)
# ---------------------------
print("\n📁 Loading: aggregated_user")
path = base_dir + "aggregated/user/country/india/state/"
for state in os.listdir(path):
    for year in os.listdir(os.path.join(path, state)):
        for file in os.listdir(os.path.join(path, state, year)):
            file_path = os.path.join(path, state, year, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                qtr = int(file.replace(".json", ""))
                users_by_device = data.get("data", {}).get("usersByDevice", [])

                # ✅ Skip if usersByDevice is not a list
                if not isinstance(users_by_device, list) or len(users_by_device) == 0:
                    print(f"⚠️ No user device data in {file_path}")
                    continue

                rows = [{
                    "state": state.replace("-", " ").title(),
                    "year": int(year),
                    "quarter": qtr,
                    "brand": u.get("brand"),
                    "user_count": u.get("count"),
                    "percentage": u.get("percentage")
                } for u in users_by_device]

                safe_insert(pd.DataFrame(rows), "aggregated_user")
            except Exception as e:
                print(f"❌ Error in {file_path}: {e}")


# ---------------------------
# 3. AGGREGATED INSURANCE
# ---------------------------
print("\n📁 Loading: aggregated_insurance")
path = base_dir + "aggregated/insurance/country/india/state/"
for state in os.listdir(path):
    for year in os.listdir(os.path.join(path, state)):
        for file in os.listdir(os.path.join(path, state, year)):
            file_path = os.path.join(path, state, year, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
            qtr = int(file.replace(".json", ""))
            rows = [{
                "state": state.replace("-", " ").title(),
                "year": int(year),
                "quarter": qtr,
                "insurance_type": entry["name"],
                "policy_count": entry["paymentInstruments"][0]["count"],
                "policy_amount": entry["paymentInstruments"][0]["amount"]
            } for entry in data.get("data", {}).get("transactionData", [])]
            safe_insert(pd.DataFrame(rows), "aggregated_insurance")

# ---------------------------
# 4. MAP USER
# ---------------------------
print("\n📁 Loading: map_user")
path = base_dir + "map/user/hover/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        qtr = int(file.replace(".json", ""))
        hover_data = data.get("data", {}).get("hoverData", {})
        rows = [{
            "state": state.title(),
            "year": int(year),
            "quarter": qtr,
            "registered_users": info["registeredUsers"],
            "app_opens": info["appOpens"]
        } for state, info in hover_data.items()]
        safe_insert(pd.DataFrame(rows), "map_user")

# ---------------------------
# 5. MAP TRANSACTION
# ---------------------------
print("\n📁 Loading: map_map")
path = base_dir + "map/transaction/hover/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        qtr = int(file.replace(".json", ""))
        rows = [{
            "state": entry["name"].title(),
            "year": int(year),
            "quarter": qtr,
            "transaction_count": entry["metric"][0]["count"],
            "transaction_amount": entry["metric"][0]["amount"]
        } for entry in data.get("data", {}).get("hoverDataList", [])]
        safe_insert(pd.DataFrame(rows), "map_map")

# ---------------------------
# 6. MAP INSURANCE
# ---------------------------
print("\n📁 Loading: map_insurance")
path = base_dir + "map/insurance/hover/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        qtr = int(file.replace(".json", ""))
        rows = [{
            "state": entry["name"].title(),
            "year": int(year),
            "quarter": qtr,
            "insurance_count": entry["metric"][0]["count"],
            "insurance_amount": entry["metric"][0]["amount"]
        } for entry in data.get("data", {}).get("hoverDataList", [])]
        safe_insert(pd.DataFrame(rows), "map_insurance")
 # ---------------------------
# 7. TOP USER (Fixed)
# ---------------------------
print("\n📁 Loading: top_user")
path = base_dir + "top/user/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)

        # ✅ Skip non-json files
        if not file.endswith(".json"):
            continue

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            qtr = int(file.replace(".json", ""))

            pincodes = data.get("data", {}).get("pincodes", [])
            rows = [{
                "state": None,  # Top user JSON doesn’t contain state at pincode level
                "year": int(year),
                "quarter": qtr,
                "pincode": p.get("name"),
                "registered_users": p.get("registeredUsers")
            } for p in pincodes]

            safe_insert(pd.DataFrame(rows), "top_user")

        except Exception as e:
            print(f"❌ Error in {file_path}: {e}")
            
# ---------------------------
# 8. TOP TRANSACTION
# ---------------------------
print("\n📁 Loading: top_map")
path = base_dir + "top/transaction/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        qtr = int(file.replace(".json", ""))
        rows = []
        for entity_type in ["states", "districts", "pincodes"]:
            for item in data.get("data", {}).get(entity_type, []):
                rows.append({
                    "state": item["entityName"].title() if entity_type == "states" else None,
                    "year": int(year),
                    "quarter": qtr,
                    "entity_type": entity_type[:-1],
                    "entity_name": item["entityName"],
                    "transaction_count": item["metric"]["count"],
                    "transaction_amount": item["metric"]["amount"]
                })
        safe_insert(pd.DataFrame(rows), "top_map")

# ---------------------------
# 9. TOP INSURANCE
# ---------------------------
print("\n📁 Loading: top_insurance")
path = base_dir + "top/insurance/country/india/"
for year in os.listdir(path):
    for file in os.listdir(os.path.join(path, year)):
        file_path = os.path.join(path, year, file)
        with open(file_path, 'r') as f:
            data = json.load(f)
        qtr = int(file.replace(".json", ""))
        rows = [{
            "state": None,
            "year": int(year),
            "quarter": qtr,
            "pincode": p["entityName"],
            "insurance_type": "Insurance",
            "policy_count": p["metric"]["count"],
            "policy_amount": p["metric"]["amount"]
        } for p in data.get("data", {}).get("pincodes", [])]
        safe_insert(pd.DataFrame(rows), "top_insurance")

print("\n🎉 Done! All tables loaded successfully.")
