import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Business Analytics", layout="wide")

st.title("Smart Business Analytics Dashboard")
st.markdown("Interactive sales, inventory, and profit performance overview.")

# Products Data (including cost_price for profit calculation)
products_data = {
    "product_id": [1, 2, 3, 4, 5],
    "product_name": ["Tea", "Biscuit", "Coffee", "Sugar (1kg)", "Cooking Oil (1L)"],
    "price": [50.00, 30.00, 120.00, 150.00, 520.00],
    "cost_price": [30.00, 20.00, 80.00, 130.00, 460.00],
    "stock_quantity": [100, 200, 75, 150, 90]
}
df_products = pd.DataFrame(products_data)

# Sales Data
sales_data = {
    "sale_id": [1, 2, 3, 4, 5, 6, 7],
    "product_id": [1, 2, 1, 3, 4, 5, 2],
    "quantity_sold": [5, 10, 8, 4, 6, 3, 15],
    "sale_date": [
        "2026-11-01", "2026-11-01", "2026-11-02",
        "2026-11-02", "2026-11-03", "2026-11-03", "2026-11-04"
    ]
}
df_sales = pd.DataFrame(sales_data)

# Merge sales and products to calculate Revenue and Profit
df_merged = pd.merge(df_sales, df_products, on="product_id")
df_merged["total_revenue"] = df_merged["quantity_sold"] * df_merged["price"]
df_merged["total_cost"] = df_merged["quantity_sold"] * df_merged["cost_price"]
df_merged["profit"] = df_merged["total_revenue"] - df_merged["total_cost"]

# Sidebar Filter
st.sidebar.header("Filter Options")
selected_products = st.sidebar.multiselect(
    "Select Products:",
    options=df_products["product_name"].unique(),
    default=df_products["product_name"].unique()
)

filtered_df = df_merged[df_merged["product_name"].isin(selected_products)]

# Top KPI Metrics
total_rev = filtered_df["total_revenue"].sum()
total_prof = filtered_df["profit"].sum()
total_units = filtered_df["quantity_sold"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (PKR)", f"{total_rev:,.2f}")
col2.metric("Total Profit (PKR)", f"{total_prof:,.2f}")
col3.metric("Total Units Sold", f"{total_units}")

st.divider()

# Charts Section
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue by Product")
    rev_by_prod = filtered_df.groupby("product_name")["total_revenue"].sum()
    st.bar_chart(rev_by_prod)

with chart_col2:
    st.subheader("Profit by Product")
    prof_by_prod = filtered_df.groupby("product_name")["profit"].sum()
    st.bar_chart(prof_by_prod)

st.divider()

# Detailed Tables
st.subheader("Detailed Sales Transactions")
st.dataframe(
    filtered_df[["sale_id", "sale_date", "product_name", "quantity_sold", "total_revenue", "profit"]],
    use_container_width=True
)

st.subheader("Current Products Inventory")
st.dataframe(df_products, use_container_width=True)
