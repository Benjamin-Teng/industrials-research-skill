# Changelog

## v1.4.0 — 2026-09-13

修正一個**指引層與引擎層互相矛盾**的缺陷：發布前檢查清單與 A 模板都寫著「fade 流量全程為
FCF 利潤率」，而 `fade_enterprise_value()` 的參數是 `nopat_margin_path`、內部算的是
`FCFF = NOPAT − k·ΔRevenue`。照清單走的人會把 FCF 利潤率餵進 NOPAT 的位置，
**等於把資本支出扣兩次**。引擎本身沒問題（`fcff_simplified` 的 docstring 早已禁止重複扣減），
出事的是規範文字。

**這是前瞻性修正，不是在指控既有報告出錯。** 舊框架（v2.0／路徑 2.7）本來就把 `m_term`
定義成 FCF 利潤率，並以恆等式 `FCF 率 = NOPAT 率 − k·g` 貫串，**在它自己的體系內是一致的**；
出事的是遷移到 `expectations-v1` 之後，引擎改吃 NOPAT 利潤率，而檢查清單與模板的文字沒跟著改。

**換算幅度取決於 `k`，差異可能很小**（實測：台光電 2383 `k`＝0.17 → 0.41pp；
奇鋐 3017 `k`＝0.115 → 0.28pp），**但對高資本強度標的不可忽略**
（台積電 2330 `k`＝0.97 → 2.37pp，`m_term` 18.11% → 20.48%，基準每股 1,656 → 1,820，＋9.9%）。

### 變更

- **`prepublish-checklist.md` 第 9 項「口徑一致性」**：`m1` 至 `m_term` 的口徑由
  「自由現金流利潤率」更正為 **NOPAT 利潤率**（即 `nopat_margin_path`），
  並新增一條「同業對標的口徑已換算」檢查。
- **A 模板 6.3「口徑聲明」**：同上更正；並明寫 FCF 利潤率是**衍生量**，
  ⛔ 不得反過來當 fade 的輸入。
- **A 模板 6.3 第 3 點（終端利潤率）**：新增換算步驟——同業組表格給的是 FCF 利潤率，
  `m_term` 要的是 NOPAT 利潤率，須先反推再對標。
- **換算須用同業自己的 `k` 與 `g`**，不是本標的的；同業的 FCF 利潤率是在它自己的
  成長與資本強度下實現的。
- **換算後的數字是對標基準，不是上限**。同業組與本標的不可比時（例如無一家在同一技術世代
  競爭），改用自設區間並在 TL;DR 揭露，⛔ 不得因為「換算過了」就把不可比母體當成合格上限。

### 修正

- **fade 形狀公式由近似式改為精確式**：`FCF 利潤率 = NOPAT 率 − k·g/(1+g)`
  （舊版為 `− k·g`）。再投資的分母是**前一年**營收，以 `k`＝0.97 實算：`g`＝2.5% 時兩式差
  6bps 可忽略，`g`＝25% 時差 **485bps**——高成長段用近似式會系統性低估 FCF 利潤率。
  恆等式的單一來源定在 `valuation-paths.md` 4.2；A 模板 6.3 口徑聲明與 4.7 路徑①的
  `k` 共識校準式（原為 `÷ g`，改為 `× (1+g) ÷ g`）已同步改為精確式。

### 已知限制

- **本次缺陷 `pytest` 抓不到**：既有測試守護的是 `valuation_math.py` 的數值行為，
  而錯的是 Markdown 規範文字。**引擎正確 ≠ 照規範寫出來的報告正確。**
  未來若要自動守護，需要一層「規範用詞 vs 函式簽名」的一致性測試。

### 驗收

`pytest` 143 passed, 44 subtests passed（本版未動程式碼，數字承接 v1.3.2）；
markdownlint 0 issues；`claude plugin validate` 通過。

## v1.3.2 — 2026-09-13

修正 v1.3.1 反解器的兩個缺陷（第四輪 Codex adversarial review 指出，經實測重現）。
方法論方向不變；新增一條鐵則：**殘差小不等於參數被識別出來**。

### 變更

- **SKILL.md 反解鐵則新增第 5 條**：估值模型在最適值附近常常平坦，殘差天生就小、
  自變數卻還沒收斂；反解值的位數不得超過模型實際能識別的精度。
  `expectations-and-decisions.md` 第 3.3 節與發布前檢查清單第 4 項同步補上
  「假精確」與「非有效評估」兩條。
- `ParameterSolveResult` 新增 `non_finite_evaluations` 欄位；`unconverged` 狀態的語意擴大為
  「未收斂、不連續、或搜尋區域根本沒被有效評估」。

### 修正

- **黃金分割搜尋耗盡 `max_iter` 仍接受候選**：偶重根分支舊版只驗殘差、不驗區間是否收斂。
  平坦函式的殘差本來就小，未收斂的中點因此被當成 `single_candidate`
  （重現：`0.001*(x−0.42)**2`、`max_iter=1`、`tol=1e-12` 回報 0.4182，誤差 0.0018 卻宣稱 16 位精度）。
  現在候選必須**同時**通過「區間已收斂」與「殘差達標」，否則計入 `unresolved_intervals`。
- **`f` 回傳 NaN／inf 被靜默當成「沒找到」**：NaN 與任何數字比較恆為 `False`，
  舊版取樣值未檢查有限性，「那段範圍算不出來」與「正常搜尋後確實無解」外觀完全相同
  （重現：`lambda x: nan` 回報 `no_candidate_in_range`；後半段 NaN 的函式照樣回報 `single_candidate`）。
  現在所有求值經單一入口計數，任一相鄰取樣點對有一端非有限即計入 `unresolved_intervals`，
  狀態落到 `unconverged`；已驗證的根仍保留在 `candidates`。
- **取樣端點有限、但二分法／黃金分割迭代內部才碰到 NaN**（第五輪 Codex review 補抓）：
  NaN 的符號比較恆為 `False`，舊版會靜默走 `else` 分支繼續縮區間，把無根函式回報成
  `single_candidate`（重現：`x<0.4 → −1e−7`、`0.4≤x≤0.6 → NaN`、`x>0.6 → 1`，`samples=2`）。
  現在 `_bisect_root` 與 `_minimize_abs_f` 迭代中任一求值非有限即回傳 `converged=False`，
  呼叫端計入 `unresolved_intervals`。

### 驗收

`ruff` / `ty` 全 repo 0 error；`pytest` 143 passed（v1.3.1 為 134，新增 9 個重現測試）。

## v1.3.1 — 2026-09-11

修正 v1.3.0 反解器的兩個缺陷（Codex adversarial review 指出，經實測重現）。
方法論方向不變，但**反解狀態的名稱與語意有變**，讀 `expectations-and-decisions.md` 第 3.3 節。

### 變更

- **反解狀態改名，讓名稱只宣稱證據支持的東西**。反解器是在搜尋範圍內等距取樣、偵測變號，
  這個方法證明不了「唯一」或「無解」：

  | 舊 | 新 |
  |---|---|
  | `unique` | `single_candidate` |
  | `multiple_roots` | `multiple_candidates` |
  | `no_solution_in_range` | `no_candidate_in_range` |

  **找到一個候選不等於解是唯一的。** 要在報告裡主張唯一，必須另外論證該搜尋範圍內的
  連續性與嚴格單調性，並把論證寫出來。舊名稱會讓報告寫出「現價隱含成長率唯一為 X%」，
  而實際上還有別的解——這違反第 3.2 節「一個價格不得同時被宣稱唯一識別多個未知參數」。
- **必揭露事項從五件增為六件**，新增**取樣密度**：網格多細直接決定哪些解看得見。
  對應新增 `samples_used` 欄位。SKILL、發布前檢查清單、A 模板與範例已同步。

### 修正

- **偶重根（切線根）看不見** —— `f` 碰到零但不變號時（例如 `(x−a)²`），舊版回報
  「範圍內無解」；`(x−0.42)²(x−0.75)` 則只找到 0.75 並宣稱唯一。
  現以「掃 `|f|` 的局部極小 ＋ 黃金分割局部搜尋」補上偵測，三個重現案例的漏根都已找回。
  **已知限制**（docstring 明載）：局部搜尋假設 `|f|` 在單一取樣格內大致單峰，
  兩個極接近的根仍可能只找到一個——此時狀態為 `single_candidate`，而它本來就不宣稱唯一。
- **NaN 與 inf 無聲穿過所有公開函式** —— NaN 與任何數字比較都是 `False`，
  `<= 0` 這類檢查攔不住，`equity_bridge(debt=NaN)` 會直接回傳 `(nan, nan)`。
  若資料源以 NaN 表示缺漏，缺資料不會觸發失敗處理，會污染估值與報告。
  現在 19 個公開函式的**輸入與回傳值**都經 `math.isfinite` 驗證，非有限值一律
  `ValueError` 並指出是哪個參數（回傳值檢查同時擋住溢位成 inf 的情形）。

### 驗收

`ruff` / `ty` 全 repo 0 error；`pytest` 134 passed（v1.3.0 為 110）；
markdownlint 0 issues；`claude plugin validate` 通過。

## v1.3.0 — 2026-09-10

**方法論改版（破壞性）**：估值架構從「三情境估值期望值 × 安全邊際 → 評等」的單一折現決策鏈，改為
**`expectations-v1`：價格隱含預期 → 可驗證預期差 → 情境估值與持有期報酬 → 催化劑與風險 → 決策覆盤**。
DCF 保留為按需工具；**單一折現估值與固定安全邊際不再自動決定評等**。

舊報告不受影響也不會被覆寫；方法論改版不等於每份報告的結論必然改變。
逐條退役紀錄與舊／新對照見 `skills/equity-valuation-discipline/references/calibration-and-governance.md`。

### 新增

- **`references/expectations-and-decisions.md`**：方法論的**公式與口徑單一來源**。定義研究契約、三種預期基線、
  價格隱含預期的識別性與反解失敗行為、預期差台帳、`V0`／`P_H`／`R_H` 三種輸出的嚴格區分、價格反映機制、
  Reward/Risk、示範機率與逐組解讀、損益兩平、風險映射、決策門檻、部位輸入門檻、`edge_status`。
- **`scripts/valuation_math.py` 與 `tests/test_valuation_math.py`**：上述公式的可測試實作（74 項測試）。
  含 fade 引擎、股權橋接、折現率配對、成長序列、再投資、終值、R/R、期望值、損益兩平與 Reverse round-trip。
- **A 型報告新增第九章「催化劑與驗證時間表」**：舊版 `output-spec.md` 宣稱有這一章、A 模板卻沒有，本次補齊並對齊。
- **Front matter 新增**：`methodology_version`、`research_question`、`as_of`、`strategy_type`、
  `holding_horizon_months`、`forecast_horizon_years`、`valuation_methods`、`expectations_status`、
  `decision_status`、`decision_policy_source`、`edge_status`。`rating` 須與 `decision_status` 一致。
- **`thesis_id` 串接**：預期差台帳、情境、催化劑、監控儀表板與輪動交接共用同一組命題 ID。

### 變更

- **模型路由**：`A/B/C` 互斥三分類改為六個方法 ID（`fcff_dcf`／`cycle_normalized`／`sotp`／
  `financial_equity`／`asset_nav`／`growth_scenario`），依公司經濟特性與資料條件路由。
  **混合型公司必須拆解**結構成長與循環因素，不得把外部 capex 循環全塞進利潤率。
- **COR-01 折現率配對**：`rf + β × ERP` 更正為**股權成本 `k_e`**（舊版誤標為 WACC）。
  FCFF 配 WACC 得營運企業價值；FCFE／股利／剩餘利益配 `k_e` 得股權價值。
- **COR-02 倍數命名**：FCFF 折現衍生的是 **EV/NOPAT**（舊稱 P/NOPAT），且**須完成股權橋接才得每股價值**。
  `(1 − g/ROIC)(1+g)/(WACC−g)` 不再稱 justified P/E。企業價值一律寫 `EV_enterprise`，
  機率加權股權價值寫 `expected_equity_value`／`E[V0]`，**`EV` 不再作為簡稱**。
- **COR-03 fade 與再投資**：成長序列第一年恆等於指定的 `g1`（舊版 `i/N` 寫法第一筆即偏離，
  `g1=20%` 實際給出 16.6%）；再投資改為 `k × (Revenue_t − Revenue_{t−1})`，不再以成長率當分母；
  展示倍數的分母改為**同時點 NOPAT**；`RONIC < WACC` 時不再自動取零成長，改回傳標記由報告明示情境。
- **風險處理**：從「財務品質警示只能調機率」改為**後果進情境、機率進權重**，兩者各記一次即為完整。
- **決策**：改為條件門檻（`decision_status` 四態）。使用者未提供風險政策時只輸出條件式結論。
- **檢查清單**：12 項無條件硬門檻改為 **27 項適用性檢查**，每項含「適用情境／不適用時／檢查內容」。
- **`product-cycle-rotation`**：週期階段**不再自動導出建倉**；市場反映度改為行情代理與價格隱含預期**分欄**；
  催化劑須登記六要素、過期分「被證偽／延後／結果未取得」三類；B 級 channel check 不自動升格為財務基準事實。
- **`.markdownlint-cli2.jsonc`**：承認既有的 PDF 樣式慣例（`<span class="tag">`／`<br>`）與模板填空佔位符，
  並修正全 repo 既有的 lint 錯誤——`main` 原有 55 個 error，本版起為 **0**。

### 移除

- **舊決策鏈**：`現價 ≤ E[V0] × (1 − 安全邊際)` → 評等；90 日波動率綁定 20／30／40% 安全邊際分級。
- **營收錨 L0–L3 階序**與其自動折讓（0／5／10／20／30%）與信用調整降級。
- **控股折價自動 0–15%**；「未套折價只能當理論上限」。
- **部位預設處方**：`min(波動率倒數配置, 1/4 Kelly)`；執行期限「逾期自動執行一半」。
- **「差距 >5pp 者終端一律採結構性口徑」**、**「出場年營業利益率一律不得做敏感度」**。
- **「未併表 JV 存在即禁用 SOTP」**、**「出場倍數一律由 fade 推導」**。
- **術語「紀律值」**（機率加權期望值）：與「框架預設值」一詞兩義，易與 `V0`／`P_H` 混用，全面改寫。

## v1.2.1 — 2026-09-08

### 變更

- **`research-report-output` 的 Briefing 模式新增觸發詞「簡介」**，並寫進 skill `description`，讓「幫我寫 XX 的簡介」也能載入 skill 並走 3 頁摘要版。

## v1.2.0 — 2026-09-07

安裝模式改為與 [xs_helper](https://github.com/Benjamin-Teng/xs_helper) 相同的雙平台原生封裝：Claude Code 與 Codex 都用 marketplace 一鍵安裝，不再教使用者手動 clone + symlink。

### 新增

- **`.codex-plugin/plugin.json`**：Codex 原生 plugin manifest（含 `interface` 展示區塊），`skills` 指向與 Claude 共用的 `./skills/`。
- **根目錄 `.agents/plugins/marketplace.json`**：Codex marketplace `research-tools`，以 `local` 來源指向 `./plugins/research-report-kit`，與 Claude 的 marketplace 同名。
- **每個 skill 的 `agents/openai.yaml`**：Codex 顯示名稱、簡述、預設提示，並允許隱式觸發。
- **`tests/test_plugin_compatibility.py`**：守住雙 manifest 同名同版、Codex marketplace 路徑真實存在、四個 openai.yaml 齊全、README 覆蓋三條安裝路徑。

### 變更

- **README 安裝章節**改為三入口矩陣：Claude Code 三行指令；Codex IDE 用 `$skill-installer` 從 GitHub 路徑裝獨立 skill；Codex CLI 用 `/plugins` 對話安裝或 `codex plugin add`。
- **`.claude-plugin/marketplace.json` 補 `version` 欄位**（部分安裝器從 marketplace 條目讀版本）。

### 移除

- **根目錄 `manifest.json`**：Codex 只讀 `.codex-plugin/plugin.json`，該檔不屬於任何一方的規格。
- **README 的 symlink 安裝教學與 Windows 開發人員模式警告**。

## v1.1.0 — 2026-09-05

跨平台可攜性。四個 skill 現在同時符合 Claude plugin 與 Agent Skills 開放標準（OpenAI Codex 採用同一份規格），`SKILL.md` 無平台專屬綁定。

### 變更

- **移除 `${CLAUDE_PLUGIN_ROOT}`**：產檔器改用相對於 skill 目錄的路徑 `scripts/md2pdf.py`，符合 Agent Skills 的檔案引用慣例，兩個平台都解析得到。
- **交付方式改為平台中立**：鐵則不再寫死 `SendUserFile`，改為「兩檔都要交付給使用者」，並註明各平台做法。
- **同層 skill 的引用去掉斜線前綴**：`/price-routing` → `price-routing`（Claude 用 `/name`、Codex 用 `$name`，裸名兩邊都不會誤解）。
- **`research-report-output` 新增 `compatibility` frontmatter**：宣告 PDF 產檔的系統依賴，讓沒有 pandoc／chromium 的環境事先知道會降級為只交 `.md`。
- **新增 repo 根目錄 `manifest.json`**（OpenAI plugin 格式），與 `.claude-plugin/plugin.json` 並存。
- **README 增補 Codex 安裝章節**：clone + symlink 進 `.agents/skills`、掃描優先序、更新方式、Windows symlink 注意事項，以及 ChatGPT 網頁版的方案門檻與沙箱限制。

## v1.0.0 — 2026-09-04

首次發布。從個人研究 project 的 skill 與框架文件泛化而成，拆為四個可分開使用的 skill。

### 新增

- **`research-report-output`**：md + PDF 雙檔輸出規範、三型報告骨架模板、F1–F5 排版鐵則、三種輸出模式（Internal／External／Briefing）與刪節後處理三步、機構風 PDF 產檔器與樣式表。
- **`equity-valuation-discipline`**：兩層估值路徑判別、三條路徑完整方法（SOTP／週期股常態化／成長股成長連動 fade）、情境機率與期望值制、敏感度排序失效三情形、12 項發布前內容檢查清單、常數校準與規則治理機制。
- **`product-cycle-rotation`**：product cycle 五問（含市場反映度與研究優先序公式）、T-18～T+6 時間軸與股價反應模型、channel check 六步 SOP 與證據分級、短線催化劑框架、輪動倉波動率配置與出場三條件。
- **`price-routing`**：執行時偵測可用行情工具，依市場路由，無 MCP 時退回 yfinance。

### 相對於原始個人版本的主要調整

- **分層**：格式層（通用）與內容層（可替換）分離；SKILL.md 明訂「使用者自有方法論優先」，並附 `customize-your-framework.md` 說明三種接法。
- **去個人化**：移除持倉權重、觀察名單設定、特定標的實戰紀錄與個人框架模組代號（★A1–A7／◇B1–B4）；保留規則本身與其實證來源。
- **不假設環境**：`price-routing` 改為執行時偵測而非硬編工具名；PDF 產檔補上依賴缺件時的降級路徑。
- **母體聲明**：所有數字門檻標明出身（實證來源或經驗值），並列出待校準清單與校準路徑。
- **F1–F5** 從主 SKILL.md 移入 `references/formatting-rules.md`，主檔改為摘要表 ＋ 六項自查，維持 progressive disclosure。
