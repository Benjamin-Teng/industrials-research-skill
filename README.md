# Claude Research Plugins

投資研究用的 Claude plugin marketplace。目前收錄一個 plugin。

---

## 安裝

在 Claude Code 或 Cowork 的對話中執行：

```
/plugin marketplace add Benjamin-Teng/industrials-research-skill
/plugin install research-report-kit@research-tools
```

裝好之後不需要任何設定，直接說「幫我做一份 XXXX 的個股深度研究報告」就會啟動。

> 之後要拿新版：`/plugin marketplace update research-tools`，再 `/reload-plugins`。
> 第三方 marketplace 預設不自動更新；想開自動更新，在 `/plugin` 的 Marketplaces 分頁把它打開。

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
