import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📊 Scanner Gà Chiến v3")

tickers = ["VCB.VN","MBB.VN","HPG.VN","SSI.VN","VND.VN"]

data = []

for ticker in tickers:
    try:
        df = yf.download(ticker, period="1mo")

        close = df["Close"]

        ema9 = close.ewm(span=9).mean()
        rsi = close.pct_change().rolling(14).mean() * 100

        data.append({
            "Mã": ticker,
            "Giá": round(close.iloc[-1],2),
            "EMA9": round(ema9.iloc[-1],2),
            "RSI": round(rsi.iloc[-1],2)
        })

    except:
        pass

df = pd.DataFrame(data)

st.dataframe(df)
