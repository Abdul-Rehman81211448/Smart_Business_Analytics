import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Business POS & Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = "pos_data.json"

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f1f5f9;
            color: #0f172a;
        }
        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
        }
        [data-testid="stSidebar"] {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] .stNumberInput input {
            color: #0f172a !important;
            background-color: #ffffff !important;
        }
        .store-title {
            font-size: 1.9rem;
            font-weight: 700;
            line-height: 1.25;
            letter-spacing: -0.02em;
            color: #0f172a;
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-left: 6px solid #1e3a8a;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 14px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-top: 3px solid #1e3a8a;
            padding: 14px 16px;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
        }
        div[data-testid="stMetric"] label {
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 1.55rem !important;
        }
        .stButton > button,
        .stDownloadButton > button {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            border: 1px solid #1e3a8a !important;
            border-radius: 6px !important;
            padding: 0.55rem 1.15rem !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            letter-spacing: 0.01em;
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background-color: #172554 !important;
            border-color: #172554 !important;
            color: #ffffff !important;
        }
        div[role="radiogroup"] {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 6px 10px;
            gap: 10px;
        }
        div[role="radiogroup"] label {
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 16px !important;
            margin-right: 4px !important;
            font-weight: 600 !important;
            color: #1e293b !important;
        }
        div[role="radiogroup"] label:has(input:checked) {
            background-color: #0f172a !important;
            border-color: #0f172a !important;
            color: #ffffff !important;
        }
        div[role="radiogroup"] label:has(input:checked) p {
            color: #ffffff !important;
        }
        .section-heading {
            font-size: 1.15rem;
            font-weight: 700;
            color: #0f172a;
            margin-top: 0.4rem;
            margin-bottom: 0.6rem;
            padding-bottom: 0.35rem;
            border-bottom: 2px solid #cbd5e1;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def default_data():
    return {
        "store_name": "Al-Madina Mart & General Store",
        "products": {
            "Basmati Rice 5kg": 1850.0,
            "Cooking Oil 5L": 2650.0,
            "Sugar 5kg": 920.0,
            "Tea Pack 900g": 1540.0,
            "Washing Powder 3kg": 1150.0,
            "Dishwash Liquid 1L": 480.0,
            "Shampoo Bottle": 790.0,
            "Biscuit Carton": 1400.0,
            "Mineral Water Crate": 840.0,
            "Tissue Box Pack": 650.0,
        },
        "transactions": [
            {
                "Date": "2026-11-21",
                "Time": "08:45 AM",
                "Customer": "Walk-in Cash",
                "Item": "Tea Pack 900g",
                "Qty": 2,
                "Unit_Price": 1540.0,
                "Total": 3080.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "09:15 AM",
                "Customer": "Usman General Store",
                "Item": "Basmati Rice 5kg",
                "Qty": 5,
                "Unit_Price": 1850.0,
                "Total": 9250.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "09:50 AM",
                "Customer": "Walk-in Cash",
                "Item": "Dishwash Liquid 1L",
                "Qty": 3,
                "Unit_Price": 480.0,
                "Total": 1440.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "10:25 AM",
                "Customer": "Haji Tariq Mart",
                "Item": "Cooking Oil 5L",
                "Qty": 4,
                "Unit_Price": 2650.0,
                "Total": 10600.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "11:05 AM",
                "Customer": "Ayesha Provision",
                "Item": "Sugar 5kg",
                "Qty": 6,
                "Unit_Price": 920.0,
                "Total": 5520.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "11:45 AM",
                "Customer": "Usman General Store",
                "Item": "Washing Powder 3kg",
                "Qty": 4,
                "Unit_Price": 1150.0,
                "Total": 4600.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "12:30 PM",
                "Customer": "Walk-in Cash",
                "Item": "Mineral Water Crate",
                "Qty": 5,
                "Unit_Price": 840.0,
                "Total": 4200.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "01:20 PM",
                "Customer": "Faisal Traders",
                "Item": "Biscuit Carton",
                "Qty": 3,
                "Unit_Price": 1400.0,
                "Total": 4200.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "02:10 PM",
                "Customer": "Ayesha Provision",
                "Item": "Shampoo Bottle",
                "Qty": 4,
                "Unit_Price": 790.0,
                "Total": 3160.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "02:55 PM",
                "Customer": "Haji Tariq Mart",
                "Item": "Tissue Box Pack",
                "Qty": 6,
                "Unit_Price": 650.0,
                "Total": 3900.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "03:40 PM",
                "Customer": "Walk-in Cash",
                "Item": "Basmati Rice 5kg",
                "Qty": 3,
                "Unit_Price": 1850.0,
                "Total": 5550.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "04:20 PM",
                "Customer": "Sana Departmental",
                "Item": "Cooking Oil 5L",
                "Qty": 3,
                "Unit_Price": 2650.0,
                "Total": 7950.0,
                "Payment_Type": "Udhaar",
            },
            {
                "Date": "2026-11-21",
                "Time": "05:05 PM",
                "Customer": "Faisal Traders",
                "Item": "Sugar 5kg",
                "Qty": 5,
                "Unit_Price": 920.0,
                "Total": 4600.0,
                "Payment_Type": "Cash",
            },
            {
                "Date": "2026-11-21",
                "Time": "05:45 PM",
                "Customer": "Sana Departmental",
                "Item": "Biscuit Carton",
                "Qty": 4,
                "Unit_Price": 1400.0,
                "Total": 5600.0,
                "Payment_Type": "Udhaar",
            },
        ],
        "udhaar_ledger": [
            {
                "Customer": "Usman General Store",
                "Udhaar_Amount": 13850.0,
                "Status": "Pending",
                "Note": "Rice & Washing Powder",
            },
            {
                "Customer": "Haji Tariq Mart",
                "Udhaar_Amount": 14500.0,
                "Status": "Pending",
                "Note": "Cooking Oil & Tissue",
            },
            {
                "Customer": "Faisal Traders",
                "Udhaar_Amount": 4200.0,
                "Status": "Pending",
                "Note": "Biscuit Carton",
            },
            {
                "Customer": "Sana Departmental",
                "Udhaar_Amount": 13550.0,
                "Status": "Pending",
                "Note": "Oil & Biscuits",
            },
        ],
        "recovered_total": 4500.0,
    }


def save_data():
    payload = {
        "store_name": st.session_state.store_name,
        "products": st.session_state.products,
        "transactions": st.session_state.transactions,
        "udhaar_ledger": st.session_state.udhaar_ledger,
        "recovered_total": st.session_state.recovered_total,
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def load_data():
    base = default_data()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data.get("transactions"):
                base.update(data)
        except Exception:
            return base
    return base


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

with st.sidebar:
    st.markdown("### Store Configuration")
    new_store_name = st.text_input("Business Name", value=st.session_state.store_name)
    if new_store_name.strip() and new_store_name.strip() != st.session_state.store_name:
        st.session_state.store_name = new_store_name.strip()
        save_data()

    st.divider()
    st.markdown("### Product Pricing")
    prod_name = st.text_input("Item Name", placeholder="e.g. Brake Pad")
    prod_price = st.number_input("Rate (PKR)", min_value=0.0, step=50.0, value=500.0)
    if st.button("Save Rate", use_container_width=True):
        if prod_name.strip():
            st.session_state.products[prod_name.strip()] = float(prod_price)
            save_data()
            st.success(f"Saved {prod_name.strip()} at {prod_price:,.0f} PKR")
        else:
            st.warning("Enter an item name first.")

    st.divider()
    st.markdown("### Safe Reset")
    if st.button("Safe Clear Sales", use_container_width=True):
        safe_clear_sales_only()
        st.success("Sales reset. Udhaar ledger remains intact.")

st.markdown(
    f'<div class="store-title">{st.session_state.store_name}</div>',
    unsafe_allow_html=True,
)

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

selected_customer = st.selectbox("Customer Filter", options=all_customers)

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

if nav_page == "Home":
    st.markdown('<div class="section-heading">New Sale Entry</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        customer_input = st.text_input("Customer Name", value="Walk-in Cash")
        item_choice = st.selectbox(
            "Product", options=list(st.session_state.products.keys())
        )

    with col_b:
        default_price = float(st.session_state.products.get(item_choice, 0.0))
        unit_price = st.number_input(
            "Unit Price (PKR)", min_value=0.0, value=default_price, step=50.0
        )
        qty = st.number_input("Quantity", min_value=1, value=1, step=1)

    with col_c:
        payment_type = st.selectbox("Payment Mode", options=["Cash", "Udhaar"])
        line_total = float(unit_price) * int(qty)
        st.metric("Bill Total (PKR)", f"{line_total:,.0f}")

    if st.button("Add Sale Entry"):
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
        st.success("Sale entry recorded.")
        st.rerun()

    st.markdown('<div class="section-heading">Udhaar Recovery</div>', unsafe_allow_html=True)
    pending_rows = [
        r for r in st.session_state.udhaar_ledger if float(r["Udhaar_Amount"]) > 0
    ]
    if pending_rows:
        r_col1, r_col2, r_col3 = st.columns(3)
        with r_col1:
            rec_cust = st.selectbox(
                "Customer Account",
                options=[r["Customer"] for r in pending_rows],
            )
        current_bal = next(
            float(r["Udhaar_Amount"])
            for r in pending_rows
            if r["Customer"] == rec_cust
        )
        with r_col2:
            st.metric("Pending Balance (PKR)", f"{current_bal:,.0f}")
        with r_col3:
            rec_amt = st.number_input(
                "Received Amount (PKR)",
                min_value=0.0,
                max_value=current_bal,
                value=min(500.0, current_bal),
                step=50.0,
            )

        if st.button("Record Payment"):
            ok, msg = recover_udhaar(rec_cust, rec_amt)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    else:
        st.info("No pending udhaar accounts.")

elif nav_page == "Dashboard":
    tx_count = len(filtered_tx)
    avg_ticket = (total_sales / tx_count) if tx_count > 0 else 0.0
    cash_share = ((cash_sales / total_sales) * 100) if total_sales > 0 else 0.0
    udhaar_share = ((udhaar_sales / total_sales) * 100) if total_sales > 0 else 0.0

    st.markdown('<div class="section-heading">Performance Analytics</div>', unsafe_allow_html=True)
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Transactions Count", f"{tx_count}")
    d2.metric("Average Ticket (PKR)", f"{avg_ticket:,.0f}")
    d3.metric("Cash Share", f"{cash_share:.1f}%")
    d4.metric("Udhaar Share", f"{udhaar_share:.1f}%")

    if not filtered_tx.empty:
        chart_df = filtered_tx.copy()
        chart_df["Total"] = pd.to_numeric(chart_df["Total"], errors="coerce").fillna(0.0)
        chart_df["Entry"] = [f"#{i + 1}" for i in range(len(chart_df))]
        chart_df["Cumulative Revenue (PKR)"] = chart_df["Total"].cumsum()

        st.markdown('<div class="section-heading">Cumulative Revenue Progression</div>', unsafe_allow_html=True)
        line_data = chart_df.set_index("Entry")[["Cumulative Revenue (PKR)"]]
        st.line_chart(line_data, height=300, use_container_width=True)

        st.markdown('<div class="section-heading">Payment Mode Comparison</div>', unsafe_allow_html=True)
        mode_series = chart_df.groupby("Payment_Type")["Total"].sum()
        bar_data = pd.DataFrame({"Amount (PKR)": mode_series})
        st.bar_chart(bar_data, height=280, use_container_width=True)
    else:
        st.info("No transaction records available for this filter.")

elif nav_page == "List":
    st.markdown('<div class="section-heading">Transactions Ledger</div>', unsafe_allow_html=True)
    if not filtered_tx.empty:
        st.dataframe(filtered_tx, use_container_width=True, hide_index=True)

        if len(st.session_state.transactions) > 0:
            del_idx = st.selectbox(
                "Select Entry to Remove",
                options=list(range(len(st.session_state.transactions))),
                format_func=lambda i: f"#{i+1} - {st.session_state.transactions[i]['Customer']} ({st.session_state.transactions[i]['Item']} - {st.session_state.transactions[i]['Total']:,.0f})",
            )
            if st.button("Delete Entry"):
                st.session_state.transactions.pop(del_idx)
                save_data()
                st.success("Entry removed.")
                st.rerun()

        csv_data = filtered_tx.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export CSV",
            data=csv_data,
            file_name="transactions_ledger.csv",
            mime="text/csv",
        )
    else:
        st.info("No transactions to show.")

    st.markdown('<div class="section-heading">Udhaar Khata</div>', unsafe_allow_html=True)
    if not filtered_udhaar.empty:
        st.dataframe(filtered_udhaar, use_container_width=True, hide_index=True)
    else:
        st.info("No udhaar records for this filter.")

    st.markdown('<div class="section-heading">Product Rate List</div>', unsafe_allow_html=True)
    prod_df = pd.DataFrame(
        [{"Product": k, "Rate (PKR)": v} for k, v in st.session_state.products.items()]
    )
    st.dataframe(prod_df, use_container_width=True, hide_index=True)
