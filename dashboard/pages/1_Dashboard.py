import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.db_operations import fetch_data

st.header("📊 Dashboard")

data = fetch_data('processed_ecommerce_data')
if not data:
    st.error("❌ No data found. Please run data cleaning first.")
else:
    df = pd.DataFrame(data)
    st.success(f"✅ {len(df)} records loaded from MongoDB!")

    # Sidebar Filters
    categories = df['Category'].dropna().unique().tolist()
    payment_methods = df['PaymentMethod'].dropna().unique().tolist()
    min_date = pd.to_datetime(df['OrderDate']).min()
    max_date = pd.to_datetime(df['OrderDate']).max()

    with st.sidebar:
        selected_categories = st.multiselect("Filter by Category", categories, default=categories)
        selected_payments = st.multiselect("Filter by Payment Method", payment_methods, default=payment_methods)
        date_range = st.date_input("Order Date Range", [min_date, max_date])

    # Apply Filters
    filtered_df = df[
        (df['Category'].isin(selected_categories)) &
        (df['PaymentMethod'].isin(selected_payments)) &
        (pd.to_datetime(df['OrderDate']) >= pd.to_datetime(date_range[0])) &
        (pd.to_datetime(df['OrderDate']) <= pd.to_datetime(date_range[1]))
    ]

    # Metrics
    total_orders = len(filtered_df)
    total_revenue = (filtered_df['Quantity'] * filtered_df['Price']).sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("🛒 Total Orders", f"{total_orders:,}")
    col2.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
    col3.metric("📦 Avg Order Value", f"₹{avg_order_value:,.2f}")

    # Charts
    st.markdown("### 📊 Category-wise Revenue")
    filtered_df['Revenue'] = filtered_df['Quantity'] * filtered_df['Price']
    cat_rev = filtered_df.groupby('Category')['Revenue'].sum().reset_index()
    fig1 = px.bar(cat_rev, x='Category', y='Revenue', color='Category', title="Revenue by Category")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 📈 Monthly Revenue Trend")
    filtered_df['OrderMonth'] = pd.to_datetime(filtered_df['OrderDate']).dt.to_period('M').astype(str)
    month_rev = filtered_df.groupby('OrderMonth')['Revenue'].sum().reset_index()
    fig2 = px.line(month_rev, x='OrderMonth', y='Revenue', markers=True, title="Monthly Revenue Trend")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 🥧 Payment Method Share")
    pay_share = filtered_df['PaymentMethod'].value_counts().reset_index()
    pay_share.columns = ['PaymentMethod', 'Count']
    fig3 = px.pie(pay_share, names='PaymentMethod', values='Count', title="Payment Method Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Data Preview")
    st.dataframe(filtered_df.head(20))
