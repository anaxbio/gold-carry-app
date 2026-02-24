import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- ACTUAL DATA (Feb 24, 2026) ---
# Use the price of 1 full Guinea Lot from your broker terminal
MARCH_GUINEA_LOT_PRICE = 131644.00 
GUINEA_GRAM_CALC = MARCH_GUINEA_LOT_PRICE / 8

# Your SGB Series (SGBJUN31I)
MY_SGB_PRICE = 15920.00
MY_COST_BASIS = 15906.67
MY_QTY = 24 # 3 lots of 8

# Your Short Entry (The price where you actually sold the 3 lots)
MY_SHORT_ENTRY_LOT = 131600.00 
SHORT_ENTRY_GRAM = MY_SHORT_ENTRY_LOT / 8

st.title("🪙 Gold Guinea Carry Tracker")

# 1. THE HEDGE ACCOUNTING
st.subheader("📝 Hedge Summary")
col1, col2 = st.columns(2)

with col1:
    st.info(f"""
    **SGB Position (Buy)**
    * Quantity: {MY_QTY} units
    * Avg Cost: ₹{MY_COST_BASIS:,.2f}
    * Current: ₹{MY_SGB_PRICE:,.2f}
    """)

with col2:
    st.warning(f"""
    **MCX Position (Short)**
    * Quantity: 3 Lots (24g)
    * Avg Sell: ₹{SHORT_ENTRY_GRAM:,.2f} / g
    * Current: ₹{GUINEA_GRAM_CALC:,.2f} / g
    """)

st.divider()

# 2. THE REAL P&L (Net)
st.subheader("💰 Total Net Performance")
sgb_pnl = (MY_SGB_PRICE - MY_COST_BASIS) * MY_QTY
# Short P&L = (Entry - Current)
mcx_pnl = (SHORT_ENTRY_GRAM - GUINEA_GRAM_CALC) * MY_QTY
total_net = sgb_pnl + mcx_pnl

c1, c2, c3 = st.columns(3)
c1.metric("SGB P&L", f"₹{sgb_pnl:,.0f}")
c2.metric("MCX P&L", f"₹{mcx_pnl:,.0f}", delta_color="inverse")
c3.metric("NET PROFIT", f"₹{total_net:,.0f}", "Pure Arbitrage")

st.divider()

# 3. SWAP SCANNER
st.subheader("🔍 SGB Swap Scanner")
# Spot is ~16,080 today
spot = 16080 
scanner_data = [
    {"Symbol": "SGBJUN31I (Yours)", "Price": MY_SGB_PRICE, "Discount": f"{((spot-MY_SGB_PRICE)/spot)*100:.2f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot-15300)/spot)*100:.2f}%"},
    {"Symbol": "SGBMAY26", "Price": 15410, "Discount": f"{((spot-15410)/spot)*100:.2f}%"},
]
st.table(pd.DataFrame(scanner_data))
