import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- DYNAMIC DATA FETCHING ---
@st.cache_data(ttl=600) # This keeps the data for 10 mins so we don't get blocked
def get_live_gold():
    # 'GC=F' is the symbol for Global Gold Futures
    # 'INR=X' is the USD to INR exchange rate
    gold = yf.Ticker("GC=F").fast_info['last_price']
    usd_inr = yf.Ticker("INR=X").fast_info['last_price']
    
    # Simple math to get approx MCX price per gram
    # (Price per ounce / 31.1035) * USD_INR
    mcx_approx = (gold / 31.1035) * usd_inr
    return mcx_approx

try:
    live_gram_price = get_live_gold()
except:
    live_gram_price = 16050.0 # Fallback if Yahoo is down

# --- YOUR PORTFOLIO ---
MY_COST_BASIS = 15906.67
qty = 24

# --- APP UI ---
st.title("🪙 My Dynamic Gold Carry Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Live Gold (Per Gram)", f"₹{live_gram_price:.2f}")
with col2:
    # Your 3 lots of Guinea (24g)
    current_value = live_gram_price * qty
    st.metric("Hedge Value (24g)", f"₹{current_value:.0f}")
with col3:
    # Carry = (Market - Cost)
    carry_profit = (live_gram_price - MY_COST_BASIS) * qty
    st.metric("Est. Carry P&L", f"₹{carry_profit:.0f}", "Live")

st.divider()

# --- SGB SCANNER (Manual for now, but linked to live spot) ---
st.subheader("🔍 SGB Market Scanner")
sgb_data = [
    {"Symbol": "SGBJUN31I", "Offer": 15920},
    {"Symbol": "SGBMAY26", "Offer": 15410},
    {"Symbol": "SGBJUN27", "Offer": 15300},
]

for sgb in sgb_data:
    discount = ((live_gram_price - sgb['Offer']) / live_gram_price) * 100
    sgb['Live Discount'] = f"{discount:.2f}%"

st.table(pd.DataFrame(sgb_data))
