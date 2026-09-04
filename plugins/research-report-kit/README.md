# Research Report Kit（機構風研究報告工具組）

把投資研究的**輸出格式**與**內容紀律**變成可重複的流程。裝上之後，Claude 產出的研究報告會有一致的章節骨架、可讀的排版、機構風格的 PDF，以及一份跑得完的發布前檢查清單。

台股與美股共用同一套骨架——只換資料源與籌碼欄位，不為單一市場另建流程。

> **English summary**: A Claude plugin for institutional-style equity and industry research. Enforces dual `.md` + PDF delivery, a readability rule set for data-dense writing, a two-layer valuation path selector (SOTP / cyclical normalization / growth fade model), scenario-probability expected value in place of single-point R/R thresholds, and a 12-item pre-publication content checklist. Content is in Traditional Chinese; the methodology layer is designed to be replaced with your own.

---

## 這個 plugin 包含什麼

| Skill | 管什麼 | 什麼時候會自己跳出來 |
|---|---|---|
| **`research-report-output`** | 格式與交付：檔名、front matter、章節骨架、F1–F5 排版鐵則、PDF 產檔、輸出模式 | 「寫一份研究報告」「做個股深度研究」「幫我出 PDF 版報告」 |
| **`equity-valuation-discipline`** | 內容紀律：估值路徑判別、fade 參數約束、情境機率與期望值、敏感度規則、12 項發布前檢查 | 「DCF」「SOTP」「目標價」「reverse DCF」「這檔值不值得買」 |
| **`product-cycle-rotation`** | 產業掃描：product cycle 五問、T-18～T+6 時間軸、channel check SOP、催化劑框架 | 「誰受惠」「design win」「BOM 拆解」「供應鏈輪動」 |
| **`price-routing`** | 取價路由：偵測可用行情工具 → 依市場選路 → 沒有 MCP 時退回 yfinance | 任何需要股價的場景 |

四個 skill 可以分開用。只想要排版與產檔的人，把後三個刪掉也能運作。

---

## 三個設計主張

**1. 排版即內容。** 任何需要讀第二次才能拆解的段落，等於沒寫。所以有 F1–F5 五條排版鐵則：≥3 個數字的段落必須拆成「一行結論 ＋ 實績表 ＋ 推導表」；表格儲存格塞多組數值必須拆出「斷言欄 ＋ 數據明細欄」；每張 >3 行的表格前面必須有一句話摘要。這些規則不是美學偏好，是從「印成 PDF 之後讀不下去」的返工紀錄裡歸納出來的。

**2. 保守性只能收一次費。** 多數估值錯誤不是某個參數抓錯，而是「營收打折 → 利潤率取下緣 → 倍數再降一級 → 折現率再加碼」四處各打一次折，相乘後的「基準情境」其實是 P10。這個 plugin 把保守集中在**情境機率**與**買入安全邊際**兩處，參數本身回到無偏最佳估計——這樣「紀律值 vs 市價」才重新是有意義的比較。

**3. 方法論該是你的，不是我的。** 估值紀律那一層是預設值不是教條。你有自己的框架文件，就讓它覆蓋掉；沒有的話，用這裡的當骨架。設定方式見 `skills/research-report-output/references/customize-your-framework.md`。

---

## 安裝

**從 marketplace 安裝（可收到更新）：**

```
/plugin marketplace add Benjamin-Teng/industrials-research-skill
/plugin install research-report-kit@research-tools
```

之後拿新版：`/plugin marketplace update research-tools`，再 `/reload-plugins`。

**或直接安裝 `.plugin` 檔**：在 Claude 桌面版把檔案拖進對話，按安裝卡片即可（這條路沒有更新通道）。

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

```
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

```
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
    │   └── references/
    │       ├── valuation-paths.md              # SOTP／週期股／成長股三條路徑
    │       ├── prepublish-checklist.md         # 內容層 12 項
    │       └── calibration-and-governance.md   # 常數怎麼校準、規則怎麼退役
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

**這個 plugin 產出的任何內容都不是投資建議。** 它管的是流程與紀律，不保證結論正確。所有紀律值（倍數上限、折讓數列、安全邊際分級）都是待校準的經驗值，母體與校準路徑列在 `calibration-and-governance.md`——**用之前先看它們是從哪類公司、哪段期間校準的**。引用的實證研究多為美股樣本，外推至其他市場前請先用自己的覆盤資料驗證。
