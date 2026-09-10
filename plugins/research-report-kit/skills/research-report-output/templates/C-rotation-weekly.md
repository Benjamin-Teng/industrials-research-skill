---
title: 〈YYYYWnn〉輪動掃描與 Channel Check 週報
subtitle: 〈本期最重要的一件事〉
type: 輪動掃描週報
market: TW+US                    # 輪動多半台美並看；單一市場則填 TW 或 US
ticker: 〈本期涉及標的，可留空〉
version: v1.0
date: YYYY-MM-DD
price_asof: YYYY-MM-DD 收盤
author: 〈你的名字或機構〉
framework: 〈你的方法論文件名 vX.Y〉 ＋ 研究報告輸出規範 v2.0
rating: 〈本期部位傾向〉
methodology_version: expectations-v1
research_question: 〈本期要驗證的輪動命題，一句話、可證偽〉
as_of: "YYYY-MM-DD HH:MM"           # 本次可用資訊的截止日期與時間（FR-01）
strategy_type: catalyst          # fundamental／catalyst／monitoring（FR-01；輪動週報預設 catalyst）
holding_horizon_months: null
forecast_horizon_years: null
valuation_methods: []
expectations_status: insufficient # supported / insufficient / no_material_gap
decision_status: watch           # actionable_candidate / watch / avoid
decision_policy_source: unspecified
kpi:
  - {label: 本期驗證問題, value: "0 題", note: "已結案 0 題"}
  - {label: A/B 級證據, value: "0 筆", note: 可行動, tone: bull}
  - {label: 部位動作, value: "0 筆", note: 加 0／減 0}
  - {label: 標題命中率, value: "00%", note: 累計 n=0}
---

## 一、本期結論

**一、新增機會**：

**二、論點變化**：

**三、部位動作**：

## 二、本期驗證問題進度（Step 2）

| # | `thesis_id` | 問題 | 可證偽？ | 進度 | 結論 | 是否改變部位 |
|---|---|---|---|---|---|---|
| 1 | | | ✓ | 已驗證／待補／證偽 | | |
| 2 | | | ✓ | | | |
| 3 | | | ✓ | | | |

## 三、Channel Check Log（本期新增）

> 欄數上限 7 欄，拆兩張表；兩表以「問題#」對應同一筆記錄。

| 日期 | 問題# | `thesis_id` | 層級 | 來源描述（不記個資） | **推定原始消息源** | 可信度 |
|---|---|---|---|---|---|---|
| | | | L2 | | | B |

| 問題# | 內容摘要 | 與前次差異 | 對論點影響 |
|---|---|---|---|
| | | | |

::: note
**升級規則**：只有 A、B 級可作為行動依據；C 級累積兩個**不同消息源**後升為 B。**獨立性 ＝ 推定原始消息源不同**——兩家媒體引用同一份通路調查只算一源。**B 級不自動升格為財務基準事實**——仍是方向性推論，升重倉仍須依 `equity-valuation-discipline/references/expectations-and-decisions.md` 第11節決策條件另行判定。合規紅線：不索取、不使用未公開重大消息（見 `product-cycle-rotation` 的 channel-check SOP 第 0 節）。
:::

## 四、Product Cycle 時間軸定位

| `thesis_id` | 追蹤世代 | 目前階段 | 距 T0 | 本期動作 |
|---|---|---|---|---|
| | | T-12～T-6 design win 期 | | channel check 密度最高 |

> 階段本身不導出建倉／加碼動作；部位判定依第七節與 `equity-valuation-discipline/references/expectations-and-decisions.md` 第11節決策條件。

## 五、催化劑日曆（未來 90 天）

> 每個催化劑須對應命題、模型輸入、預期觀察值／區間、資料來源、日期、更新規則（FR-12）；欄數上限 7 欄，拆兩張表，以「事件」對應同一筆記錄。

| 事件 | 市場 | `thesis_id` | 預計日期 | 資料來源 |
|---|---|---|---|---|
| 【TW】月營收公布 | TW | | 每月 10 日前 | |
| 【US】財報季／Investor Day／keynote | US | | | |
| 高頻報價轉折（DRAM／CCL／面板／運價） | 共用 | | | |

| 事件 | 模型輸入 | 預期觀察值／區間 | 預期影響方向 | 更新規則 |
|---|---|---|---|---|
| 【TW】月營收公布 | | | | |
| 【US】財報季／Investor Day／keynote | | | | |
| 高頻報價轉折（DRAM／CCL／面板／運價） | | | | |

⚠️ **催化劑發生不等於利多，須比對事前預期**：實際結果對照登記時寫下的「預期觀察值／區間」，不是對照「有沒有發生」。

**已發生事件核對**：上期表中已發生者移入此處，依「預期觀察值／區間」判定為**被證偽**／**延後**／**結果未取得**三類之一並更新結論，不得殘留為未來訊號。短期事件策略若因此失去成立前提，依事前政策退出或覆核，**不得默默轉為「長期投資」**；長期命題若不依賴單一日期，事件延後不自動等於命題失效。

## 六、「2–3 個月後新聞標題」推演

### 本期新寫標題

| # | 預測標題 | **主觀機率** | 若成真受惠標的 | 現價已反映多少 | 證偽訊號 | 檢查日 |
|---|---|---|---|---|---|---|
| 1 | | 0.__ | | | | |

### 上期標題驗收

| # | 上期標題 | 宣稱機率 | 是否成真 | **Brier `(p−結果)²`** | 市場反應 vs 預期差 | 歸因（資料／邏輯／時機／運氣） |
|---|---|---|---|---|---|---|
| | | | | | | |

## 七、部位動作與紀律檢查

> 欄數上限 7 欄，拆兩張表，以「標的」對應同一筆記錄。**折價 vs 安全邊際綁定已退役**（見下方 note），不再列為欄位。

| 標的 | `thesis_id` | 動作 | 進場理由 | 執行期限 |
|---|---|---|---|---|
| | | | | __ 交易日 |

| 標的 | 預期催化劑與日期 | 失效條件 | 牛／熊 R/R | 基準／熊 R/R |
|---|---|---|---|---|
| | | | | |

::: note
**個股交易方案的 R/R 與示範機率表（FR-15）**：本表僅列進場基準與牛／熊、基準／熊 R/R 摘要，定義與方向規則見 `equity-valuation-discipline/references/expectations-and-decisions.md` 第7節，不得另抄公式變體。完整的至少三組示範機率配置與期望價差報酬逐組解讀（第8–9節），依該標的深度研究附表或連結另附；不得省略。

**折價 vs 安全邊際綁定已退役**：是否建倉／加碼依 `expectations-and-decisions.md` 第11節決策條件（`decision_status`）判定，不再以「折價 ≥ 固定安全邊際」單一門檻自動決定；安全邊際如採用屬使用者買價政策，非自動門檻。
:::

::: bear
**出場三條件（任一即出場）**：①市價 > 牛情境的持有期末價格 `P_H,bull`（無深度報告者用簡化三情境，並標明是簡化值）；②核心論點門檻被證偽／design win 被證偽；③下一代 delta 由正轉負。**進入 T+6 只觸發覆核，時間本身不是出場理由。**
> ⚠️ 舊版寫「牛情境紀律值」（機率加權期望值），該術語已隨舊決策鏈退役。出場比的是**同一持有期的價格**，不是折回今天的內在價值——兩者混用正是 `expectations-and-decisions.md` 第 5 節要擋的錯。

**催化劑過期分三類處理**：**被證偽**（依失效條件出場）／**延後**（短期事件策略若已失去成立前提，依事前政策退出或覆核，**不得默默轉為「長期投資」**）／**結果未取得**（標記待驗證，不預設方向）。**長期命題若不依賴單一日期，催化劑延後不自動等於命題失效。**
:::

## 八、觀察名單異動

| 標的 | `thesis_id` | 動作 | 理由 |
|---|---|---|---|
| | | 新增／移除／升級為深度研究候選 | |

## 九、Caveats

::: caveat
〈本期資訊的來源層級限制、未驗證項目〉
:::
