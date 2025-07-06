import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
import sys, os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.db_operations import fetch_data

st.header("🔮 ML Predictions")

st.info("This section shows predicted sales and revenue. (Demo with mock data for now)")

data = fetch_data('processed_ecommerce_data')
if not data:
    st.error("❌ No data found. Please run data cleaning first.")
else:
    df = pd.DataFrame(data)
    categories = df['Category'].dropna().unique().tolist()
    products = df['ProductName'].dropna().unique().tolist()
    months = pd.to_datetime(df['OrderDate']).dt.to_period('M').astype(str).unique().tolist()

    selected_month = st.selectbox("Select Month", months)
    selected_category = st.selectbox("Select Category", categories)
    selected_product = st.selectbox("Select Product", products)

    st.markdown("---")

    # --- Mock Prediction Results ---
    predicted_quantity = random.randint(50, 500)
    predicted_revenue = random.randint(10000, 100000)

    st.subheader("📈 Prediction Results")
    st.metric("Predicted Quantity Sold", f"{predicted_quantity}")
    st.metric("Predicted Revenue", f"₹{predicted_revenue:,}")

    st.info("Replace these values with real ML model predictions when ready.")
