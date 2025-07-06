import os
import json
import pandas as pd
from sqlalchemy import create_engine

# MySQL connection (update with your password)
engine = create_engine("mysql+mysqlconnector://root:yourpassword@localhost/phonepe")

# Path to transaction data
base_path = "pulse/data/aggregated/transaction/country/india/state/"

# Loop through states and files
for state in os.listdir(base_path):
    state_path = os.path.join(base_path, state)
    for file in os.listdir(state_path):
        if file.endswith(".json"):
            with open(os.path.join(state_path, file)) as f:
                data = json.load(f)
                year = int(file.replace(".json", ""))
                quarter = data["quarter"]
                transaction_data = data["data"]["transactionData"]
                
                for entry in transaction_data:
                    row = {
                        "state": state.replace("-", " ").title(),
                        "year": year,
                        "quarter": quarter,
                        "transaction_type": entry["name"],
                        "transaction_count": entry["paymentInstruments"][0]["count"],
                        "transaction_amount": entry["paymentInstruments"][0]["amount"]
                    }
                    df = pd.DataFrame([row])
                    df.to_sql("aggregated_transaction", con=engine, if_exists="append", index=False)
