# 💰 Smart Expense Analyzer

> A beginner-friendly yet professional web application to analyze, visualize, and gain insights from your daily expenses — built with Python, Streamlit, Pandas, and Matplotlib.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.1%2B-lightblue?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

**Smart Expense Analyzer** is a data-driven personal finance tool that lets users upload their expense data (as a CSV file) and instantly receive:

- A **visual breakdown** of spending by category (pie + bar charts)
- **Key financial metrics** like total expenses, transaction count, and daily average
- **Smart saving suggestions** tailored to each spending category
- An **alert system** for categories consuming more than 30% of the total budget

This project demonstrates practical skills in **data analysis**, **data visualization**, and **web app development** — making it ideal for a beginner's data science or Python portfolio.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 CSV Upload | Drag & drop or browse to upload your expense CSV |
| 📊 Summary Metrics | Total expenses, transaction count, average per transaction |
| 🥧 Pie Chart | Donut-style chart showing percentage distribution by category |
| 📉 Bar Chart | Horizontal bar chart comparing category-wise spending |
| 🔍 Top Insight | Automatically identifies and highlights your highest spending category |
| 💡 Smart Suggestions | Actionable saving tips for each category (Food, Travel, Shopping, etc.) |
| ⚠️ Overspend Alert | Visual warning when a category exceeds 30% of total budget |
| 🗂️ Data Preview | Expandable section to review cleaned raw data |
| 📋 Category Table | Tabular breakdown with totals and percentage share |
| 🧪 Sample Data | One-click "Try with Sample Data" button for instant demo |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Streamlit** | Web UI framework — turns Python scripts into interactive web apps |
| **Pandas** | Data loading, cleaning, grouping, and aggregation |
| **Matplotlib** | Chart generation (pie chart + bar chart) |
| **NumPy** | Numerical support (used internally by Pandas/Matplotlib) |

---

## 📁 Project Structure

```
smart_expense_analyzer/
│
├── app.py              # Main Streamlit application
├── data.csv            # Sample expense dataset (50 rows, 8 categories)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (you're reading it!)
```

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.10 or higher installed
- pip package manager

### Step 1 — Clone or Download the Project

```bash
git clone https://github.com/your-username/smart-expense-analyzer.git
cd smart-expense-analyzer
```

Or simply download and unzip the project folder.

### Step 2 — Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📂 CSV Format

Your CSV file **must** contain these three columns (column names are case-insensitive):

| Column | Format | Example |
|---|---|---|
| `Date` | Any standard date format | `2024-01-15` or `15/01/2024` |
| `Category` | Text string | `Food`, `Shopping`, `Travel` |
| `Amount` | Numeric (₹ symbol optional) | `450` or `₹450` |

**Example CSV:**

```csv
Date,Category,Amount
2024-01-01,Food,350
2024-01-02,Transport,120
2024-01-03,Shopping,800
2024-01-04,Entertainment,500
2024-01-05,Bills,1200
```

Supported categories with built-in suggestions:
`Food` · `Shopping` · `Travel` · `Entertainment` · `Transport` · `Health` · `Education` · `Bills` · `Rent` · `Others`

---

## 📸 Screenshots

> _Replace the placeholders below with actual screenshots after running the app._

### Home / Upload Screen
```
[ Screenshot: Upload screen with sidebar and file uploader ]
```

### Summary Metrics
```
[ Screenshot: 4 KPI metric cards — Total, Transactions, Average, Date Range ]
```

### Pie Chart
```
[ Screenshot: Donut-style pie chart showing category percentages ]
```

### Bar Chart
```
[ Screenshot: Horizontal bar chart with color-coded categories ]
```

### Smart Suggestions
```
[ Screenshot: Insight boxes with saving tips and overspend alerts ]
```

---

## 🧠 How It Works (Logic Overview)

```
User uploads CSV
       ↓
Validate columns (Date, Category, Amount)
       ↓
Clean data (parse dates, remove invalid amounts)
       ↓
Group by Category → Sum amounts
       ↓
Calculate KPIs (total, avg, date range)
       ↓
Generate Pie Chart + Bar Chart using Matplotlib
       ↓
Identify top-spending category
       ↓
Apply rule-based suggestions per category
       ↓
Display everything in Streamlit UI
```

---

## 🔮 Future Enhancements

- [ ] Monthly trend line chart (spending over time)
- [ ] Savings goal tracker with progress bar
- [ ] Auto-categorization using ML (scikit-learn)
- [ ] Export analyzed report as PDF
- [ ] Bank/UPI statement parser for real-time integration
- [ ] Multi-currency support

---

## ⚠️ Limitations

- Requires manual CSV input (no bank/UPI integration)
- Suggestions are rule-based, not ML-powered
- No persistent storage — data is not saved between sessions

---

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [linkedin.com/in/your-profile](https://linkedin.com/in/your-profile)
- Email: your.email@example.com

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute it.

---

> ⭐ If you found this project helpful, please give it a star on GitHub!
