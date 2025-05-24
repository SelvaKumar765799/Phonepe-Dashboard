# 📊 PhonePe Data Visualization Dashboard

Welcome to the **PhonePe Dashboard** — a full-stack data visualization project that extracts real-time data from PhonePe Pulse GitHub repository, stores it in a MySQL database, and displays insightful visualizations using Streamlit.

---

## 🚀 Project Highlights

- 📥 **Real-time Data Extraction** from PhonePe Pulse GitHub repo (via GitPython)
- 🧾 **JSON Parsing** to extract structured data
- 🛢️ **MySQL Database Integration** for persistent storage
- 📊 **Streamlit Dashboard** for interactive data exploration
- 🗺️ **Choropleth Maps & Dynamic Charts** using Plotly

---

## 🛠️ Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Data Source | PhonePe Pulse (GitHub JSON) |
| Backend     | Python, pandas, MySQL |
| Frontend    | Streamlit, Plotly  |
| DB Engine   | MySQL              |
| Data Tools  | GitPython, JSON    |

---
## ⚙️ How It Works

1. **Git Clone & JSON Load**  
   Clone the Pulse repo and parse JSON files into structured pandas DataFrames.

2. **Data Ingestion**  
   Load DataFrames into MySQL tables (transactions, users, insurance).

3. **Dashboard Visualization**  
   Use Streamlit to filter, aggregate, and plot data using Plotly maps/charts.

---

## 📊 Dashboard Features

- **Home**: Overview of PhonePe usage trends
- **Explore Data**: Payments, Insurance breakdowns
- **Insights**: Transaction trends, user adoption, insurance growth
- **Filters**: Year, Quarter, State, Transaction type

---


## 🌍 Screenshots

![image](https://github.com/user-attachments/assets/954ec3e2-8cb9-4b75-a1ff-1156ce824929)

![image](https://github.com/user-attachments/assets/19292013-16ad-4553-9d04-c2c0908b7238)

![image](https://github.com/user-attachments/assets/8c6db833-037a-4f5e-8ce7-60aea0728600)


## 🧠 Insights Delivered

- 📈 Transaction growth trends across years/states
- 📍 Regional adoption patterns via maps
- 📲 User growth by device type
- 🛡️ Insurance penetration analysis
