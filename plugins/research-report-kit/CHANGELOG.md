# Changelog

## v1.7.0 — 2026-11-07

新增**產品技術拆解**：第六個 skill `product-technology-walkthrough`，替投資人拆解一家公司主力產品的技術細節，
跟著產品的最小單位（一片晶圓、一個網路請求）從頭走到尾，說明產品線怎麼跑、供應鏈怎麼撐。**不評價股價**，
不分析商業模式與財務（屬 Layer 1）。

起因是 Layer 1 方法檔把技術的機理、材料與製程標為「技術報告（另案）」，一直沒有承接的 skill。這一版由台積電 N2
與 Cloudflare（NET）兩個產品技術研究實作出來，主要成品是手機上閱讀的互動頁，md 與 PDF 由互動頁衍生。

### 新增

- **`product-technology-walkthrough` skill 與方法檔 `product-technology-v1`**：`SKILL.md` 管觸發、分工、流程摘要、
  資料取得、Codex 交接點與交付前檢查；`agents/openai.yaml` 為 Codex 介面。
  `references/product-technology-method.md` 是第三份方法論單一來源，涵蓋範圍、主線與兩條線、來源效力、
  整合、生成、示意圖審查、限制與治理。
- **互動頁骨架 `assets/walkthrough-skeleton.html`**：資料常數、`TAG`、`META`、`STEPS`、場景與對外介面
  `window.walkthrough` 的格式見方法檔 5.1。
- **`scripts/build_walkthrough_md.py`**：互動頁逐拍轉 md 與截圖。重產採暫存區，失敗時不會動到原成品；
  發布中斷或還原失敗時保留舊圖備份；必填欄位或 `META` 欄位缺值時直接停止，不產出 md；CLI 支援相對路徑。
  截圖目錄依報告檔名分開（`pdf-img/<md 檔名去副檔名>/`），新舊版 md 可並存；來源缺 label 或 url、
  key 不在 `SRC`、url 不是 http(s) 時擋下；廠商區的說明段落（含 `META.supCaveat`）照頁面原文放進 md。
- **`scripts/schematic_topology.py`**：示意圖連接關係檢查，逐拍傾印 `data-net`、`data-kind` 標註的矩形，
  檢查懸空端點、短路、過近與孤立通孔，輸出連接表。exit code：0 沒有問題且至少一拍有標註元件、
  1 任一拍有問題、2 受檢的拍都沒有標註元件（不算通過）、3 用法或頁面錯誤（含 Playwright 例外）。
- **`research-report-output` 新增 E 型「產品技術研究」**：`type: 產品技術研究`、`methodology_version: product-technology-v1`，
  front matter 由互動頁的 `META` 產生；沒有價格與市場數據，以查證日與來源分級取代查價日。
  E 型暫不支援 Briefing（md 一律由互動頁重產，產檔器沒有摘要模式）；External 模式是先改互動頁再重產。
  `SKILL.md`、`output-spec.md`（檔名規則、front matter、E 型骨架說明、格式層檢查清單）同步。
- **首例 `examples/tsmc-n2-walkthrough/`**（repo 根目錄，不進 plugin 打包範圍，不含第三方圖片）：N2 互動頁、md、
  各幕證據檔、廠商名單、逐幕審查紀錄（r1 至 r6）與 `CONFORMANCE.md`（對照方法檔 5.1 的改動紀錄）。
- **新測試**：`tests/test_product_technology_skill.py`、`tests/test_walkthrough_skeleton.py`、
  `tests/test_build_walkthrough_md.py`、`tests/test_schematic_topology.py`，以及共用的 `tests/browser_helpers.py`
  （缺瀏覽器時預設 skip，設 `REQUIRE_BROWSER=1` 改為 fail）；`tests/test_plugin_compatibility.py` 的 skill 清單加入第六個。
- 根 README、plugin README：skill 數量、觸發詞、Codex 安裝指令與目錄結構樹同步；`AGENTS.md` 改為三份方法論單一來源，
  規則增修加上第三條分流。

### 變更

- **Layer 1 方法檔**（`business-industry-method.md`）：1.3 表格「技術報告（另案）」一列改指向
  `product-technology-walkthrough`，「以技術主題為主體的研究」一列改指向 B 型；1.4 節補一句技術報告由新 skill 承擔。
- **`research-report-output`**：報告類型由四型改為五型；內容標準分工加入 E 型。

### 方法論規則與來源（使用者決定，2026-11-07）

- 維基百科列入方法檔 3.3 的清單：只當線索，引用時引條目所引的原始文件。
- 專利的先前技術段可以當第 4 級間接來源；實施例與請求項只寫成「該公司申請過這種做法的專利」（方法檔 3.2）。
  審查結果裁決後，使用者未提異議。

### 不變

- 估值方法論與 Layer 1 方法論的規則不變，只更動指向技術報告的兩處文字（見「變更」）。
- Codex `defaultPrompt` 維持三筆。

### 治理附件（產品技術拆解）

依方法檔第八章與 `AGENTS.md`「方法論規則的增修」，三項齊備。

1. **證據**：兩個公開首例，不是盲測的樣本外資料，案例名稱直接列出。
   - 台積電 N2：對照方法檔的全面審查 r1 至 r6，審查紀錄與逐項對照收在 `examples/tsmc-n2-walkthrough/research/` 與 `CONFORMANCE.md`。
   - Cloudflare（NET）：依方法檔從零實作，六份證據檔、三段頁面審查，並由使用者在 iPhone 實機確認版面。
2. **回溯影響**：`business-industry-method.md` 1.4 節與 1.3 表格兩列改為指向新 skill；其他既有 skill 不受影響。
3. **半年檢驗條件（2027-05 前）**：
   - 再用於一家不同產業的公司，確認方法檔不只適用半導體製程與網路服務。
   - 發布後使用者仍抓到示意圖連接錯誤，就檢討方法檔第六章。

## v1.6.1 — 2026-11-01

修正版：PDF 產檔器的相對路徑圖片恢復正常，報告可以嵌入圖片。

### 修正

- **`md2pdf.py` 以相對路徑引用的圖片不再變破圖**：中間 HTML 原本寫在系統暫存目錄，瀏覽器以那裡為基準解析
  `![說明](fig.png)`，PDF 只嵌入破圖圖示且不報錯；`output-spec.md` 4.5 要求的「圖輸出到報告同目錄、
  用相對路徑引用」因此無法運作。現在中間 HTML 寫在報告同目錄（隱藏檔名，產檔後刪除），並以正確編碼的
  檔案 URI 載入，報告路徑含空白或中文也能用。`tests/test_md2pdf.py` 新增端到端測試，以 PDF 內嵌圖片的
  像素尺寸驗證（環境沒有 pandoc 或 playwright 時 skip）。

## v1.6.0 — 2026-11-01

新增**企業與產業分析（Layer 1）**：第五個 skill `business-industry-analysis`，回答「這家公司靠什麼賺錢、
產業利潤由誰掌握」，**不評價股價**，不給估值、目標價、報酬風險比與買賣判斷（完整範圍見 `business-industry-method.md` 第四章）。

起因是研究架構需要一層先於估值的業務理解：沒有提估值的單一個股請求，過去直接走 A 型個股深度研究，
被迫在業務還沒釐清時就進入估值。Layer 1 把業務與產業結構獨立出來，結論以「最關鍵的業務變數與待驗證問題」
交接給估值層。

### 新增

- **`business-industry-analysis` skill**：`SKILL.md` 管觸發、與其他 skill 的分工、流程摘要、資料取得與
  交付前的內容層檢查；`agents/openai.yaml` 為 Codex 介面。不依賴估值 skill 的任何檔案也能完整運作。
  Windows 取得 SEC 文件的樣板：PowerShell 7 的 `Invoke-WebRequest` 需加 `-SkipHeaderValidation`，
  否則 header 驗證失敗時會回顯聯絡信箱；Windows PowerShell 5.1 沒有此參數，樣板會停止並指向 bash 路徑。
- **`references/business-industry-method.md`（`business-industry-v1`，Layer 1 方法論單一來源）**：
  範圍、八個步驟（研究契約與資料時點、營收來源重建與商業模式類型、單位經濟量尺、逐營收來源 SWOT、
  縱向產業鏈與利潤池、橫向同業與替代方案、產業結構與護城河、業務交接）、商業模式類型對量尺的路由表、
  不評價股價的紅線、資料標示與紀律、治理、引用文獻。
- **D 骨架 `templates/D-business-industry.md`**：`type: 企業與產業研究`，檔名
  `{公司名＋代號}_企業與產業研究_{版本}_{YYYYMMDD}.md／.pdf`。
- **路由規則**：沒有要求估值、目標價、報酬風險比或買賣判斷的單一個股研究請求，內容層走
  `business-industry-analysis`、格式層走 D 骨架；要求估值或買賣判斷時仍走 A 型。
  `research-report-output` 的 SKILL.md 與 `output-spec.md` 同步 D 型規則，`market-localization.md` 補上 SEC 下載的指引；
  同一標的已有 D 型報告時，A 模板第四章直接引用；B、C 模板與 `product-cycle-rotation` 中指估值驗證的「深度研究」
  改為明指 A 型。
- **`SEC_USER_AGENT` 設定說明**：`customize-your-framework.md` 第六節說明 SEC 文件全文下載所需的環境變數
  與設定方式；plugin README 的「資料源」一節同步。
- **新測試**：`tests/test_business_industry_skill.py`（方法論檔、SKILL.md、D 骨架、路由文字的結構測試）；
  `tests/test_report_schema.py` 的 front matter 檢查依 `methodology_version` 分流，並加入 D 型守門；
  `tests/test_plugin_compatibility.py` 的 skill 清單加入第五個。
- 根 README 與 plugin README：skill 數量、觸發詞、`怎麼用` 範例、目錄結構樹與資料源說明同步。
- `AGENTS.md`：方法論改為兩份單一來源（估值、Layer 1），規則增修依方法論分流。
- **`scripts/fa_check.py`（F-a 數字密集檢查）**：只用標準函式庫，標出含 3 個以上數字、需要拆表或分行的段落與表格儲存格；
  `research-report-output` 的工作流程要求產 PDF 前跑到 `0 hit(s)`。測試在 `tests/test_fa_check.py`。
- **中文用語校對（選用）**：環境裡有 [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) 時，產 PDF 前用它校對正文的台灣用語與標點；
  表格、數字、標籤與版面仍以 F-rules 為準。沒有安裝時略過。
- **D 骨架對齊 F-rules 與數字出處**：TL;DR 改為一句結論加實績表；10.1、10.2 補結論句；SWOT 數字欄一行一個數字；
  關係人拆分與營運資金改為表格；證據標示與 KPI 卡要寫出文件名與期間。交付前檢查補格式、資料層級與台股來源三項。

### 修正

- `md2pdf.py` 的目錄標題不再雙重轉義 HTML 實體（例如 `O&M` 印成 `O&amp;M`）。

### 不變

- 估值方法論與估值 skill 的 description 不變。
- Codex `defaultPrompt` 的三筆文字不變；第 1 筆（台積電個股深度研究報告）在新路由下改走 D 型，正好當作示範。
- 估值 skill `calibration-and-governance.md` 4.2 的升版節奏不適用於 Layer 1（維護者決定）。本版不修訂估值方法論的任何規則；Layer 1 另訂每季至多一代方法論（`business-industry-method.md` 6.5）。
- `expectations-and-decisions.md` 第 4 行只把「三份報告模板」改成「A／B／C 三份報告模板」。這是範圍字樣，
  不是規則變更（維護者同意）。

### 治理附件（Layer 1）

比照 v1.5.0 的「治理 4.1 附件」，三項齊備。

1. **案例與來源**：
   - **規則判定表**：2026-10-24 判定，門檻為「至少兩個獨立案例出現同一失效模式，或一個理論／實證來源；
     兩者都沒有的單一案例進觀察區」。維護者決定的框架（逐營收來源 SWOT、六塊、不評價股價的紅線、交接只談業務、
     樣本外驗收）本身的定義與必要結構，判為「設計要求」，不受證據門檻管。共 43 條編號規則（R1.1–R8.3 共 38 條，加
     RD.1–RD.5）；R5.7 與 R8.4 改寫為 `business-industry-method.md` 第一章「定位與範圍」的範圍說明，不編號。案例取自開發組九家的研究紀錄（保存在維護者本機）。
     「部分核實」的文獻只在已核實部分涵蓋規則主張時才算。

   | 編號 | 規則 | 案例 | 文獻 | 判定 |
   |---|---|---|---|---|
   | R1.1 | 研究契約三要素 | — | — | 規則（沿用 repo 規則） |
   | R1.2 | 資料疊加順序與完整會計期間 | BE、高明鐵、富喬、台積電、CRWD、MCD | — | 規則（案例） |
   | R1.3 | 體制轉換旗標 | BE、高明鐵、台積電、富喬 | — | 規則（案例） |
   | R2.1 | 依定價與認列機制劃分來源 | BE、MCD、台積電、富喬、高明鐵、CRWD、ARM、晶心科、BRK | — | 規則（案例） |
   | R2.2 | 一或多個類型並記轉換跡象 | BE、MCD、BRK、ARM、高明鐵 | — | 規則（案例） |
   | R2.3 | 依利潤加權排序與篇幅 | MCD、BRK | — | 規則（案例） |
   | R2.4 | 比重標證據等級、未揭露時 SWOT 只做質性 | 高明鐵、BE、CRWD、富喬、BRK、ARM、晶心科 | — | 規則（案例） |
   | R2.5 | 關係人拆分與剔除後成長 | ARM、BE | — | 規則（案例） |
   | R3.1 | 類型→量尺路由表 | MCD、BRK、ARM、晶心科、台積電、CRWD、BE、高明鐵 | — | 規則（案例） |
   | R3.2 | 路由表只收開發組類型 | — | — | 規則（設計要求） |
   | R3.3 | 表外類型通用程序 | — | — | 規則（設計要求） |
   | R3.4 | 不適用量尺寫進表 | IP 毛利率：ARM、晶心科；混合單位：高明鐵、台積電 | — | 規則（案例） |
   | R3.5 | 自定義 KPI 引原文並以 GAAP 錨點核對 | BE、CRWD | — | 規則（案例） |
   | R3.6 | 營運資金機制（應收、存貨、收付款條件、現金流對照） | 高明鐵、樣本外案例（匿名） | — | 規則（案例） |
   | R4.1 | 議題四欄 | MCD、台積電（BE 次之） | — | 規則（案例） |
   | R4.3 | 內外部分界與法規拆入外部 | — | — | 規則（設計要求） |
   | R4.4 | S／W 相對具名對手、比較基準未查 | 富喬、晶心科、CRWD | — | 規則（案例） |
   | R4.5 | O／T 觸發條件與時間窗、循環與結構 | 台積電、CRWD、BRK、ARM、晶心科、BE、富喬；時間窗終點與狀態：MCD、樣本外案例（匿名） | — | 規則（案例） |
   | R4.6 | 互綁來源改矩陣 | ARM、晶心科、台積電、BE | — | 規則（案例） |
   | R4.8 | TOWS 為選用；寫的話只寫條件式含義 | — | — | 規則（設計要求） |
   | R5.1 | 實體×角色矩陣 | CRWD、台積電、ARM、晶心科、BRK | — | 規則（案例） |
   | R5.2 | 下游兩層 | BE、MCD、CRWD、富喬 | — | 規則（案例） |
   | R5.3 | 上游範圍（平台主、人才與工具、燃料、資本財） | CRWD、BE、ARM、晶心科 | — | 規則（案例） |
   | R5.4 | 分潤層 | MCD、BRK | — | 規則（案例） |
   | R5.6 | 利潤池四步＋跨期＋降級 | 允許降級成質化：CRWD、ARM、晶心科；跨期：富喬、高明鐵 | Gadiesh & Gilbert（1998，已核實）；Porter（2008）完整循環（已核實部分） | 規則（文獻） |
   | R5.8 | 交易對手申報反查 | MCD、台積電 | — | 規則（案例） |
   | R6.1 | 同業依來源或類型分組、標分析者建構 | 高明鐵、CRWD、富喬、BE、台積電、ARM、晶心科、BRK | Porter（2008，已核實） | 規則（案例） |
   | R6.2 | 定義差異與不可比欄、期間與單位對齊 | CRWD、MCD、台積電、ARM／晶心科、高明鐵 | — | 規則（案例） |
   | R6.3 | 替代方案五層 | BRK、BE、台積電（另有高明鐵、ARM、晶心科、CRWD、富喬觸發個別層） | — | 規則（案例） |
   | R7.1 | 先定產業邊界再談集中度與五力 | MCD、富喬、台積電、ARM、晶心科、高明鐵 | Porter（2008，已核實） | 規則（案例） |
   | R7.2 | 以「有無進入障礙」為產業結構的核心問題 | — | Greenwald & Kahn（2005，部分核實：出版社簡介） | 規則（文獻） |
   | R7.3 | Morningstar 五類＋Helmer 補足 | — | Morningstar 五類（經 Mauboussin & Callahan 2024 轉述，部分核實）；Helmer Benefit／Barrier（作者受訪逐字稿，已核實） | 規則（文獻） |
   | R7.4 | 公司主張與可驗證證據分開＋窗口關閉指標 | CRWD、高明鐵、富喬、BE、晶心科 | — | 規則（案例） |
   | R7.5 | 週期依來源分開 | BRK、台積電、ARM、晶心科、富喬 | — | 規則（案例） |
   | R7.6 | 循環高點不當結構 | 富喬、高明鐵 | Porter（2008）完整循環（已核實部分） | 規則（文獻） |
   | R8.1 | 一至三個主導業務變數 | — | — | 規則（設計要求） |
   | R8.2 | 指標、資料源、待驗證問題、資料缺口 | — | — | 規則（設計要求） |
   | R8.3 | 交接只談業務 | — | — | 規則（設計要求） |
   | RD.1 | 匿名客戶不猜 | 台積電、高明鐵、富喬、晶心科、CRWD、BE | — | 規則（案例） |
   | RD.2 | 自述與申報矛盾檢查 | MCD、高明鐵 | — | 規則（案例） |
   | RD.3 | 口徑標示、KPI 口徑變更不接續 | 口徑：台積電、高明鐵、富喬、ARM、晶心科、MCD；KPI 變更：ARM、CRWD | — | 規則（案例） |
   | RD.4 | 營業外分離、SBC 雙口徑、不可重複項目分離 | 營業外為富喬、BRK、晶心科；SBC 為 CRWD、ARM；不在營業外的不可重複項目為 BE、樣本外案例（匿名） | — | 規則（案例） |
   | RD.5 | 官方簡報優先於第三方逐字稿 | CRWD | — | 規則（沿用 repo 規則） |

   - **觀察區清單**：單一案例或沒有案例的項目。R4.2、R4.7、R5.5、R6.4、RD.6 原列規則，判定後改列觀察區，
     分別對應 OB-6、OB-8、OB-4、OB-7、OB-5。R3.6 原判觀察區（OB-2），因樣本外案例成為第二個獨立案例，依 6.4 升為規則。OB-3 由 R5.3 的資本財與耗材分表拆出。

   | 編號 | 項目名 | 適用步驟 | 案例 | 判定 |
   |---|---|---|---|---|
   | OB-1 | 開放標準削弱指令集護城河 | 7 | 晶心科 | 觀察區 |
   | OB-3 | 資本財與營運耗材分表 | 5 | 台積電 | 觀察區 |
   | OB-4 | 不受控的轉授權商 | 5 | ARM（Arm China） | 觀察區 |
   | OB-5 | 公司已澄清的媒體推測不引用 | 資料紀律 | 高明鐵 | 觀察區 |
   | OB-6 | 每象限至多 3 項，依對該來源利潤的影響排序 | 4 | — | 觀察區 |
   | OB-7 | 自家產品的世代路線圖也算替代 | 6 | 富喬 | 觀察區 |
   | OB-8 | 影響兩個以上來源的共同因子，抽到跨來源彙總表 | 4 | — | 觀察區 |
   | OB-9 | 公司層級的彙總結論 | 4、5 | 樣本外案例（匿名） | 觀察區 |
   | OB-10 | 跨章節的期間與口徑一致 | 資料紀律 | 樣本外案例（匿名） | 觀察區 |

   - FR-04 的簡稱「台帳」改為「分歧追蹤表」，指同一張表；另把多處用語改為台灣慣用（消息來源、市占率、揭露細緻度等），不涉規則變更。
   - **第一輪盲測後的修正**：R3.6、R4.5 時間窗、RD.4 不可重複項目的第二個案例，以及 OB-9、OB-10，來自第一輪盲測樣本外案例的失效機制（隔離保管員去識別化後提供）；修正後重跑的結果標「修正後重跑」，不當作樣本外證據。來自樣本外案例的條目，經保管員檢查合看是否可識別後，改寫為通用寫法；原始機制留在維護者本機的樣本外保管區，2027-04 半年檢驗後再評估是否細化。
   - R5.6 補寫：比較基準取不到時一樣走降級，並分開寫流經各環節的規模與各環節留下的利潤。後者即 Gadiesh & Gilbert（1998）營收池與利潤池的區分，屬既有文獻已涵蓋的主張；「比較基準未查」只用於 S／W 判定的部分屬措辭修正。

   - **盲測**：`evals/blind-tests/2026-10-24-layer1-business-industry/`。驗收結果以樣本外三家為主要證據，
     開發組九家為回歸檢查。
     - **第一輪（樣本外證據）**：七項條件通過四項。樣本外三家與開發組九家的門檻總分都是新版較高；新版紅線 0 次；路由 6/6。
       不通過三項：樣本外 H2 的公司題小計新版 22、舊版 24；BE 對照晨星 90 項中 31 項未涵蓋（第二意見複核後 27 項）；
       格式 F-rules 12/12 不通過，主因 F-a。
     - **修正後重跑（第 2、3 輪，不當作樣本外證據）**：第 3 輪公司題小計 12/12 新版較高（H2 29／24），門檻總分、紅線、路由維持通過；
       格式 F-rules 進步到 4/12 通過，BE 晨星仍有 34 項未涵蓋，兩項維持不通過。
     - **發布判定**：第一輪樣本外有一家不通過，維護者 2026-11-01 裁定修正後發布，並照實列出上述失敗。
2. **回溯影響**：
   - 沒有提估值的單一個股請求，過去走 A 型，之後走 D 型。
   - 同一標的已有 D 型報告時，A 型第四章直接引用。
   - B、C 骨架與 `product-cycle-rotation` 的交接字樣，由「深度研究」改為明指 A 型。
   - repo 沒有歷史 Layer 1 報告，比照 v1.5.0 以新舊版盲測代替回溯對照。
3. **半年檢驗條件**（2027-04，和 v1.5.0 的半年檢驗同時進行）：
   - 升降級只依樣本外三家，加上半年內至少一個新案例；開發組九家重跑只當回歸檢查。例外：R3.6、R4.5 時間窗、RD.4 不可重複項目與 OB-9、OB-10 已採用第一輪樣本外案例作證據，它們的升降級不採計第一輪樣本外三家，只依之後的新案例。
   - 記錄每條規則與觀察區項目被觸發、改變結論的次數。
   - R3.6、R4.5 時間窗、RD.4 不可重複項目，依 6.4 在半年內未被觸發或未影響任何結論時降為註記；OB-9、OB-10 記錄觸發次數，出現第二個獨立案例才升級。
   - 沒被觸發或沒影響任何結論的規則降為註記；觀察區項目出現第二個獨立案例就升級。

## v1.5.0 — 2026-10-11

新增**建倉／加碼前的最低檢查**，並要求**決策段逐項回應財務品質警示**。

起因是一次覆盤：一個沒有經過本 skill 研究的建倉判斷，事後發現關鍵的資產負債表風險在建倉當天
大多已經公開。盲測結果顯示，現行規則若完整跑一遍，多數風險抓得到；缺口在三處：

- 快速判斷與 Briefing 不跑財務品質檢核。
- A 模板的美股欄與監控儀表板沒有質押；市場在地化對照表只指向 13D/A，漏了 DEF 14A 的質押註腳。
- 判了警示的項目，沒有進入決策理由。

三家公司的盲測方法與彙總結果見 repo 根目錄的 `evals/blind-tests/2026-10-11-pre-entry-check/`；
評分表、標準答案與受測輸出保存在維護者本機。

### 新增

- **`valuation-paths.md` 5.2「建倉／加碼前的最低檢查」**：槓桿與到期結構、承諾與或有事項、
  資本強度、信用評等與展望、控股股東與董監質押，共五項。每一項都沿用 5.1 或市場在地化對照表
  既有的定義與門檻，**本節不另設門檻**。快速判斷、口頭討論與 Briefing 都要跑，並附一行輸出格式。
  走 `financial_equity` 的銀行與保險：槓桿與資本強度標「不適用」，改看第 1 節路由表為該路徑列出的
  監理資本與資產品質；承諾與或有事項照查，放款承諾等本業授信額度列出金額、不套總額門檻；
  另附金融業專用的快速格式。沒有外部信用評等的公司，改看公司債殖利率或利差、借款利率與契約條款、
  近期再融資條件，這些也取不到才標「未查」。門檻需要的比較基準（同業中位、自身歷史均值）
  取不到時，判定標「未查」並列出已取得的原始數值，⛔ 不得暫判警示或暫判正常；盲測中新版的兩份
  CHTR 報告曾在同業中位未取得時把資本強度判成警示，加上這條後重跑，改判「未查」或「正常（邊際）」。
- **`expectations-and-decisions.md` 第 11 節**：新建倉或加碼時，決策段須逐項回應判為警示的
  項目，寫明後果進了哪個情境，以及是否改變 `decision_status`。同一條傳導鏈上的多個警示合併
  回應，後果與機率只記一次。最低檢查標「未查」的項目列為待補資料，是否構成「核心資料缺失」
  須寫明理由。這是揭露要求，**不是另設一道自動改寫 `decision_status` 的燈號 gate**。
- **美股質押的查核來源**：`market-localization.md` 的內部人訊號、A 模板 5.2 與監控儀表板的
  美股列，補上 DEF 14A 實益持股表註腳（Reg S-K Item 403(b)），大股東另查 Schedule 13D
  Item 6。美股不設質押門檻，判定屬研究判斷。
- **`calibration-and-governance.md` 4.5「觀察區」**：收錄五個觀察項目（美股質押門檻、
  控股股東或家族的個人擔保、承諾的彙整期間、5.1 全表在比較基準缺漏時的判定、金融業最低檢查的
  具體指標），以及三個評估過但不採納的提案。
- `equity-valuation-discipline/SKILL.md`：description 補上建倉、加碼、要不要買等觸發詞；
  第一步之後指向最低檢查，8.2 指向警示回應。
- `research-report-output/SKILL.md`：新建倉或加碼的 Briefing 必須保留最低檢查與警示回應。
- A 模板第十章：新增「財務品質警示的回應」段，新建倉或加碼時必填；涵蓋警示的回應，以及
  最低檢查「未查」項目的待補資料與「核心資料缺失」判斷。發布前檢查清單與 Briefing 保留清單同步。
- `prepublish-checklist.md` 第 10 項補一條檢查。
- `equity-valuation-discipline/agents/openai.yaml`：short_description 補上建倉前最低檢查。

### 修正

- **A 模板財務品質表**：「負債比／利息保障」列改為與 5.1 同名的「負債比／流動比／利息保障／
  到期結構」，深度報告才不會漏掉到期結構。
- **A 模板三處殘留的「只調機率」指令**：第五章的警示處理、基準情境參數紀律、折現率段，原本都寫成
  警示只進情境機率，這是已退役的寫法（`calibration-and-governance.md` 退役表 2.2），也和新增的
  「決策段逐項回應」互相矛盾。三處改為與 `expectations-and-decisions.md` 第 10 節一致：
  可估算的後果寫進適用情境，發生機率進權重，只禁止同一後果在同一路徑重複扣價。
- **範例報告**：資本強度警示原寫「後果已反映在熊情境機率」，同屬上述退役寫法。改為依 FR-09
  示範：轉嫁不足的後果放在熊情境淨利率（較基準低 4pp），並標出熊情境營收、淨利率、出場本益比
  各自對應的路徑，說明沒有重複扣價。發生機率沒有可靠估計，機率面依 `expectations-and-decisions.md`
  8.4 以 6.7 的示範配置 B、C 呈現；6.5 的 25／50／25 是 `illustrative` 示範先驗，範例據實註明它
  不代表已承接這項風險，6.5 的 `E[R_H]` 不作正式預期報酬。財務品質表的槓桿列與承諾列補齊門檻
  所需的比較資料（同業、自身 5 年均值、對一年營收），判「正常」才有依據。數值沿用第 14 節固定
  示範案例，數值驗收基準不變。決策段補上對這項警示的回應。
- **退役規則掃描**：`tests/test_report_schema.py` 的退役樣式新增「只調機率」的各種寫法，
  掃描範圍是 plugin 底下全部 Markdown。改版前的 A 模板與範例共 5 處，都會被抓到。

### 不採納

這版取代的是同名的前一份提案（PR #3），以下三點經盲測與方法論審查後不採納，理由記在
`calibration-and-governance.md` 4.5：

- 承諾改用「未來 24 個月付款的現值年化」計量：起租在窗口外的長天期租約整筆漏掉。
- 以 S1–S6 固定門檻亮紅燈，紅燈預設擋下 `actionable_candidate`：未校準的門檻直接決定
  `decision_status`，與已退役的「波動率分級 → 安全邊際」同型。
- 新增「建倉前研究不足」出場分類：歸因一律沿用 `calibration-and-governance.md` 5.4 的五分類。

### 不變

- 估值引擎與 `valuation_math.py`。
- 5.1 各檢核項的門檻，包括承諾的「總額 > 一年營收」。
- FR-10 的路由表；發布前檢查清單仍為 27 項。

### 治理 4.1 附件

1. **案例與來源**：`evals/blind-tests/2026-10-11-pre-entry-check/`。

2. **回溯影響**：repo 內沒有歷史正式報告（見 `calibration-and-governance.md` 第三節），以盲測中同一題目的新舊兩版結果
   代替。結論都沒有變，變的是決策理由與揭露：

   | 題目 | main 版 | 本版 | 差別 |
   |---|---|---|---|
   | 新建倉，2026-09 的美股案例 | `watch` | `watch` | 快速判斷抓到承諾與質押，資產負債表成為主要理由 |
   | 加碼，淨現金公司 | `watch` | `watch` | 判出採購承諾警示，列為次要理由；無誤報 |
   | 新建倉，高槓桿公司 | `watch` | `watch` | 決策段逐項回應槓桿等警示；main 版只在風險章節提及 |
   | 範例報告 | `watch` | `watch` | 決策段補上警示回應；改正「只調機率」的寫法 |

   外部既有的建倉或加碼報告，需補最低檢查與決策段的警示回應。

3. **半年檢驗條件**（2027-04）：用 `evals/blind-tests/` 的同一組題目，以當時的 skill 重跑，
   再加上半年內至少一個新案例，記錄偵測分數、誤報件數與決策段的回應率；使用者若另有建倉或
   加碼報告存檔，一併統計。最低檢查沒有影響任何結論、或誤報多於有效偵測者，依 4.1 降為註記。

## v1.4.1 — 2026-09-15

命名修正：FR-04 的「預期差台帳」改名為**「個人判斷與市場定價落差」**。舊名不說明比較的兩端，
而口語替代「與市場共識落差」會與第 1 節的**賣方共識**基線撞名，讓讀者以為是在跟分析師共識比；
實際比的是**本研究判斷 vs 價格隱含預期**，賣方共識只是表中一欄參考。

### 變更

- `equity-valuation-discipline/SKILL.md` 第三步、`references/expectations-and-decisions.md` 第 4 節、
  `prepublish-checklist.md`、`calibration-and-governance.md`、`product-cycle-rotation` 兩處交接引用、
  `research-report-output` 的 Briefing 保留清單、`output-spec.md`、A 模板、範例報告與 `openai.yaml`
  描述：一律改用新名稱；模板內「台帳」簡稱維持，指的仍是同一張表。
- `expectations-and-decisions.md` 第 4 節新增一段說明比較的兩端，並禁止改稱「與市場共識落差」。
- `docs/v1.3.0-spec.md` 為歷史規格，保留舊名不動。

不影響任何計算與引擎行為。

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
