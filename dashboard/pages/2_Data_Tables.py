import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import pandas as pd
import io
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.db_operations import fetch_data

st.header("📄 Data Tables")

data = fetch_data('processed_ecommerce_data')
if not data:
    st.error("❌ No data found. Please run data cleaning first.")
else:
    df = pd.DataFrame(data)
    st.success(f"✅ {len(df)} records loaded from MongoDB!")

    # Ensure Revenue column exists
    if 'Revenue' not in df.columns:
        df['Revenue'] = df['Quantity'] * df['Price']

    st.dataframe(df)

    # Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name='insightx_data.csv',
        mime='text/csv'
    )

    # Download as Excel (using BytesIO buffer)
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    st.download_button(
        label="⬇️ Download as Excel",
        data=output.getvalue(),
        file_name='insightx_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Category-wise summary
    cat_summary = df.groupby('Category').agg({
        'Quantity': 'sum',
        'Price': 'mean',
        'Revenue': 'sum'
    }).reset_index()

    st.markdown("### 📊 Category-wise Summary")
    st.dataframe(cat_summary)
