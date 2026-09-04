---
name: price-routing
description: "任何需要取得股票、ETF、期貨報價或歷史價格的場景自動路由：先偵測 session 中有哪些行情工具可用，再依標的市場選路（台股優先走台股資料源 MCP，美股優先走券商 MCP），皆不可用時 fallback yfinance。在調用任何取價工具前先確認可用性。也在使用者說「查一下股價」「這檔現在多少」「抓歷史價」時使用。"
---

# 取價工具路由（Price Routing）

## 適用時機

任何需要取得股票、ETF、期貨報價或歷史價格的場景：研究報告、個股分析、價格比較、技術分析、估值計算。

**設計前提：不假設任何 MCP 存在。** 本 skill 每次都先偵測可用工具再選路，沒有任何資料源時仍能透過 `yfinance` 完成任務。

---

## Step 1：判別市場

依以下順序判別標的所屬市場：

1. **明確指定**：使用者或 front matter 的 `market` 欄位（`TW`、`US`、`TW+US`）
2. **Ticker 格式推斷**：
   - 純數字 4–6 碼（如 `2330`、`00878`） → 台股
   - `TWSE:` / `TPEx:` 前綴 → 台股
   - 英文字母 1–5 碼（如 `AAPL`、`NVDA`） → 美股
   - `NYSE:` / `NASDAQ:` 前綴 → 美股
3. **中文名稱**：使用者用中文公司名（如「台積電」「鴻海」） → 台股
4. **其他市場**（港股、日股、歐股）→ 直接走 `yfinance`，用該市場的 Yahoo 後綴（`.HK`、`.T`、`.DE` 等）
5. **無法判別** → 詢問使用者

---

## Step 2：偵測可用工具

**在發出任何取價呼叫之前**，掃描當前 session 的工具清單，判斷下列三類是否存在（工具名稱依安裝方式而異，用關鍵字比對）：

| 類別 | 判斷方式 | 典型工具名 |
|---|---|---|
| **台股資料源 MCP** | 工具名含 `finmind`、或含 `taiwan` + `stock` | `finmind__get_stock_info`、`finmind__query_dataset`、`plugin_finmind-mcp_finmind__*` |
| **券商／美股行情 MCP** | 工具名含 `price_history`、`price_snapshot`、`quote`，或含券商名（`ibkr`、`interactive_brokers`、`schwab`、`alpaca`） | `Interactive_Brokers_IBKR__get_price_history`、`*__get_price_snapshot` |
| **yfinance** | 永遠可用（Python 環境安裝即可） | — |

工具可能被延遲載入（deferred）。若工具清單顯示某工具存在但尚未載入 schema，**先載入再呼叫**，不要因為「還沒載入」就判定不可用。

---

## Step 3：依市場執行取價

### 台股（`market: TW`）

```
台股資料源 MCP 可用？
  ├─ 是 → 用它（股價、月營收、三大法人、融資融券等台股特有欄位都在這裡）
  │       └─ 失敗（timeout／5xx）→ 券商 MCP 可用？
  │           ├─ 是 → fallback 券商（先用合約搜尋找到台股標的 → 取歷史價）
  │           └─ 否 → fallback yfinance（上市加 `.TW`、上櫃加 `.TWO`）
  └─ 否 → 券商 MCP 可用？
      ├─ 是 → 用券商 MCP
      └─ 否 → fallback yfinance
```

### 美股（`market: US`）

```
券商／美股行情 MCP 可用？
  ├─ 是 → 用它（取歷史價或即時快照）
  │       └─ 失敗 → fallback yfinance（直接用 ticker）
  └─ 否 → fallback yfinance
```

### 台＋美混合（`market: TW+US`）

各標的依上述規則**分別**路由。不要為了統一而把兩邊都降級到 yfinance。

---

## yfinance Fallback 用法

```bash
pip install yfinance --break-system-packages
```

```python
import yfinance as yf

# 台股：上市加 .TW、上櫃加 .TWO
df = yf.download("2330.TW", start="2026-06-01", end="2026-09-03")
otc = yf.download("6547.TWO", start="2026-06-01", end="2026-09-03")

# 美股：直接用 ticker
us = yf.download("AAPL", start="2026-06-01", end="2026-09-03")

# 其他市場：港股 .HK、日股 .T、德股 .DE
```

**限制**（使用時須知會使用者）：

- 資料可能有 15–20 分鐘延遲，不適合當「即時報價」
- **不含台股特有欄位**：三大法人、融資融券、月營收、質押比都取不到——這些欄位缺失時，報告的監控儀表板須改用替代指標並在 Caveats 註明
- 除權息調整口徑與台灣本地資料源可能不同，跨源比對前先確認是否為還原股價

---

## 價格書寫格式（強制）

取到價之後，寫進報告時**一律用「數值＋日期＋盤別」三件套**：

```
US$218.98（2026-08-14 正常盤收盤）
NT$1,085（2026-09-02 收盤）
```

盤別要寫清楚：正常盤收盤／盤中／盤後／夜盤。**缺任一件即視為未查證數據，不得跨文件引用。**

---

## 告知原則

- **正常路由**（台股走台股資料源、美股走券商 MCP）：不需特別說明。
- **發生 fallback 時**：簡短告知「〈原資料源〉暫時無法連線，改用〈替代源〉取價」。
- **使用 yfinance 時**：提醒資料可能有延遲，且部分進階欄位不可用。
- **一個 MCP 都沒有時**：第一次取價時說明一次「目前沒有連接行情資料源，改用 yfinance；要更即時或更完整的台股籌碼資料，可以連接對應的 MCP」，之後不再重複。
