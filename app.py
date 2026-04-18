import streamlit as st
import pandas as pd
import random

st.title("📊 Scanner Gà Chiến v2")

tickers = ["VCB","CTG","TCB","MBB","STB","SSI","VND","HCM","VCI","HPG","HSG","NKG","GMD","VSC","MWG"]

data = []

for ticker in tickers:
    price = random.randint(10,100)

    score = random.randint(7,11)

    if score >= 10:
        status = "ƯU TIÊN MUA"
        action = "Mua"
        nav = "30%"
    elif score >= 8:
        status = "THEO DÕI"
        action = "Chờ"
        nav = "0%"
    else:
        status = "LOẠI"
        action = "Bỏ"
        nav = "0%"

    data.append({
        "Mã": ticker,
        "Giá": price,
        "Điểm": score,
        "Trạng thái": status,
        "Hành động": action,
        "NAV": nav
    })

df = pd.DataFrame(data)

st.dataframe(df)
