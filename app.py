<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Scanner CP mạnh V15.2</title>
  <style>
    :root {
      --bg: #0b1220;
      --panel: #121a2b;
      --panel-2: #172238;
      --text: #e8eefc;
      --muted: #9cb0d0;
      --line: #253453;
      --good: #1f9d55;
      --warn: #d69e2e;
      --bad: #e53e3e;
      --blue: #3b82f6;
      --chip: #23304d;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    .wrap {
      max-width: 1500px;
      margin: 0 auto;
      padding: 16px;
    }
    .topbar {
      display: grid;
      grid-template-columns: 1.6fr 1fr 1fr 1fr 1fr;
      gap: 12px;
      margin-bottom: 14px;
    }
    .card {
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    }
    .title {
      font-weight: 800;
      font-size: 20px;
      margin-bottom: 6px;
    }
    .muted { color: var(--muted); }
    .big {
      font-size: 28px;
      font-weight: 900;
      line-height: 1.1;
    }
    .controls {
      display: grid;
      grid-template-columns: 1.3fr 0.7fr 0.8fr 0.8fr 0.8fr 0.8fr 0.8fr;
      gap: 10px;
      margin-bottom: 14px;
    }
    input, select, textarea, button {
      width: 100%;
      background: #0f1728;
      color: var(--text);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px 12px;
      font-size: 14px;
      outline: none;
    }
    textarea {
      min-height: 160px;
      resize: vertical;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    button {
      cursor: pointer;
      font-weight: 700;
      background: linear-gradient(180deg, #1d4ed8, #1e40af);
      border: none;
    }
    button.secondary {
      background: #172238;
      border: 1px solid var(--line);
    }
    button.warn {
      background: linear-gradient(180deg, #b45309, #92400e);
    }
    .section-title {
      margin: 18px 0 10px;
      font-size: 18px;
      font-weight: 800;
    }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    .table-wrap {
      overflow: auto;
      border-radius: 14px;
      border: 1px solid var(--line);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1280px;
      background: #0f1728;
    }
    th, td {
      padding: 10px 8px;
      border-bottom: 1px solid #1d2942;
      text-align: left;
      font-size: 13px;
      white-space: nowrap;
    }
    thead th {
      position: sticky;
      top: 0;
      z-index: 2;
      background: #15213a;
      color: #dce8ff;
    }
    tbody tr:hover { background: rgba(59,130,246,0.08); }
    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 8px;
      border-radius: 999px;
      background: var(--chip);
      border: 1px solid #33456b;
      font-size: 12px;
      font-weight: 700;
    }
    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }
    .green { background: var(--good); }
    .yellow { background: var(--warn); }
    .red { background: var(--bad); }
    .blue { background: var(--blue); }
    .buy { color: #9ef0b8; font-weight: 800; }
    .wait { color: #ffd97a; font-weight: 800; }
    .avoid { color: #ff9b9b; font-weight: 800; }
    .small { font-size: 12px; }
    .footer-note {
      margin-top: 12px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.55;
    }
    .pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
    .ok { color: #9ef0b8; }
    .danger { color: #ff9b9b; }
    .layout {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 14px;
      margin-top: 14px;
    }
    .list-box {
      max-height: 220px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 10px;
      background: #0f1728;
      line-height: 1.7;
      font-size: 13px;
    }
    .toolbar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    @media (max-width: 1100px) {
      .topbar, .controls, .layout, .grid-2 {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div class="card">
        <div class="title">Scanner CP mạnh V15.2</div>
        <div class="muted">Tách rõ: <b>Sức mạnh</b> và <b>Khả năng mua</b></div>
        <div class="pill-row">
          <span class="chip"><span class="dot green"></span> BUY</span>
          <span class="chip"><span class="dot yellow"></span> WAIT_PULL</span>
          <span class="chip"><span class="dot red"></span> AVOID</span>
        </div>
      </div>
      <div class="card">
        <div class="muted">Tổng mã</div>
        <div class="big" id="totalCount">0</div>
      </div>
      <div class="card">
        <div class="muted">BUY</div>
        <div class="big ok" id="buyCount">0</div>
      </div>
      <div class="card">
        <div class="muted">WAIT_PULL</div>
        <div class="big" style="color:#ffd97a" id="waitCount">0</div>
      </div>
      <div class="card">
        <div class="muted">Lần cập nhật</div>
        <div class="big small" id="lastUpdate">Chưa có</div>
      </div>
    </div>

    <div class="controls">
      <input id="searchInput" placeholder="Tìm mã / ngành..." />
      <select id="sectorFilter">
        <option value="ALL">Tất cả ngành</option>
      </select>
      <select id="actionFilter">
        <option value="ALL">Tất cả trạng thái</option>
        <option value="BUY">BUY</option>
        <option value="WAIT_PULL">WAIT_PULL</option>
        <option value="AVOID">AVOID</option>
      </select>
      <select id="stageFilter">
        <option value="ALL">Tất cả stage</option>
        <option value="EARLY">EARLY</option>
        <option value="MID">MID</option>
        <option value="LATE">LATE</option>
      </select>
      <select id="refreshSelect">
        <option value="0">Không auto</option>
        <option value="5" selected>5 phút</option>
        <option value="10">10 phút</option>
        <option value="15">15 phút</option>
      </select>
      <button id="scanBtn">Scan ngay</button>
      <button id="exportBtn" class="secondary">Xuất CSV</button>
    </div>

    <div class="layout">
      <div class="card">
        <div class="section-title">1) Danh mục theo dõi V15.2</div>
        <div class="muted">Anh có thể sửa trực tiếp ở đây. Mỗi dòng 1 mã hoặc giữ nguyên theo mẫu em đã nhập.</div>
        <textarea id="watchlistEditor"></textarea>
        <div class="toolbar" style="margin-top:10px;">
          <button id="saveWatchlistBtn">Lưu watchlist</button>
          <button id="resetWatchlistBtn" class="secondary">Khôi phục watchlist chuẩn</button>
          <button id="sampleDataBtn" class="warn">Nạp dữ liệu mẫu để test</button>
        </div>
      </div>
      <div class="card">
        <div class="section-title">2) Nguồn dữ liệu</div>
        <div class="muted">Em không có chính xác endpoint V15 cũ trong cuộc chat này, nên em viết sẵn <b>engine V15.2 + UI + logic</b>. Anh chỉ cần sửa hàm <code>fetchRealtimeRows()</code> ở cuối file để nối lại đúng nguồn dữ liệu anh đang dùng.</div>
        <div class="footer-note">
          Dữ liệu mỗi mã nên có tối thiểu các field sau:<br/>
          <code>symbol, close, changePct, distEma9Pct, distMa20Pct, rsi, rsiEma9, obvTrend, obvAboveEma, macd, macdSignal, hist, atrTrend, breakoutStrength, breakoutConfirmed, failedAfterBreak, priceStructure, sector</code><br/><br/>
          Nếu chưa nối API, bấm <b>Nạp dữ liệu mẫu để test</b> rồi xem bộ lọc và bảng chạy trước.
        </div>
      </div>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="section-title">BUY – ưu tiên mua</div>
        <div class="list-box" id="buyList"></div>
      </div>
      <div class="card">
        <div class="section-title">WAIT_PULL – mạnh nhưng không đu</div>
        <div class="list-box" id="waitList"></div>
      </div>
    </div>

    <div class="section-title">Bảng quét chi tiết</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Mã</th>
            <th>Ngành</th>
            <th>Stage</th>
            <th>Action</th>
            <th>Strength</th>
            <th>BuyScore</th>
            <th>Break</th>
            <th>Giá</th>
            <th>%</th>
            <th>Dist EMA9</th>
            <th>Dist MA20</th>
            <th>RSI</th>
            <th>RSI vs EMA9</th>
            <th>OBV</th>
            <th>MACD</th>
            <th>ATR</th>
            <th>Cấu trúc</th>
            <th>Ghi chú</th>
          </tr>
        </thead>
        <tbody id="scannerBody"></tbody>
      </table>
    </div>

    <div class="footer-note">
      Logic chính V15.2:<br/>
      1) <b>Break mạnh vẫn được chấm mạnh</b> để không bỏ sót leader.<br/>
      2) Nhưng nếu <b>quá xa EMA9 / RSI quá cao / RR xấu</b> thì đưa vào <b>WAIT_PULL</b>, không cho vào BUY.<br/>
      3) Nghĩa là: <b>mạnh ≠ mua được</b>. Chỉ <b>mạnh + vị trí đẹp</b> mới BUY.
    </div>
  </div>

  <script>
    const DEFAULT_GROUPS = {
      'BANK': ['VCB','BID','CTG','TCB','MBB','VPB','STB','HDB','ACB','SHB','TPB','LPB','EIB','ABB','MSB','KLB','EVF','SSB','VIB','BVB','OCB'],
      'CK': ['SSI','VIX','SHS','MBS','TCX','VCK','VPX','HCM','VCI','VND','CTS','FTS','BSI','BVS','ORS','VDS','AGR'],
      'BĐS': ['VHM','NLG','KDH','CEO','CII','DXG','TCH','HHS','DPG','HDC','NVL','NTL','NHA','HUT','DIG','PDR','DXS','VRE','VPL'],
      'BĐS CN': ['VGC','IDC','KBC','SZC','BCM','DTD','LHG','IJC','GVR','PHR','DPR','DRI','SIP','TRC','DRC','CSM'],
      'THÉP': ['HPG','HSG','NKG','VGS','TLH','TVN'],
      'BÁN LẺ': ['MWG','DGW','FRT','PET','PNJ','MSN','MCH','PAN','FMC','DBC','HAG','VNM','MML','SAB','SBT','TLG','HPA','BAF'],
      'ĐIỆN': ['REE','GEE','GEX','PC1','NT2','GEL','HDG','GEG','POW'],
      'HÓA CHẤT': ['DPM','DCM','LAS','DDV','DGC','CSV','BFC','MSR','BMP','NTP'],
      'DẦU': ['BSR','PVS','PVD','PVB','PVC','PVT','OIL','PLX','GAS'],
      'LOGIS': ['HAH','GMD','VSC','VOS','VTO','HVN','VJC','ACV'],
      'CNTT': ['VTP','CTR','VGI','FPT','FOX','CMG','MFS','ELC'],
      'XK': ['MSH','TNG','TCM','GIL','VGT','HTG','VHC','ANV','VCS','PTB'],
      'DTC': ['CTD','HHV','FCN','LCG','CTI','KSB','C4G','VCG','DHA','PLC','HT1'],
      'BẢO HIỂM': ['BVH','MIG','BMI'],
      'DƯỢC': ['DVN','DCL','DHG','IMP','DBD','DHT']
    };

    const STORAGE_KEYS = {
      watchlist: 'scanner_v15_2_watchlist',
      refresh: 'scanner_v15_2_refresh'
    };

    function buildDefaultWatchlistText() {
      let lines = [];
      Object.entries(DEFAULT_GROUPS).forEach(([group, arr]) => {
        lines.push(group);
        arr.forEach(s => lines.push(s));
        lines.push('');
      });
      return lines.join('\n').trim();
    }

    function parseWatchlist(text) {
      const lines = text.split(/\r?\n/).map(v => v.trim()).filter(Boolean);
      const groups = {};
      let current = 'KHÁC';
      for (const line of lines) {
        const upper = line.toUpperCase();
        const isTicker = /^[A-Z0-9]{2,5}$/.test(upper);
        if (!isTicker) {
          current = line;
          if (!groups[current]) groups[current] = [];
        } else {
          if (!groups[current]) groups[current] = [];
          groups[current].push(upper);
        }
      }
      return groups;
    }

    function flattenGroups(groups) {
      const out = [];
      Object.entries(groups).forEach(([sector, list]) => {
        list.forEach(symbol => out.push({ symbol, sector }));
      });
      return out;
    }

    function safeNum(v, fallback = 0) {
      const n = Number(v);
      return Number.isFinite(n) ? n : fallback;
    }

    function clamp(n, min, max) {
      return Math.max(min, Math.min(max, n));
    }

    function scoreBreak(row) {
      // Ý chính của V15.2:
      // Break mạnh vẫn là mạnh, nhưng nếu quá nóng thì chuyển WAIT_PULL thay vì đánh trượt.
      let score = 0;
      const bs = safeNum(row.breakoutStrength);
      const confirmed = !!row.breakoutConfirmed;
      const failed = !!row.failedAfterBreak;
      const distEma9 = safeNum(row.distEma9Pct);
      const rsi = safeNum(row.rsi);
      const obvGood = !!row.obvAboveEma || String(row.obvTrend).toUpperCase() === 'UP';
      const macdGood = safeNum(row.macd) >= safeNum(row.macdSignal) || safeNum(row.hist) > 0;

      if (bs >= 85) score += 4;
      else if (bs >= 70) score += 3;
      else if (bs >= 55) score += 2;
      else if (bs >= 40) score += 1;

      if (confirmed) score += 2;
      if (obvGood) score += 1;
      if (macdGood) score += 1;
      if (failed) score -= 4;

      // Break rất mạnh nhưng quá nóng -> vẫn giữ mạnh, không cộng mua.
      if (distEma9 > 8) score += 1; // vẫn là break mạnh
      if (rsi >= 78) score += 1;    // vẫn là rất nóng / leader đang phi

      return clamp(score, 0, 9);
    }

    function detectStage(row) {
      const bs = safeNum(row.breakoutStrength);
      const distEma9 = safeNum(row.distEma9Pct);
      const rsi = safeNum(row.rsi);
      const structure = String(row.priceStructure || '').toUpperCase();

      if (structure.includes('BASE') || structure.includes('SIDEWAY') || (rsi >= 48 && rsi < 58 && bs < 55)) {
        return 'EARLY';
      }
      if (bs >= 55 && distEma9 <= 9 && rsi >= 55 && rsi <= 74) {
        return 'MID';
      }
      return 'LATE';
    }

    function scoreStrength(row) {
      let s = 0;
      const distEma9 = safeNum(row.distEma9Pct);
      const distMa20 = safeNum(row.distMa20Pct);
      const rsi = safeNum(row.rsi);
      const rsiVs = safeNum(row.rsi) - safeNum(row.rsiEma9);
      const obvAbove = !!row.obvAboveEma;
      const obvTrend = String(row.obvTrend || '').toUpperCase();
      const macd = safeNum(row.macd);
      const signal = safeNum(row.macdSignal);
      const hist = safeNum(row.hist);
      const atrTrend = String(row.atrTrend || '').toUpperCase();
      const structure = String(row.priceStructure || '').toUpperCase();

      if (distEma9 >= 0 && distEma9 <= 10) s += 2;
      else if (distEma9 > 10 && distEma9 <= 16) s += 1;
      else if (distEma9 < -3) s -= 1;

      if (distMa20 >= 0) s += 1;
      if (rsi >= 55) s += 2;
      else if (rsi >= 50) s += 1;
      if (rsiVs >= 0) s += 1;
      if (obvAbove) s += 2;
      if (obvTrend === 'UP' || obvTrend === 'FLAT') s += 1;
      if (macd >= signal) s += 1;
      if (hist > 0) s += 1;
      if (atrTrend === 'UP' || atrTrend === 'FLAT') s += 1;
      if (structure.includes('HH') || structure.includes('UP') || structure.includes('BASE')) s += 1;

      s += Math.min(3, scoreBreak(row) / 3);
      return clamp(Math.round(s), 0, 15);
    }

    function scoreBuyability(row) {
      let b = 0;
      const distEma9 = safeNum(row.distEma9Pct);
      const distMa20 = safeNum(row.distMa20Pct);
      const rsi = safeNum(row.rsi);
      const breakScore = scoreBreak(row);
      const failed = !!row.failedAfterBreak;
      const structure = String(row.priceStructure || '').toUpperCase();
      const obvTrend = String(row.obvTrend || '').toUpperCase();

      // Vị trí mua đẹp
      if (distEma9 >= -1.5 && distEma9 <= 4.5) b += 4;
      else if (distEma9 > 4.5 && distEma9 <= 7) b += 2;
      else if (distEma9 > 7) b -= 3;
      else if (distEma9 < -2.5) b -= 2;

      if (distMa20 >= 0 && distMa20 <= 8) b += 2;
      if (rsi >= 55 && rsi <= 72) b += 3;
      else if (rsi > 72 && rsi <= 78) b += 1;
      else if (rsi > 78) b -= 2;

      if (breakScore >= 4 && breakScore <= 7) b += 2;  // break vừa đẹp để mua
      if (breakScore >= 8) b -= 1;                     // quá nóng, thiên về chờ pull
      if (failed) b -= 4;
      if (structure.includes('PULL') || structure.includes('RETEST') || structure.includes('BASE')) b += 2;
      if (obvTrend === 'UP' || obvTrend === 'FLAT') b += 1;

      return clamp(Math.round(b), 0, 12);
    }

    function classifyAction(row) {
      const strength = scoreStrength(row);
      const buyScore = scoreBuyability(row);
      const breakScore = scoreBreak(row);
      const distEma9 = safeNum(row.distEma9Pct);
      const rsi = safeNum(row.rsi);
      const failed = !!row.failedAfterBreak;

      if (failed || strength < 7) {
        return 'AVOID';
      }

      // Ý anh chốt: break quá mạnh thì vẫn là mạnh nhưng không đưa vào mua, đưa chờ pull.
      const overExtended = distEma9 > 7 || rsi >= 78 || breakScore >= 8;
      if (strength >= 9 && overExtended) {
        return 'WAIT_PULL';
      }

      if (strength >= 9 && buyScore >= 7) {
        return 'BUY';
      }

      if (strength >= 8) {
        return 'WAIT_PULL';
      }

      return 'AVOID';
    }

    function notesFor(row) {
      const action = row.action;
      const parts = [];
      if (row.breakScore >= 8) parts.push('break rất mạnh');
      else if (row.breakScore >= 5) parts.push('break ổn');
      if (safeNum(row.distEma9Pct) > 7) parts.push('xa EMA9');
      if (safeNum(row.rsi) >= 78) parts.push('RSI cao');
      if (String(row.obvTrend).toUpperCase() === 'UP') parts.push('OBV lên');
      if (String(row.priceStructure).toUpperCase().includes('PULL')) parts.push('đang pull');
      if (action === 'BUY') parts.push('vị trí mua được');
      if (action === 'WAIT_PULL') parts.push('không đu, chờ pull');
      if (action === 'AVOID') parts.push('chưa đủ điều kiện');
      return parts.join(' | ');
    }

    function enrichRow(raw, sectorMap) {
      const row = {
        symbol: String(raw.symbol || '').toUpperCase(),
        sector: raw.sector || sectorMap[String(raw.symbol || '').toUpperCase()] || 'KHÁC',
        close: safeNum(raw.close),
        changePct: safeNum(raw.changePct),
        distEma9Pct: safeNum(raw.distEma9Pct),
        distMa20Pct: safeNum(raw.distMa20Pct),
        rsi: safeNum(raw.rsi),
        rsiEma9: safeNum(raw.rsiEma9),
        obvTrend: String(raw.obvTrend || 'FLAT').toUpperCase(),
        obvAboveEma: !!raw.obvAboveEma,
        macd: safeNum(raw.macd),
        macdSignal: safeNum(raw.macdSignal),
        hist: safeNum(raw.hist),
        atrTrend: String(raw.atrTrend || 'FLAT').toUpperCase(),
        breakoutStrength: safeNum(raw.breakoutStrength),
        breakoutConfirmed: !!raw.breakoutConfirmed,
        failedAfterBreak: !!raw.failedAfterBreak,
        priceStructure: String(raw.priceStructure || 'SIDEWAY').toUpperCase()
      };
      row.breakScore = scoreBreak(row);
      row.stage = detectStage(row);
      row.strength = scoreStrength(row);
      row.buyScore = scoreBuyability(row);
      row.action = classifyAction(row);
      row.notes = notesFor(row);
      return row;
    }

    function badgeHtml(action) {
      if (action === 'BUY') return '<span class="buy">BUY</span>';
      if (action === 'WAIT_PULL') return '<span class="wait">WAIT_PULL</span>';
      return '<span class="avoid">AVOID</span>';
    }

    function formatPct(n) {
      return `${n > 0 ? '+' : ''}${safeNum(n).toFixed(2)}%`;
    }

    function escapeHtml(s) {
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    const state = {
      rows: [],
      timer: null,
      groups: parseWatchlist(localStorage.getItem(STORAGE_KEYS.watchlist) || buildDefaultWatchlistText())
    };

    function getSectorMap() {
      const map = {};
      Object.entries(state.groups).forEach(([sector, list]) => {
        list.forEach(symbol => map[symbol] = sector);
      });
      return map;
    }

    function hydrateWatchlistUI() {
      const text = localStorage.getItem(STORAGE_KEYS.watchlist) || buildDefaultWatchlistText();
      document.getElementById('watchlistEditor').value = text;

      const sectorFilter = document.getElementById('sectorFilter');
      const current = sectorFilter.value || 'ALL';
      sectorFilter.innerHTML = '<option value="ALL">Tất cả ngành</option>';
      Object.keys(state.groups).forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        sectorFilter.appendChild(opt);
      });
      sectorFilter.value = Array.from(sectorFilter.options).some(o => o.value === current) ? current : 'ALL';
    }

    function renderRows() {
      const body = document.getElementById('scannerBody');
      const search = document.getElementById('searchInput').value.trim().toUpperCase();
      const sector = document.getElementById('sectorFilter').value;
      const action = document.getElementById('actionFilter').value;
      const stage = document.getElementById('stageFilter').value;

      let rows = [...state.rows].filter(r => {
        const okSearch = !search || r.symbol.includes(search) || r.sector.toUpperCase().includes(search);
        const okSector = sector === 'ALL' || r.sector === sector;
        const okAction = action === 'ALL' || r.action === action;
        const okStage = stage === 'ALL' || r.stage === stage;
        return okSearch && okSector && okAction && okStage;
      });

      rows.sort((a, b) => {
        const actionRank = { BUY: 0, WAIT_PULL: 1, AVOID: 2 };
        return actionRank[a.action] - actionRank[b.action] || b.strength - a.strength || b.buyScore - a.buyScore || b.changePct - a.changePct;
      });

      body.innerHTML = rows.map((r, idx) => `
        <tr>
          <td>${idx + 1}</td>
          <td><b>${escapeHtml(r.symbol)}</b></td>
          <td>${escapeHtml(r.sector)}</td>
          <td>${r.stage}</td>
          <td>${badgeHtml(r.action)}</td>
          <td>${r.strength}</td>
          <td>${r.buyScore}</td>
          <td>${r.breakScore}</td>
          <td>${r.close.toFixed(2)}</td>
          <td>${formatPct(r.changePct)}</td>
          <td>${formatPct(r.distEma9Pct)}</td>
          <td>${formatPct(r.distMa20Pct)}</td>
          <td>${r.rsi.toFixed(1)}</td>
          <td>${(r.rsi - r.rsiEma9).toFixed(1)}</td>
          <td>${r.obvAboveEma ? 'Trên EMA9' : 'Dưới EMA9'} / ${r.obvTrend}</td>
          <td>${r.macd.toFixed(2)} / ${r.macdSignal.toFixed(2)} / ${r.hist.toFixed(2)}</td>
          <td>${r.atrTrend}</td>
          <td>${escapeHtml(r.priceStructure)}</td>
          <td>${escapeHtml(r.notes)}</td>
        </tr>
      `).join('');

      document.getElementById('totalCount').textContent = state.rows.length;
      document.getElementById('buyCount').textContent = state.rows.filter(r => r.action === 'BUY').length;
      document.getElementById('waitCount').textContent = state.rows.filter(r => r.action === 'WAIT_PULL').length;

      document.getElementById('buyList').innerHTML = state.rows
        .filter(r => r.action === 'BUY')
        .sort((a,b) => b.buyScore - a.buyScore || b.strength - a.strength)
        .slice(0, 25)
        .map(r => `<div><b>${r.symbol}</b> - ${r.sector} - Strength ${r.strength} - Buy ${r.buyScore} <span class="ok">| ${escapeHtml(r.notes)}</span></div>`)
        .join('') || '<span class="muted">Chưa có dữ liệu</span>';

      document.getElementById('waitList').innerHTML = state.rows
        .filter(r => r.action === 'WAIT_PULL')
        .sort((a,b) => b.strength - a.strength || b.breakScore - a.breakScore)
        .slice(0, 25)
        .map(r => `<div><b>${r.symbol}</b> - ${r.sector} - Strength ${r.strength} - Break ${r.breakScore} <span style="color:#ffd97a">| ${escapeHtml(r.notes)}</span></div>`)
        .join('') || '<span class="muted">Chưa có dữ liệu</span>';
    }

    function exportCsv() {
      const header = ['symbol','sector','stage','action','strength','buyScore','breakScore','close','changePct','distEma9Pct','distMa20Pct','rsi','rsiEma9','obvTrend','obvAboveEma','macd','macdSignal','hist','atrTrend','breakoutStrength','breakoutConfirmed','failedAfterBreak','priceStructure','notes'];
      const lines = [header.join(',')];
      state.rows.forEach(r => {
        lines.push([
          r.symbol, r.sector, r.stage, r.action, r.strength, r.buyScore, r.breakScore,
          r.close, r.changePct, r.distEma9Pct, r.distMa20Pct, r.rsi, r.rsiEma9,
          r.obvTrend, r.obvAboveEma, r.macd, r.macdSignal, r.hist, r.atrTrend,
          r.breakoutStrength, r.breakoutConfirmed, r.failedAfterBreak, r.priceStructure,
          '"' + String(r.notes).replaceAll('"', '""') + '"'
        ].join(','));
      });
      const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'scanner_v15_2.csv';
      a.click();
      URL.revokeObjectURL(a.href);
    }

    function updateAutoRefresh() {
      const v = Number(document.getElementById('refreshSelect').value);
      localStorage.setItem(STORAGE_KEYS.refresh, String(v));
      if (state.timer) clearInterval(state.timer);
      state.timer = null;
      if (v > 0) {
        state.timer = setInterval(() => runScan(false), v * 60 * 1000);
      }
    }

    async function runScan(showAlertOnEmpty = false) {
      try {
        const watchlist = flattenGroups(state.groups);
        const symbols = watchlist.map(v => v.symbol);
        const sectorMap = getSectorMap();
        const rawRows = await fetchRealtimeRows(symbols, sectorMap);
        state.rows = rawRows.map(r => enrichRow(r, sectorMap));
        renderRows();
        document.getElementById('lastUpdate').textContent = new Date().toLocaleString('vi-VN');
        if (showAlertOnEmpty && !state.rows.length) {
          alert('Không có dữ liệu. Anh kiểm tra lại hàm fetchRealtimeRows() hoặc bấm Nạp dữ liệu mẫu để test.');
        }
      } catch (err) {
        console.error(err);
        alert('Lỗi scan: ' + (err?.message || err));
      }
    }

    function makeSampleRows(symbols, sectorMap) {
      // Dữ liệu mẫu để test logic. Có chủ ý tạo các case break mạnh nhưng WAIT_PULL.
      const hotNames = new Set(['NVL','VIC','VHM','HCM','VJC','KBC','BMP','MWG','TCH','HHS','CII']);
      return symbols.map((symbol, i) => {
        const hot = hotNames.has(symbol);
        const seed = symbol.split('').reduce((a, c) => a + c.charCodeAt(0), 0) + i * 17;
        const rand = (min, max) => min + (Math.sin(seed + max) + 1) / 2 * (max - min);

        if (hot) {
          return {
            symbol,
            sector: sectorMap[symbol],
            close: rand(18, 95),
            changePct: rand(2.5, 6.8),
            distEma9Pct: rand(7.5, 14),
            distMa20Pct: rand(11, 19),
            rsi: rand(76, 86),
            rsiEma9: rand(68, 77),
            obvTrend: 'UP',
            obvAboveEma: true,
            macd: rand(1.4, 3.5),
            macdSignal: rand(0.8, 2.0),
            hist: rand(0.3, 1.2),
            atrTrend: 'UP',
            breakoutStrength: rand(84, 97),
            breakoutConfirmed: true,
            failedAfterBreak: false,
            priceStructure: 'UP_BREAK'
          };
        }

        const phase = seed % 3;
        if (phase === 0) {
          return {
            symbol,
            sector: sectorMap[symbol],
            close: rand(12, 68),
            changePct: rand(-0.8, 2.2),
            distEma9Pct: rand(-1.2, 3.8),
            distMa20Pct: rand(0.2, 7.5),
            rsi: rand(56, 71),
            rsiEma9: rand(52, 67),
            obvTrend: 'UP',
            obvAboveEma: true,
            macd: rand(0.2, 1.8),
            macdSignal: rand(0.1, 1.2),
            hist: rand(0.05, 0.8),
            atrTrend: 'FLAT',
            breakoutStrength: rand(48, 72),
            breakoutConfirmed: true,
            failedAfterBreak: false,
            priceStructure: 'PULL_RETEST'
          };
        }
        if (phase === 1) {
          return {
            symbol,
            sector: sectorMap[symbol],
            close: rand(10, 55),
            changePct: rand(-2.5, 0.9),
            distEma9Pct: rand(-4.5, 1.5),
            distMa20Pct: rand(-7.5, 1.5),
            rsi: rand(41, 56),
            rsiEma9: rand(43, 54),
            obvTrend: 'DOWN',
            obvAboveEma: false,
            macd: rand(-1.5, 0.2),
            macdSignal: rand(-1.2, 0.5),
            hist: rand(-0.8, 0.1),
            atrTrend: 'UP',
            breakoutStrength: rand(15, 42),
            breakoutConfirmed: false,
            failedAfterBreak: seed % 5 === 0,
            priceStructure: 'SIDEWAY_DOWN'
          };
        }
        return {
          symbol,
          sector: sectorMap[symbol],
          close: rand(8, 72),
          changePct: rand(-0.5, 1.6),
          distEma9Pct: rand(-0.8, 2.8),
          distMa20Pct: rand(-0.5, 4.5),
          rsi: rand(49, 58),
          rsiEma9: rand(47, 57),
          obvTrend: 'FLAT',
          obvAboveEma: seed % 2 === 0,
          macd: rand(-0.2, 0.6),
          macdSignal: rand(-0.3, 0.7),
          hist: rand(-0.1, 0.25),
          atrTrend: 'FLAT',
          breakoutStrength: rand(28, 52),
          breakoutConfirmed: seed % 2 === 0,
          failedAfterBreak: false,
          priceStructure: 'BASE_SIDEWAY'
        };
      });
    }

    // =============================================================
    //  QUAN TRỌNG: CHỈNH HÀM NÀY NẾU ANH MUỐN NỐI ĐÚNG API V15 CŨ
    // =============================================================
    async function fetchRealtimeRows(symbols, sectorMap) {
      // CÁCH 1: Dùng dữ liệu mẫu mặc định để test giao diện + logic
      if (window.__USE_SAMPLE_DATA__ === true) {
        return makeSampleRows(symbols, sectorMap);
      }

      // CÁCH 2: Nối lại API thật.
      // Ví dụ nếu V15 cũ của anh đã có endpoint trả JSON, anh thay đoạn này bằng fetch(endpoint).
      // Mỗi row trả về cần map được về các field ở phần hướng dẫn phía trên.
      //
      // Ví dụ mẫu:
      // const res = await fetch(`http://127.0.0.1:5000/api/scanner?symbols=${symbols.join(',')}`);
      // const data = await res.json();
      // return data.rows;
      //
      // Vì em không có endpoint V15 cũ ở cuộc chat này nên em chủ động báo rõ để tránh viết bừa.

      return [];
    }

    function initEvents() {
      document.getElementById('searchInput').addEventListener('input', renderRows);
      document.getElementById('sectorFilter').addEventListener('change', renderRows);
      document.getElementById('actionFilter').addEventListener('change', renderRows);
      document.getElementById('stageFilter').addEventListener('change', renderRows);
      document.getElementById('refreshSelect').addEventListener('change', updateAutoRefresh);
      document.getElementById('scanBtn').addEventListener('click', () => runScan(true));
      document.getElementById('exportBtn').addEventListener('click', exportCsv);

      document.getElementById('saveWatchlistBtn').addEventListener('click', () => {
        const text = document.getElementById('watchlistEditor').value.trim();
        localStorage.setItem(STORAGE_KEYS.watchlist, text);
        state.groups = parseWatchlist(text);
        hydrateWatchlistUI();
        alert('Đã lưu watchlist mới.');
      });

      document.getElementById('resetWatchlistBtn').addEventListener('click', () => {
        const text = buildDefaultWatchlistText();
        localStorage.setItem(STORAGE_KEYS.watchlist, text);
        state.groups = parseWatchlist(text);
        hydrateWatchlistUI();
        alert('Đã khôi phục watchlist chuẩn V15.2.');
      });

      document.getElementById('sampleDataBtn').addEventListener('click', async () => {
        window.__USE_SAMPLE_DATA__ = true;
        await runScan(true);
      });
    }

    function bootstrap() {
      const savedRefresh = localStorage.getItem(STORAGE_KEYS.refresh) || '5';
      document.getElementById('refreshSelect').value = savedRefresh;
      hydrateWatchlistUI();
      initEvents();
      updateAutoRefresh();
      renderRows();
    }

    bootstrap();
  </script>
</body>
</html>
