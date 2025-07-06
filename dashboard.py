import sys
import pandas as pd
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QTabWidget, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ✅ Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Radha@1474",
        database="phonepe"
    )

# ✅ Main App Window
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 PhonePe Pulse - PyQt6 Dashboard")
        self.setGeometry(100, 100, 1000, 700)

        self.conn = get_connection()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # ✅ Dropdown for state selection
        self.state_selector = QComboBox()
        self.state_selector.addItems(self.get_states())
        self.state_selector.currentTextChanged.connect(self.update_tabs)
        layout.addWidget(QLabel("Select a State:"))
        layout.addWidget(self.state_selector)

        # ✅ Tabs for Transaction, User, Insurance
        self.tabs = QTabWidget()
        self.transaction_tab = QWidget()
        self.user_tab = QWidget()
        self.insurance_tab = QWidget()

        self.tabs.addTab(self.transaction_tab, "Transactions")
        self.tabs.addTab(self.user_tab, "Users")
        self.tabs.addTab(self.insurance_tab, "Insurance")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.update_tabs(self.state_selector.currentText())

    def get_states(self):
        df = pd.read_sql("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state", self.conn)
        return df['state'].dropna().tolist()

    def update_tabs(self, state):
        self.load_transaction_tab(state)
        self.load_user_tab(state)
        self.load_insurance_tab(state)

    def load_transaction_tab(self, state):
        layout = QVBoxLayout()
        query = f"""
        SELECT year, quarter, transaction_type, SUM(transaction_amount) AS amount
        FROM aggregated_transaction
        WHERE state = '{state}'
        GROUP BY year, quarter, transaction_type
        ORDER BY year, quarter;
        """
        df = pd.read_sql(query, self.conn)

        fig = Figure(figsize=(8, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot()
        for t_type in df['transaction_type'].unique():
            subset = df[df['transaction_type'] == t_type]
            ax.plot(subset['year'].astype(str) + ' Q' + subset['quarter'].astype(str),
                    subset['amount'], label=t_type)
        ax.set_title("Transaction Volume by Type")
        ax.set_ylabel("Amount (₹)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.legend()
        layout.addWidget(canvas)

        self.transaction_tab.setLayout(layout)

    def load_user_tab(self, state):
        layout = QVBoxLayout()
        query = f"""
        SELECT year, quarter, brand, user_count
        FROM aggregated_user
        WHERE state = '{state}'
        ORDER BY year, quarter;
        """
        df = pd.read_sql(query, self.conn)

        fig = Figure(figsize=(8, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot()
        for brand in df['brand'].unique():
            subset = df[df['brand'] == brand]
            ax.plot(subset['year'].astype(str) + ' Q' + subset['quarter'].astype(str),
                    subset['user_count'], label=brand)
        ax.set_title("Users by Device Brand")
        ax.set_ylabel("Users")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.legend()
        layout.addWidget(canvas)

        self.user_tab.setLayout(layout)

    def load_insurance_tab(self, state):
        layout = QVBoxLayout()
        query = f"""
        SELECT year, quarter, insurance_type, SUM(policy_amount) AS amount
        FROM aggregated_insurance
        WHERE state = '{state}'
        GROUP BY year, quarter, insurance_type
        ORDER BY year, quarter;
        """
        df = pd.read_sql(query, self.conn)

        fig = Figure(figsize=(8, 4))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot()
        for ins_type in df['insurance_type'].unique():
            subset = df[df['insurance_type'] == ins_type]
            ax.plot(subset['year'].astype(str) + ' Q' + subset['quarter'].astype(str),
                    subset['amount'], label=ins_type)
        ax.set_title("Insurance Trend")
        ax.set_ylabel("Amount (₹)")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.legend()
        layout.addWidget(canvas)

        self.insurance_tab.setLayout(layout)

# ✅ Run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())

