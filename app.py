import streamlit as st
import pandas as pd
import requests

st.title("📊 Scanner Gà Chiến v2 (Realtime)")

# Danh sách mã
tickers = ["VCB","CTG","TCB","MBB","STB","SSI","VND","HCM","VCI","HPG","HSG","NKG","GMD","VSC","MWG"]

data = []

for ticker in tickers:
    try:
        url = f"https://price-api.vndirect.com.vn/prices?q=code:{ticker}"
        r = requests.get(url).json()
        price = r["data"][0]["price"]

        # Demo logic đơn giản (sẽ nâng cấp sau)
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
        pass

df = pd.DataFrame(data)

st.dataframe(df)
