# processing/clean_data.py

import os
import sys
import pandas as pd

# Fix: Correct __file__ usage for setting import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from storage.db_operations import fetch_data, insert_data, delete_data


def clean_data():
    # ✅ Step 1: Fetch Raw Data
    raw_data = fetch_data('raw_ecommerce_data')

    if not raw_data:
        print("❌ No data found in 'raw_ecommerce_data' collection.")
        return

    print(f"✅ {len(raw_data)} records fetched from 'raw_ecommerce_data'")

    # ✅ Step 2: Convert to DataFrame
    df = pd.DataFrame(raw_data)

    # ✅ Step 3: Remove MongoDB's _id column
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    # ✅ Step 4: Remove Duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"🗑️ Removed {before - after} duplicate rows.")

    # ✅ Step 5: Handle Missing Values
    df['PaymentMethod'] = df['PaymentMethod'].fillna('Unknown')
    df['Status'] = df['Status'].fillna('Pending')
    df['City'] = df['City'].fillna('Unknown')
    df['State'] = df['State'].fillna('Unknown')

    # ✅ Step 6: Standardize Formats
    df['CustomerName'] = df['CustomerName'].str.title()
    df['ProductName'] = df['ProductName'].str.title()
    df['Category'] = df['Category'].str.title()
    df['Status'] = df['Status'].str.title()

    # ✅ Step 7: Convert Data Types
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0).astype(float)

    # ✅ Step 8: Standardize Dates
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    # ✅ Step 9: Clear existing processed data (optional)
    delete_data('processed_ecommerce_data')

    # ✅ Step 10: Insert cleaned data
    cleaned_data = df.to_dict(orient='records')
    insert_data('processed_ecommerce_data', cleaned_data)

    print(f"✅ {len(cleaned_data)} cleaned records inserted into 'processed_ecommerce_data'")


# Fix: Correct the main guard block
if __name__ == "__main__":
    clean_data()
