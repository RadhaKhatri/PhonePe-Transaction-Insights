import pandas as pd
import mysql.connector

# ✅ MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Radha@1474",
    database="phonepe"
)

print("\n📊 Running PhonePe Pulse SQL Analysis...\n")

# -------------------------------
# 1. Total Transactions per State
# -------------------------------
query1 = """
SELECT 
    state,
    SUM(transaction_amount) AS total_transaction_amount,
    SUM(transaction_count) AS total_transaction_count
FROM 
    aggregated_transaction
GROUP BY 
    state
ORDER BY 
    total_transaction_amount DESC;
"""

df1 = pd.read_sql(query1, conn)
print("✅ Total Transactions per State:\n", df1)
df1.to_csv("total_transactions_per_state.csv", index=False)


# -----------------------------------------
# 2. Top 5 States by Total Transaction Amount
# -----------------------------------------
query2 = """
SELECT 
    state,
    SUM(transaction_amount) AS total_transaction_amount
FROM 
    aggregated_transaction
GROUP BY 
    state
ORDER BY 
    total_transaction_amount DESC
LIMIT 5;
"""

df2 = pd.read_sql(query2, conn)
print("\n✅ Top 5 States by Transaction Volume:\n", df2)
df2.to_csv("top_5_states_by_volume.csv", index=False)


# -----------------------------------------
# 3. Insurance Trends by State and Quarter
# -----------------------------------------
query3 = """
SELECT 
    state,
    year,
    quarter,
    SUM(policy_count) AS total_policies,
    SUM(policy_amount) AS total_insurance_amount
FROM 
    aggregated_insurance
GROUP BY 
    state, year, quarter
ORDER BY 
    state, year, quarter;
"""

df3 = pd.read_sql(query3, conn)
print("\n✅ Insurance Trends by Location:\n", df3)
df3.to_csv("insurance_trends_by_location.csv", index=False)


# -----------------------------------------
# 4. User Engagement Growth (App Opens)
# -----------------------------------------
query4 = """
SELECT 
    state,
    year,
    quarter,
    SUM(app_opens) AS total_app_opens
FROM 
    map_user
GROUP BY 
    state, year, quarter
ORDER BY 
    year, quarter, total_app_opens DESC;
"""

df4 = pd.read_sql(query4, conn)
print("\n✅ User Engagement Growth:\n", df4)
df4.to_csv("user_engagement_growth.csv", index=False)

# ✅ Close connection
conn.close()

print("\n🎉 All queries executed and saved as CSV successfully.")
