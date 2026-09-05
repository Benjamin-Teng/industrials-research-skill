# Claude Research Plugins

投資研究用的 Claude plugin marketplace。目前收錄一個 plugin。

---

## 安裝

這個 repo 同時符合兩套 skill 規格：**Claude plugin** 與 **Agent Skills 開放標準**（OpenAI Codex 採用同一份規格）。四個 skill 的 `SKILL.md` 未做任何平台專屬綁定，兩邊共用同一份檔案。

### Claude（Cowork / Claude Code）

```
/plugin marketplace add Benjamin-Teng/industrials-research-skill
/plugin install research-report-kit@research-tools
```

> 之後拿新版：`/plugin marketplace update research-tools`，再 `/reload-plugins`。
> 第三方 marketplace 預設不自動更新；要開自動更新，在 `/plugin` 的 Marketplaces 分頁打開。

### Codex

Codex 從 `.agents/skills` 目錄掃描 skill，**支援 symlink 並會跟隨到目標**，所以 clone 一份再連結過去就好，更新只要 `git pull`。

```bash
# 1) clone 到你放原始碼的地方
git clone https://github.com/Benjamin-Teng/industrials-research-skill.git ~/src/industrials-research-skill

# 2A) 全域安裝——所有專案都吃得到
mkdir -p ~/.agents/skills
ln -s ~/src/industrials-research-skill/plugins/research-report-kit/skills/* ~/.agents/skills/

# 2B) 或只在單一專案啟用
mkdir -p /path/to/your/project/.agents/skills
ln -s ~/src/industrials-research-skill/plugins/research-report-kit/skills/* /path/to/your/project/.agents/skills/
```

**驗證**：在 Codex 裡輸入 `/skills`，應該列出 `research-report-output`、`equity-valuation-discipline`、`product-cycle-rotation`、`price-routing` 四個。

**呼叫**：打 `$research-report-output` 明確指定，或直接描述任務（「幫我做一份 XXXX 的個股深度研究報告」）讓 Codex 依 description 自動匹配。

**更新**：`cd ~/src/industrials-research-skill && git pull` — symlink 會自動指到新版。

**Codex 的掃描優先序**（前面的蓋過後面的）：

```
$CWD/.agents/skills  →  $CWD/../.agents/skills  →  $REPO_ROOT/.agents/skills
→  $HOME/.agents/skills  →  /etc/codex/skills  →  系統內建
```

> **Windows 使用者**：`ln -s` 需要開發人員模式或系統管理員權限。不想開的話直接複製資料夾（`xcopy /E /I`），代價是每次更新都要重新複製。

### ChatGPT 網頁版

⚠️ **ChatGPT 的 Skills 功能只開放 Business / Enterprise / Edu 方案**，Free、Go、Plus、Pro 都不能用。個人帳號的替代做法是開一個 **Project**，把 `skills/research-report-output/SKILL.md` 的內容貼進 project instructions，再把 `references/` 底下的檔案當附件上傳。

另外 ChatGPT 的 Python 沙箱**沒有一般對外網路、`apt` 不通**，所以 pandoc 與 Chromium 都裝不進去，**PDF 產檔在那個環境無法運作**，只能交付 `.md`。取價也只能靠內建搜尋，拿不到台股籌碼欄位。

---

## 收錄的 plugin

### research-report-kit

把投資研究的**輸出格式**與**內容紀律**變成可重複的流程。裝上之後，Claude 產出的研究報告會有一致的章節骨架、可讀的排版、機構風格的 PDF，以及一份跑得完的發布前檢查清單。

四個可分開使用的 skill：

| Skill | 管什麼 |
|---|---|
| `research-report-output` | 格式與交付：檔名、front matter、章節骨架、F1–F5 排版鐵則、PDF 產檔、三種輸出模式 |
| `equity-valuation-discipline` | 內容紀律：估值路徑判別、fade 參數約束、情境機率與期望值、12 項發布前檢查 |
| `product-cycle-rotation` | 產業掃描：product cycle 五問、T-18～T+6 時間軸、channel check SOP |
| `price-routing` | 取價路由：偵測可用行情工具 → 依市場選路 → 無 MCP 時退回 yfinance |

完整說明見 [`plugins/research-report-kit/README.md`](plugins/research-report-kit/README.md)。

**PDF 產檔的環境依賴**（雲端容器多半已具備）：

```bash
pip install pypdf pyyaml playwright --break-system-packages
playwright install chromium
apt-get install -y pandoc fonts-noto-cjk      # 或 brew install pandoc
```

缺件時的降級路徑寫在 plugin 的 `references/output-spec.md` 第六章。

---

## 授權

MIT License，見 [LICENSE](LICENSE)。

**這裡的任何內容都不是投資建議。** plugin 管的是流程與紀律，不保證結論正確。所有紀律值（倍數上限、折讓數列、安全邊際分級）都是待校準的經驗值，母體與校準路徑列在 `calibration-and-governance.md`——用之前先看它們是從哪類公司、哪段期間校準的。

---

## 維護

改完 plugin 內容後：

1. 進 `plugins/research-report-kit/.claude-plugin/plugin.json` 的 `version`（semver）
2. 在該 plugin 的 `CHANGELOG.md` 寫一段
3. commit & push

使用者端跑 `/plugin marketplace update research-tools` 就會拿到新版。
