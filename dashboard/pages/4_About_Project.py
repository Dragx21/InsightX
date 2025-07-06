import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st

st.header("ℹ️ About InsightX")
st.markdown("""
**InsightX** is a modern, interactive analytics dashboard for e-commerce businesses.

---
### **Features**
- 📊 Real-time sales metrics
- 📈 Interactive visualizations (bar, line, pie charts)
- 🔮 ML-powered sales and revenue predictions
- 📥 Data export (CSV, Excel)
- 🗂️ Category-wise summaries
- 🔎 Powerful filtering and drill-down

---
### **Tech Stack**
- **Frontend:** Streamlit (Python)
- **Backend:** MongoDB, Pandas
- **Visualization:** Plotly
- **ML:** (Pluggable, coming soon)

---
### **Team**
- Project Lead: [Your Name]
- Contributors: [Add team members here]

---
### **Contact**
- GitHub: [github.com/hardikpareek20/InsightX](https://github.com/hardikpareek20/InsightX)
- Email: [your.email@example.com](mailto:your.email@example.com)

---
**2025 © InsightX. All rights reserved.**
""")
