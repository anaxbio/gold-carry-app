import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- DATA (Update these manually or via scraper) ---
LIVE_SGB_PRICE = 15920.00
LIVE_GUINEA_GRAM = 16486.00 # MCX March Guinea divided by 8

# Your Actual Entries
SGB_AVG_BUY = 15906.67
MCX_AVG_SELL = 16455.00 # The price at which you shorted
qty = 24

st.title("🪙 SGB-MCX Two-Leg Dashboard")

# 1. THE "NET" CARRY VIEW
st.subheader("📊 Combined Portfolio Performance")
col1, col2, col3 = st.columns(3)

# Leg 1: SGB
sgb_pnl = (LIVE_SGB_PRICE - SGB_AVG_BUY) * qty
with col1:
    st.metric("SGB Leg P&L", f"₹{sgb_pnl:.0f}", delta=f"Price: {LIVE_SGB_PRICE}")

# Leg 2: MCX (Loss here is expected if gold goes up!)
# P&L for Short = (Sell Price - Buy Price)
mcx_pnl = (MCX_AVG_SELL - LIVE_GUINEA_GRAM) * qty
with col2:
    st.metric("MCX Hedge P&L", f"₹{mcx_pnl:.0f}", delta=f"Price: {LIVE_GUINEA_GRAM:.0f}", delta_color="inverse")

# THE REAL NET PROFIT
net_pnl = sgb_pnl + mcx_pnl
with col3:
    st.metric("NET Carry Profit", f"₹{net_pnl:.0f}", "Locked Spread")

st.divider()

# 2. ANALYSIS
st.info(f"""
💡 **Why is MCX showing a loss?** Because Gold prices rose! But look at your SGB leg—it gained **more** than the MCX lost. 
The difference (**₹{net_pnl:.0f}**) is your 'Arbitrage' profit.
""")

# 3. SCANNER
st.subheader("🔍 SGB Market Scanner")
# Spot is ~16,100 today
spot = 16100 
sgb_data = [
    {"Symbol": "SGBJUN31I", "Price": LIVE_SGB_PRICE, "Discount": f"{((spot-LIVE_SGB_PRICE)/spot)*100:.1f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot-15300)/spot)*100:.1f}%"},
]
st.table(pd.DataFrame(sgb_data))
