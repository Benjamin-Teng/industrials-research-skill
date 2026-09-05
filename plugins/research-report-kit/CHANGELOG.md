# Changelog

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
