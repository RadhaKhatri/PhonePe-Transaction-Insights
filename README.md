# PhonePe-Transaction-Insights
PhonePe Transaction Insights
# 📊 PhonePe Pulse Dashboard – Data Visualization & Analytics

This is a full-stack data visualization dashboard project built using Python, MySQL, and PyQt6 that visualizes **PhonePe Pulse** data (aggregated from the [PhonePe Pulse GitHub repo](https://github.com/PhonePe/pulse)). It provides interactive charts and insights for digital payments, user activity, and insurance trends across India.

---

## 🚀 Features

- 🔍 State-wise dropdown for filtering insights
- 📂 Separate tabs for Transactions, Users, and Insurance
- 📈 Interactive charts using Matplotlib
- 🧠 Insights on:
  - Total transactions per state
  - Top 5 states by transaction volume
  - Insurance trends by location
  - User engagement growth
- 🗃️ Data is stored and queried from MySQL
- ✅ Clean PyQt6-based GUI dashboard
- 📊 Exportable insights as CSV

---

## 🛠️ Tech Stack

| Component     | Tool / Library              |
|---------------|-----------------------------|
| GUI           | PyQt6                       |
| Backend       | Python                      |
| Database      | MySQL                       |
| ORM/Connector | SQLAlchemy + mysql-connector-python |
| Visualization | Matplotlib, Pandas          |
| Data Source   | [PhonePe Pulse Open Dataset](https://github.com/PhonePe/pulse) |

---

## 📁 Project Structure

pulse/
│
├── data/ # PhonePe Pulse JSON data
│ ├── aggregated/
│ ├── map/
│ └── top/
│
├── dashboard.py # Main PyQt6 dashboard
├── load.py # Loads JSON data into MySQL
├── data.py # Optional data access script
├── visuvalization.py # Chart rendering (non-GUI)
├── *.csv # Exported insights as CSV
│ ├── total_transactions_per_state.csv
│ ├── top_5_states_by_volume.csv
│ ├── insurance_trends_by_location.csv
│ └── user_engagement_growth.csv
├── README.md # You are here!
└── LICENSE

yaml
Copy
Edit

---

## ✅ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/phonepe-dashboard.git
cd phonepe-dashboard
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is missing, install manually:

bash
Copy
Edit
pip install pandas pyqt6 matplotlib sqlalchemy mysql-connector-python
3. Import Data to MySQL
Ensure MySQL is running

Create a database called phonepe

Run load.py to populate data:

bash
Copy
Edit
python load.py
This script reads JSON files from data/ and inserts them into respective MySQL tables.

4. Run the Dashboard
bash
Copy
Edit
python dashboard.py
📸 Screenshots
Add screenshots of your dashboard UI here (optional)
You can add ea70b795-7671-4baa-bdbd-90427970df68.png here after uploading it to GitHub.

📈 Sample Insights
Top 5 states by transaction volume

State-wise user growth by quarter

Insurance trends across states

Device brand usage trends

CSV output files:

total_transactions_per_state.csv

top_5_states_by_volume.csv

user_engagement_growth.csv

insurance_trends_by_location.csv

📚 Data License
This project uses anonymized aggregate data from the PhonePe Pulse initiative, licensed under the CDLA-Permissive-2.0.

🙌 Acknowledgements
PhonePe for the Pulse dataset and public API initiative.

Community inspiration from full-stack Python, fintech, and open data enthusiasts.
