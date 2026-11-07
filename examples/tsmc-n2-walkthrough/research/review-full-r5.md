# 台積電 N2 互動頁示意圖全面審查 r5

- 審查日：2026-11-07
- 審查對象：`台積電N2製程_產品技術研究_v1.0_20261101.html`（對應 repo commit `42402fd`），20 步、52 拍；另核對 `research/01-design-to-mask.md` 第 9 節、`research/03-evolution-roadmap.md` 新增的 GIGAFAB 與 IEEE Spectrum 引文、repo 的 `examples/tsmc-n2-walkthrough/CONFORMANCE.md`
- 使用的標準：方法檔 `product-technology-method.md` 第六章、3.1–3.3 節（3.3 已加上維基百科一條，使用者 2026-11-07 決定）
- 上一輪：`review-full-r4.md`；實作者修正報告為 repo 內 `task-6-report.md` 末段
- 截圖：scratchpad，未隨附（每拍 375px 亮色、1180px 亮色、375px 暗色各一張，共 156 張）

## 怎麼查的

1. 新來源逐筆開頁比對：用 WebFetch 打開 5 個 Synopsys 術語頁、5 份 Google Patents 專利頁，以及 TSMC GIGAFAB 頁、IEEE Spectrum 2013 一文，逐句確認證據檔的引文是否在原頁、在哪一節、作者與日期是否相符。請求沒有附任何聯絡資訊。
2. 頁面的 `SRC`、各步 `sources` 與材料說明，逐句對照 01 第 9 節的引文，判斷有沒有說得比引文強。
3. 腳本沿用前四輪：52 拍逐拍傾印，與 r4 比對；`schematic_topology.py` 跑全頁與步驟 2、13、14 每一拍，與 r4 逐字比對；改過的拍看亮色與暗色截圖。
4. CONFORMANCE 補回的三節與 `7c18ac7` 版逐行 diff。
5. 頁面 console 錯誤 0；暫存頁審完已刪除。

## 結論：不可發布

W1 已修好：6 筆維基百科來源全部換掉，抽查的引文都在原頁。別家公司的專利，只要引的是「先前技術」段，可以當第 4 級的業界通用依據（見第二節）。卡住的只剩一處：鉬／矽多層膜說明裡的「幾十層」，依據是專利自己的實施例，不是先前技術，撐不住「業界通用」這個標示（R5-1，中）。改成「多層」這一個詞，就沒有剩下的中、高嚴重度問題，複查只要確認這一處，就可以判定可發布。

## 一、W1 的判定：ADDRESSED

頁面上已經沒有 `wiki_` 開頭的來源 key，01 原有的維基百科引文改註「只當線索，不作來源」，符合 3.3。新來源逐筆開頁比對結果：

| 來源 | 頁面狀態 | 比對結果 |
| --- | --- | --- |
| Synopsys：What is Lithography? | 打開，Claris Leung，2025-10-24 | 5 句全部原文都在：正型或負型光阻、layer by layer、電子束主要用在直接寫入尤其光罩、OPC 定義、SRAF 定義 |
| Synopsys：What is DRC? | 打開，Synopsys Editorial Staff，2021-01-04 | DRC 定義原文都在；表格「Minimum Spacing / Minimum distance between two wires or features.」也在 |
| Synopsys：What is LVS? | 打開，Manoz Palaparthi，2020-03-17 | 句子在；工具一次只能回傳前 120 字元，前 120 字元逐字相符，後半由工具轉述確認 |
| Synopsys：What is IC Design? | 打開，Synopsys Editorial Staff，2021-01-04 | 句子在；前半逐字相符，後半「verified against the results of “golden signoff” quality tools」由工具轉述確認 |
| Synopsys：What is Physical Design? | 打開，Frank Malloy，2025-10-16 | 流程清單 5 項的順序是架構、邏輯、實體設計、分析與驗證、tape-out，兩句引文都在 |
| UMC US6598218B2 | 打開，United Microelectronics Corp.，2003-07-22 核准 | 引文在 Background 的「Description of Related Art」，屬先前技術 |
| IBM US6127071A | 打開，International Business Machines Corp，2000-10-03 核准 | 引文在「Discussion of the Prior Art」，屬先前技術 |
| Applied Materials US11630385B2 | 打開，Applied Materials Inc，2023-04-18 | 「work by reflection」「molybdenum and silicon」在 Background；「20-60 of the reflective pairs」在 Detailed Description 的 FIG. 4 實施例，**不是**先前技術；全文沒有「典型 40 對」之類的說法（工具讀到前 100,000 字元） |
| Applied Materials US11366379B2 | 打開，Applied Materials, Inc.，2022-06-21 | Bragg 反射、覆蓋層在蝕刻時保護多層膜、TaN 系吸收層 3 句都在 Background |
| ASML US11977326B2 | 打開，ASML Netherlands BV，2024-05-07 | 保護膜防微粒、汙染造成缺陷、保護膜裝在框架上 3 句都在 Background |
| TSMC GIGAFAB 頁（F7） | 打開 | 「13 million 12-inch equivalent wafers」「0.13 micrometers to 2 nanometers」「six 12-inch GIGAFAB® facilities…」都在（原頁有 ® 符號，03 漏寫，不影響意思） |
| IEEE Spectrum 2013（F7） | 打開，Rachel Courtland，2013-10-28 | 節點名稱一句、Mark Bohr 一句都在 |

沒有打不開的頁面。頁面文字對照引文，除了 R5-1 和 R5-2，都沒有說得比引文強，例如：

- DRC「例如導線之間的最小間距」對應 Minimum Spacing 那一列。
- 「驗證之後才進到 tape-out」對應流程清單的順序。
- 吸收層「例如以氮化鉭（TaN）為主的材料」與圖內標籤「吸收層（例如鉭系）」，對應「For example, TaN-based…」。
- 保護膜的說法縮到 ASML 先前技術段講的範圍。
- 找不到來源的五個說法已經刪掉：晶圓廠修改光罩資料、轉角圓化很難補償、灰塵落在遠處、雷射寫入、40 到 50 層。

## 二、判定：別家公司的專利能不能當第 4 級「業界通用」的依據

**判定：看引的是專利的哪一段。**

- **先前技術段（Background、Description of Related Art、Prior Art）可以。** 這一段是申請人描述「現在業界一般怎麼做」，好拿來襯托自己的發明。它不是在講申請人自己的產品，而是在描述同類技術的一般做法，符合 3.1 第 4 級「不是這家公司寫的，但描述同類技術一般做法的……業界文件」。3.1 也說分級看的是「這句話在講誰」：先前技術段講的是業界通行做法，不是 UMC、IBM、AMAT、ASML 自己的量產。
- **發明本身（Summary、Detailed Description、實施例、請求項）不行。** 這些段落描述的是申請人提出的新做法，只能依 3.2 寫成「某公司申請過這種做法的專利」，不能撐「業界通用」，也不能證明有人已經量產。

用這條判準逐筆檢查，證據檔 01 第 9 節的 11 句專利引文裡，10 句出自先前技術段，用法合格。唯一例外是 AMAT US11630385B2 的「20-60 of the reflective pairs」，出自 FIG. 4 的實施例（原文還寫明「In a non-limiting embodiment」），這就是 R5-1。

建議（低，不擋發布）：頁面來源清單的專利標籤加註「先前技術段」，例如「UMC 專利 US6598218B2 先前技術段」。讓讀者知道引的不是發明本身，3.2 的提醒也就不用每處重寫。證據檔 01 第 9 節已經逐列寫了「先前技術段」，頁面上還沒有。

## 三、判定：「幾十層」撐不撐得住：撐不住

- 依據只有 AMAT 專利實施例的「20-60 對」。依第二節，實施例只能說「Applied Materials 申請過這種做法的專利」，不能當業界通用，而頁面的寫法是「幾十層交替的矽與鉬，把 EUV 光反射出去（業界通用）」。
- 數字本身也對不上：20 到 60 對是 40 到 120 層，60 對已經上百層，「幾十層」只涵蓋其中一部分。
- 同一份專利的先前技術段只說多層膜是「materials such as molybdenum and silicon」，沒有講層數。

可接受的寫法，擇一：

1. **「多層交替的矽與鉬，把 EUV 光反射出去（業界通用）。圖中只畫 10 層。」**（建議，改一個詞就好）
2. 要保留數字的話，寫成專利的口吻並拿掉業界通用：「Applied Materials 申請過的專利中，一個實施例是 20 到 60 對（40 到 120 層）。圖中只畫 10 層。」
3. 找一份在先前技術段、教科書或廠商技術頁明講典型層數的來源，記進 01 再寫數字。

## 四、CONFORMANCE 補回的三節：完整

`7c18ac7` 版第 151 行起的「方法檔的修正」「七、限制」「修方法項目的證據」共 29 行，與現行版第 183 行起逐行 diff，內容完全相同，只多了一列新證據：「3.6｜N2 的 6 筆維基百科來源換掉……」。三節沒有缺漏。

## 五、新發現

| 編號 | 嚴重度 | 步驟.拍 | 位置 | 問題與證據 | 建議修法 |
| --- | --- | --- | --- | --- | --- |
| R5-1 | 中 | 5.1–5.5 | `ml` 材料說明 | 「幾十層」的唯一依據是專利實施例，見第三節 | 改成「多層」 |
| R5-2 | 低 | 5.2 | `resist` 材料說明 | 說明開頭寫「感光材料」，引文是 Synopsys 講光學微影的 photoresist；5.2 畫的是電子束寫入，電子束用的阻劑是對電子束敏感，不是「感光」。正型、負型那一句可以當微影的一般原理，但「感光」兩字套在電子束上不準確 | 改成「阻劑（光阻）」或「塗在吸收層上的阻劑」，正型、負型那句前面加「微影用的光阻」 |
| R5-3 | 低 | 2–5 | 來源清單的專利標籤 | 見第二節建議 | 標籤加註「先前技術段」 |

## 六、回歸檢查

- 拓撲：全頁 exit 1，只剩步驟 2 三拍的刻意示範「過近」；2.1–2.3 exit 1，13.1、13.2、14.1–14.3 exit 0。全頁與 8 個單拍輸出都和 r4 逐字相同。
- 座標與圖說：52 拍逐拍比對 r4 傾印，元件、座標、顏色全部相同。差異只有：
  - 2.3 圖說改成「違反最小間距的規則」。
  - 4.2 圖說改成「轉角仍略圓（示意）」。
  - 5.1–5.5 左圖標籤由「吸收層（鉭系）」改成「吸收層（例如鉭系）」。

  這些都是第一節列的預期改動。
- 新標籤 bbox 為 x 262–370、y 128–146，在 viewBox 內，與上下標籤不重疊；5.2 亮色與暗色截圖確認看得清楚。

## 七、仍待處理

- 中：R5-1（5.1–5.5 的 `ml` 說明，「幾十層」改成「多層」）。
- 低：R5-2、R5-3。
- r1 的 F7 已由 03 的新增引文解決，原頁核對相符。
