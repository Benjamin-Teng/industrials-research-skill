# Research Report Kit（機構風研究報告工具組）

把投資研究的**輸出格式**與**內容紀律**變成可重複的流程。裝上之後，Claude 產出的研究報告會有一致的章節骨架、可讀的排版、機構風格的 PDF，以及一份跑得完的發布前檢查清單。

台股與美股共用同一套骨架——只換資料源與籌碼欄位，不為單一市場另建流程。

> **English summary**: A Claude plugin for institutional-style equity and industry research. Enforces dual `.md` + PDF delivery, a readability rule set for data-dense writing, and an expectations-driven research workflow: read the expectations priced in, build a falsifiable expectations-gap ledger, keep present intrinsic value / holding-period price / holding-period return strictly separate, state reward-risk and illustrative-probability expected values, and route decisions through conditional thresholds rather than a fixed margin of safety. Content is in Traditional Chinese; the methodology layer is designed to be replaced with your own.

---

## 這個 plugin 包含什麼

| Skill | 管什麼 | 什麼時候會自己跳出來 |
|---|---|---|
| **`research-report-output`** | 格式與交付：檔名、front matter、章節骨架、F1–F5 排版鐵則、PDF 產檔、輸出模式 | 「寫一份研究報告」「做個股深度研究」「幫我出 PDF 版報告」 |
| **`equity-valuation-discipline`** | 內容紀律：價格隱含預期與預期差、模型路由、三種價值／報酬分離、R/R 與示範機率、決策門檻、發布前檢查 | 「DCF」「SOTP」「目標價」「reverse DCF」「預期差」「R/R」「這檔值不值得買」 |
| **`product-cycle-rotation`** | 產業掃描：product cycle 五問、T-18～T+6 時間軸、channel check SOP、催化劑框架 | 「誰受惠」「design win」「BOM 拆解」「供應鏈輪動」 |
| **`price-routing`** | 取價路由：偵測可用行情工具 → 依市場選路 → 沒有 MCP 時退回 yfinance | 任何需要股價的場景 |

四個 skill 可以分開用。只想要排版與產檔的人，把後三個刪掉也能運作。

---

## 三個設計主張

**1. 排版即內容。** 任何需要讀第二次才能拆解的段落，等於沒寫。所以有 F1–F5 五條排版鐵則：≥3 個數字的段落必須拆成「一行結論 ＋ 實績表 ＋ 推導表」；表格儲存格塞多組數值必須拆出「斷言欄 ＋ 數據明細欄」；每張 >3 行的表格前面必須有一句話摘要。這些規則不是美學偏好，是從「印成 PDF 之後讀不下去」的返工紀錄裡歸納出來的。

**2. 便宜不是理由，預期差才是。** 研究的對象不是「這家公司值多少」，而是「現價已經假設了什麼、我有什麼可驗證的理由認為它不對、以及市場會在什麼時候因為什麼而改變假設」。所以流程強制分開三件過去被混在一起的東西：**當前內在價值**（折回今天）、**持有期末價格**（需要一個說得出口的價格反映機制）、**持有期總報酬**（含股利、成本與稅）。同樣保留「保守性只能收一次費」——營收打折、利潤率取下緣、倍數再降一級、折現率再加碼，相乘後的「基準情境」其實是 P10——但改以「後果進情境、機率進權重」處理，而不是把風險一律塞進機率。

> **v1.3.0 的破壞性變更**：舊版「三情境估值期望值 × 安全邊際 → 評等」的單一決策鏈已退役。單一折現估值與固定安全邊際**不再自動決定評等**；決策改走條件門檻，且使用者未提供風險政策時只輸出條件式結論。退役規則逐條列在 `skills/equity-valuation-discipline/references/calibration-and-governance.md`，舊報告不受影響、也不會被覆寫。

**3. 方法論該是你的，不是我的。** 估值紀律那一層是預設值不是教條。你有自己的框架文件，就讓它覆蓋掉；沒有的話，用這裡的當骨架。設定方式見 `skills/research-report-output/references/customize-your-framework.md`。

---

## 安裝

**從 marketplace 安裝（可收到更新）：**

```text
/plugin marketplace add Benjamin-Teng/industrials-research-skill
/plugin install research-report-kit@research-tools
```

之後拿新版：`/plugin marketplace update research-tools`，再 `/reload-plugins`。

**或直接安裝 `.plugin` 檔**：在 Claude 桌面版把檔案拖進對話，按安裝卡片即可（這條路沒有更新通道）。

**Codex**：本 plugin 也是 Codex 原生 plugin。終端機兩行裝好：

```shell
codex plugin marketplace add Benjamin-Teng/industrials-research-skill
codex plugin add research-report-kit@research-tools
```

VS Code／Codex IDE 不支援完整 plugin，改在對話框用 `$skill-installer` 從 GitHub 路徑裝獨立 skill；完整三入口與 ChatGPT 網頁版的限制見 [repo 根目錄 README](../../README.md)。裝好後以 `$research-report-output` 明確呼叫。

### PDF 產檔的環境依賴

PDF 由 `md → pandoc → HTML → Chromium → PDF` 產生，需要：

```bash
pip install pypdf pyyaml playwright --break-system-packages
playwright install chromium
apt-get install -y pandoc fonts-noto-cjk      # 或 brew install pandoc
```

雲端容器多半已有這些。缺件時的降級路徑（只交 md、保留 HTML、換字型）寫在 `skills/research-report-output/references/output-spec.md` 第六章。

### 資料源（全部選配）

`price-routing` 在執行時偵測工具是否存在，**一個 MCP 都沒有也能運作**（退回 `yfinance`）。想要更好的資料品質時可連接：

- 台股資料源 MCP（股價、月營收、三大法人、融資融券）
- 券商 MCP（美股即時報價、歷史價、選擇權）

連上之後不需改任何設定。

---

## 怎麼用

直接說要什麼就好：

```text
幫我做一份 XXXX 的個股深度研究報告
把這個產業的供應鏈拆一拆，看誰受惠
這檔現在的估值合理嗎
出一份這週的輪動掃描週報
剛剛那份報告出一個 external 版給別人看
```

Claude 會自動選對 skill、選對模板、跑完檢查清單，最後交付 `.md` 與 `.pdf` 兩個檔。

### 三種輸出模式

| 模式 | 觸發 | 內容 | 檔名 |
|---|---|---|---|
| **Internal**（預設） | — | 完整版，含所有框架引用與方法論補充 | `主體_類型_版本_日期.md` |
| **External** | 「給別人」「傳播」「外部版」 | 剝離內部框架標記，保留全部數據與結論 | 加 `_ext` |
| **Briefing** | 「摘要」「重點速覽」「3 頁」 | ≤3 頁，只留結論與最關鍵數字 | 加 `_brief` |

---

## 目錄結構

```text
research-report-kit/
├── .claude-plugin/plugin.json
├── README.md
├── CHANGELOG.md
├── examples/
│   └── sample-report.md              # 最小可跑範例（可直接產 PDF 驗證環境）
└── skills/
    ├── research-report-output/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── output-spec.md             # 完整輸出規範 ＋ 格式層檢查清單
    │   │   ├── formatting-rules.md        # F1–F5 完整版（正反例）
    │   │   ├── market-localization.md     # 台股／美股對照 ＋ 三個真差異
    │   │   └── customize-your-framework.md # 怎麼換成你自己的方法論
    │   ├── templates/{A,B,C}-*.md         # 個股／產業／週報三型骨架
    │   ├── scripts/md2pdf.py
    │   └── assets/report.css
    ├── equity-valuation-discipline/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── expectations-and-decisions.md   # 方法論單一來源：預期差、報酬、R/R、決策
    │   │   ├── valuation-paths.md              # 模型路由與計算口徑（折現配對、股權橋接、fade）
    │   │   ├── prepublish-checklist.md         # 發布前內容層適用性檢查
    │   │   └── calibration-and-governance.md   # 常數怎麼校準、規則怎麼退役、退役表
    │   └── scripts/valuation_math.py           # 上述公式的可測試實作
    ├── product-cycle-rotation/
    │   ├── SKILL.md
    │   └── references/channel-check-sop.md
    └── price-routing/SKILL.md
```

---

## 幾個值得先知道的規則

- **價格三件套**：所有價格一律寫成「數值＋日期＋盤別」（`US$218.98（2026-08-14 正常盤收盤）`）。缺任一件視為未查證數據。
- **資料層級標籤**：關鍵數據標 `l1`（公司揭露，可當基準）／`l2`（分析師估算，情境參考）／`l3`（第二手，**不得納入基準假設**）。PDF 會渲染成彩色徽章。
- **表格上限 7 欄**：超過就拆表，否則 PDF 會擠壓。
- **報告不進知識庫**：只有方法論更新、可複用的產業地圖、覆盤結論才寫回。單一標的的長報告會把知識庫灌爆。
- **對標同業須具名**：以同業作為參數上限者，須具名同業組（≥3 家）、列出各家 ≥5 年中位數與查詢日。寫「參考同業水準」而不具名，視同未查證。

---

## 授權與免責

MIT License。

**這個 plugin 產出的任何內容都不是投資建議。** 它管的是流程與紀律，不保證結論正確。框架內任何常數與門檻都是**使用者政策或待校準假設**，不是已驗證的投資優勢；母體與校準路徑列在 `calibration-and-governance.md`——**用之前先看它們是從哪類公司、哪段期間校準的**。引用的實證研究多為美股樣本，外推至其他市場前請先用自己的覆盤資料驗證。

報告中的示範機率（`illustrative`）**沒有實證勝率含義**，用途是說明「這筆交易需要什麼條件才成立」；`edge_status` 預設為 `hypothesis_only`，**研究輸出不等於交易授權**。
