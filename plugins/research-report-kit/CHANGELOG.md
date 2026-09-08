# Changelog

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
