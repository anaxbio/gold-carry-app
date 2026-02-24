import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- 1. PORTFOLIO EDITOR (ELI5: The Mini-Excel) ---
st.title("🪙 Gold Guinea Carry Tracker")

st.subheader("📝 Manage Your Portfolio")
st.info("Edit the table below to update your trade prices or quantity. It updates everything instantly!")

# Initial data for your 3 lots
if 'portfolio_df' not in st.session_state:
    st.session_state.portfolio_df = pd.DataFrame([
        {
            "SGB Series": "SGBJUN31I",
            "Units": 24,
            "SGB Buy Price": 15906.67,
            "Guinea Sell Price (Lot)": 131600.00
        }
    ])

# Display the editable table
edited_df = st.data_editor(st.session_state.portfolio_df, num_rows="dynamic")
st.session_state.portfolio_df = edited_df

# --- 2. CURRENT MARKET PRICES (Hardcoded or Scraped) ---
# Update these as per market LTP
LIVE_SGB_LTP = 15920.00
LIVE_GUINEA_LOT_LTP = 131644.00

# --- 3. THE MATH ENGINE ---
# We take the first row of your edited table for calculations
row = edited_df.iloc[0]
my_qty = row["Units"]
my_sgb_cost = row["SGB Buy Price"]
my_guinea_sell_gram = row["Guinea Sell Price (Lot)"] / 8
live_guinea_gram = LIVE_GUINEA_LOT_LTP / 8

st.divider()

# --- 4. LIVE PERFORMANCE ---
st.subheader("💰 Live Performance")
sgb_pnl = (LIVE_SGB_LTP - my_sgb_cost) * my_qty
mcx_pnl = (my_guinea_sell_gram - live_guinea_gram) * my_qty
total_net = sgb_pnl + mcx_pnl

c1, c2, c3 = st.columns(3)
c1.metric("SGB P&L", f"₹{sgb_pnl:,.0f}")
c2.metric("MCX P&L", f"₹{mcx_pnl:,.0f}", delta_color="inverse")
c3.metric("NET PROFIT", f"₹{total_net:,.0f}", "Pure Carry")

# --- 5. THE SWAP SCANNER ---
st.divider()
st.subheader("🔍 SGB Market Scanner")
spot = 16080 
scanner_data = [
    {"Symbol": row["SGB Series"], "Price": LIVE_SGB_LTP, "Discount": f"{((spot-LIVE_SGB_LTP)/spot)*100:.2f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot-15300)/spot)*100:.2f}%"},
]
st.table(pd.DataFrame(scanner_data))
