import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- 1. SIDEBAR: PORTFOLIO EDITOR (Mobile Friendly) ---
st.sidebar.header("⚙️ My Portfolio Settings")

# Using number_input instead of a table for better mobile support
my_sgb_series = st.sidebar.text_input("SGB Series Name", value="SGBJUN31I")
my_qty = st.sidebar.number_input("Units (Must be multiple of 8)", value=24, step=8)
my_sgb_cost = st.sidebar.number_input("SGB Buy Price (per gram)", value=15906.67, format="%.2f")
my_guinea_sell_lot = st.sidebar.number_input("Guinea Sell Price (Full Lot)", value=131600.0, step=100.0)

# --- 2. MARKET PRICES (Update these as per LTP) ---
st.sidebar.header("📈 Market LTP")
live_sgb_ltp = st.sidebar.number_input("Live SGB Price", value=15920.0)
live_guinea_lot_ltp = st.sidebar.number_input("Live Guinea Lot Price", value=131644.0)

# --- 3. THE MATH ENGINE ---
my_guinea_sell_gram = my_guinea_sell_lot / 8
live_guinea_gram = live_guinea_lot_ltp / 8

# --- 4. MAIN DASHBOARD ---
st.title("🪙 Gold Guinea Carry Tracker")

col1, col2, col3 = st.columns(3)

# Leg 1: SGB
sgb_pnl = (live_sgb_ltp - my_sgb_cost) * my_qty
with col1:
    st.metric("SGB Leg P&L", f"₹{sgb_pnl:,.0f}", delta=f"Price: {live_sgb_ltp}")

# Leg 2: MCX
mcx_pnl = (my_guinea_sell_gram - live_guinea_gram) * my_qty
with col2:
    st.metric("MCX Hedge P&L", f"₹{mcx_pnl:,.0f}", delta=f"Price: {live_guinea_gram:.0f}", delta_color="inverse")

# THE NET PROFIT
net_pnl = sgb_pnl + mcx_pnl
with col3:
    st.metric("NET Carry Profit", f"₹{net_pnl:,.0f}", "Locked Spread")

st.divider()

# 5. SCANNER (Simplified)
st.subheader("🔍 SGB Market Scanner")
spot = 16080 
scanner_data = [
    {"Symbol": my_sgb_series, "Price": live_sgb_ltp, "Discount": f"{((spot-live_sgb_ltp)/spot)*100:.2f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot-15300)/spot)*100:.2f}%"},
]
st.table(pd.DataFrame(scanner_data))
