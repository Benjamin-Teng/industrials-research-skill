# AGENTS.md

給在這個 repo 上工作的 coding agent（Codex、Claude Code 等）。

## 這個 repo 是什麼

`research-report-kit` —— 一個同時封裝成 Claude Code plugin 與 Codex plugin 的投資研究工具組。
內容是**方法論文件與報告模板**（繁體中文），加上一支支撐它們的數值核心。

方法論的**單一來源**是
`plugins/research-report-kit/skills/equity-valuation-discipline/references/expectations-and-decisions.md`。
公式、符號與口徑一律以該檔為準；其他檔案引用它，**不得另抄一份變體**。
文件與程式若不一致，以文件的定義為準、修程式。

## 在唯讀沙箱裡怎麼跑驗證（重要）

**`uv run` 在唯讀沙箱下一定失敗**——uv 需要寫快取與解析 venv，加 `--offline`／`--no-sync`／
`--no-cache` 都繞不過去。這不是環境壞掉，是 uv 的運作前提與唯讀沙箱互斥。

專案的虛擬環境已經建好，**直接用 venv 裡的執行檔即可，全程零寫入**：

```bash
# 測試（停用 bytecode 與 pytest 快取）
.venv/Scripts/python.exe -B -m pytest tests/ -q -p no:cacheprovider

# lint（停用 ruff 快取）
.venv/Scripts/ruff.exe check . --no-cache
.venv/Scripts/ty.exe check .
```

Linux／macOS 把 `.venv/Scripts/` 換成 `.venv/bin/`，去掉 `.exe`。

有寫入權限時才用一般寫法：`uv run --with pytest pytest tests/ -q`、`uv run ruff check .`、
`uv run ty check .`。

## 品質門檻

宣稱完成前，下列全部要 0 error，且**輸出要實際貼出來**：

- `ruff check` 與 `ty check`（改了 `.py` 時）
- `pytest tests/`（全數通過；數字以當場輸出為準）
- `npx --yes markdownlint-cli2 "plugins/research-report-kit/**/*.md" "README.md"`（改了 `.md` 時）
- `claude plugin validate .`（改了 manifest 時）
- **表格欄數上限 7 欄**——這不是 lint 規則，lint 抓不到，PDF 版面會擠壓。
  `tests/test_report_schema.py` 有守這條。

## 這個 repo 特別容易踩的兩件事

1. **文字編碼**：報告內容到處是 `−`（U+2212）`≤` `≥` `→` `✓`。任何 text-mode IO
   沒明寫 `encoding="utf-8"` 就會吃系統 locale——Linux 是 UTF-8 所以測不出來，
   中文 Windows（cp950）與西文 Windows（cp1252）直接 `UnicodeEncodeError`。
   跑一次性腳本時前面加 `PYTHONIOENCODING=utf-8`。
2. **數值反解的成功判定**：`valuation_math.solve_scalar_parameter()` 是「價格隱含預期」
   的實作核心，它的每個回傳狀態都是一句對外斷言。成功路徑必須同時通過
   **自變數收斂**與**殘差達標**兩關，且要能分辨「沒偵測到」「未收斂」「區域未被有效評估」。
   ⛔ 不得因為殘差小就宣稱參數被識別出來——估值模型在最適值附近常常平坦，那是假精確的來源。

## 版本與發布

`plugins/research-report-kit/CHANGELOG.md` 是變更紀錄。版本號有三處必須同步
（`tests/test_plugin_compatibility.py` 會擋不一致）：

- `.claude-plugin/marketplace.json` 的 entry
- `plugins/research-report-kit/.claude-plugin/plugin.json`
- `plugins/research-report-kit/.codex-plugin/plugin.json`

⛔ 不要 commit 或 push，除非使用者明確要求。
