# 接上你自己的方法論

這個 plugin 分成兩層：

| 層 | 內容 | 該不該改 |
|---|---|---|
| **格式層**（`research-report-output`） | 檔名、front matter、章節骨架、F1–F5 排版鐵則、PDF 樣式、交付流程 | 多數人直接用；只需改署名與免責標語 |
| **內容層**（`equity-valuation-discipline`、`product-cycle-rotation`） | 估值路徑、參數紀律、情境機率、channel check SOP、發布前內容檢查 | **這是預設值，不是教條**——有自己方法論的人應該覆蓋掉 |

分層的理由：排版與交付規則跨方法論通用（不管你用 DCF 還是 EV/EBITDA，數據密集段落都該拆表）；但估值方法論高度個人化，硬套別人的紀律值只會產生假精確。

---

## 一、最小設定（5 分鐘）

### 1. 署名與免責標語

在每份報告的 front matter：

```yaml
author: 〈你的名字或機構〉
footer_right: 〈頁尾右欄標語〉      # 預設「個人研究筆記 · 非投資建議」
framework: 〈你的方法論文件名 vX.Y〉
```

**封面免責條款全文**也可以直接在 front matter 覆蓋：

```yaml
disclaimer: 本報告由〈機構〉編製，僅供內部參考，不構成投資建議。
```

想改掉所有報告的預設值（而非逐份覆蓋），編輯 `scripts/md2pdf.py` 的 `DISCLAIMER` 常數。

### 2. 建立自己的 front matter 預設

把常填欄位寫進一個 `my-defaults.yaml` 放在工作目錄，每次從模板複製後覆蓋。或直接改 `templates/` 下的三份模板——它們就是你的預設值。

---

## 二、接上自己的方法論（建議做法）

### 做法 A：用專案／知識庫文件當 source of truth（推薦）

如果你用的介面支援專案知識庫（Claude Projects、CLAUDE.md、AGENTS.md 之類），把你的方法論寫成一份文件放進去，並在其開頭寫明：

```markdown
> 本文件為研究內容標準的 source of truth。
> 與 research-report-kit 的 equity-valuation-discipline 衝突時，一律以本文件為準。
```

`research-report-output` 的 SKILL.md 已寫明「使用者方法論優先」，Claude 會先讀你的文件。

**一份可用的方法論文件至少要回答四件事**：

1. **估值路徑怎麼選**——什麼樣的標的走 SOTP、什麼樣的走可比法、什麼樣的走現金流折現。
2. **每條路徑的參數紀律**——哪些參數有上限、上限是多少、母體是從哪類公司哪段期間校準的。
3. **保守性放在哪裡**——放在每個參數（容易多重收費）、放在情境機率、還是放在買入折價。**只能放一處。**
4. **發布前必查什麼**——你自己反覆犯的錯，寫成檢查清單。

### 做法 B：直接改 skill 檔案

`equity-valuation-discipline/references/valuation-paths.md` 與 `prepublish-checklist.md` 是純 markdown，直接改寫即可。改完重新打包 plugin（見下）。

適合：你的方法論骨架與預設值接近，只想換掉紀律值與門檻。

### 做法 C：整個停用內容層

只留 `research-report-output` 與 `price-routing`，把另外兩個 skill 目錄刪掉。SKILL.md 中對它們的引用會自然降級為「照使用者的方法論做」。

適合：你有完整的既有流程，只想要排版與產檔這一段。

---

## 三、改 PDF 樣式

`assets/report.css` 的可調處：

| 想改什麼 | 改哪裡 |
|---|---|
| 主色（深藍 `#16324f`） | CSS 開頭的顏色變數／`--brand` 相關宣告 |
| 頁面邊界、紙張大小 | `@page` 區塊的 `size` 與 `margin` |
| 內文與表格字級 | `body` 的 `font-size`、`table` 的 `font-size` |
| 中文字型 | `font-family` 串列（容器內先用 `fc-list \| grep -i cjk` 確認有哪些） |
| 頁尾三欄內容 | `@page` 的 `@bottom-left` / `@bottom-center` / `@bottom-right`，以及 `md2pdf.py` 的 footer 組裝段 |
| 標籤徽章（l1/l2/l3）配色 | `.tag.l1` / `.tag.l2` / `.tag.l3` |
| 提示框（bull/bear/caveat/note）配色 | 對應的 class 區塊 |

**建議不要逐份報告微調樣式**——跨報告視覺一致本身就是可信度的一部分。要改就改 CSS，一次改全部。

---

## 四、改完之後重新打包

**若你是從 marketplace 安裝的**（repo 形式）：改完 `plugins/research-report-kit/` 底下的檔案 → 進 `plugin.json` 的 `version` → 寫 CHANGELOG → commit & push。使用者端 `/plugin marketplace update` 就會拿到。

**若你要打成單一檔案傳給別人**：

```bash
cd /path/to/research-report-kit
zip -r ~/research-report-kit.plugin . -x "*.DS_Store" -x "__pycache__/*"
```

產出的 `.plugin` 檔可直接在 Cowork／Claude Code 安裝。改了 `plugin.json` 的 `version` 再打包，之後才分得清版本。

---

## 五、資料源 MCP（選配）

`price-routing` 會自動偵測可用的取價工具，**一個都沒有時退回 `yfinance`**，所以不裝任何 MCP 也能運作。想要更好的資料品質時：

| 需求 | 建議連接 |
|---|---|
| 台股股價、月營收、三大法人、融資融券 | FinMind MCP |
| 美股即時報價、歷史價、選擇權 | 券商 MCP（如 Interactive Brokers） |
| 財報原文（10-K／10-Q／MOPS） | 對應市場的文件庫，或直接用網頁抓取 |
| 產業報價與供應鏈情報 | 產業研究機構訂閱（付費，見 `/product-cycle-rotation` 的工具箱） |

連上之後不需要改任何設定——`price-routing` 是在執行時偵測工具是否存在，不是讀設定檔。
