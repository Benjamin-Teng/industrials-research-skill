# Claude Research Plugins

投資研究用的 Claude plugin marketplace。目前收錄一個 plugin。

---

## 安裝

同一份 skill 同時封裝成 **Claude Code plugin** 與 **Codex plugin**：Claude 讀 `.claude-plugin/`，Codex 讀 `.codex-plugin/` 與根目錄的 `.agents/plugins/marketplace.json`，兩邊共用 `plugins/research-report-kit/skills/` 底下同一份 `SKILL.md` 與 references。marketplace 名稱在兩邊都叫 `research-tools`。

### Claude Code

```text
/plugin marketplace add Benjamin-Teng/industrials-research-skill
/plugin install research-report-kit@research-tools
/reload-plugins
```

> `/reload-plugins` 讓剛裝好的 plugin 立即生效，不必重開 Claude Code。
> 之後拿新版：`/plugin marketplace update research-tools`，再 `/reload-plugins`。
> 第三方 marketplace 預設不自動更新；要開自動更新，在 `/plugin` 的 Marketplaces 分頁打開。

### Codex

#### VS Code／Codex IDE（推薦）

Codex IDE extension 目前不支援完整 plugin，但支援獨立 skill。本 plugin 沒有 MCP、connector 或 hook，所以用這條路可取得目前全部功能。四個 skill 各自獨立，要哪個裝哪個；在 Codex 對話框貼上：

```text
$skill-installer 請從 https://github.com/Benjamin-Teng/industrials-research-skill/tree/main/plugins/research-report-kit/skills/research-report-output 安裝 research-report-output skill
$skill-installer 請從 https://github.com/Benjamin-Teng/industrials-research-skill/tree/main/plugins/research-report-kit/skills/equity-valuation-discipline 安裝 equity-valuation-discipline skill
$skill-installer 請從 https://github.com/Benjamin-Teng/industrials-research-skill/tree/main/plugins/research-report-kit/skills/product-cycle-rotation 安裝 product-cycle-rotation skill
$skill-installer 請從 https://github.com/Benjamin-Teng/industrials-research-skill/tree/main/plugins/research-report-kit/skills/price-routing 安裝 price-routing skill
```

同意下載後開啟新對話，輸入 `/skills` 應該看到剛裝的 skill；若沒出現，重新載入 VS Code。

#### Codex CLI 對話介面

先在終端機註冊一次 marketplace：

```shell
codex plugin marketplace add Benjamin-Teng/industrials-research-skill
```

接著啟動 `codex`，在對話介面輸入 `/plugins`，切換到 `research-tools` marketplace、開啟 `research-report-kit` 並選擇安裝。安裝後開始新 session。

#### 終端機進階安裝

若偏好完全使用命令列：

```shell
codex plugin marketplace add Benjamin-Teng/industrials-research-skill
codex plugin add research-report-kit@research-tools
```

安裝後開啟新的 Codex session。完整 plugin 流程適用於 Codex CLI 與支援 Plugins Directory 的桌面介面，不會把 plugin 安裝進 VS Code IDE extension。

**更新**：Git marketplace 的快照不會自動刷新，先 upgrade 再重裝：

```shell
codex plugin marketplace upgrade research-tools
codex plugin add research-report-kit@research-tools
```

### 使用方式

- **自動觸發（主要）**：不必打任何指令——只要對話講到研究報告、估值、產業輪動、查股價，Claude Code 或 Codex 會依 skill 的 `description` 自動載入。
- **Claude Code 手動觸發**：`/research-report-output`（依環境亦可能顯示為 `/research-report-kit:research-report-output`）。
- **Codex 手動觸發**：`$research-report-output`。其餘三個 skill 同理。

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
