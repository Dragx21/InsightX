import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from storage.db_operations import fetch_data


def sales_prediction():
    # ✅ Fetch Processed Data
    data = fetch_data('processed_ecommerce_data')

    if not data:
        print("❌ No data found in 'processed_ecommerce_data'. Run cleaning first.")
        return

    df = pd.DataFrame(data)

    # ✅ Feature Engineering
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    df['Month'] = df['OrderDate'].dt.month

    # ✅ Calculate Average Price Per Product
    avg_price = df.groupby('ProductName')['Price'].mean().to_dict()

    # ✅ Map Product to Category
    category_map = df.set_index('ProductName')['Category'].to_dict()

    # ✅ Prepare Features
    product_dummies = pd.get_dummies(df['ProductName'], prefix='Product')
    category_dummies = pd.get_dummies(df['Category'], prefix='Category')
    payment_dummies = pd.get_dummies(df['PaymentMethod'], prefix='Payment')

    X = pd.concat([
        df[['Month']],
        product_dummies,
        category_dummies,
        payment_dummies
    ], axis=1)

    if 'Quantity' not in df.columns:
        print("❌ 'Quantity' column not found.")
        return

    y = df['Quantity']

    # ✅ Split Dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ✅ Model Training
    model = LinearRegression()
    model.fit(X_train, y_train)

    # ✅ Model Evaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("\n✅ Quantity Prediction Model Evaluation:")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R² Score: {r2:.2f}")

    # ✅ Product-wise Prediction (Month=7)
    print("\n🛍️ Product-wise Quantity & Revenue Prediction (for July):")
    input_template = pd.DataFrame(0, index=[0], columns=X.columns)

    products = df['ProductName'].unique()
    category_wise_revenue = {}

    for product in products:
        row = input_template.copy()
        row.loc[0, 'Month'] = 7
        prod_col = f'Product_{product}'
        if prod_col in row.columns:
            row.loc[0, prod_col] = 1

        category = category_map.get(product, '')
        cat_col = f'Category_{category}'
        if cat_col in row.columns:
            row.loc[0, cat_col] = 1

        # payment method stays 0 (neutral)

        # ✅ Predict quantity
        quantity_pred = model.predict(row)[0]
        quantity_pred = max(int(round(quantity_pred)), 0)

        # ✅ Calculate revenue
        price = avg_price.get(product, 0)
        total_sales = quantity_pred * price

        print(f"→ {product}: Predicted Quantity: {quantity_pred}, Predicted Sales: ₹{total_sales:.2f}")

        if category in category_wise_revenue:
            category_wise_revenue[category] += total_sales
        else:
            category_wise_revenue[category] = total_sales

    # ✅ Category-wise Summary
    print("\n🏢 Category-wise Revenue Prediction (for July):")
    for category, revenue in category_wise_revenue.items():
        print(f"→ {category}: ₹{revenue:.2f}")


if __name__ == "__main__":
    sales_prediction()
