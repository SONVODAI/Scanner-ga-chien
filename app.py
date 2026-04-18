import streamlit as st
import pandas as pd

st.title("📊 Scanner Gà Chiến v1")

data = [
    {"Mã": "VCG", "Điểm": 11, "Trạng thái": "ƯU TIÊN MUA", "Mẫu": "Pull đẹp", "Hành động": "Mua", "NAV": "30%"},
    {"Mã": "MBB", "Điểm": 10, "Trạng thái": "ƯU TIÊN MUA", "Mẫu": "Strong", "Hành động": "Mua", "NAV": "40%"},
    {"Mã": "HPG", "Điểm": 8, "Trạng thái": "THEO DÕI ĐẢO CHIỀU", "Mẫu": "Early", "Hành động": "Mua thăm dò", "NAV": "15%"},
    {"Mã": "GMD", "Điểm": 9, "Trạng thái": "THEO DÕI", "Mẫu": "Pull", "Hành động": "Chờ xác nhận", "NAV": "0%"},
]

df = pd.DataFrame(data)

option = st.selectbox("Chọn bộ lọc", ["Tất cả", "Pull đẹp", "Early", "Strong"])

if option != "Tất cả":
    df = df[df["Mẫu"].str.contains(option)]

st.dataframe(df)
