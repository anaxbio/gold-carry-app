import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙")

st.title("🪙 SGB-MCX Carry Tracker")

# 1. USER INPUTS
st.sidebar.header("Your Portfolio")
held_sgb = st.sidebar.number_input("SGB Units Held", value=40, step=8)
avg_cost = st.sidebar.number_input("Avg Purchase Price", value=7500)

# 2. THE 8-GRAM LOGIC
hedge_needed = held_sgb // 8
st.metric("Hedge Needed", f"{hedge_needed} Lots (Gold Guinea)")

# 3. TRACKER SECTION
col1, col2 = st.columns(2)
with col1:
    sgb_price = st.number_input("Live SGB Price (NSE)", value=8000)
with col2:
    mcx_price = st.number_input("Live Guinea Price (MCX)", value=8200)

# 4. CALCULATIONS
spread = mcx_price - sgb_price
discount = ((8200 - sgb_price)/8200) * 100 # Approx vs spot

st.divider()
st.subheader("Market Analysis")
st.write(f"Current Profit Gap: **₹{spread} per unit**")
st.write(f"Estimated Discount: **{discount:.2f}%**")

if discount > 4:
    st.success("🔥 ACTION: SGB is cheap. Good time to enter/add.")
elif discount < 1:
    st.warning("⚠️ ACTION: SGB is expensive. Consider 'Swapping' or Booking Profit.")

# 5. EXPIRY WARNING
st.info("💡 REMINDER: Roll your MCX hedge 6 days before expiry to avoid margin spikes!")
