<!-- markdownlint-disable MD013 MD034 MD060 -->

# 05 各製程步驟的主要廠商名單

查證日期：2026-11-01

## 閱讀方式

層級只有兩種，不混用：

- **台積電供應商（有公開證據）**：來源明說它供貨給台積電（台積電公開資料、廠商公告、可信媒體明確報導）。
- **該類主要廠商**：來源只證明它是該類設備或材料的主要廠商，或是台積電官方列出的生態系夥伴，沒有證據顯示它供貨給台積電。

本檔沒有任何一家被寫成「供應 N2」。所有來源都沒有逐廠明說 N2 供貨；N2 字樣只出現在兩處，且都不是供貨聲明：步驟 1 的 Synopsys 設計流程認證，與步驟 2 的運算微影報導標題。

### 常用來源縮寫（完整 URL 仍逐列寫出）

- 台積電 2025 供應商獎：`https://pr.tsmc.com/english/news/3274`
- 台積電 2024 供應商獎：`https://pr.tsmc.com/english/news/3192`
- 台積電 2023 供應商獎：`https://pr.tsmc.com/english/news/3086`
- 台積電 2022 供應商獎：`https://pr.tsmc.com/english/news/2995`
- 台積電 2014 供應商獎：`https://pr.tsmc.com/english/news/1836`
- 台積電 2025 台灣持續改善獎（TCIA，列出台積電在地原物料供應商）：`https://www.tsmc.com/english/event/CSD_37`
- 台積電 3DFabric 聯盟頁（EDA、IP、記憶體、OSAT、載板、測試夥伴）：`https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance`

### 台股代號驗證方式

代號以 FinMind `TaiwanStockInfo`（資料日 2026-11-01，來源為證交所與櫃買中心上市櫃清單）逐檔查詢；各表代號皆已查到對應中文簡稱與市場別。英文名與中文名的對應，除另註「待查證」外，皆經台積電中文版新聞稿或公司資料比對。

---

## 步驟 1　設計工具與 IP

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Synopsys | EDA、IP | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/eda_alliance | TSMC EDA 聯盟成員 |
| Cadence Design Systems | EDA、IP | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/eda_alliance | TSMC EDA 聯盟成員 |
| Siemens EDA | EDA（實體驗證 Calibre） | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/eda_alliance | TSMC EDA 聯盟成員 |
| Arm | CPU IP | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance | 3DFabric 聯盟頁的 IP 夥伴 |
| 創意 Global Unichip（GUC，3443） | ASIC 設計服務、IP | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/value-chain-alliance/guc | TSMC 官方 VCA 成員 |
| 力旺 eMemory（3529） | 嵌入式非揮發記憶體 IP | 該類主要廠商 | https://us.design-reuse.com/news/52958/ememory-2022-tsmc-oip-partner-of-the-year-award-for-embedded-memory-ip.html | 2022 TSMC OIP 年度夥伴獎 |

備註：

- 「聯盟成員」是台積電官方列為生態系夥伴，不等於供貨給台積電，故全數歸「該類主要廠商」。
- Synopsys 的 N2 設計流程認證見 `https://www.design-reuse.com/news/53899/synopsys-tsmc-n2-process.html`（轉載新聞稿，2023-09）。Cadence 與 Siemens EDA 的 N2 認證細節只有二手報導（`https://allaboutcircuits.com/news/tsmc-certifies-host-top-eda-tools-new-process-nodes`），待查證原始新聞稿。
- 力旺：查得 N3P 認證（2025-06），N2 授權查無。
- 備選：世芯-KY Alchip（3661），同為 TSMC VCA 成員，來源 `https://www.tsmc.com/dedicatedFoundry/oip/value-chain-aggregator`，層級同為「該類主要廠商」。
- GUC 與台積電的持股關係（約 35% 最大股東）只有二手資料，未入表；證據偏弱。

## 步驟 2　光罩資料準備（OPC／運算微影）

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Synopsys | OPC 軟體（Proteus） | 台積電供應商（有公開證據） | https://www.eenewseurope.com/en/tmsc-taps-synopsys-for-2nm-computational-lithography/ | 2024-03，台積電與 Synopsys 導入 cuLitho |
| Nvidia | GPU 加速運算微影（cuLitho） | 台積電供應商（有公開證據） | https://nvidianews.nvidia.com/news/nvidia-asml-tsmc-and-synopsys-set-foundation-for-next-generation-chip-manufacturing | 2023-03 稿，台積電導入 cuLitho |
| ASML | 運算微影軟體（Brion 系列） | 該類主要廠商 | https://nvidianews.nvidia.com/news/nvidia-asml-tsmc-and-synopsys-set-foundation-for-next-generation-chip-manufacturing | 稿中只說 ASML 計畫為運算微影軟體加 GPU 支援 |

備註：

- 台灣廠商：查無。已搜關鍵字：「OPC 運算微影 台積電 台灣廠商」「cuLitho 台灣 伺服器」；結果只有台積電自家導入，沒有第三方台灣供應商。
- eenews 標題寫「2nm computational lithography」，是本檔唯一在標題層級提到 2 奈米的來源；內文為 TSMC 與 Synopsys 將 cuLitho 整合進軟體與流程，未逐項聲明 N2 量產用途。
- Nvidia 稿中 TSMC 執行長引言屬 2023 年版；2024 年「moving cuLitho into production」的引言見上列 eenews。
- ASML 作為曝光機供應商是台積電供應商（見步驟 6），但運算微影軟體對台積電的供貨查無明說來源，故此列為「該類主要廠商」。

## 步驟 3　光罩製作

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| HOYA | 空白光罩（EUV mask blank） | 該類主要廠商 | https://semiengineering.com/euv-mask-blank-biz-heats-up | 與 AGC 並列主要供應商 |
| NuFlare Technology | 光罩寫入機 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 獎項類別 Distinguished Mask Writer Collaboration |
| IMS Nanofabrication | 多電子束光罩寫入機 | 台積電供應商（有公開證據） | https://www.tomshardware.com/news/intel-sells-minority-stake-in-ims-nano-to-tsmc | 台積電自 2012 起合作並於 2023 買入 10% |
| Lasertec | EUV 光罩檢測 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3086 | 2023 獎項類別 Distinguished EUV Mask Inspection and Metrology Collaboration |
| Mitsui Chemicals 三井化學 | EUV pellicle | 該類主要廠商 | https://ap.mitsuichemicals.com/release/2021/2021_0526.htm | ASML 授權，2021 起量產 |
| 家登 Gudeng（3680） | EUV 光罩盒（pod） | 該類主要廠商 | https://uanalyze.com.tw/articles/407009553 | High-NA EUV Pod 通過 ASML 認證 |

備註：

- 備選：AGC（空白光罩，該類主要廠商，來源同 HOYA 列 `https://semiengineering.com/euv-mask-blank-biz-heats-up`）。Lasertec 的廠商側公告見 `https://www.lasertec.co.jp/en/news/2023/20231227_3852.html`。
- IMS：來源說「台積電與 IMS 自 2012 年起合作開發多電子束寫入機並買入 10% 股權」，屬合作與投資關係，未直言採購量；歸供應商層級的依據是長期共同開發。
- 家登：媒體只寫「台積電等晶圓大廠擴產帶動需求」，沒有一則明說台積電為其 EUV 光罩盒客戶，故歸「該類主要廠商」；台積電是否直接採購查無。
- 台灣光罩（2338）：客戶含台積電的說法只有財經媒體摘述，且主力為成熟製程，未入表。
- 光罩盒 Entegris、EUV pellicle 的 FST 等：查無可引用的一手來源，未入表。
- 空白光罩的市占數字各來源差異大，本檔不引用任何市占數字。

## 步驟 4　矽晶圓（300mm）

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| SUMCO | 300mm 矽晶圓 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022 至 2025 連年得獎 |
| Shin-Etsu Handotai 信越半導體 | 300mm 矽晶圓 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022、2025 得獎 |
| 環球晶 GlobalWafers（6488） | 矽晶圓 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | 2025 TCIA 金獎（第二層級） |
| 台勝科 Formosa Sumco（3532） | 矽晶圓 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 名單列有 FORMOSA SUMCO |
| 合晶 Wafer Works（6182） | 矽晶圓、磊晶片 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 名單列有 Wafer Works Corporation |

備註：

- 合晶：英文名 Wafer Works Corporation 與 6182 的對應來自公司登記資料，TCIA 頁面未附中文名；屬「待查證」。
- TCIA 是台積電對在地原物料供應商的持續改善獎項，名單僅證明有交易往來，沒有逐廠說明供貨品項與製程節點。
- 備選：Siltronic、SK siltron，僅有市場研究摘要（`https://faxiangongchang.com/en/reports/china-semiconductor-silicon-wafer-2026`）指為前五大，證據偏弱，層級「該類主要廠商」，未入表。
- 全球前五大組成（信越、SUMCO、環球晶、Siltronic、SK siltron）各來源一致，市占百分比不一致，本檔不引用。

## 步驟 5　磊晶與薄膜沉積

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| ASM International | 磊晶、ALD | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2022 至 2024 連年得獎 |
| Applied Materials | 磊晶、PVD、CVD | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/1836 | 2014 獎項明載 EPI/PVD 設備；2022 至 2025 續獲獎 |
| KOKUSAI ELECTRIC | 批次式 CVD、ALD | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022、2025 得獎；產品別見備註 |
| Lam Research | 沉積設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022 至 2025 連年得獎 |
| Tokyo Electron 東京威力科創 | 成膜設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2022 至 2024 得獎，2025 名單未列 |

備註：

- 台積電獎項稿多不載明設備品項。KOKUSAI 的批次式 CVD／ALD 產品別依 SEMI 會員目錄（`https://www.semi.org/en/resources/member-directory/kokusai-electric-corporation`）；Lam、TEL 的具體沉積機型本檔未逐一查證，故類別只寫通稱。
- ASM 的 GAA 磊晶與 ALD 機會見其 CTO 訪談 `https://asm.com/downloads/232221-annual-interim-reports/cto-interview`。
- 台灣廠商：查無。已搜關鍵字：「漢民科技 3402 代理 ASM Kokusai」「台灣 磊晶 設備 台積電」；漢民科技與台積電的設備代理關係沒有查到來源。

## 步驟 6　微影

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| ASML | EUV、DUV 曝光機 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022 至 2025 連年得獎 |
| Canon | 曝光機 | 台積電供應商（有公開證據） | https://global.canon/en/news/2025/20251224.html | 2025 獎項，稿中未載機型 |
| Tokyo Electron 東京威力科創 | 塗佈顯影（CLEAN TRACK） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 產品線見 TEL 官網 |
| JSR | 光阻 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/2995 | 2022 獲 Litho Materials 獎；2025 續獲獎 |
| 東京應化 TOK | 光阻 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 獎項類別 Novel Technology Collaboration |
| 新應材 eChem Solutions（4749） | 微影材料 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/2995 | 2022 獲 Litho Materials 獎 |

備註：

- 備選：Nikon（ArF 浸潤式掃描機，該類主要廠商，`https://www.nikon.com/company/news/2023/0508_nsr-s625e_01/`，查無對台積電供貨來源）。Shin-Etsu Chemical（光阻等微影材料，台積電供應商，`https://pr.tsmc.com/english/news/3086`）。SCREEN Semiconductor Solutions（2024、2025 獲獎 `https://pr.tsmc.com/english/news/3192`，獎項稿未載設備品項，是否供應塗佈顯影查無來源）。
- TEL 塗佈顯影品項：TEL 官網稱其在 EUV 用塗佈顯影幾近 100% 市占，屬廠商自述，見 `https://www.tel.com/blog/all/20260428_001.html`。
- 新應材：英文名 eChem Solutions Corp（現稱 Advanced Echem Materials）對 4749 的對應見公司資料；獎項類別為微影材料，但其產品多為顯示器與一般半導體光阻、溶劑，與先進製程 EUV 光阻的關聯查無，證據偏弱。
- ASML 為 EUV 唯一供應商，但本檔不以此為單獨來源，僅引台積電獎項稿。

## 步驟 7　蝕刻（含 nanosheet 通道釋放選擇性蝕刻）

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Lam Research | 乾蝕刻；選擇性蝕刻（Argos、Prevos、Selis） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 選擇性蝕刻產品見 Lam 2022 新聞稿 |
| Tokyo Electron 東京威力科創 | 乾蝕刻 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | TEL 自述乾蝕刻市占居第二 |
| Applied Materials | 選擇性蝕刻（Producer Selectra） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | Selectra 官方產品頁見備註 |
| Hitachi High-Tech | 蝕刻設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/1836 | 證據為 2014 年獎項，過舊 |
| 崇越科技 Topco Scientific（5434） | 蝕刻、擴散用石英零組件 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 得獎者為崇越石英（崇越與信越石英合資） |

備註：

- Lam 選擇性蝕刻：`https://newsroom.lamresearch.com/2022-02-09-Lam-Research-Introduces-Groundbreaking-Suite-of-Selective-Etch-Tools-to-Accelerate-Chipmakers-3D-Roadmaps`，稿中將該產品組合定位於 GAA 電晶體結構。
- Applied Selectra：`https://www.appliedmaterials.com/us/en/product-library/producer-selectra-etch.html`，頁面描述選擇性移除 SiGe 同時保留矽。Applied 官網部分頁面（blog）回 403，未繞過。
- 台積電獎項稿只列公司名，沒有逐廠說明用於哪個節點或哪個蝕刻步驟；Lam、TEL、Applied 是否用於 N2 nanosheet 釋放蝕刻，查無明說來源。
- 崇越科技 5434 為母公司代號，得獎主體是崇越石英製造廠；「新廠產能全數供台積電」的說法見 `https://apps.digitimes.com/news/a20240418PD215.html`，原文待查證，本檔不引為事實。石英零組件用於擴散、蝕刻、薄膜部門，是消耗零件，不是蝕刻機本體。
- Hitachi High-Tech 為舊證據，若前端頁面要求「近年」，建議不使用該列。

## 步驟 8　金屬閘極與導線（PVD、電鍍、CMP）

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Applied Materials | PVD、CMP 設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/1836 | 2014 獎項明載 EPI/PVD 設備 |
| Lam Research | 電鍍（ECD）設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 獎項稿未載品項，ECD 為廠商產品線，待查證 |
| EBARA 荏原 | CMP 設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/1836 | 2014 獎項明載 CMP equipment；2025 續獲獎 |
| DuPont | CMP 研磨墊、研磨液 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 2025 銀獎；產品見 DuPont 官網 |
| 中砂 Kinik（1560） | CMP 鑽石碟（研磨墊修整器） | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 2025 銅獎，名單列 KINIK COMPANY |
| 光洋科 Solar Applied Materials（1785） | 濺鍍靶材 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 名單列 Solar Applied Materials Technology Corp |

備註：

- DuPont 產品：`https://www.dupont.com/electronic-materials/cmp-pads.html`。
- 中砂產品與先進製程市占：「台積電 2 奈米鑽石碟市占 80% 以上」之類說法只有券商與媒體引述，未經公司正式揭露（`https://uanalyze.com.tw/articles/5723255790`），本檔不採計。
- 光洋科：英文名與中文名對應依公司資料（台南、濺鍍靶材製造），屬待查證；TCIA 頁面只證明往來，未載品項。
- 備選：Fujifilm（CMP 研磨液，2014 獎項明載 CMP slurry，`https://pr.tsmc.com/english/news/1836`；另有 Arizona 廠擬供應台積電與英特爾的報導 `https://technews.tw/?p=1628975`）。頌勝科技 IV Technologies（7768，CMP 研磨墊，TCIA 名單列 IV Technologies Co., Ltd.，`https://www.tsmc.com/english/event/CSD_37`；英文名與 7768 對應見 `https://blog.fugle.tw/post/earnings-call-7768-2026-04-08`，待查證）。ULVAC（PVD，2023、2025 獲獎 `https://pr.tsmc.com/english/news/3274`，品項待查證）。JX Advanced Metals（金屬靶材，2024 獲獎 `https://pr.tsmc.com/english/news/3192`）。Resonac（2025 獲獎 `https://pr.tsmc.com/english/news/3274`，品項待查證）。
- 台灣廠商以 CMP 耗材（中砂、頌勝）與靶材（光洋科）為主，證據來自 TCIA，品項與節點需再查。

## 步驟 9　濕製程與清洗

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| SCREEN Semiconductor Solutions（台灣迪恩士） | 清洗設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024、2025 得獎；品項見備註 |
| 辛耘 Scientech（3583） | 濕製程設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 獲先進封裝量產支援獎 |
| 弘塑 Grand Process Technology（3131） | 濕製程設備 | 該類主要廠商 | https://technews.tw/2024/10/18/cowos-equipment-factory/ | 媒體列為 CoWoS 濕製程設備商，未提台積電 |
| 勝一化工（1773） | 化學品（特用化學品） | 台積電供應商（有公開證據） | https://pr.tsmc.com/chinese/news/3086 | 2023 獲化學品量產支援與綠色製造獎 |
| 長春石化 Chang Chun Petrochemical | 化學品 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2023、2025 得獎；台股代號查無 |
| Merck 默克 | 前驅物、特用化學品 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3086 | 2023、2025 得獎 |

備註：

- SCREEN 清洗設備領先地位來自市場研究摘要（`https://semiconductorx.com/wfe-cleaning.php`），市占百分比各來源不一，本檔不引用；獎項稿未載品項。
- 辛耘：中文版獎項稿列「辛耘企業股份有限公司：先進封裝卓越量產支援」（`https://pr.tsmc.com/chinese/news/3192`）；辛耘的 CoWoS 濕製程設備訂單較同業多，見 `https://technews.tw/2024/10/18/cowos-equipment-factory/`。該獎項屬先進封裝，不一定是前段清洗。
- 弘塑：媒體只寫其為日月光、美光、Amkor 等封測廠關鍵供應商，沒有提台積電。
- 長春石化：獎項稿列 Chang Chun Petrochemical Co., Ltd.，我未查到其上市櫃代號，標「查無」，不填訓練記憶值。
- 備選：TEL（清洗為其產品之一，`https://pr.tsmc.com/english/news/3192`）。李長榮集團（榮化 1704，2024 獎項為集團名，是否即榮化待查證，`https://pr.tsmc.com/english/news/3192`）。
- Merck 的 2023 獎項類別為前驅物（沉積用），2025 獎項為綠色製造；此列以特用化學品通稱，品項待查證。

## 步驟 10　線上檢測與量測

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| KLA | 缺陷檢測、製程控制 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022 至 2025 連年得獎 |
| Onto Innovation | 量測、檢測 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2022、2025 得獎 |
| Nova | 光學量測（OCD） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/2995 | 2022 得獎，2023 以後名單未列 |
| Hitachi High-Tech | CD-SEM 量測 | 該類主要廠商 | https://semiconductorx.com/wfe-metrology.php | 市場資料站敘述，證據偏弱 |
| 閎康 MA-tek（3587） | 材料分析、故障分析（第三方實驗室） | 該類主要廠商 | https://uanalyze.com.tw/articles/6905734573 | 稱具 2 奈米以下檢測經驗，客戶未點名 |

備註：

- Onto 為 GAA 製程關鍵量測供應商一說（台積電、三星、英特爾皆選用）出自 SemiAnalysis 訂閱內容，來源為匿名消息，未採計。
- 閎康是第三方分析服務，非產線上的檢測設備；放在此步是因其服務於先進製程研發除錯。「2 奈米」一詞出自閎康自述與媒體，未指名台積電為客戶。
- 備選：Applied Materials（eBeam，台積電供應商，`https://pr.tsmc.com/english/news/3274`，但獎項稿未載檢測品項）。

## 步驟 11　晶圓測試

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Advantest | 測試機（ATE） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2025 首次獲獎 |
| Technoprobe | 探針卡 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 得獎 |
| 京元電子 KYEC（2449） | 晶圓測試代工 | 台積電供應商（有公開證據） | https://technews.tw/2026/01/12/ai-cowos-war/ | 法人稱晶圓測試外包由台積電轉向日月光投控與京元電 |
| 日月光投控 ASE（3711） | 晶圓測試代工 | 台積電供應商（有公開證據） | https://technews.tw/2026/01/12/ai-cowos-war/ | 同上 |
| 精測 CHPT（6510） | 探針卡（高階） | 該類主要廠商 | https://www.cw.com.tw/article/5134356 | 天下雜誌稱打入 CoWoS 供應鏈，公司不評論 |
| 旺矽 MPI（6223） | 探針卡（MEMS） | 該類主要廠商 | https://money.udn.com/money/amp/story/5607/9139576 | 探針卡台廠之一，台積電供貨查無 |

備註：

- 京元電、日月光的證據是中央社稿經 TechNews 轉載，原文「越來越多晶圓測試外包訂單，由台積電轉向日月光投控和京元電」，出處為法人說法，非公司聲明，範圍僅晶圓測試。
- 旺矽、精測：媒體以「受惠 AI 晶片測試」敘述，未有一則明確寫出供貨給台積電。
- 備選：Teradyne（測試機，台積電 3DFabric 聯盟的測試夥伴，`https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance`，層級為「該類主要廠商」）。
- 旺矽、精測的英文縮寫（MPI、CHPT）為常用稱法，未逐一對證券交易所英文簡稱，標待查證。

## 步驟 12　先進封裝（CoWoS／SoIC）

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| 日月光投控 ASE（3711） | CoWoS 外包 OSAT | 台積電供應商（有公開證據） | https://www.trendforce.com/news/2024/11/04/news-tsmcs-cowos-prices-may-rise-20-ase-and-amkor-compete-for-outsourcing-orders | 稿稱 ASE 與 SPIL 與台積電合作 CoWoS-S oS |
| Amkor | CoWoS 外包 OSAT | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3174 | 台積電 2024-10 與 Amkor 簽 Arizona 封裝合作備忘錄 |
| 欣興 Unimicron（3037） | ABF 載板 | 台積電供應商（有公開證據） | https://www.tsmc.com/english/event/CSD_37 | TCIA 2025 第一層級獎；同為 3DFabric 載板夥伴 |
| Ajinomoto 味之素 | ABF 絕緣膜（ABF） | 該類主要廠商 | https://www.aft-website.com/en/products/insulating_film-abf/ | 官網自稱近乎 100% 市占，屬自述 |
| DISCO | 晶圓切割、研磨設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 獲先進封裝量產支援獎 |
| 辛耘 Scientech（3583） | 先進封裝濕製程設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/chinese/news/3192 | 2024 首次獲獎 |

備選（同欄位）：

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| 矽品 SPIL（日月光投控子公司，無獨立代號） | CoWoS 外包 OSAT | 台積電供應商（有公開證據） | https://www.trendforce.com/news/2024/08/06/news-tsmc-assigns-cow-order-for-the-first-time-reportedly-to-osat-provider-spil/ | 報導稱 CoW 首次釋單給矽品，為轉述 MoneyDJ |
| 萬潤 All Ring Tech（6187） | 先進封裝設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/chinese/news/3274 | 2025 首度入列，獎項稿未載品項 |
| 健策 Jentech（3653） | 散熱元件 | 台積電供應商（有公開證據） | https://pr.tsmc.com/chinese/news/3274 | 2025 首度入列，品項待查證 |
| 志聖 CSUN（2467） | 烘烤、壓膜設備 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3086 | 2023、2025 得獎，品項待查證 |
| Asahi Kasei 旭化成 | 感光絕緣材料 PIMEL | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024、2025 得獎 |
| NAMICS | 底部填充膠等封裝材料 | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3192 | 2024 先進封裝獎；TCIA 2025 亦列名 |
| 景碩 Kinsus（3189） | 載板 | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance | 3DFabric 載板夥伴 |
| Ibiden | 載板 | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance | 3DFabric 載板夥伴 |
| Besi | 混合鍵合（SoIC 相關） | 該類主要廠商 | https://bits-chips.com/article/applied-and-besi-unveil-integrated-die-to-wafer-hybrid-bonder/ | 與 Applied 合作混合鍵合，台積電採用情形查無明說 |
| 弘塑 Grand Process Technology（3131） | CoWoS 濕製程設備 | 該類主要廠商 | https://technews.tw/2024/10/18/cowos-equipment-factory/ | 媒體未提台積電 |

備註：

- 媒體曾報導台積電將 CoWoS-S 後段（oS）外包比重 40% 至 50% 給日月光，TrendForce 稱「by 2025」，屬估計，不是確定數字，本檔不引用。2026-08 另有報導稱台積電擴大把 CoW 外包給 ASE 等 OSAT（`https://www.trendforce.com/news/2026/08/05/news-tsmc-reportedly-expands-outsourcing-of-key-cowos-front-end-step-to-osats-amid-rising-nvidia-asic-demand/`），未開全文查證。
- OSAT 列內「台積電供應商」是基於媒體明確報導該 OSAT 承接台積電 CoWoS 後段，不是台積電官方聲明；Amkor 的證據是台積電自己的新聞稿（`https://pr.tsmc.com/english/news/3174`）。
- 欣興：TCIA 屬原物料／載板往來證據；載板賣給封測廠與客戶的關係不同，是否直接賣給台積電的 CoWoS 載板，查無明說。
- Ajinomoto ABF：近乎 100% 為官網自述；與台積電的往來查無。
- 辛耘：英文名 Scientech 對應中文版獎項稿「辛耘企業股份有限公司」。
- 萬潤、健策、志聖：品項依 TechNews 與 TCIA 比對，獎項稿本身未載；志聖英文名 CSUN 與「志聖工業」對應見 2023 中文稿 `https://pr.tsmc.com/chinese/news/3086`；2025 獎項稿的 `CSUN / G2C+ Alliance` 並列名稱的成員組成未查證。
- 先進封裝證據整體屬「中等」：獎項是強證據，品項是弱證據。

## 步驟 13　最終測試

| 廠商名 | 類別 | 層級 | 來源 URL | 備註 |
|---|---|---|---|---|
| Advantest | 測試機（ATE） | 台積電供應商（有公開證據） | https://pr.tsmc.com/english/news/3274 | 2025 首次獲獎 |
| Teradyne | 測試機（ATE） | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance | 3DFabric 聯盟的測試夥伴 |
| 京元電子 KYEC（2449） | 測試代工 | 該類主要廠商 | https://money.udn.com/money/story/5607/9455306 | 最終測試為台積電外包的證據查無 |
| 日月光投控 ASE（3711） | 封測代工 | 該類主要廠商 | https://www.tsmc.com/english/dedicatedFoundry/oip/3dfabric_alliance | 3DFabric OSAT 夥伴；最終測試外包證據查無 |
| 矽格 Sigurd（6257） | 測試代工 | 該類主要廠商 | https://wantrich.chinatimes.com/news/20260120900391-420101 | 與台積電關係查無 |
| 欣銓 Ardentec（3264） | 測試代工 | 該類主要廠商 | https://www.cmoney.tw/notes/note-detail.aspx?nid=930536 | 與台積電關係查無 |

備註：

- 最終測試的測試代工廠，沒有找到明說「台積電把 N2 或任何先進製程的最終測試外包給某廠」的來源。京元電、日月光的外包證據只涵蓋晶圓測試（步驟 11），故步驟 13 全歸「該類主要廠商」。
- 只有 Advantest 的證據明確（台積電獎項稿），但稿中是「量產支援」，未區分晶圓測試或最終測試。
- 矽格、欣銓、京元電的英文縮寫（Sigurd、Ardentec、KYEC）為常用稱法，未逐一對證券交易所英文簡稱，標待查證。
- 備選：南茂（8150）、力成（6239），本檔未查到與台積電有關的來源，未入表。

---

## 證據偏弱的步驟（彙整）

1. **步驟 2 運算微影**：台灣廠商查無；ASML 軟體對台積電供貨無明說來源。
2. **步驟 3 光罩製作**：空白光罩、pellicle、光罩盒皆無「供貨給台積電」的明說來源；家登的台積電客戶身分只見於媒體概述。
3. **步驟 5 磊晶與薄膜沉積**：台灣廠商查無；台積電獎項稿不載機型，品項（ALD、磊晶）靠廠商資料推定。
4. **步驟 7 蝕刻**：選擇性蝕刻與台積電的對應查無明說；Hitachi High-Tech 證據為 2014 年。
5. **步驟 8 金屬閘極與導線**：台灣廠商來自 TCIA，僅證明往來，不載品項與節點；Lam ECD 品項待查證。
6. **步驟 10 量測**：閎康非設備；Hitachi High-Tech 僅市場網站敘述。
7. **步驟 11 與 13 測試**：探針卡台廠（精測、旺矽）與測試代工（矽格、欣銓）均為媒體敘述；最終測試外包證據整體查無。

## 已知限制

- 台積電官網部分頁面（EDA 聯盟、3DFabric 聯盟）顯示的成員為抓取當日內容，成員名單可能變動。
- Applied Materials 官網部分頁面回 403，未繞過；改用 TSMC 獎項稿與 Applied 產品庫頁面。
- 本檔所有「N2」字樣僅用於步驟 1、2 的引述；其餘來源未逐廠聲明 N2。
- 本檔未以任何 HTTP 標頭、URL 或表單提供聯絡資訊。
- 本檔為研究筆記，來源以 2026-11-01 前可取得的內容為準。
