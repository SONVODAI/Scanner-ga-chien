import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Scanner Gà Chiến V18.6", layout="wide")

# =========================
# WATCHLIST CỦA ANH
# =========================
WATCHLIST = {
    "Dầu khí & Vận tải": ["PLX","PVS","PVD","PVB","PVC","PVT","BSR","OIL","GAS","HAH","VSC","GMD","VOS","VTO","ACV"],
    "Xuất khẩu": ["MSH","TNG","TCM","GIL","VHC","ANV","FMC","VCS","PTB"],
    "Điện & Hóa chất": ["BFC","DCM","DPM","CSV","DDV","LAS","BMP","NTP","AAA","PAC","MSR","REE","GEE","GEX","PC1","HDG","GEG","NT2","TV2","DGC"],
    "Đầu tư công & vật liệu": ["C4G","FCN","CII","KSB","DHA","CTI","HBC","HPG","HSG","NKG","VGS","CTD","HHV","VCG"],
    "Bán lẻ & chăn nuôi": ["MWG","FRT","DGW","PET","HAX","MSN","DBC","HAG","BAF","MCH","PAN","VNM","MML"],
    "Ngân hàng & tài chính": ["VCB","BID","CTG","TCB","VPB","MBB","ACB","SHB","SSB","STB","HDB","TPB","VIB","LPB","OCB","MSB","NAB","EIB","VND","SSI","HCM","SHS","VIX","BSI","FTS","TVS","APS","AGR","VCI"],
    "Công nghệ & logistic": ["FPT","VGI","CTR","VTP","CMG","ELC","FOX"],
    "Cổ phiếu lẻ": ["HVN","VJC","IMP","BVH","SBT","LSS","PNJ","TLG","DHT","TNH","NVL","VHM","VIC","YEG"]
}

ALL_TICKERS = []
TICKER_TO_GROUP = {}
for group, tickers in WATCHLIST.items():
    for t in tickers:
        if t not in ALL_TICKERS:
            ALL_TICKERS.append(t)
            TICKER_TO_GROUP[t] = group

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.block-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}
.small-note {
    color: #666;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def vn_ticker(symbol: str) -> str:
    return f"{symbol}.VN"

@st.cache_data(ttl=900, show_spinner=False)
def load_data(symbol: str) -> pd.DataFrame:
    ticker = vn_ticker(symbol)
    df = yf.download(ticker, period="8mo", interval="1d", auto_adjust=False, progress=False)
    if df is None or df.empty:
        return pd.DataFrame()

    # yfinance đôi khi trả về multiindex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    need_cols = ["Open", "High", "Low", "Close", "Volume"]
    miss = [c for c in need_cols if c not in df.columns]
    if miss:
        return pd.DataFrame()

    df = df[need_cols].copy()
    df.dropna(inplace=True)
    return df

def calc_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["ema9"] = out["Close"].ewm(span=9, adjust=False).mean()
    out["ma20"] = out["Close"].rolling(20).mean()
    out["ma50"] = out["Close"].rolling(50).mean()

    out["rsi14"] = calc_rsi(out["Close"], 14)
    out["rsi_ema9"] = out["rsi14"].ewm(span=9, adjust=False).mean()
    out["rsi_slope"] = out["rsi14"].diff(3)

    direction = np.sign(out["Close"].diff()).fillna(0)
    out["obv"] = (direction * out["Volume"]).cumsum()
    out["obv_ema9"] = out["obv"].ewm(span=9, adjust=False).mean()

    ema12 = out["Close"].ewm(span=12, adjust=False).mean()
    ema26 = out["Close"].ewm(span=26, adjust=False).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]

    bb_mid = out["Close"].rolling(20).mean()
    bb_std = out["Close"].rolling(20).std()
    out["bb_upper"] = bb_mid + 2 * bb_std
    out["bb_lower"] = bb_mid - 2 * bb_std
    out["bb_width"] = (out["bb_upper"] - out["bb_lower"]) / out["Close"]

    tr1 = out["High"] - out["Low"]
    tr2 = (out["High"] - out["Close"].shift(1)).abs()
    tr3 = (out["Low"] - out["Close"].shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    out["atr14"] = tr.rolling(14).mean()

    out.dropna(inplace=True)
    return out

# =========================
# SCORING E / R / O / ACC
# =========================
def score_E(last: pd.Series) -> int:
    price_ok = (last["Close"] > last["ema9"] > last["ma20"])
    rsi_ok = (last["rsi14"] > 55) and (last["rsi14"] >= last["rsi_ema9"])
    obv_ok = (last["obv"] >= last["obv_ema9"])

    score = int(price_ok) + int(rsi_ok) + int(obv_ok)
    if score == 3:
        return 2
    elif score == 2:
        return 1
    return 0

def score_R(last: pd.Series) -> int:
    dist = abs(last["Close"] - last["ema9"]) / last["ema9"]

    if dist <= 0.025:
        return 2
    elif dist <= 0.06:
        return 1
    return 0

def score_O(df: pd.DataFrame) -> int:
    last = df.iloc[-1]
    prev = df.iloc[-2]

    cond_price = last["Close"] > prev["Close"]
    cond_rsi = last["rsi14"] > prev["rsi14"]
    cond_obv = last["obv"] > prev["obv"]

    score = int(cond_price) + int(cond_rsi) + int(cond_obv)
    if score == 3:
        return 2
    elif score == 2:
        return 1
    return 0

def score_ACC(df: pd.DataFrame) -> int:
    data = df.tail(60)
    if len(data) < 50:
        return 0

    price_range = (data["Close"].max() - data["Close"].min()) / data["Close"].mean()
    cond_price = price_range < 0.15

    vol_slope = np.polyfit(np.arange(len(data)), data["Volume"].values, 1)[0]
    cond_vol = vol_slope < 0

    rsi_mean = data["rsi14"].mean()
    cond_rsi = 43 <= rsi_mean <= 60

    obv_slope = np.polyfit(np.arange(len(data)), data["obv"].values, 1)[0]
    cond_obv = obv_slope >= 0

    bb_mean = data["bb_width"].mean()
    cond_bb = bb_mean < 0.22

    return int(cond_price) + int(cond_vol) + int(cond_rsi) + int(cond_obv) + int(cond_bb)

# =========================
# PULL LABEL MỚI
# =========================
def classify_pull(last: pd.Series) -> str:
    price = last["Close"]
    ema9 = last["ema9"]
    ma20 = last["ma20"]
    rsi = last["rsi14"]
    obv = last["obv"]
    obv_ema9 = last["obv_ema9"]

    dist = abs(price - ema9) / ema9

    # quá xa EMA nhưng trục chưa gãy
    if dist > 0.05 and rsi > 55 and obv >= obv_ema9 and price > ma20:
        return "PULL CHỜ THÊM"

    # pull đẹp: gần EMA và trục vẫn ổn
    if dist <= 0.035 and rsi > 55 and obv >= obv_ema9 and price >= ema9:
        return "PULL ĐẸP"

    # còn lại xem là pull xấu
    return "PULL XẤU"

# =========================
# GROUP CLASSIFICATION
# =========================
def classify_group(E: int, R: int, O: int, ACC: int, pull_label: str, last: pd.Series) -> str:
    price = last["Close"]
    ema9 = last["ema9"]
    ma20 = last["ma20"]
    rsi = last["rsi14"]

    if E == 2 and R == 2 and O == 2:
        return "CP MẠNH"

    if E == 2 and O == 2 and R == 1:
        if pull_label == "PULL ĐẸP":
            return "PULL ĐẸP"
        return "PULL VỪA"

    if E == 2 and O == 1 and R >= 1:
        return "PULL VỪA"

    if E >= 1 and O == 2 and rsi >= 48 and price >= ma20:
        return "MUA EARLY"

    if ACC >= 4:
        return "TÍCH LŨY"

    if E >= 1 or O >= 1:
        return "THEO DÕI"

    return "LOẠI"

# =========================
# KHUYẾN NGHỊ 222
# =========================
def recommend_action(E: int, R: int, O: int, ACC: int, pull_label: str, last: pd.Series) -> str:
    dist = abs(last["Close"] - last["ema9"]) / last["ema9"]

    if E == 2 and R == 2 and O == 2:
        if dist <= 0.04:
            return "✅ ƯU TIÊN MUA 222"
        return "⚠️ 222 NHƯNG XA EMA"

    if E == 2 and O == 2 and R == 1:
        if pull_label == "PULL CHỜ THÊM":
            return "🟡 CHỜ PULL THÊM"
        return "🟡 THEO DÕI SÁT"

    if ACC >= 4 and O >= 1:
        return "🐣 TÍCH LŨY ĐẸP"

    if E == 2 and R == 0:
        return "⚠️ KHỎE NHƯNG XA EMA"

    if pull_label == "PULL XẤU":
        return "🔴 TRÁNH / CHỜ LẠI"

    return "👀 THEO DÕI"

# =========================
# SCAN
# =========================
def scan_one(symbol: str):
    raw = load_data(symbol)
    if raw.empty or len(raw) < 80:
        return None

    df = add_indicators(raw)
    if df.empty or len(df) < 60:
        return None

    last = df.iloc[-1]

    E = score_E(last)
    R = score_R(last)
    O = score_O(df)
    ACC = score_ACC(df)
    pull_label = classify_pull(last)
    group = classify_group(E, R, O, ACC, pull_label, last)
    reco = recommend_action(E, R, O, ACC, pull_label, last)

    obv_status = "🟢" if last["obv"] >= last["obv_ema9"] else "🔴"
    dist_from_ema9_pct = round(abs(last["Close"] - last["ema9"]) / last["ema9"] * 100, 2)

    return {
        "symbol": symbol,
        "sector": TICKER_TO_GROUP.get(symbol, ""),
        "group": group,
        "price": round(float(last["Close"]), 2),
        "ema9": round(float(last["ema9"]), 2),
        "ma20": round(float(last["ma20"]), 2),
        "rsi14": round(float(last["rsi14"]), 2),
        "rsi_slope": round(float(last["rsi_slope"]), 2),
        "obv": int(last["obv"]),
        "obv_ema9": int(last["obv_ema9"]),
        "obv_status": obv_status,
        "E": E,
        "R": R,
        "O": O,
        "ACC": ACC,
        "total_score": E + R + O,
        "dist_from_ema9_pct": dist_from_ema9_pct,
        "pull_label": pull_label,
        "khuyen_nghi": reco
    }

# =========================
# HEADER
# =========================
st.title("🔥 Scanner Gà Chiến V18.6")
st.caption(f"Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

with st.sidebar:
    st.markdown("### Tùy chọn")
    show_detail = st.checkbox("Hiện bảng tổng chi tiết", value=True)
    only_watch = st.checkbox("Ẩn nhóm LOẠI", value=True)
    scan_btn = st.button("Quét lại", use_container_width=True)

# Auto run
results = []
progress = st.progress(0, text="Đang quét dữ liệu...")

for i, symbol in enumerate(ALL_TICKERS):
    item = scan_one(symbol)
    if item is not None:
        results.append(item)
    progress.progress((i + 1) / len(ALL_TICKERS), text=f"Đang quét: {symbol}")

progress.empty()

if not results:
    st.error("Không tải được dữ liệu. Anh thử quét lại sau.")
    st.stop()

df_all = pd.DataFrame(results)

if only_watch:
    df_all = df_all[df_all["group"] != "LOẠI"].copy()

# ưu tiên sắp xếp
df_all = df_all.sort_values(
    by=["total_score", "ACC", "dist_from_ema9_pct"],
    ascending=[False, False, True]
).reset_index(drop=True)

# =========================
# BẢNG NHÓM PHÍA TRÊN
# =========================
top_groups = ["CP MẠNH", "MUA BREAK", "PULL ĐẸP", "PULL VỪA", "MUA EARLY", "TÍCH LŨY", "THEO DÕI"]
cols = st.columns(len(top_groups))

for col, g in zip(cols, top_groups):
    sub = df_all[df_all["group"] == g][["symbol", "price"]].reset_index(drop=True)
    col.markdown(f'<div class="block-title">{g}</div>', unsafe_allow_html=True)
    if sub.empty:
        col.info("Không có mã")
    else:
        col.dataframe(sub, use_container_width=True, hide_index=True)

# =========================
# BẢNG ƯU TIÊN 222
# =========================
st.markdown("## 🎯 Khuyến nghị 222")
df_222 = df_all[
    (df_all["E"] == 2) &
    (df_all["R"] == 2) &
    (df_all["O"] == 2)
][["symbol", "price", "group", "ACC", "pull_label", "khuyen_nghi"]].reset_index(drop=True)

if df_222.empty:
    st.info("Hiện chưa có mã đạt 2-2-2.")
else:
    st.dataframe(df_222, use_container_width=True, hide_index=True)

# =========================
# BẢNG TÍCH LŨY ĐẸP
# =========================
st.markdown("## 🐣 Tích lũy đẹp dài")
df_acc = df_all[df_all["ACC"] >= 4][
    ["symbol", "price", "ACC", "rsi14", "dist_from_ema9_pct", "khuyen_nghi"]
].reset_index(drop=True)

if df_acc.empty:
    st.info("Hiện chưa có mã tích lũy đẹp.")
else:
    st.dataframe(df_acc, use_container_width=True, hide_index=True)

# =========================
# BẢNG TỔNG CHI TIẾT
# =========================
if show_detail:
    st.markdown("## 📋 Bảng tổng chi tiết")
    show_cols = [
        "symbol", "sector", "group", "price", "ema9", "ma20",
        "rsi14", "rsi_slope", "obv", "obv_ema9", "obv_status",
        "E", "R", "O", "ACC", "total_score", "dist_from_ema9_pct",
        "pull_label", "khuyen_nghi"
    ]
    st.dataframe(df_all[show_cols], use_container_width=True)

st.caption("Gợi ý đọc nhanh: 222 + gần EMA = ưu tiên; 222 nhưng xa EMA = chờ pull; ACC cao = gà đang ấp trứng.")
