# 研究報告輸出規範（格式與交付標準）

> **版本**：v2.0（發布版）　|　**適用**：個股深度研究、產業／供應鏈研究、輪動掃描週報，**台股與美股共用同一套骨架**
> **本文件管的是「格式與交付」，不是「研究內容」**：內容對錯看方法論文件（`equity-valuation-discipline` 或你自己的框架），長什麼樣、怎麼交、怎麼歸檔看本文件。
> **回報語言**：繁體中文（專有名詞、財務科目、公司代號保留原文）。

---

## 零、鐵則（Non-negotiable）

1. **每份研究輸出一律同時產出 `.md` 與 `.pdf` 兩個檔**，且兩檔內容必須一致（PDF 由該 md 直接產生，不得手改）。
2. **PDF 由 `md2pdf.py` 產生**，套用機構研究報告樣式；不得用未套樣式的裸轉檔交付。
3. **兩個檔都必須交付給使用者**，並在同一則訊息內附一句話結論。Claude 用 `SendUserFile`；Codex／其他環境把檔案寫進工作目錄並告知路徑。
4. **md 檔必須含 YAML front matter**（第二章），缺必填欄位即不得交付。
5. **所有關鍵數據標註資料層級標籤與查價日**（第四章），未標註者視為未完成。
6. **骨架不因市場而變**：台股、美股共用同一套章節與檢查清單，**只換資料源、籌碼欄位與幣別口徑**（`market-localization.md`）。
7. **發布前跑完第八章格式層檢查清單＋F-rules 自查**（`formatting-rules.md`）；內容層檢查清單另見方法論文件。

---

## 一、檔名規則

```text
{主體}_{報告類型}_{版本}_{YYYYMMDD}.md / .pdf
```

| 報告類型 | 主體寫法 | 範例 |
|---|---|---|
| A 個股深度研究 | 公司名＋代號 | `台玻1802_個股深度研究_v1.0_20260806.pdf`／`Corning_GLW_個股深度研究_v1.0_20260806.pdf` |
| B 產業供應鏈研究 | 產業／技術主題 | `AI伺服器液冷_產業供應鏈研究_v1.0_20260806.pdf` |
| C 輪動掃描週報 | 期間 | `2026W32_輪動掃描週報_v1.0_20260806.pdf` |

- 版本語意：`v1.0` 首發；`v1.1` 小幅更新或補資料；**`v2.0` 結論改變**。結論改變一律進位主版號，並在文件開頭「版本紀錄」寫明改了什麼、為什麼改。
- 同一標的的新版**不覆蓋舊版**，兩版並存以利覆盤。
- 輸出模式後綴：External 加 `_ext`、Briefing 加 `_brief`（見 SKILL.md「輸出模式」）。

---

## 二、YAML Front Matter 規格

每份 md 開頭必附，★ 為必填：

```yaml
---
title: 〈公司名〉〈代號〉個股深度研究報告   # ★
subtitle: 一句話講清楚論點與方法            # ★
type: 個股深度研究                         # ★ 個股深度研究 / 產業供應鏈研究 / 輪動掃描週報
market: TW                                 # ★ TW / US / TW+US → 決定套哪一組在地化欄位
ticker: TWSE:0000                          # ★ 台股 TWSE:xxxx／TPEx:xxxx；美股 NYSE:XXX／NASDAQ:XXXX
version: v1.0                              # ★ 報告版本（見下方三者分開說明）
date: 2026-08-06                           # ★ 發布日
price_asof: 2026-08-05 正常盤收盤           # ★ 市場數據基準日與口徑（三件套）
author: 〈你的名字或機構〉                   # ★
framework: 〈方法論文件名 vX.Y〉             # ★ 本報告套用的上位框架與版本
methodology_version: expectations-v1       # ★ A 型必填；方法論主版本（見下方三者分開說明）
research_question: 〈本次要驗證的投資命題〉  # ★ 一句話、可證偽（FR-01）
as_of: 2026-08-05 18:00                    # ★ 本次可用資訊截止日期與時間（FR-01）
strategy_type: fundamental                 # fundamental / catalyst / monitoring；未定填 unknown 並說明影響
holding_horizon_months: 12                 # 未指定時填暫定值並在 Caveats 標為研究假設
forecast_horizon_years: 5                  # 營運模型明確預測年限，與 holding_horizon_months 分開，不得互代
valuation_methods: [cycle_normalized]      # 對應 FR-05 方法 ID，可多選
expectations_status: insufficient          # supported / insufficient / no_material_gap；預設 insufficient
decision_status: watch                     # actionable_candidate / watch / avoid；預設 watch；須與 rating 一致
decision_policy_source: unspecified        # 使用者報酬要求與風險政策來源；預設 unspecified
edge_status:                               # hypothesis_only / evidence_supported / validated_with_limits；提出 edge 結論時必填，預設不得高於 hypothesis_only
rating: 〈分批布局／觀察／回避〉              # A 型必填；B/C 型填產業評等或結論標籤
footer_right: 個人研究筆記 · 非投資建議      # 選填；頁尾右欄標語
disclaimer: 〈封面免責條款全文〉            # 選填；不填則用產檔器預設值
baseline_of: 2026-08-13 Investor Day       # 選填；未來 30 天內有已排定事件、或事件已發生但結果未取得時必填
kpi:                                       # ★ 首頁 KPI 摘要卡，3–5 張
  - {label: 現價, value: "NT$28.5", note: "2026-08-05 正常盤收盤"}
  - {label: 核心價格隱含要求, value: "〈成長率／利潤率組合〉", note: 條件性假設組合}
  - {label: 內在價值區間 V0, value: "34–41", note: 三情境, tone: bull}
  - {label: "指定持有期成本後預期報酬 E[R_H]", value: "11%", note: 機率加權}
  - {label: 熊情境持有期損失, value: "-18%", note: 非最大損失, tone: bear}
---
```

`tone` 可填 `bull`／`bear`／留空（中性）。B 型的 KPI 卡改放市場規模、CAGR、關鍵瓶頸環節、滲透率；C 型改放本期問題數、A/B 級證據數、部位動作數、Brier 分數。A 型 KPI 卡可含現價、核心價格隱含要求、內在價值區間、指定持有期成本後預期報酬、熊情境持有期損失；**未知項不填零，缺值行為見下方**；⛔ **不得把熊情境持有期損失標為最大可能損失**。

### 2.1 `methodology_version`／`version`／plugin semver 三者分開

| 欄位 | 管的是什麼 | 誰改它 |
|---|---|---|
| `methodology_version` | 本報告套用的**方法論主版本**（如 `expectations-v1`），對應 `equity-valuation-discipline` 的方法論代際 | 方法論改版時才變 |
| `version`（front matter 既有欄位） | **這份報告**本身的版本（`v1.0`／`v1.1`／`v2.0`），見第一章版本語意 | 每次補資料或結論改變時變 |
| plugin manifest 的 semver | **這個 plugin 套件**的版本（`plugin.json`） | plugin 發布新版時變 |

三者不得互相替代：同一 `methodology_version` 下可以有很多份不同 `version` 的報告；plugin 升版不代表所有既有報告的 `methodology_version` 自動變更。

### 2.2 `rating` 必須與 `decision_status` 一致

`rating` 是**閱讀用的評等文字**，`decision_status` 是**機器可讀的條件門檻結果**（定義見 `equity-valuation-discipline/references/expectations-and-decisions.md` 第 11 節）。兩者必須一致，對應規則：

| `decision_status` | `rating` 應填 |
|---|---|
| `actionable_candidate` | 分批布局／可建首批（依框架用語） |
| `watch` | 觀察 |
| `avoid` | 回避 |

⛔ 兩者不一致視為未完成；改其中一個必須同步改另一個。

### 2.3 新增欄位的缺值行為

- `strategy_type`／`holding_horizon_months`／`forecast_horizon_years`／`decision_policy_source` 等 FR-01 契約欄位：**未知者一律標 `unknown`（或對應預設值）並在正文說明對結論成熟度的影響**，不得捏造使用者偏好。
- `holding_horizon_months` 未指定時可提暫定值，但須在十二、Caveats 明標為研究假設，不得直接當成使用者要求。
- `valuation_methods` 為空陣列時，代表尚未完成路徑判別，報告不得宣稱已完成估值。
- `expectations_status` 缺省為 `insufficient`；分歧不足或模型不可識別時應維持 `insufficient` 或改為 `no_material_gap`，不得因未填而預設 `supported`。
- `decision_status` 缺省為 `watch`；升為 `actionable_candidate` 前須通過 `expectations-and-decisions.md` 第 11 節條件門檻全部項目。
- `decision_policy_source` 缺省為 `unspecified`；為 `unspecified` 時，Recommendations 只能輸出條件式結論，不得輸出最適部位或自動交易指令。
- `edge_status` 選填，但**提出 edge 結論時必填**；未填視為未提出 edge 結論；填寫時預設不得高於 `hypothesis_only`，除非在文中補齊對應證據（`expectations-and-decisions.md` 第 13 節交付條件）。

::: note
**`baseline_of` 渲染**：`md2pdf.py` 會讀取此欄位，封面出現琥珀色「基線版」橫幅（含事件內容），封面資訊表也會列出一列。**只填 `baseline_of` 即可**；是否併寫進 `subtitle` 為建議而非必要。
:::

**幣別與價格書寫紀律**：`kpi` 與內文的價格一律**明寫幣別前綴**（`NT$` / `US$`）；跨市場比較表另設「原幣」與「換算幣別＋匯率基準日」兩欄，不得混用。

**價格書寫格式強制為「數值＋日期＋盤別」三件套**（例：`US$218.98（2026-08-14 正常盤收盤）`），`price_asof` 亦須含盤別。**缺任一件即視為未查證數據，不得跨文件引用。** 同一報告內若有第二個價格基準，須另標並在 Caveats 揭露結論對基準日的依賴。

---

## 三、三種報告的骨架

### A 型｜個股深度研究報告（`methodology_version: expectations-v1`）

0. 首頁 KPI 摘要卡（由 front matter `kpi` 自動生成）
1. **TL;DR**：決策狀態、主要預期差、持有期／最大不確定性（三點，每點粗體開頭）
2. **Key Findings**（約 5 點，每點附一手來源與資料層級標籤）
3. **市場預期基線與預期差台帳**：公司指引、賣方共識、價格隱含預期分列；含 FR-04 兩張預期差台帳表（`thesis_id` 串連情境與監控）
4. **事業結構與供應鏈**：(a) 事業結構拆解｜(b) 供應鏈定位（一般／高階兩層）
5. **財務品質**：具體風險如何進入現金流與情境（風險映射，不得只調機率）
6. **模型選擇、三情境內在價值、持有期價格與報酬、交叉比較**：**先跑路徑判別**，歸類結果寫在估值節開頭；依 FR-07 分開 `V0_i`／`P_H_i`／`R_H_i` 三個量；於價格情境後依 FR-15／16 插入「R/R → 示範機率表 → 各組條列解讀」
7. **敏感度分析**：主導變數、機率與必要的價格反映假設；二維表標現價
8. **反方論證與 Pre-mortem**（用 `::: bear` 框，含情境機率的書面理由）
9. **催化劑與驗證時間表**：每個催化劑對應命題、模型輸入、預期觀察值／區間、資料來源、日期、更新規則（FR-12）
10. **Recommendations**：條件門檻（`decision_status`）、政策來源（`decision_policy_source`）與選用部位分析（FR-10／FR-11），含 `edge_status`
11. **命題監控儀表板**（表格七欄，`thesis_id` 可回溯，規格見方法論文件）
12. **Caveats 與來源追蹤**（用 `::: caveat` 框，含付費資料來源追蹤）

> 章節重編後所有交叉引用（模板內互指、本文件、`SKILL.md`）必須同步更新；公式與口徑一律引用 `equity-valuation-discipline/references/expectations-and-decisions.md`，不得另抄一份變體。

### B 型｜產業／供應鏈技術研究報告

0. 首頁 KPI 摘要卡
1. **TL;DR**（三點：產業結論＋最緊張環節＋最大變數）
2. **Key Findings**（約 5 點，附一手來源）
3. **產業定義與規模**：範圍界定、市場規模與 CAGR（列出估算機構與口徑差異，不同機構數字並陳、不擅自取單一值）
4. **技術路線與瓶頸**：主流方案 vs 挑戰者方案對照表；逐項標註「技術瓶頸｜卡在哪一關｜誰有解｜預計解決時點」
5. **供應鏈上下游地圖**：上游材料 → 中游元件 → 下游系統／客戶；每環節列出主要供應商（主供／二供／送樣中／出局）與集中度
6. **Content value 增減表**（世代交替題材必做）：新舊世代 dollar content 對照，標註 ↑↑／↑／持平／↓／design-out，**並加「市場反映度」欄**
7. **供需與產能**：新增需求 vs 在建產能、擴產週期、認證門檻、交期與報價趨勢
8. **產品銷售展望**：三情境（保守／基準／樂觀）出貨量與產值，列出每個情境成立的前提
9. **投資意涵與標的清單**：分「純度高／受惠但稀釋／被 design-out 風險」三類，每檔一句話理由＋現階段動作
10. **風險與反方論證**（`::: bear`）
11. **產業監控儀表板**
12. **Caveats**（`::: caveat`）
13. **付費資料來源追蹤**

### C 型｜輪動掃描／Channel Check 週報

0. 首頁 KPI 摘要卡
1. **本期結論**（三點：新增機會／論點變化／部位動作）
2. **本期驗證問題進度**（3–5 題，逐題寫「已驗證／待補／證偽」）
3. **Channel check log 摘要**（只列本期新增；不記可識別個資與機密數字）
4. **Product cycle 時間軸定位**：追蹤中的每個世代目前落在 T-18～T+6 哪一段，對應動作
5. **催化劑日曆（未來 90 天）**：事件｜日期｜預期方向｜對應加減碼訊號；已發生者移入下一節
6. **「2–3 個月後新聞標題」推演與驗收**：本期新寫標題（附主觀機率）＋上期標題的 Brier 記分
7. **部位動作與紀律檢查**：本期加減碼、失效條件、執行期限
8. **觀察名單異動**
9. **Caveats**

---

## 四、內容標註規範（三種報告共用）

### 4.1 資料層級標籤

關鍵數據後面接標籤，PDF 會渲染成彩色徽章：

```markdown
稼動率自 68% → 76% <span class="tag l1">公司揭露</span>
二供認證 Q4 完成 <span class="tag l2">分析師估算</span>
客戶追加訂單 <span class="tag l3">第二手</span>
```

- `l1` 公司揭露／一手權威來源（綠）— 可當基準假設
- `l2` 分析師／媒體估算（黃）— 情境參考
- `l3` 未具名／第二手轉述（紅）— **不得納入基準假設**，僅可記錄

### 4.2 查價日

所有市場數據（股價、市值、倍數、共識、同業 P/E、報價、short interest）**逐處標註查詢日與口徑**；同業倍數比較表**每列**標查價日。front matter 的 `price_asof` 是全報告的預設基準日，個別數據不同日者須另標。格式一律「數值＋日期＋盤別」三件套。

### 4.3 來源引用

- 行內寫法：`（2026-07-24 法說會簡報 p.12）`、`（2026Q2 10-Q, Note 7）`、`（重大訊息 2026-06-18）`。
- 有網址者在報告末尾「來源清單」列出；**不得引用一般投資人部落格**，若參考到須回溯改引原始一手來源。
- **一手取證失敗時須明寫**：超大檔案（>5MB）無法完整抓取而改用第二手整理時，須在該節以 `::: caveat` 寫明「已一手驗證者為 X、其餘為第二手」，第二手部分**不得納入基準假設**。
- **對標同業須具名**：凡以同業作為假設上限者，必須具名該同業（組）、列出實際數值與查詢日。寫「參考同業水準」而不具名，視同未查證。

### 4.4 提示框語法

```markdown
::: bull      多方論點／實據端（綠）
::: bear      空方論述／Pre-mortem／風險端（紅）
::: caveat    資料限制、估算揭露、方法論依賴（黃）
::: note      一般提示、規則說明（藍）
:::
```

框內第一行用 `**標題**：` 開頭。**同一框內含對立主題時，拆成 bull／bear 雙色區塊**（見 SKILL.md）。

### 4.5 表格與圖

- 表格一律用 GFM pipe table；**欄數超過 7 欄改拆兩張表**（PDF 版面上限）。估值三情境表常見 8–10 欄，須拆成「分母（營收×利潤率÷股數→EPS）」與「倍數與折現」兩張。
- 數字靠左寫即可，但同一欄單位一致，並在欄名寫單位（如 `EV（NT$ bn）`）。
- 需要圖時輸出 PNG／SVG 到報告同目錄，用 `![說明](檔名.png)` 引用；配色沿用 PDF 樣式的深藍／金／綠紅系。
- 強制分頁：插入 `::: page` `:::` 空區塊。

---

## 五、在地化

台股／美股的資料源、籌碼欄位、信用評等與三個真正的方法論差異，見 `market-localization.md`。**原則：方法一致，資料源在地化。** 不要為了美股另建一套骨架。

---

## 六、產檔流程

```bash
# 1) 依骨架寫好 報告.md（含 front matter）
# 2) 產 PDF（同名 .pdf 落在同目錄）
# $SKILL_DIR = research-report-output 這個 skill 的資料夾（見 SKILL.md 工作流程第 5 步）
python3 "$SKILL_DIR/scripts/md2pdf.py" 報告.md

# 3) 抽查排版（轉圖後目視檢查封面、表格跨頁、頁碼）
pdftoppm -png -r 80 報告.pdf pg && ls pg*
```

**環境依賴**：`pandoc`、`playwright`（chromium）、`pypdf`、`PyYAML`、字型 `Noto Sans/Serif CJK TC`。

```bash
pip install pypdf pyyaml playwright --break-system-packages
playwright install chromium
# pandoc：apt-get install -y pandoc（或 brew install pandoc）
# 字型（Debian/Ubuntu）：apt-get install -y fonts-noto-cjk
```

**依賴不全時的降級路徑**：

| 缺什麼 | 症狀 | 處理 |
|---|---|---|
| `pandoc` | 腳本直接報錯 | 必裝，無替代；裝不了則本 skill 的 PDF 鐵則暫時放寬為只交 md，並在訊息中說明 |
| `playwright`／chromium | HTML 產出但 PDF 失敗 | 先試 `playwright install chromium`；仍失敗可用 `--keep-html` 保留 HTML 交付，並註明 PDF 未產出 |
| CJK 字型 | PDF 中文變豆腐方塊 | 安裝 Noto CJK；容器內無 root 時改用 `fc-list` 找現有 CJK 字型並在 `report.css` 的 font-family 補上 |
| `pypdf` | 頁碼／合併步驟失敗 | `pip install pypdf --break-system-packages` |

**PDF 版面規格**（由 `assets/report.css` 定義，勿逐份微調）：A4、邊界 16mm、內文 10pt、表格 8.6pt、深藍 `#16324f` 主色；封面頁＋目錄頁不編頁碼，內文自第 1 頁起編、頁尾三欄（報告名｜頁碼｜免責標語）；表頭跨頁自動重複。改樣式的方法見 `customize-your-framework.md`。

---

## 七、交付與歸檔

1. **交付**：同時交付 `.md` 與 `.pdf`，附一句話結論（不要複述報告內容）。
2. **歸檔**：報告本體**不寫進知識庫**（避免被單一標的長文灌爆）；只有下列三種寫回：
   - 框架／規範／手冊等**方法論文件**的更新
   - 跨報告可複用的**產業地圖或觀察名單**
   - 覆盤結論（每檔 ≤3 行）
3. **監控儀表板**同步寫入觀察名單設定檔；名單異動時須在同一次作業內同步排程任務設定。

---

## 八、發布前檢查清單（格式層）

每份報告必跑。內容層檢查清單見 `equity-valuation-discipline` 的 `references/prepublish-checklist.md`。

1. `.md` 與 `.pdf` 皆已產出，PDF 由該 md 直接生成，未手改。
2. front matter 必填欄位齊全（含 `market`、`framework` 版本、`methodology_version`、`research_question`、`as_of`）；KPI 卡 3–5 張且與內文數字一致、未知項未填零；價格均有幣別前綴與「數值＋日期＋盤別」三件套。
2.1 `rating` 與 `decision_status` 一致（見第二章 2.2）；提出 edge 結論者 `edge_status` 已填且不高於 `hypothesis_only`，除非補齊對應證據。
3. 檔名符合第一章規則；版本語意正確（結論改變＝主版號進位）；輸出模式後綴正確。
4. 抽查 PDF：封面資訊正確、目錄無斷字、寬表未溢出版面（**欄數 >7 已拆表**）、頁碼正常、提示框顏色語意正確。
5. 資料層級標籤與查價日已標；`l3` 資訊未被用作基準假設；一手取證失敗處已依 4.3 明寫。
6. **F-rules 六項自查（F-a 至 F-f）已逐條通過**（`formatting-rules.md`）。
7. 資料源、籌碼欄位、信用評等欄位已依 `market` 換成對應版本，無台美混用。
8. **刪節後處理**（External／Briefing）：章次已重編、子節已重編、交叉引用已同步。

---

## 版本紀錄

| 版本 | 變更 |
|---|---|
| v2.0（發布版） | 從個人 project 規範泛化為可發布版本：抽離內容層檢查清單至 `equity-valuation-discipline`；F1–F5 完整版移入 `formatting-rules.md`；台美對照移入 `market-localization.md`；新增依賴降級路徑；新增輸出模式後綴與刪節後處理；front matter 加入 `footer_right`。 |
