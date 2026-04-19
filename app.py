import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from vnstock import *

st.set_page_config(layout="wide")

# ================= WATCHLIST =================
WATCHLIST = [
"VCB","BID","CTG","TCB","MBB","VPB","STB","HDB","ACB","SHB","TPB","LPB","EIB","ABB","MSB","KLB","EVF","SSB","VIB","BVB","OCB",
"SSI","VIX","SHS","MBS","TCX","VCK","VPX","HCM","VCI","VND","CTS","FTS","BSI","BVS","ORS","VDS","AGR",
"VHM","VIC","NLG","KDH","CEO","CII","DXG","TCH","HHS","DPG","HDC","NVL","NTL","NHA","HUT","DIG","PDR","DXS","VRE","VPL",
"VGC","IDC","KBC","SZC","BCM","DTD","LHG","IJC","GVR","PHR","DPR","DRI","SIP","TRC","DRC","CSM",
"MWG","DGW","FRT","PET","PNJ","MSN","MCH","PAN","FMC","DBC","HAG","VNM","MML","SAB","SBT","TLG","HPA","BAF",
"REE","GEE","GEX","PC1","NT2","GEL","HDG","GEG","POW",
"DPM","DCM","LAS","DDV","DGC","CSV","BFC","MSR","BMP","NTP",
"BSR","PVS","PVD","PVB","PVC","PVT","OIL","PLX","GAS",
"HAH","GMD","VSC","VOS","VTO","HVN","VJC","ACV",
"VTP","CTR","VGI","FPT","FOX","CMG","MFS","ELC",
"MSH","TNG","TCM","GIL","VGT","HTG","VHC","ANV","VCS","PTB",
"CTD","HHV","FCN","LCG","CTI","KSB","C4G","VCG","DHA","PLC","HT1",
"HPG","HSG","NKG","VGS","TLH","TVN",
"DVN","DCL","DHG","IMP","DBD","DHT",
"BVH","MIG","BMI"
]

# ================= INDICATORS =================
def calc_indicators(df):
    df['EMA9'] = df['close'].ewm(span=9).mean()
    df['EMA20'] = df['close'].ewm(span=20).mean()

    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['MACD'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
    df['MACD_SIGNAL'] = df['MACD'].ewm(span=9).mean()

    df['OBV'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    df['OBV_EMA'] = df['OBV'].ewm(span=9).mean()

    return df

# ================= CLASSIFY =================
def classify(row):
    rsi = row['RSI']
    ema9 = row['EMA9']
    price = row['close']

    dist = (price - ema9)/ema9*100

    if rsi >= 60 and rsi <= 75 and abs(dist) < 4:
        return "BUY_PULL"
    elif rsi <= 55 and rsi > 40:
        return "BUY_EARLY"
    elif rsi > 75:
        return "WAIT_PULL"
    elif rsi >=45 and rsi <=58:
        return "ACCUMULATION"
    else:
        return "AVOID"

# ================= MAIN =================
results = []

for symbol in WATCHLIST:
    try:
        df = stock_historical_data(symbol, "2024-01-01", "2025-01-01", "1D")
        df = calc_indicators(df)

        row = df.iloc[-1]

        results.append({
            "symbol": symbol,
            "price": row['close'],
            "RSI": row['RSI'],
            "action": classify(row)
        })
    except:
        pass

df = pd.DataFrame(results)

st.title("🔥 SCANNER GÀ CHIẾN V15.3 PRO")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("BUY_PULL")
    st.dataframe(df[df.action=="BUY_PULL"])

with col2:
    st.subheader("BUY_EARLY")
    st.dataframe(df[df.action=="BUY_EARLY"])

with col3:
    st.subheader("WAIT_PULL")
    st.dataframe(df[df.action=="WAIT_PULL"])

with col4:
    st.subheader("ACCUMULATION")
    st.dataframe(df[df.action=="ACCUMULATION"])
