import streamlit as st
import pandas as pd

st.title("📊 Scanner Gà Chiến - Stable")

data = [
    {"Mã": "VCB", "Giá": 90, "EMA9": 88, "RSI": 60},
    {"Mã": "MBB", "Giá": 22, "EMA9": 21, "RSI": 58},
    {"Mã": "HPG", "Giá": 28, "EMA9": 27, "RSI": 55},
    {"Mã": "SSI", "Giá": 35, "EMA9": 34, "RSI": 62},
]

df = pd.DataFrame(data)

st.dataframe(df)
