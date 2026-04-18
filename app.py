import streamlit as st
import pandas as pd
import requests

st.title("📊 Scanner Gà Chiến v2 (Realtime)")

tickers = ["VCB","CTG","TCB","MBB","STB","SSI","VND","HCM","VCI","HPG","HSG","NKG","GMD","VSC","MWG"]

data = []

for ticker in tickers:
    try:
        url = f"https://finfo-api.vndirect.com.vn/v4/stock_prices?q=code:{ticker}&size=1"
        r = requests.get(url).json()

        price = r["data"][0]["close"]

        score = 8 + (price % 3)

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

    except:
        data.append({
            "Mã": ticker,
            "Giá": "N/A",
            "Điểm": 0,
            "Trạng thái": "Lỗi dữ liệu",
            "Hành động": "-",
            "NAV": "-"
        })

df = pd.DataFrame(data)

st.dataframe(df)
