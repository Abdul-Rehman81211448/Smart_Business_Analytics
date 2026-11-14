import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Business Analytics", layout="wide")

st.title("Smart Business Analytics Dashboard")
st.markdown("Interactive sales, inventory, and profit performance overview.")

# Initialize Session State
if "df_products" not in st.session_state:
    st.session_state.df_products = pd.DataFrame({
        "product_id": [1, 2, 3, 4, 5],
        "product_name": ["Tea", "Biscuit", "Coffee", "Sugar (1kg)", "Cooking Oil (1L)"],
        "price": [50.00, 30.00, 120.00, 150.00, 520.00],
        "cost_price": [30.00, 20.00, 80.00, 130.00, 460.00],
        "stock_quantity": [100, 200, 75, 150, 90]
    })

if "df_sales" not in st.session_state:
    st.session_state.df_sales = pd.DataFrame({
        "sale_id": [1, 2, 3, 4, 5, 6, 7],
        "product_id": [1, 2, 1, 3, 4, 5, 2],
        "quantity_sold": [5, 10, 8, 4, 6, 3, 15],
        "sale_date": [
            "2026-11-01", "2026-11-01", "2026-11-02",
            "2026-11-02", "2026-11-03", "2026-11-03", "2026-11-04"
        ]
    })

df_products = st.session_state.df_products
df_sales = st.session_state.df_sales

# Merge data for calculation
df_merged = pd.merge(df_sales, df_products, on="product_id")
df_merged["total_revenue"] = df_merged["quantity_sold"] * df_merged["price"]
df_merged["total_cost"] = df_merged["quantity_sold"] * df_merged["cost_price"]
df_merged["profit"] = df_merged["total_revenue"] - df_merged["total_cost"]

# Sidebar - Filters & Management
st.sidebar.header("Filter Options")
selected_products = st.sidebar.multiselect(
    "Select Products:",
    options=df_products["product_name"].unique(),
    default=df_products["product_name"].unique()
)

filtered_df = df_merged[df_merged["product_name"].isin(selected_products)]

# Sidebar - Add New Product Form
st.sidebar.divider()
st.sidebar.header("📦 Add New Product")
with st.sidebar.form("product_form"):
    new_pname = st.text_input("Product Name")
    new_price = st.number_input("Selling Price (PKR)", min_value=1.0, value=100.0)
    new_cost = st.number_input("Cost Price (PKR)", min_value=1.0, value=70.0)
    new_stock = st.number_input("Stock Quantity", min_value=1, value=50)
    prod_submit = st.form_submit_button("Add Product")

    if prod_submit and new_pname:
        new_pid = int(df_products["product_id"].max() + 1)
        new_prod_row = pd.DataFrame({
            "product_id": [new_pid],
            "product_name": [new_pname],
            "price": [new_price],
            "cost_price": [new_cost],
            "stock_quantity": [new_stock]
        })
        st.session_state.df_products = pd.concat([st.session_state.df_products, new_prod_row], ignore_index=True)
        st.rerun()

# Sidebar - Add New Sale Form
st.sidebar.divider()
st.sidebar.header("➕ Add New Sale")
with st.sidebar.form("sale_form"):
    new_prod_name = st.selectbox("Product for Sale", options=df_products["product_name"].tolist())
    new_qty = st.number_input("Quantity Sold", min_value=1, value=1)
    new_date = st.date_input("Sale Date")
    submit_btn = st.form_submit_button("Add Sale Record")

    if submit_btn:
        prod_row = df_products[df_products["product_name"] == new_prod_name].iloc[0]
        new_sale_id = int(df_sales["sale_id"].max() + 1)
        new_row = pd.DataFrame({
            "sale_id": [new_sale_id],
            "product_id": [prod_row["product_id"]],
            "quantity_sold": [new_qty],
            "sale_date": [str(new_date)]
        })
        st.session_state.df_sales = pd.concat([st.session_state.df_sales, new_row], ignore_index=True)
        st.rerun()

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

# Detailed Tables & Download Button
st.subheader("Detailed Sales Transactions")
st.dataframe(
    filtered_df[["sale_id", "sale_date", "product_name", "quantity_sold", "total_revenue", "profit"]],
    use_container_width=True
)

# CSV Download Button
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name="smart_business_report.csv",
    mime="text/csv",
)

st.subheader("Current Products Inventory")
st.dataframe(df_products, use_container_width=True)
