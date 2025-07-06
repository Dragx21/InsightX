import os
import sys
import pandas as pd

# ✅ Set up path to import fetch_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.db_operations import fetch_data


def run_eda():
    # ✅ Step 1: Fetch Processed Data
    data = fetch_data('processed_ecommerce_data')

    if not data:
        print("❌ No data found in 'processed_ecommerce_data'. Run data cleaning first.")
        return

    print(f"✅ {len(data)} records fetched for EDA.")

    # ✅ Step 2: Convert to DataFrame
    df = pd.DataFrame(data)

    # ✅ Step 3: Basic Stats
    print("\n📊 Basic Statistics (non-datetime columns):")
    print(df.describe(include='all'))  # ✅ pandas 1.5.3 compatible

    # ✅ Step 4: Revenue Metrics
    if {'Quantity', 'Price'}.issubset(df.columns):
        total_orders = len(df)
        total_revenue = (df['Quantity'] * df['Price']).sum()
        avg_order_value = total_revenue / total_orders

        print(f"\n🛒 Total Orders: {total_orders}")
        print(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
        print(f"📦 Average Order Value: ₹{avg_order_value:,.2f}")
    else:
        print("⚠️ Columns 'Quantity' and/or 'Price' missing for revenue analysis.")

    # ✅ Step 5: Category-wise Revenue
    if 'Category' in df.columns:
        print("\n📊 Revenue by Category:")
        cat_rev = df.groupby('Category').apply(lambda x: (x['Quantity'] * x['Price']).sum())
        print(cat_rev)
    else:
        print("⚠️ 'Category' column missing.")

    # ✅ Step 6: Payment Method Breakdown
    if 'PaymentMethod' in df.columns:
        print("\n💳 Payment Method Distribution:")
        print(df['PaymentMethod'].value_counts())
    else:
        print("⚠️ 'PaymentMethod' column missing.")

    # ✅ Step 7: Order Status Breakdown
    if 'Status' in df.columns:
        print("\n🚚 Order Status Distribution:")
        print(df['Status'].value_counts())
    else:
        print("⚠️ 'Status' column missing.")

    # ✅ Step 8: Monthly Revenue Trend
    if 'OrderDate' in df.columns:
        df['Month'] = pd.to_datetime(df['OrderDate'], errors='coerce').dt.to_period('M')
        month_rev = df.groupby('Month').apply(lambda x: (x['Quantity'] * x['Price']).sum())

        print("\n📅 Monthly Revenue Trend:")
        print(month_rev)

        print("\n🕒 Order Date Range:")
        print(f"From: {df['OrderDate'].min()} → To: {df['OrderDate'].max()}")
    else:
        print("⚠️ 'OrderDate' column missing.")

    # ✅ Step 9: Top 5 Cities by Revenue
    if 'City' in df.columns:
        city_rev = df.groupby('City').apply(lambda x: (x['Quantity'] * x['Price']).sum())
        top_cities = city_rev.sort_values(ascending=False).head(5)
        print("\n🏙️ Top 5 Cities by Revenue:")
        print(top_cities)
    else:
        print("⚠️ 'City' column missing.")


if __name__ == "__main__":
    run_eda()
