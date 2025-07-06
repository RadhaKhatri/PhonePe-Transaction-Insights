import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# ✅ Set up MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Radha@1474",
    database="phonepe"
)

print("\n📊 Connected to MySQL Database...")

# ---------------------------------------
# 🔹 1. Top 5 States by Transaction Volume
# ---------------------------------------
query1 = """
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

df1 = pd.read_sql(query1, conn)

# ✅ Bar Chart
plt.figure(figsize=(10,6))
sns.barplot(x='total_transaction_amount', y='state', data=df1, palette='viridis')
plt.title('Top 5 States by Transaction Volume')
plt.xlabel('Transaction Amount (₹)')
plt.ylabel('State')
plt.tight_layout()
plt.show()

# ---------------------------------------
# 🔹 2. Pie Chart: Transaction Categories
# ---------------------------------------
query2 = """
SELECT 
    transaction_type,
    SUM(transaction_amount) AS total_amount
FROM 
    aggregated_transaction
GROUP BY 
    transaction_type;
"""

df2 = pd.read_sql(query2, conn)

# ✅ Pie Chart
plt.figure(figsize=(8,8))
plt.pie(df2['total_amount'], labels=df2['transaction_type'], autopct='%1.1f%%', startangle=140)
plt.title('Transaction Distribution by Type')
plt.axis('equal')
plt.tight_layout()
plt.show()

# ---------------------------------------
# 🔹 3. Line Chart: User Engagement Growth
# ---------------------------------------
query3 = """
SELECT 
    CONCAT(year, ' Q', quarter) AS period,
    SUM(app_opens) AS total_opens
FROM 
    map_user
GROUP BY 
    year, quarter
ORDER BY 
    year, quarter;
"""

df3 = pd.read_sql(query3, conn)

# ✅ Line Chart
plt.figure(figsize=(12,6))
sns.lineplot(x='period', y='total_opens', data=df3, marker='o', linewidth=2.5, color='blue')
plt.xticks(rotation=45)
plt.title('User Engagement Growth Over Time (App Opens)')
plt.xlabel('Quarter')
plt.ylabel('Total App Opens')
plt.tight_layout()
plt.show()

# ✅ Close connection
conn.close()
print("\n✅ Analysis and Visualization Complete.")
