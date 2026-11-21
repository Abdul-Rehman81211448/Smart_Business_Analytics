import json
import os
from datetime import datetime
import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Smart Business & POS Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "pos_data.json"

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2rem;
        }
        .store-title {
            font-size: 1.85rem;
            font-weight: 700;
            line-height: 1.3;
            margin-top: 0.25rem;
            margin-bottom: 0.6rem;
            color: #0f172a;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        div[data-testid="stMetric"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 12px 14px;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def default_data():
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "store_name": "Al-Arifeen Store & Khata",
        "products": {
            "Oil Filter": 850.0,
            "Spark Plug": 600.0,
            "AC Gas Service": 3500.0,
            "Battery Terminal": 450.0,
            "Coolant Bottle": 1200.0,
        },
        "transactions": [
            {
                "Date": today,
                "Time": "09:30 AM",
                "Customer": "Walk-in Cash",
                "Item": "Spark Plug",
                "Qty": 2,
                "Unit_Price": 600.0,
                "Total": 1200.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": today,
                "Time": "11:15 AM",
                "Customer": "Kamran Traders",
                "Item": "AC Gas Service",
                "Qty": 1,
                "Unit_Price": 3500.0,
                "Total": 3500.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": today,
                "Time": "01:40 PM",
                "Customer": "Bilal Auto",
                "Item": "Oil Filter",
                "Qty": 2,
                "Unit_Price": 850.0,
                "Total": 1700.0,
                "Payment_Type": "Cash",
            },
        ],
        "udhaar_ledger": [
            {
                "Customer": "Kamran Traders",
                "Udhaar_Amount": 3500.0,
                "Status": "Pending",
                "Note": "AC Gas Service",
            },
            {
                "Customer": "Tariq Workshop",
                "Udhaar_Amount": 2500.0,
                "Status": "Pending",
                "Note": "Opening Balance",
            },
        ],
        "recovered_total": 0.0,
    }


def save_data():
    payload = {
        "store_name": st.session_state.store_name,
        "products": st.session_state.products,
        "transactions": st.session_state.transactions,
        "udhaar_ledger": st.session_state.udhaar_ledger,
        "recovered_total": st.session_state.recovered_total,
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            base = default_data()
            base.update(data)
            return base
        except Exception:
            return default_data()
    return default_data()


def init_state():
    if "initialized" not in st.session_state:
        data = load_data()
        st.session_state.store_name = data["store_name"]
        st.session_state.products = data["products"]
        st.session_state.transactions = data["transactions"]
        st.session_state.udhaar_ledger = data["udhaar_ledger"]
        st.session_state.recovered_total = float(data.get("recovered_total", 0.0))
        st.session_state.initialized = True
        save_data()


def add_udhaar_to_customer(customer: str, amount: float, note: str = "Udhaar Sale"):
    customer = customer.strip()
    amount = round(float(amount), 2)
    if amount <= 0:
        return
    for row in st.session_state.udhaar_ledger:
        if row["Customer"].lower() == customer.lower():
            row["Udhaar_Amount"] = round(float(row["Udhaar_Amount"]) + amount, 2)
            row["Status"] = "Pending"
            if note:
                row["Note"] = note
            return
    st.session_state.udhaar_ledger.append(
        {
            "Customer": customer,
            "Udhaar_Amount": amount,
            "Status": "Pending",
            "Note": note,
        }
    )


def recover_udhaar(customer: str, paid_amount: float):
    paid_amount = round(float(paid_amount), 2)
    if paid_amount <= 0:
        return False, "Enter an amount greater than 0."
    for row in st.session_state.udhaar_ledger:
        if row["Customer"] == customer:
            current_due = float(row["Udhaar_Amount"])
            if paid_amount > current_due:
                return False, f"Amount exceeds pending udhaar ({current_due:,.0f})."
            new_due = round(current_due - paid_amount, 2)
            row["Udhaar_Amount"] = new_due
            row["Status"] = "Cleared" if new_due == 0 else "Pending"
            st.session_state.recovered_total = round(
                float(st.session_state.recovered_total) + paid_amount, 2
            )
            save_data()
            return True, f"Received {paid_amount:,.0f} from {customer}."
    return False, "Customer not found in udhaar ledger."


def safe_clear_sales_only():
    st.session_state.transactions = []
    save_data()


init_state()

# --- Sidebar: Store Name, Product Price & Safe Clear ---
with st.sidebar:
    st.header("Shop Settings")
    new_store_name = st.text_input("Store Name", value=st.session_state.store_name)
    if new_store_name.strip() and new_store_name.strip() != st.session_state.store_name:
        st.session_state.store_name = new_store_name.strip()
        save_data()

    st.divider()
    st.subheader("Add / Update Product Price")
    prod_name = st.text_input("Product Name", placeholder="e.g. Brake Pad")
    prod_price = st.number_input("Price (PKR)", min_value=0.0, step=50.0, value=500.0)
    if st.button("Save Product", use_container_width=True):
        if prod_name.strip():
            st.session_state.products[prod_name.strip()] = float(prod_price)
            save_data()
            st.success(f"Saved {prod_name.strip()} ({prod_price:,.0f} PKR)")
        else:
            st.warning("Please enter a product name.")

    st.divider()
    st.subheader("Safe Reset")
    if st.button("Safe Clear Sales (Keep Udhaar)", use_container_width=True):
        safe_clear_sales_only()
        st.success("Sales cleared safely. Udhaar ledger preserved.")

# --- Clean Full Header ---
st.markdown(
    f'<div class="store-title">{st.session_state.store_name}</div>',
    unsafe_allow_html=True,
)

# --- Top Horizontal Navigation ---
nav_page = st.radio(
    "Navigation",
    options=["Home", "Dashboard", "List"],
    horizontal=True,
    label_visibility="collapsed",
)

df_tx = pd.DataFrame(st.session_state.transactions)
df_udhaar = pd.DataFrame(st.session_state.udhaar_ledger)

all_customers = ["All Customers"]
cust_names = set()
if not df_tx.empty and "Customer" in df_tx.columns:
    cust_names.update(df_tx["Customer"].dropna().unique().tolist())
if not df_udhaar.empty and "Customer" in df_udhaar.columns:
    cust_names.update(df_udhaar["Customer"].dropna().unique().tolist())
all_customers.extend(sorted(cust_names))

selected_customer = st.selectbox("Filter by Customer", options=all_customers)

if not df_tx.empty and selected_customer != "All Customers":
    filtered_tx = df_tx[df_tx["Customer"] == selected_customer].copy()
else:
    filtered_tx = df_tx.copy()

if not df_udhaar.empty and selected_customer != "All Customers":
    filtered_udhaar = df_udhaar[df_udhaar["Customer"] == selected_customer].copy()
else:
    filtered_udhaar = df_udhaar.copy()

total_sales = float(filtered_tx["Total"].sum()) if not filtered_tx.empty else 0.0
cash_sales = (
    float(filtered_tx[filtered_tx["Payment_Type"] == "Cash"]["Total"].sum())
    if not filtered_tx.empty
    else 0.0
)
udhaar_sales = (
    float(filtered_tx[filtered_tx["Payment_Type"] == "Udhaar"]["Total"].sum())
    if not filtered_tx.empty
    else 0.0
)
total_udhaar_due = (
    float(filtered_udhaar["Udhaar_Amount"].sum()) if not filtered_udhaar.empty else 0.0
)
items_sold = int(filtered_tx["Qty"].sum()) if not filtered_tx.empty else 0
recovered_cash = float(st.session_state.recovered_total)

st.divider()

# ==================== PAGE 1: HOME ====================
if nav_page == "Home":
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Sales", f"{total_sales:,.0f}")
    c2.metric("Cash Sales", f"{cash_sales:,.0f}")
    c3.metric("Udhaar Recovered", f"{recovered_cash:,.0f}")
    c4.metric("Pending Udhaar", f"{total_udhaar_due:,.0f}")
    c5.metric("Items Sold", f"{items_sold}")

    st.subheader("New Sale / POS Entry")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        customer_input = st.text_input("Customer Name", value="Walk-in Cash")
        item_choice = st.selectbox(
            "Select Product", options=list(st.session_state.products.keys())
        )

    with col_b:
        default_price = float(st.session_state.products.get(item_choice, 0.0))
        unit_price = st.number_input(
            "Unit Price", min_value=0.0, value=default_price, step=50.0
        )
        qty = st.number_input("Quantity", min_value=1, value=1, step=1)

    with col_c:
        payment_type = st.selectbox("Payment Mode", options=["Cash", "Udhaar"])
        line_total = float(unit_price) * int(qty)
        st.metric("Entry Total", f"{line_total:,.0f}")

    if st.button("Add Entry", type="primary"):
        now = datetime.now()
        clean_cust = (
            customer_input.strip() if customer_input.strip() else "Walk-in Cash"
        )
        entry = {
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%I:%M %p"),
            "Customer": clean_cust,
            "Item": item_choice,
            "Qty": int(qty),
            "Unit_Price": float(unit_price),
            "Total": float(line_total),
            "Payment_Type": payment_type,
        }
        st.session_state.transactions.append(entry)
        if payment_type == "Udhaar":
            add_udhaar_to_customer(clean_cust, line_total, note=item_choice)
        save_data()
        st.success("Entry added and saved locally.")
        st.rerun()

    st.divider()
    st.subheader("Udhaar Recovery (Receive Payment)")
    pending_rows = [
        r for r in st.session_state.udhaar_ledger if float(r["Udhaar_Amount"]) > 0
    ]
    if pending_rows:
        r_col1, r_col2, r_col3 = st.columns(3)
        with r_col1:
            rec_cust = st.selectbox(
                "Select Udhaar Customer",
                options=[r["Customer"] for r in pending_rows],
            )
        current_bal = next(
            float(r["Udhaar_Amount"])
            for r in pending_rows
            if r["Customer"] == rec_cust
        )
        with r_col2:
            st.metric("Pending Balance", f"{current_bal:,.0f}")
        with r_col3:
            rec_amt = st.number_input(
                "Amount Received",
                min_value=0.0,
                max_value=current_bal,
                value=min(500.0, current_bal),
                step=50.0,
            )

        if st.button("Record Udhaar Payment"):
            ok, msg = recover_udhaar(rec_cust, rec_amt)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    else:
        st.info("No pending udhaar balances right now.")

# ==================== PAGE 2: DASHBOARD ====================
elif nav_page == "Dashboard":
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sales", f"{total_sales:,.0f}")
    k2.metric("Cash Sales", f"{cash_sales:,.0f}")
    k3.metric("Udhaar Sales", f"{udhaar_sales:,.0f}")
    k4.metric("Pending Udhaar", f"{total_udhaar_due:,.0f}")

    if not filtered_tx.empty:
        chart_df = filtered_tx.copy()
        chart_df["Step"] = range(1, len(chart_df) + 1)
        chart_df["Cumulative_Amount"] = chart_df["Total"].cumsum()

        st.subheader("Stepwise Amount Movement (Live Update)")
        step_chart = (
            alt.Chart(chart_df)
            .mark_line(point=True, strokeWidth=3)
            .encode(
                x=alt.X("Step:O", title="Entry Step"),
                y=alt.Y("Cumulative_Amount:Q", title="Cumulative Amount"),
                color=alt.Color("Payment_Type:N", title="Type"),
                tooltip=[
                    "Step",
                    "Customer",
                    "Item",
                    "Total",
                    "Payment_Type",
                    "Cumulative_Amount",
                ],
            )
            .properties(height=300)
            .interactive()
        )
        st.altair_chart(step_chart, use_container_width=True)

        st.subheader("Cash vs Udhaar Breakdown")
        mode_df = filtered_tx.groupby("Payment_Type", as_index=False)["Total"].sum()
        bar_chart = (
            alt.Chart(mode_df)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("Payment_Type:N", title="Payment Type"),
                y=alt.Y("Total:Q", title="Amount"),
                color=alt.Color("Payment_Type:N", legend=None),
                tooltip=["Payment_Type", "Total"],
            )
            .properties(height=280)
        )
        st.altair_chart(bar_chart, use_container_width=True)
    else:
        st.info("No transactions available for the selected filter.")

# ==================== PAGE 3: LIST ====================
elif nav_page == "List":
    st.subheader("Transactions List (Cash & Udhaar)")
    if not filtered_tx.empty:
        st.dataframe(filtered_tx, use_container_width=True, hide_index=True)

        if len(st.session_state.transactions) > 0:
            del_idx = st.selectbox(
                "Select Row Index to Delete",
                options=list(range(len(st.session_state.transactions))),
                format_func=lambda i: f"#{i+1} - {st.session_state.transactions[i]['Customer']} ({st.session_state.transactions[i]['Item']} - {st.session_state.transactions[i]['Total']:,.0f})",
            )
            if st.button("Delete Selected Transaction"):
                st.session_state.transactions.pop(del_idx)
                save_data()
                st.success("Transaction deleted.")
                st.rerun()

        csv_data = filtered_tx.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Transactions CSV",
            data=csv_data,
            file_name="transactions_list.csv",
            mime="text/csv",
        )
    else:
        st.info("No transaction records to display.")

    st.divider()
    st.subheader("Udhaar / Credit Khata List")
    if not filtered_udhaar.empty:
        st.dataframe(filtered_udhaar, use_container_width=True, hide_index=True)
    else:
        st.info("No udhaar records for the selected filter.")

    st.divider()
    st.subheader("Products & Price List")
    prod_df = pd.DataFrame(
        [{"Product": k, "Price": v} for k, v in st.session_state.products.items()]
    )
    st.dataframe(prod_df, use_container_width=True, hide_index=True)
