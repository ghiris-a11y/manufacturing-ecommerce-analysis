 
# 🏭 U.S. Manufacturing E-commerce Penetration Analysis (1999-2015)

[![Dash App](https://img.shields.io/badge/Live_Demo-Dash-blue?style=for-the-badge&logo=plotly)](https://your-railway-url.railway.app)

**Interactive dashboard** analyzing U.S. Census Bureau data on how e-commerce transformed manufacturing shipments across 12 NAICS industries from 1999-2015.

## 📊 Key Insights
- **Overall growth**: E-commerce share rose from ~5% to 15% across manufacturing
- **Fastest digitizers**: Computer/Electronics, Transportation Equipment led adoption
- **Laggards**: Furniture, Plastics showed slowest e-commerce penetration
- Transportation equipment had **highest absolute e-commerce $ growth**

## 🛠️ Tech Stack
<div align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white" />
<img src="https://img.shields.io/badge/Dash-119DFF?style=for-the-badge&logo=dash&logoColor=white" />
</div>

## 🚀 Quick Start

### Local
```bash
git clone https://github.com/YOUR_USERNAME/manufacturing-ecommerce-analysis
cd manufacturing-ecommerce-analysis
pip install -r requirements.txt
python src/data_cleaning.py
python dash_app/app.py  # http://localhost:8050

