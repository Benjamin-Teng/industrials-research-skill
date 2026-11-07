<!-- markdownlint-disable MD013 MD034 MD060 -->

# 第一幕（步驟 1–5）審查報告 r1

審查日期：2026-11-01。頁面：（本機路徑，未隨附）。
證據：`01-design-to-mask.md`、`05-suppliers.md`、三個維基頁（本次用 WebFetch 重新讀取）。
結論：**不可發布**（必修 7 項，皆為文字超出證據或圖文不符；沒有發現圖的結構性畫錯）。

## 一、怎麼查的

- 讀完 `STEPS`（步驟 1–5 全部欄位）、`PARTS`、`SRC`、`SUP`、`STEP_SUP`、第一幕場景程式（約 150 行）。
- 看 `act1-chromium` 的 a-1-1 到 a-5-4 全部亮色圖、a-dark-5-4、a-m-4-2，另用自己的腳本重畫 11 個第二幕畫面。
- 維基三頁以 WebFetch 逐句核對作者聲稱的原文（結果見第四節）。
- 01／05 的引文當作一手證據的代理，沒有重新抓 TSMC、NVIDIA、SPIE、Tom's Hardware 原頁（見第七節「沒查」）。

## 二、問題清單

編號依嚴重度與步驟排序。「必修」＝發布前一定要改。

### 必修

**P1　中　必修　Cadence 引文被讀成「台積電把 DRM 與 PDK 交給 Cadence」**
- 位置：`PARTS.kit` 最後一句；`STEPS[1].detail[1]`；`SRC.cadence2023` 的 label 無誤。
- 原因：01 第 36 行原文是「Cadence 的流程已通過台積電新 DRM 的認證（certified to support）」，「The companies also delivered N3E and N2 PDKs to facilitate … IC design innovation」。DRM 是「認證」不是「交付」；PDK 是 Cadence 與台積電「雙方」交付，目的是讓設計者使用，沒有說「台積電交給 Cadence」。01 第 29 行的摘要「已交付 Cadence」比原文強，頁面照抄。
- 建議：「Cadence 宣稱其設計流程已通過台積電 N2 設計規則手冊（DRM）的認證，並與台積電一起交付 N2 PDK（廠商聲明，2023 年 4 月）。」同步修 01 第 29 行。

**P2　中　必修　混合單元列（hybrid cell row）被寫成 N2 的新要求**
- 位置：`STEPS[2].detail[1]`「N2 對設計工具提出新要求，例如 Cadence 提到的混合單元列最佳化與單元接腳對齊」。
- 原因：01 第 75 行原文是「native hybrid cell row optimization from synthesis to signoff ECO for optimal PPA **at N3E**, cell pin alignment and connection support」，混合單元列綁在 N3E，不是 N2。01 第 71 行把它列為「N2 特有」是研究者的歸納，不是引文。
- 建議：改成「Cadence 2023 年的新聞稿列出新版流程支援的設計特徵，包括混合單元列最佳化（原文綁 N3E）與單元接腳對齊」，不要寫成 N2 要求；或刪掉混合單元列只留接腳對齊，並標「待查證是否 N2 專屬」。

**P3　中　必修　「通過台積電認證才能用」太絕對**
- 位置：1.2 左圖 EDA 方框「通過台積電認證才能用」、1.2 caption a「EDA 軟體要先通過台積電認證才能用」、`PARTS.eda`「每個新製程都要先通過台積電認證」。
- 原因：01 第 27 行只說「Certified 才算可用」，官方表另有 Work in Progress；01 第 6、193 行還註明台積電官網認證頁（as of 10/01/2026）已不再單列 N2，N2 認證只有 EDA 廠 2023–24 年自家稿件。頁面兩處都沒揭露這點。
- 建議：圖內改「通過台積電認證才算可用於該製程」；detail 補一句「台積電官網現行認證表已不單列 N2，N2 的認證紀錄來自 EDA 廠聲明」。

**P4　中　必修　4.3 右圖的面板標題與內容不符**
- 位置：4.3 右圖。標題「②　印到晶圓上的結果」，內容是「運算量非常大…3,000 萬 CPU 小時」的文字卡（`a-4-3.png`）。
- 原因：`STEPS[4].pb` 整步共用同一個標題，4.3 的右圖已不是晶圓結果。讀者會找不到「結果」。
- 建議：改成每拍可覆寫的標題（4.3 用「②　運算量」），或在 4.3 右圖仍畫曲線光罩的預期印出結果、把運算量移到下方 caption。

**P5　中　必修　OPC 後的印出結果畫成完美直角，與維基原文相反**
- 位置：4.2 右圖（`a-4-2.png`）。OPC 後的綠色圖形是矩形與銳角 L，連 L 的凹角、外角都是尖的。
- 原因：維基 OPC 原文「Other distortions such as rounded corners are driven by the resolution of the optical imaging tool and **are harder to compensate for**」。頁面自己引用的這頁說轉角圓化較難補償；畫面卻顯示轉角被補到完全方正，並暗示 OPC 能消除圓角。4.1 的左下外角也沒有對應的凹角填角（凹角在 4.1 是尖的，真實會被填圓）。
- 建議：4.2 右圖保留輕微圓角（半徑縮小但不為零），caption 改「印出來的形狀接近設計；轉角仍會有些圓」。

**P6　中　必修　「最後貼上保護膜才上線使用」過度一般化**
- 位置：`STEPS[5].plain` 末句；5.4 now「貼上保護膜（pellicle），光罩完成」；5.4 左右圖整套。
- 原因：01 沒有「N2 的 EUV 光罩一律貼 pellicle」的證據；證據只有台積電例行檢查項目含「pellicle frames」（官方）、自製 EUV pellicle 的媒體轉述（Tom's，2024 中）、論文做 pellicle 檢測。頁面引用的維基 EUV 頁自己寫 pellicle 可行性「severely challenged」、台積電 2019 年起「limited use」，並稱後續報導找不到使用者（維基的 pellicle 段可能過時，但不能支持「一律貼」）。
- 建議：plain 與 5.4 改為「通常會貼上保護膜（台積電有自製 EUV 保護膜；哪些層、N2 是否全部使用未公開）」。

**P7　中　必修　4.3 右圖「台積電 2024 年起導入 NVIDIA cuLitho」沒有標廠商聲明**
- 位置：4.3 右圖文字卡第二段。上一段有標「（NVIDIA 說法）」，這一段沒有。
- 原因：來源是 NVIDIA 2024-03-18 新聞稿，台積電 CEO 引言為「We are moving NVIDIA cuLitho into production at TSMC」（01 第 121 行，廠商聲明）。頁面 `detail[2]` 有標「廠商聲明」，但圖上的句子是裸斷言。另 05 第 63 行對這句引言的出處與 01 不同（05 說 2024 引言見 eenews，01 說在 NVIDIA 2024 稿），兩份證據檔需對齊。
- 建議：圖上補「（NVIDIA 新聞稿，台積電執行長引言）」；detail 的「證實」改「在稿中表示」。

### 建議修

**P8　中　保護層與保護膜兩個名稱同圖出現**
- 位置：5.1–5.4 左圖。「保護層」（capping layer，釕）與「保護膜」（pellicle）同一張圖，字只差一個。
- 原因：兩者位置、功能完全不同，一般投資人會混；維基 EUV 頁的 capping layer 材質為 ruthenium，頁面沒說。
- 建議：capping layer 改「覆蓋層（釕）」，或 pellicle 改「防塵薄膜」。`PARTS.cap`、`PARTS.pellicle`、圖內標籤、`STEPS[5]` 文字同步改。

**P9　中　CyberShuttle 圖把「一套光罩」畫成單一片光罩**
- 位置：3.1–3.2 右圖、`PARTS.design`「一套光罩只放一個晶片設計」、`PARTS.shuttle`。
- 原因：「一套光罩（mask set）」是每一層一片、共數十片的集合（台積電原文為 "multi-project mask set"）；圖只畫一片 9 宮格板子，會讓讀者以為一套光罩就是一片。
- 建議：標題改「一片光罩上放幾個設計」，或加註「每一層各有一片，圖只畫其中一片」。

**P10　中　5.4 俯視圖的保護膜框架超出光罩板外**
- 位置：5.4 右圖（`a-5-4.png`）。框架外緣（x72–328）比光罩板（x80–320）寬 8 單位，紅框向外突出一圈。左圖框架則在板內（x20–250 與基板同寬），兩圖不一致。
- 原因：真實框架黏在光罩板上、在圖形區之外，不會超出板邊（維基：glued over one side of the photomask）。
- 建議：把 B 圖框架縮到板內，框架位置與 A 圖一致。

**P11　低　5.2 電子束箭頭指向「要被移除」的位置**
- 位置：5.2 左圖虛線箭頭在 x=65、135、205，是保留的吸收層之間的縫（保留段 20–50、80–120、150–190、220–250）。
- 原因：對應正型光阻（被曝到的地方被蝕掉），合理，但caption 只說「圖形寫上去」，讀者會預期箭頭落在留下的圖形上。
- 建議：caption 加「（光阻被電子束照到的地方，吸收層會被蝕掉）」或把箭頭畫在保留段上並註明光阻種類。

**P12　低　左圖截面與右圖俯視的圖形不對應**
- 位置：5.2–5.3。左圖吸收層切成 4 段，右圖是 10 條橫線（沿 x 方向連續），若左圖沿 x 切則不會有 4 段。
- 建議：右圖改直線或在 caption 說「兩圖是示意，不是同一處的切面」。

**P13　低　暗色模式下 5.2 之後的俯視圖吸收圖形幾乎看不見**
- 位置：`a-dark-5-4.png` 右圖。吸收層色 `--m-mask`（#8b96a3）與基板 `--m-sti`（#8d9ea0）幾乎同亮度，橫線隱約可辨。
- 建議：暗色下吸收層改較深或加描邊。

**P14　低　2.x 右圖的橫線與直線疊在同一層，等於短路**
- 位置：2.1–2.3 右圖。水平與垂直導線都畫在同一平面且互相接觸（如灰線與橘線在 917 附近重疊），`PARTS.wire` 雖說「圖中只畫一層」，但同層交疊的畫法在行家眼中是短路。
- 建議：橫線與直線用兩種色，並註明「橫向、縱向實際在不同金屬層」。

**P15　低　3.1 的四層平行四邊形借用第二幕的材料色**
- 位置：3.1–3.2 左圖。藍、黃、紫、綠與第二幕的矽、矽鍺、高介電層、源汲極同色，讀者可能把「版圖每一層」當成「材料層」。
- 建議：改用中性色階，或 caption 加「顏色只用來區分，不是材料」。

**P16　低　「2031 年建立」應為「2031 年前」**
- 位置：`PARTS.mask-sub`、`STEPS[5].detail[3]`。
- 原因：01 第 172 行原文 "by 2031"。
- 建議：「目標在 2031 年前建立 12 吋光罩試產線」。

**P17　低　「過去要實際印到晶圓上評估」與原文時態不同**
- 位置：`STEPS[5].detail[1]`。
- 原因：論文原文是 "Currently, every potential defect must be judged by wafer printing assessment for almost 3 days"（2023 年，且是 SPIE 摘要經 Semantic Scholar 取得，01 第 201 行註明全文頁取不到）。「過去」暗示已被取代；論文只是提出新系統。
- 建議：「在這套系統之前，缺陷要靠晶圓印製評估，一個缺陷近 3 天」，並註明依論文摘要。

**P18　低　OPC 通用機制未標明台積電沒有點名 N2**
- 位置：`STEPS[4].plain`、`detail[0]`。
- 原因：01 第 114 行「TSMC 公開說法未點名 N2」，頁面只在「曲線光罩」那一句標明。其餘 OPC 內容放在 N2 頁面裡，讀者會當成 N2 的做法。
- 建議：detail 第 1 點末加「台積電公開資料沒有逐一點名 N2」。

**P19　低　「孤立線條旁邊」的限定詞維基沒有**
- 位置：`PARTS.sraf`。維基原文只說 "placed adjacent to resolvable lines"，WebFetch 回覆「never explicitly states near isolated lines」。
- 建議：刪「孤立」，或標為業界通用說法。圖中 SRAF 只畫在最左線條外側，與「孤立線旁」的說法一致，但畫面沒有解釋。

**P20　低　`kit` 的 DRM、PDK 定義沒有來源**
- 位置：`PARTS.kit`、1.1 左圖「規定版圖可以怎麼畫」「給設計軟體用的製程資料」。
- 原因：01 沒有 DRM 與 PDK 的定義引文，頁面也沒標「業界通用」。定義本身通行，不構成錯誤。
- 建議：補一個通用來源，或在 PARTS 註「通用定義」。

**P21　低　供應商 ●／○ 圖例對同一家公司前後不一致**
- 位置：步驟 1–3 的 Synopsys 是 ○，步驟 4 的 Synopsys 是 ●（`SUP.eda`、`SUP.opcsw`）。
- 原因：與 05 一致（EDA 聯盟成員 vs 導入 cuLitho 報導），但讀者看不出為什麼同一家公司兩種符號。
- 建議：圖例加一句「同一家公司在不同類別的證據不同，符號可能不同」。

**P22　低　步驟 3（tape-out）顯示 EDA 廠商名單**
- 位置：`STEP_SUP[3]=['eda']`。05 的「設計工具與 IP」只對應步驟 1；步驟 3 的 tape-out 與光罩服務沒有對應的廠商名單。
- 建議：步驟 3 改不顯示供應商，或用 05 步驟 3 的光罩寫入機等（但那屬步驟 5）。

**P23　低　IMS 的 ● 證據是合作與投資，非採購**
- 位置：`SUP.mask` 的 IMS Nanofabrication。05 第 80 行自己註明「未直言採購量」，01 第 141 行：「採用現況查無」。
- 圖例已寫「供貨…或與台積電合作」，不算錯，但讀者看到 ● 會當成「供貨」。
- 建議：圖例把「供貨」與「合作／投資」分開，或 IMS 單獨加註。

**P24　低　一般投資人可讀性**
- 步驟 2 detail 一行塞進 APR、STA、EMIR、dummy fill、寄生參數萃取，沒有任何解釋；電遷移與壓降也沒說明。
- 「3,000 萬 CPU 小時」沒有換算，讀者無法感受大小（約 3,400 年單核）。
- 「梯次」、「sign-off」、「GDS」第一次出現只有一句話。
- 頁首 notice「依學術論文與公開資料中的業界通用做法繪製」，第一幕主要依維基、EDA 廠稿與台積電官網，沒有以學術論文為主。
- `lede`「一顆奈米片電晶體怎麼做出來」，第一幕講的是設計與光罩，不是電晶體。
- 建議：把專有縮寫收進 `PARTS` 圖例，CPU 小時加一句比喻，notice 改成「依台積電公開資料、廠商聲明與公開文獻」。

**P25　低　`ml`「40 到 50 層」可能是「對」不是「層」**
- 位置：`PARTS.ml`、5.1 文字「幾十層」。維基原文 "40–50 alternating silicon and molybdenum layers"，頁面忠實，但業界文獻常稱 40 對（80 層）。WebFetch 未取得維基此段更多脈絡。列「待確認」。

## 三、第二幕回歸

- 用 `before_act1.html`（第一幕加入前）與現行頁各畫 11 個第二幕畫面（6.1、7.1、8.1–8.3、9.1、10.1、11.1、12.1–12.3）。
- 面板標題（paText／pbText）、步驟標題逐一相同，無 console 錯誤。
- 11 張圖中 7 張位元組相同；8.2、8.3、12.2、12.3 位元組不同，目視 8.3、12.3 前後無差別（差異來自動畫時序或 hover 亮度，非內容）。8.2、12.2 沒有逐張目視。
- 程式差異只有：`TAG` 加 `vendor`、`PART_ORDER` 與 swatch 擴充、`STEP_SUP` 加第一幕、`s.sup` 對第二幕仍加 `inspect`、面板標題改成可覆寫並保留第二幕預設值。
- **有一處影響第二幕的文字變動**：供應商圖例由「台積電的供應商獎或官方名單列有這家公司」改為「有公開資料顯示供貨給台積電**或與台積電合作**（供應商獎、官方名單、雙方新聞稿）」。第二幕所有 ● 的證據仍然是供應商獎／官方名單，圖例變寬後定義變鬆（低）。建議第一幕與第二幕用不同圖例，或只對 IMS／NuFlare 單獨加註。

## 四、維基原文核對

| 作者聲稱 | 核對 | 備註 |
|---|---|---|
| OPC：rounded corners driven by resolution | 符 | 原文接 "harder to compensate for"，見 P5 |
| line end shortening | 符 | 原文 "line end shortening (e.g., gate overlap on field oxide)" |
| moving edges or adding extra polygons | 符 | |
| dog-ear (serif or hammerhead) at the line end | 符 | 原文說「在設計的線端產生」，沒有說光罩上的位置；頁面把 serif 說成「轉角」、hammerhead 說成「線端加寬」，屬業界慣用，非原文 |
| scattering bars | 符 | |
| assist in their printing, while not being printed | 符 | 這是 SRAF 的定義句 |
| EUV masks work by reflecting light | 符 | |
| alternating Mo/Si layers | 符 | |
| 40–50 layers | 符 | 見 P25 |
| tantalum-based absorbing layer over the capping layer | 符 | 原文另寫 capping layer 為釕 |
| photomask：electron beam lithography and laser-driven mask writer | 符 | 原文是「取代原本的圖形產生器」，並非 EUV 專用；EUV 光罩用電子束，頁面「（或雷射）」置於 EUV 光罩步驟，略誤導（低） |
| pellicle：thin transparent film stretched over a frame glued over one side | 符 | |
| 「particles on it are far enough away」 | 近似 | 原文主詞是 pellicle 離圖形夠遠，微粒因失焦不會印出；頁面省略「失焦」機制 |

## 五、數字核對

| 數字 | 頁面 | 證據 | 結果 |
|---|---|---|---|
| 3,000 萬 CPU 小時 | 4.3、detail | 01 第 122 行 "30 million or more hours"（"a typical mask set"） | 符，標了 NVIDIA 說法 |
| 80 個位置 | 5 detail | 01 第 158 行 "more than 80 sites/hr" | 符；原文是 review 平台的產能 |
| 3 天 | 5 detail | 01 第 156 行 | 符，時態見 P17 |
| 4 倍／80 倍 | 5 detail | 01 第 161 行 "four times longer lifespan"、"80x reduction in defects" | 符，已標媒體轉述 |
| 0.5 微米到 A14 | 3 | 01 第 101 行 | 符 |
| 每月 10 個梯次 | 3 | "up to 10 shuttles per month" | 符，「最多」已寫 |
| 40–50 層 | PARTS.ml | 維基 | 符，見 P25 |
| 6 吋 | PARTS、5 | 01 第 171 行 | 符 |
| 2031 年 | PARTS、5 | "by 2031" | 見 P16 |
| 2023 年 4 月 | 1 | Cadence 2023-04-27 轉載 | 符，見 P1 |
| 2023 年 9 月 | 2 | Siemens 09-27、Synopsys 09-25 | 符 |
| N5、N3 | 5 | 論文 | 符；頁面另註「論文沒有點名 N2」 |
| NanoFlex Pro 2025 | 1 | pr3228 2025-04-23 | 符 |

## 六、來源類型標示

- 各步驟 `badges` 與 `sources` 的 `t` 逐筆比對：台積電官網與新聞稿標台積電官方；Cadence、Siemens、Synopsys、NVIDIA 標廠商聲明；SPIE 兩篇標論文；Tom's 標媒體轉述；維基標業界通用。**沒有把廠商聲明寫成台積電官方說法**。
- `pr3338` 標台積電官方，實為台積電與 ASML 聯合稿，建議 label 已寫「聯合」，保留。
- 灰色地帶：(a) 維基標「業界通用」是自訂標籤，維基是三級來源，不是業界標準；(b) 兩篇 SPIE 論文是台積電作者自述，與「台積電官方」邊界模糊，頁面標論文是對的；(c) 論文只讀到摘要（01 第 201 行），頁面沒有揭露。
- 超出標籤的句子（P1、P2、P7）是本節唯一的實質問題，成因是文字比引文強，而非標籤錯。
- 第二幕 `SRC.pmc*`（論文）標 `generic`，不在本次範圍，僅供參考。

## 七、供應商核對

- 名單：`SUP.eda`（6 家全 ○）、`opcsw`（Synopsys ●、NVIDIA ●、ASML ○）、`mask`（NuFlare ●、IMS ●、Lasertec ●、HOYA ○、三井化學 ○、家登 ○）與 05 步驟 1／2／3 的層級逐家一致；備選名單（Alchip、AGC）正確未入表；股票代號 3443、3529、3680 與 05 相同。
- ● 圖例已寫「供貨給台積電或與台積電合作」，且註明沒有任何一家明確供應 N2，與 05 第 14 行相符。
- 問題見 P21、P22、P23。
- 05 內部有一處與 01 不一致（不影響頁面）：05 第 46 行稱 Cadence 與 Siemens 的 N2 認證只有二手報導、待查原始新聞稿，01 已有 Siemens 官方稿。

## 八、待確認

1. 維基 EUV 頁的 40–50 層指層還是對（P25）。
2. Cadence 2023-04 稿的 "delivered … PDKs" 的交付對象，需取得原稿（CIMdata 轉載頁）全文判斷（P1）。
3. 「混合單元列」是否 N2 才有（P2）。
4. 台積電 N2 EUV 光罩是否一律使用 pellicle（P6）。
5. EUV 光罩 6 吋是否包含 N2 全部層（尚有 DUV 光罩，頁面沒有交代 N2 同時用傳統透光光罩；01 第 174 行 EUV 層數查無）。

## 九、沒查

- TSMC 官網 mask_services、cybershuttle、OIP、NVIDIA 新聞稿、SPIE 摘要、Tom's Hardware 原頁：未重新抓取，依 01 的逐字引文核對。
- 維基 EUV 頁最後約 24,000 字元、photomask 頁 pellicle 與寫入順序段落：未讀到。
- WebKit 版畫面：只掃過一張（且該張是被裁切的比例），未逐張檢視；手機版只看 a-m-4-2。
- 全螢幕（immersive）模式、鍵盤操作、aria 標籤與螢幕閱讀器。
- 第二幕：只做 11 張畫面的位元組比對與 8.3、12.3 目視；8.2、12.2 與第二幕文字內容未重審。
- 第一幕各拍的 caption 文字長度是否截斷（只看到 4.2 手機版沒有截斷）。

## 十、已檢查且無問題

- 圖的結構：EUV 光罩剖面由下而上為基板→鉬／矽多層膜→覆蓋層→吸收層，與維基順序一致；pellicle 在圖形面之上、框架撐起、與圖形有距離；寫入→蝕刻→檢測修補→貼 pellicle 的順序與業界流程相符（省略光阻已標註）。
- OPC：hammerhead 在線端外緣加寬、serif 在凸角外緣補小方塊、SRAF 細線離主線一段距離且在 4.2 右圖不印出，位置與畫法正確。
- NanoFlex 圖：矮單元列與高單元列同區塊混排，標註「示意」，與 TSMC 原文一致。
- 第一幕 1.2、2.x 右圖偶有一格淺藍色，是 hover 亮度（`svg .el.on:hover` 的 `brightness(1.12)`）造成的截圖假象，不是程式錯誤。
