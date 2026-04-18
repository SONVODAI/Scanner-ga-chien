import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scanner Gà Chiến", layout="wide")
st.title("📊 Scanner Gà Chiến - Bản kiểm tra lỗi")

st.write("App đã chạy tới đây.")

try:
    import yfinance as yf
    st.success("Import yfinance: OK")
except Exception as e:
    st.error(f"Lỗi import yfinance: {e}")
    st.stop()

tickers = ["VCB.VN", "MBB.VN", "HPG.VN", "SSI.VN", "VND.VN"]

rows = []

for ticker in tickers:
    try:
        df = yf.download(
            ticker,
            period="1mo",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False,
        )

        if df is None or df.empty:
            rows.append({
                "Mã": ticker,
                "Trạng thái": "Không có dữ liệu",
                "Giá": None,
                "EMA9": None,
                "RSI": None,
            })
            continue

        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]

        close = pd.to_numeric(close, errors="coerce").dropna()

        if close.empty:
            rows.append({
                "Mã": ticker,
                "Trạng thái": "Close rỗng",
                "Giá": None,
                "EMA9": None,
                "RSI": None,
            })
            continue

        ema9 = close.ewm(span=9, adjust=False).mean()

        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(14, min_periods=14).mean()
        avg_loss = loss.rolling(14, min_periods=14).mean()
        rs = avg_gain / avg_loss.replace(0, pd.NA)
        rsi = 100 - (100 / (1 + rs))

        price = round(float(close.iloc[-1]), 2)
        ema9_now = round(float(ema9.iloc[-1]), 2) if pd.notna(ema9.iloc[-1]) else None
        rsi_now = round(float(rsi.iloc[-1]), 2) if pd.notna(rsi.iloc[-1]) else None

        rows.append({
            "Mã": ticker.replace(".VN", ""),
            "Trạng thái": "OK",
            "Giá": price,
            "EMA9": ema9_now,
            "RSI": rsi_now,
        })

    except Exception as e:
        rows.append({
            "Mã": ticker.replace(".VN", ""),
            "Trạng thái": f"Lỗi: {str(e)}",
            "Giá": None,
            "EMA9": None,
            "RSI": None,
        })

out = pd.DataFrame(rows)
st.dataframe(out, use_container_width=True)
