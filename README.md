 
# 🏭 U.S. Manufacturing E-commerce Penetration Analysis (1999–2015)

## 🚀 Live Dashboard

🔗 **Live App**: https://web-production-a0f5.up.railway.app/  
[![Railway](https://img.shields.io/badge/Live-Dashboard-success)](https://manufacturing-ecommerce-analysis.up.railway.app)

[![GitHub](https://img.shields.io/github/stars/ghiris-a11y/manufacturing-ecommerce-analysis?style=social)](https://github.com/ghiris-a11y/manufacturing-ecommerce-analysis)

---

## 📊 Project Overview

This project analyzes **U.S. Census Bureau manufacturing e-commerce data** to understand how
e-commerce adoption evolved in the **U.S. manufacturing sector** between **1999 and 2015**.

An interactive **Dash dashboard** visualizes the **trend of manufacturing e-commerce activity over time**
using official Census shipment tables.

---
---

## 🧩 Dashboard Features

- 📈 **Industry-level e-commerce trends** (1999–2015)
- 📊 **E-commerce share (% of total shipments)** by industry
- 🧮 **KPI cards** showing:
  - Latest e-commerce penetration (%)
  - Latest e-commerce value
  - Year-over-year growth
- 📝 **Annotated insights** highlighting key economic events
- 🎨 **Custom CSS styling** for clean, modern dashboard layout
---
## 📈 Key Insights

- U.S. manufacturing e-commerce activity **increased steadily** from 1999 to 2015  
- The data highlights a **structural shift toward digital sales channels**  
- Acceleration is especially visible in the mid-to-late 2000s  

> 📌 Note: This dashboard currently focuses on **aggregate manufacturing-level trends** derived from U.S. Census data.

# ✅ 5️⃣ Add a **Metrics Explanation** section (HIGH IMPACT)

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

