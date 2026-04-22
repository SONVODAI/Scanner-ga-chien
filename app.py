import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.title("🔥 SCANNER GÀ CHIẾN V18.5")

# =========================
# LOAD DATA
# =========================
def load_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    df.dropna(inplace=True)
    return df

# =========================
# INDICATORS
# =========================
def add_indicators(df):
    df['ema9'] = df['Close'].ewm(span=9).mean()
    df['ma20'] = df['Close'].rolling(20).mean()

    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    df['obv'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
    df['obv_ema9'] = df['obv'].ewm(span=9).mean()

    df['bb_mid'] = df['Close'].rolling(20).mean()
    df['bb_std'] = df['Close'].rolling(20).std()
    df['bb_upper'] = df['bb_mid'] + 2 * df['bb_std']
    df['bb_lower'] = df['bb_mid'] - 2 * df['bb_std']

    return df

# =========================
# E – ENERGY
# =========================
def score_E(df):
    last = df.iloc[-1]

    cond_price = last['Close'] > last['ema9'] > last['ma20']
    cond_rsi = last['rsi'] > 55
    cond_obv = last['obv'] > last['obv_ema9']

    score = sum([cond_price, cond_rsi, cond_obv])

    return 2 if score == 3 else 1 if score == 2 else 0

# =========================
# R – RISK
# =========================
def score_R(df):
    last = df.iloc[-1]
    dist = abs(last['Close'] - last['ema9']) / last['ema9']

    if dist < 0.03:
        return 2
    elif dist < 0.07:
        return 1
    else:
        return 0

# =========================
# O – OPPORTUNITY
# =========================
def score_O(df):
    last = df.iloc[-1]
    prev = df.iloc[-2]

    cond_rsi = last['rsi'] > prev['rsi']
    cond_obv = last['obv'] > prev['obv']
    cond_price = last['Close'] > prev['Close']

    score = sum([cond_rsi, cond_obv, cond_price])

    return 2 if score == 3 else 1 if score == 2 else 0

# =========================
# ACC – TÍCH LŨY ĐẸP
# =========================
def score_ACC(df):
    data = df.tail(60)
    if len(data) < 50:
        return 0

    price_range = (data['Close'].max() - data['Close'].min()) / data['Close'].mean()
    cond_price = price_range < 0.12

    vol_slope = np.polyfit(range(len(data)), data['Volume'], 1)[0]
    cond_vol = vol_slope < 0

    rsi_mean = data['rsi'].mean()
    cond_rsi = 45 < rsi_mean < 60

    obv_slope = np.polyfit(range(len(data)), data['obv'], 1)[0]
    cond_obv = obv_slope >= 0

    bb_width = (data['bb_upper'] - data['bb_lower']) / data['Close']
    cond_bb = bb_width.mean() < 0.18

    return sum([cond_price, cond_vol, cond_rsi, cond_obv, cond_bb])

# =========================
# PULL PHÂN LOẠI (NEW)
# =========================
def classify_pull(df):
    last = df.iloc[-1]

    price = last['Close']
    ema9 = last['ema9']
    ma20 = last['ma20']
    rsi = last['rsi']
    obv = last['obv']
    obv_ema9 = last['obv_ema9']

    dist = abs(price - ema9) / ema9

    # 🟢 Pull đẹp
    if price >= ema9 and rsi > 55 and obv >= obv_ema9:
        return "🟢 PULL ĐẸP"

    # 🟡 Xa EMA (chờ thêm)
    elif dist > 0.05 and rsi > 55 and obv >= obv_ema9:
        return "🟡 CHỜ PULL"

    # 🔴 Gãy
    else:
        return "🔴 PULL XẤU"

# =========================
# WATCHLIST (anh thay list của anh vào đây)
# =========================
tickers = [
    "MBB.VN","TCB.VN","SSI.VN","VND.VN",
    "MWG.VN","FPT.VN","HCM.VN","NVL.VN"
]

results = []

for ticker in tickers:
    try:
        df = load_data(ticker)
        df = add_indicators(df)

        E = score_E(df)
        R = score_R(df)
        O = score_O(df)
        ACC = score_ACC(df)
        pull = classify_pull(df)

        # 🔥 CHỈ GIỮ TÍCH LŨY ĐẸP
        if ACC >= 4:
            results.append({
                "Ticker": ticker,
                "E": E,
                "R": R,
                "O": O,
                "ACC": ACC,
                "TOTAL": E + R + O,
                "PULL": pull
            })

    except:
        continue

# =========================
# OUTPUT
# =========================
df_out = pd.DataFrame(results)

if not df_out.empty:
    df_out = df_out.sort_values(by="TOTAL", ascending=False)
    st.dataframe(df_out)
else:
    st.write("❌ Không có cp tích lũy đẹp")
