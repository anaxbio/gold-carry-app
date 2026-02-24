import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- 1. SIDEBAR: PORTFOLIO EDITOR (Mobile Friendly) ---
st.sidebar.header("⚙️ My Portfolio Settings")

# Update your actual buy/sell info here
my_qty = st.sidebar.number_input("Units Held (24 units = 3 lots)", value=24, step=8)
my_sgb_cost = st.sidebar.number_input("My SGB Buy Price (Avg)", value=15906.67, format="%.2f")
my_guinea_sell_lot = st.sidebar.number_input("My Guinea Sell Price (Lot)", value=131600.0)

# --- 2. MARKET LTP (Updated Feb 24, 2026) ---
st.sidebar.header("📈 Market Live Rates")
live_sgb_ltp = st.sidebar.number_input("SGB Market Price", value=15920.0)
# March Guinea Lot is trading at ~1,31,644
live_guinea_lot_ltp = st.sidebar.number_input("Guinea March Lot Price", value=131644.0)

# --- 3. MATH ENGINE ---
my_guinea_sell_gram = my_guinea_sell_lot / 8
live_guinea_gram = live_guinea_lot_ltp / 8
spot_gold = 16082.0 # Current 24K Spot

# --- 4. MAIN DASHBOARD ---
st.title("🪙 Gold Guinea Carry Tracker")

c1, c2, c3 = st.columns(3)

# SGB Leg: (Market - Cost)
sgb_pnl = (live_sgb_ltp - my_sgb_cost) * my_qty
with c1:
    st.metric("SGB Leg P&L", f"₹{sgb_pnl:,.0f}", delta=f"Price: {live_sgb_ltp}")

# MCX Leg: (Sell Price - Current Price)
mcx_pnl = (my_guinea_sell_gram - live_guinea_gram) * my_qty
with c2:
    st.metric("MCX Hedge P&L", f"₹{mcx_pnl:,.0f}", delta=f"Price: {live_guinea_gram:.0f}", delta_color="inverse")

# NET PROFIT
total_net = sgb_pnl + mcx_pnl
with c3:
    st.metric("NET Carry Profit", f"₹{total_net:,.0f}", "Locked Spread")

st.divider()

# 5. SWAP SCANNER (Live Discount Calculation)
st.subheader("🔍 SGB Market Scanner")
scanner_data = [
    {"Symbol": "SGBJUN31I (Yours)", "Price": live_sgb_ltp, "Discount": f"{((spot_gold-live_sgb_ltp)/spot_gold)*100:.2f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot_gold-15300)/spot_gold)*100:.2f}%"},
    {"Symbol": "SGBMAY26", "Price": 15410, "Discount": f"{((spot_gold-15410)/spot_gold)*100:.2f}%"},
]
st.table(pd.DataFrame(scanner_data))

st.info("💡 **Pro-Tip:** If SGBJUN27 shows a discount > 5%, you can swap your JUN31 holdings to gain more gold grams instantly!")
