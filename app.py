import streamlit as st
import pandas as pd

st.title("Smart Business Analytics Dashboard")
st.write("Welcome Abdul-Rehman! Your business analytics dashboard is now live.")

products_data = {
    "product_id": [1, 2],
    "product_name": ["Tea", "Biscuit"],
    "price": [50.00, 30.00],
    "stock_quantity": [100, 200]
}
df_products = pd.DataFrame(products_data)

st.subheader("Products Inventory")
st.dataframe(df_products)

sales_data = {
    "sale_id": [1, 2, 3],
    "product_id": [1, 2, 1],
    "quantity_sold": [5, 10, 8],
    "total_amount": [250.00, 300.00, 400.00],
    "sale_date": ["2026-11-01", "2026-11-01", "2026-11-02"]
}
df_sales = pd.DataFrame(sales_data)

st.subheader("Sales Performance")
st.dataframe(df_sales)

st.bar_chart(df_sales.set_index("sale_id")["total_amount"])
