import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Scanner Gà Chiến V18.7", layout="wide")

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
    "Bất động sản công nghiệp": ["VGC","SZC","IDC","KBC","LHG","IJC","DTD","BCM"],
    "Cao su":["GVR","SIP","PHR","DRI","DPR","CSM","DRC"],
}

ALL_TICKERS = []
TICKER_TO_GROUP = {}
for group, tickers in WATCHLIST.items():
    for t in tickers:
        if t not in ALL_TICKERS:
            ALL_TICKERS.append(t)
            TICKER_TO_GROUP[t] = group

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main-title {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.sub-note {
    color: #666;
    font-size: 13px;
}
.block-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 8px;
}
.green-box {
    background-color: #e9f8ee;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid #b7e4c7;
}
.yellow-box {
    background-color: #fff8e6;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid #ffe08a;
}
.red-box {
    background-color: #fff0f0;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid #ffc2c2;
}
.blue-box {
    background-color: #eef5ff;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid #c9dcff;
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

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    need_cols = ["Open", "High", "Low", "Close", "Volume"]
    if not all(col in df.columns for col in need_cols):
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

    # Price
    out["ema9"] = out["Close"].ewm(span=9, adjust=False).mean()
    out["ma20"] = out["Close"].rolling(20).mean()
    out["ma50"] = out["Close"].rolling(50).mean()

    # RSI
    out["rsi14"] = calc_rsi(out["Close"], 14)
    out["rsi_ema9"] = out["rsi14"].ewm(span=9, adjust=False).mean()
    out["rsi_slope"] = out["rsi14"].diff(3)

    # OBV
    direction = np.sign(out["Close"].diff()).fillna(0)
    out["obv"] = (direction * out["Volume"]).cumsum()
    out["obv_ema9"] = out["obv"].ewm(span=9, adjust=False).mean()

    # MACD
    ema12 = out["Close"].ewm(span=12, adjust=False).mean()
    ema26 = out["Close"].ewm(span=26, adjust=False).mean()
    out["macd"] = ema12 - ema26
    out["macd_signal"] = out["macd"].ewm(span=9, adjust=False).mean()
    out["macd_hist"] = out["macd"] - out["macd_signal"]

    # Bollinger Band
    bb_mid = out["Close"].rolling(20).mean()
    bb_std = out["Close"].rolling(20).std()
    out["bb_upper"] = bb_mid + 2 * bb_std
    out["bb_lower"] = bb_mid - 2 * bb_std
    out["bb_width"] = (out["bb_upper"] - out["bb_lower"]) / out["Close"]

    # ATR
    tr1 = out["High"] - out["Low"]
    tr2 = (out["High"] - out["Close"].shift(1)).abs()
    tr3 = (out["Low"] - out["Close"].shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    out["atr14"] = tr.rolling(14).mean()

    out.dropna(inplace=True)
    return out

# =========================
# SCORING
# =========================
def score_E(last: pd.Series) -> int:
    cond_price = last["Close"] > last["ema9"] > last["ma20"]
    cond_rsi = (last["rsi14"] > 55) and (last["rsi14"] >= last["rsi_ema9"])
    cond_obv = last["obv"] >= last["obv_ema9"]

    score = int(cond_price) + int(cond_rsi) + int(cond_obv)
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
# LABELS
# =========================
def classify_pull(last: pd.Series) -> str:
    price = last["Close"]
    ema9 = last["ema9"]
    ma20 = last["ma20"]
    rsi = last["rsi14"]
    obv = last["obv"]
    obv_ema9 = last["obv_ema9"]

    dist = abs(price - ema9) / ema9

    if dist > 0.05 and rsi > 55 and obv >= obv_ema9 and price > ma20:
        return "PULL CHỜ THÊM"

    if dist <= 0.035 and rsi > 55 and obv >= obv_ema9 and price >= ema9:
        return "PULL ĐẸP"

    return "PULL XẤU"

def classify_group(E: int, R: int, O: int, ACC: int, pull_label: str, last: pd.Series) -> str:
    price = last["Close"]
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
# MAIN SCAN
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

    dist_pct = round(abs(last["Close"] - last["ema9"]) / last["ema9"] * 100, 2)
    obv_status = "🟢" if last["obv"] >= last["obv_ema9"] else "🔴"

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
        "dist_from_ema9_pct": dist_pct,
        "pull_label": pull_label,
        "khuyen_nghi": reco
    }

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">🔥 Scanner Gà Chiến V18.7</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-note">Cập nhật: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} | '
    'Đọc nhanh: 222 + gần EMA = ưu tiên; 222 nhưng xa EMA = chờ pull; ACC cao = gà đang ấp trứng.</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("### Tùy chọn")
    show_detail = st.checkbox("Hiện bảng tổng chi tiết", value=True)
    hide_loai = st.checkbox("Ẩn nhóm LOẠI", value=True)
    top_n_action = st.slider("Số mã ưu tiên hành động", min_value=3, max_value=10, value=5)
    st.button("Quét lại", use_container_width=True)

# =========================
# RUN SCAN
# =========================
results = []
progress = st.progress(0, text="Đang quét dữ liệu...")

for i, symbol in enumerate(ALL_TICKERS):
    item = scan_one(symbol)
    if item is not None:
        results.append(item)
    progress.progress((i + 1) / len(ALL_TICKERS), text=f"Đang quét: {symbol}")

progress.empty()

if not results:
    st.error("Không tải được dữ liệu. Anh thử lại sau.")
    st.stop()

df_all = pd.DataFrame(results)

if hide_loai:
    df_all = df_all[df_all["group"] != "LOẠI"].copy()

df_all = df_all.sort_values(
    by=["total_score", "ACC", "dist_from_ema9_pct"],
    ascending=[False, False, True]
).reset_index(drop=True)

# =========================
# TOP 5 ƯU TIÊN HÀNH ĐỘNG
# =========================
st.markdown("## 🎯 Top ưu tiên hành động")

priority_order = {
    "✅ ƯU TIÊN MUA 222": 1,
    "⚠️ 222 NHƯNG XA EMA": 2,
    "🟡 THEO DÕI SÁT": 3,
    "🟡 CHỜ PULL THÊM": 4,
    "🐣 TÍCH LŨY ĐẸP": 5,
    "⚠️ KHỎE NHƯNG XA EMA": 6,
    "👀 THEO DÕI": 7,
    "🔴 TRÁNH / CHỜ LẠI": 8
}
df_all["priority_rank"] = df_all["khuyen_nghi"].map(priority_order).fillna(99)

df_action = df_all.sort_values(
    by=["priority_rank", "total_score", "ACC", "dist_from_ema9_pct"],
    ascending=[True, False, False, True]
).head(top_n_action)

c1, c2, c3 = st.columns(3)

with c1:
    buy_now = df_action[df_action["khuyen_nghi"] == "✅ ƯU TIÊN MUA 222"][["symbol", "price", "pull_label"]]
    st.markdown('<div class="green-box"><b>Ưu tiên mua ngay</b></div>', unsafe_allow_html=True)
    if buy_now.empty:
        st.info("Chưa có mã")
    else:
        st.dataframe(buy_now, use_container_width=True, hide_index=True)

with c2:
    wait_pull = df_action[df_action["khuyen_nghi"].isin(["⚠️ 222 NHƯNG XA EMA", "🟡 CHỜ PULL THÊM"])][["symbol", "price", "pull_label"]]
    st.markdown('<div class="yellow-box"><b>Chờ pull thêm</b></div>', unsafe_allow_html=True)
    if wait_pull.empty:
        st.info("Chưa có mã")
    else:
        st.dataframe(wait_pull, use_container_width=True, hide_index=True)

with c3:
    avoid_now = df_action[df_action["khuyen_nghi"] == "🔴 TRÁNH / CHỜ LẠI"][["symbol", "price", "pull_label"]]
    st.markdown('<div class="red-box"><b>Tránh / chờ lại</b></div>', unsafe_allow_html=True)
    if avoid_now.empty:
        st.info("Chưa có mã")
    else:
        st.dataframe(avoid_now, use_container_width=True, hide_index=True)

st.dataframe(
    df_action[["symbol", "price", "group", "E", "R", "O", "ACC", "pull_label", "khuyen_nghi"]],
    use_container_width=True,
    hide_index=True
)

# =========================
# BẢNG NHÓM PHÍA TRÊN
# =========================
st.markdown("## 📌 Phân nhóm nhanh")
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
# 222 CHIA 2 NHÓM
# =========================
st.markdown("## 🚀 Khuyến nghị 222")

df_222 = df_all[(df_all["E"] == 2) & (df_all["R"] == 2) & (df_all["O"] == 2)].copy()
df_222_near = df_222[df_222["dist_from_ema9_pct"] <= 4].copy()
df_222_far = df_222[df_222["dist_from_ema9_pct"] > 4].copy()

left, right = st.columns(2)

with left:
    st.markdown('<div class="green-box"><b>222 gần EMA – ưu tiên cao</b></div>', unsafe_allow_html=True)
    if df_222_near.empty:
        st.info("Hiện chưa có mã")
    else:
        st.dataframe(
            df_222_near[["symbol", "price", "group", "ACC", "dist_from_ema9_pct", "pull_label", "khuyen_nghi"]],
            use_container_width=True,
            hide_index=True
        )

with right:
    st.markdown('<div class="yellow-box"><b>222 xa EMA – chờ pull thêm</b></div>', unsafe_allow_html=True)
    if df_222_far.empty:
        st.info("Hiện chưa có mã")
    else:
        st.dataframe(
            df_222_far[["symbol", "price", "group", "ACC", "dist_from_ema9_pct", "pull_label", "khuyen_nghi"]],
            use_container_width=True,
            hide_index=True
        )

# =========================
# TÍCH LŨY ĐẸP
# =========================
st.markdown("## 🐣 Tích lũy đẹp dài")
df_acc = df_all[df_all["ACC"] >= 4].copy()
if df_acc.empty:
    st.info("Hiện chưa có mã tích lũy đẹp.")
else:
    st.dataframe(
        df_acc[["symbol", "price", "ACC", "rsi14", "dist_from_ema9_pct", "pull_label", "khuyen_nghi"]],
        use_container_width=True,
        hide_index=True
    )

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
    st.dataframe(df_all[show_cols], use_container_width=True, hide_index=True)
