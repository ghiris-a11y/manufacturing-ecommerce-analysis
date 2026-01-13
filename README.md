 
# 🏭 U.S. Manufacturing E-commerce Dashboard (1999–2015)

![Dashboard Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Dash](https://img.shields.io/badge/Framework-Dash-orange)

## 🚀 Live Dashboard

🔗 **Live App**: https://web-production-a0f5.up.railway.app/  
[![Railway](https://img.shields.io/badge/Live-Dashboard-success)](https://manufacturing-ecommerce-analysis.up.railway.app)

[![GitHub](https://img.shields.io/github/stars/ghiris-a11y/manufacturing-ecommerce-analysis?style=social)](https://github.com/ghiris-a11y/manufacturing-ecommerce-analysis)

---

## 📊 Project Overview

This project analyzes **U.S. Census Bureau manufacturing e-commerce data** to understand how
e-commerce adoption evolved in the **U.S. manufacturing sector** between **1999 and 2015**.

An interactive, **Power BI-style analytics dashboard** visualizing the shift from traditional manufacturing to e-commerce in the United States. Built with **Python (Dash & Plotly)** and styled with custom CSS for a professional business intelligence look.

---

## 📊 New Features (v2.0)

This dashboard has been upgraded with a modern **Grid Layout** and advanced analytics features:

* **⚡ Power BI-Style Interface:** A clean 2x2 grid layout with distinct shadow-boxed cards for professional presentation.
* ## 🧩 Dashboard Features
- 📈 **Industry-level e-commerce trends** (1999–2015)
- 📊 **E-commerce share (% of total shipments)** by industry
- 🧮 **KPI cards** showing:
  - Latest e-commerce penetration (%)
  - Latest e-commerce value
  - Year-over-year growth
    
* **🔢 Dynamic KPI Cards:** Real-time "Big Number" metrics that update instantly based on filters:
    * **Digital Penetration:** The % of market share owned by e-commerce.
    * **E-commerce Sales:** Total value in Millions (USD).
    * **Total Market:** Total manufacturing shipment value.
* **🎛️ Interactive Controls:**
    * **Year Slider:** Scrub through 16 years of historical data (1999–2015).
    * **Sector Drill-down:** Filter the entire dashboard by specific industries (e.g., "Food Manufacturing" or "Transportation").
* **📈 Advanced Charts:**
    * **Growth Trend:** Dual-line chart comparing Total Shipments vs. E-commerce growth.
    * **Market Composition:** Stacked area chart showing the "Traditional vs. Digital" split.
    * **Sector Ranking:** Top 10 industries by value.
    * * **Maturity Matrix (New):** A scatter plot analyzing **Market Size vs. Digital Adoption**. This helps identify "Digital Giants" (High Value, High Tech) vs.         "Sleeping Giants" (High Value, Low Tech)..

---
---

## 🧩 Dashboard Features

- 📈 **Industry-level e-commerce trends** (1999–2015)
- 📊 **E-commerce share (% of total shipments)** by industry
- 🧮 **KPI cards** showing:
  - Latest e-commerce penetration (%)
  - Latest e-commerce value
  - Year-over-year growth
  - 

- 📝 **Annotated insights** highlighting key economic events
- 🎨 **Custom CSS styling** for clean, modern dashboard layout
---
## 📈 Key Insights

- U.S. manufacturing e-commerce activity **increased steadily** from 1999 to 2015  
- The data highlights a **structural shift toward digital sales channels**  
- Acceleration is especially visible in the mid-to-late 2000s  

> 📌 Note: This dashboard currently focuses on **aggregate manufacturing-level trends** derived from U.S. Census data.

# ✅ **Metrics Explanation** section

This turns your project into an **analytics case study**.

```md
---

## 📐 Metrics Explained

- **E-commerce Value**: Value of manufacturing shipments conducted via e-commerce (USD millions)
- **Total Shipments**: Total manufacturing shipment value (USD millions)
- **E-commerce Share (%)**:
  
  ```text
  (E-commerce Value / Total Shipments) × 100
---

## 🛠️ Tech Stack

- **Python**
- **Pandas** – data cleaning & transformation
- **Plotly** – interactive visualizations
- **Dash** – web dashboard framework
- **CSS** – custom styling for KPI cards and layout
- **Railway** – cloud deployment

---

## 🏃‍♂️ Quick Start (Local)

```bash
git clone https://github.com/ghiris-a11y/manufacturing-ecommerce-analysis
cd manufacturing-ecommerce-analysis

pip install -r requirements.txt

# Generate cleaned dataset with penetration metrics
python src/data_cleaning.py

# Run dashboard (CSS loads automatically from assets/)
python dash_app/app.py

