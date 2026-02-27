import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gold Carry Pro", page_icon="🪙", layout="wide")

# --- 1. SGB MAPPING ---
MC_MAP = {
    "SGBNOV25VI": "SGBNO398", "SGBDEC2512": "SGBDE795", "SGBDEC25XI": "SGBDE729", 
    "SGBDEC2513": "SGBDE862", "SGBJUN27": "SGB15", "SGBOCT25V": "SGBOC355", 
    "SGBDEC25": "SGBDE623", "SGBDE30III": "SGB52", "SGBDEC26": "SGBDE7654", 
    "SGBFEB29XI": "SGB35", "SGBMAR31IV": "SGB53", "SGBMAR30X": "SGB49", 
    "SGBJUN30": "SGB50", "SGBFEB32IV": "SGB58", "SGBAUG30": "SGB51", 
    "SGBJAN30IX": "SGB48", "SGBJUN29I": "GB202", "SGBOCT27VI": "SGB16", 
    "SGBDE31III": "SGB57", "SGBSEP31II": "SGB55", "SGBDC27VII": "SGB17", 
    "SGBSEP28VI": "SGB29", "SGBJAN26": "SGBJA945", "SGBJ28VIII": "SGB18", 
    "SGBNOV25": "SGBNO458", "SGBJUL29IV": "SGB39", "SGBJAN29X": "SGB34", 
    "SGBNV29VII": "SGB44", "SGBD29VIII": "SGB46", "SGBMAY29I": "GB201", 
    "SGBMR29XII": "SGB36", "SGBJUL27": "SGB12", "SGBSEP29VI": "SGB42", 
    "SGBJAN29IX": "SGB33", "SGBJUN31I": "SGB54", "SGBFEB28IX": "SGB21", 
    "SGBOCT25IV": "SGB11", "SGBN28VIII": "SGB32", "SGBOCT25": "SGBOC250", 
    "SGBOC28VII": "SGB30", "SGBJUN28": "SGB26", "SGBJUL28IV": "SGB27", 
    "SGBAUG29V": "SGB40", "SGBOCT27": "SGB19", "SGBMAR28X": "SGB20", 
    "SGBMAY28": "SGB25", "SGBOCT26": "SGBOC5960", "SGBNOV258": "SGBNO497", 
    "SGBFEB27": "SGBFE8766", "SGBAPR28I": "SGB24", "SGBAUG27": "SGB13", 
    "SGBJU29III": "SGB37", "SGBAUG28V": "SGB28", "SGBSEP27": "SGB14", 
    "SGBJAN27": "SGBJA8308", "SGBNOV26": "SGBNO6355", "SGBMAY26": "SGB10", 
    "SGBNOV25IX": "SGBNO540"
}

@st.cache_data(ttl=600)
def get_sgb_data(nse_symbol):
    mc_code = MC_MAP.get(nse_symbol)
    if not mc_code: return 0.0, 0
    url = f"https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/{mc_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=5).json()
        data = res.get('data', {})
        if not data: return 0.0, 0
        
        offer = float(data.get('OPrice') or 0.0)
        ltp = float(data.get('pricecurrent') or 0.0)
        
        def safe_int(val):
            try:
                if not val: return 0
                return int(str(val).replace(',', '').split('.')[0])
            except: return 0
            
        oqty = safe_int(data.get('OQty'))
        vol = safe_int(data.get('vol_traded'))
        
        final_price = offer if offer > 0 else ltp
        final_qty = oqty if offer > 0 else vol 
        
        return final_price, final_qty
    except: 
        return 0.0, 0

# --- 2. SIDEBAR: PORTFOLIO EDITOR ---
st.sidebar.header("⚙️ My Portfolio Settings")
my_qty = st.sidebar.number_input("Units Held (24 units = 3 lots)", value=24, step=8)
my_sgb_cost = st.sidebar.number_input("My SGB Buy Price (Avg)", value=15906.67, format="%.2f")
my_guinea_sell_lot = st.sidebar.number_input("My Guinea Sell Price (Lot)", value=131600.0)

st.sidebar.divider()
st.sidebar.header("📈 Market Live Rates")
live_sgb_ltp = st.sidebar.number_input("SGB Market Price", value=15920.0)
live_guinea_lot_ltp = st.sidebar.number_input("Guinea March Lot Price", value=130177.0)
spot_gold = st.sidebar.number_input("Spot 24K Gold Price", value=16183.0) 

# --- 3. MATH ENGINE ---
my_guinea_sell_gram = my_guinea_sell_lot / 8
live_guinea_gram = live_guinea_lot_ltp / 8

# --- 4. MAIN DASHBOARD ---
st.title("🪙 Gold Guinea Carry Tracker")

c1, c2, c3 = st.columns(3)
sgb_pnl = (live_sgb_ltp - my_sgb_cost) * my_qty
with c1:
    st.metric("SGB Leg P&L", f"₹{sgb_pnl:,.0f}", delta=f"Price: {live_sgb_ltp}")

mcx_pnl = (my_guinea_sell_gram - live_guinea_gram) * my_qty
with c2:
    st.metric("MCX Hedge P&L", f"₹{mcx_pnl:,.0f}", delta=f"Price: {live_guinea_gram:.0f}", delta_color="inverse")

total_net = sgb_pnl + mcx_pnl
with c3:
    st.metric("NET Carry Profit", f"₹{total_net:,.0f}", "Locked Spread")

st.divider()

# --- 5. SWAP SCANNER (Live Discount Calculation) ---
st.subheader("🔍 SGB Market Scanner (Mini)")
scanner_data = [
    {"Symbol": "SGBJUN31I (Yours)", "Price": live_sgb_ltp, "Discount": f"{((spot_gold-live_sgb_ltp)/spot_gold)*100:.2f}%"},
    {"Symbol": "SGBJUN27", "Price": 15300, "Discount": f"{((spot_gold-15300)/spot_gold)*100:.2f}%"},
    {"Symbol": "SGBMAY26", "Price": 15410, "Discount": f"{((spot_gold-15410)/spot_gold)*100:.2f}%"},
]
st.table(pd.DataFrame(scanner_data))

st.info("💡 **Pro-Tip:** If SGBJUN27 shows a discount > 5%, you can swap your JUN31 holdings to gain more gold grams instantly!")

st.divider()

# --- 6. LIVE SGB ANALYZER (LITE) ---
st.subheader("⚡ Live SGB Market Analyzer")
st.caption("Click the button below to scan all 50+ active SGBs on the NSE right now.")

if st.button("Run Full Market Scan", type="primary"):
    progress_text = "Scanning NSE feeds for all SGBs..."
    my_bar = st.progress(0, text=progress_text)
    
    analyzer_data = []
    symbols = list(MC_MAP.keys())
    total = len(symbols)
    
    for i, symbol in enumerate(symbols):
        price, qty = get_sgb_data(symbol)
        if price > 0 and spot_gold > 0:
            discount = ((spot_gold - price) / spot_gold) * 100
            analyzer_data.append({
                "Symbol": symbol,
                "Price": price,
                "Qty Avail.": qty,
                "Discount %": discount,
                "Est. Yield %": discount + 2.5 
            })
        my_bar.progress((i + 1) / total, text=f"Scanning {symbol}...")
        
    if analyzer_data:
        df = pd.DataFrame(analyzer_data).sort_values("Discount %", ascending=False)
        
        st.dataframe(
            df.style.format({
                "Price": "₹{:,.0f}",
                "Qty Avail.": "{:,.0f}",
                "Discount %": "{:.2f}%",
                "Est. Yield %": "{:.2f}%"
            }).background_gradient(subset=["Discount %"], cmap="Greens"),
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.error("Could not fetch data from the exchange. Please try again in a few minutes.")
    my_bar.empty()
