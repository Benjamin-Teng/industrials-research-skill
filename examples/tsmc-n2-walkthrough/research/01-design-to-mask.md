# 01 設計完成 → tape-out → 光罩製作（TSMC N2）一手證據

- 查證日期：2026-11-01（下列每筆引文的「查證日」皆同）
- 性質：只交證據，不下結論。引文為原文語言逐字摘錄（≤3 句），逐字內容皆自抓回的頁面文字比對過。
- 標示規則：【公司說法】＝TSMC 自家頁面／新聞稿；【EDA 廠說法】＝Synopsys／Cadence／Siemens 自家新聞稿（利益相關方，等同「公司說法」的合作夥伴版）；【論文】＝TSMC 作者的 SPIE 論文；【第三方】＝媒體、經紀商、百科。
- 重要範圍提醒：TSMC 官方 EDA 認證頁（as of 10/01/2026）的狀態表只列 A14／A16／N2P／N3C，**不再單列 N2**；N2 本身的認證證據來自 2023–2024 年 EDA 廠新聞稿。TSMC 官網 N2 頁（2026 版）只是摘要，沒有 NanoFlex、設計流程等細節。

## 關卡總表

| # | 關卡 | 證據強度 |
|---|---|---|
| 1 | 設計-fab 交接介面：OIP／PDK／DRM／EDA 認證 | 官方＋EDA 廠 |
| 2 | 設計端 DTCO：N2 NanoFlex 標準元件 | 官方＋第三方 |
| 3 | 設計實作與 sign-off（APR、時序、EMIR、DRC／LVS、ESD） | 官方（類別）＋EDA 廠（N2 實例） |
| 4 | Tape-out：定義與交付物（GDSII／OASIS）、CyberShuttle | 官方（shuttle）＋第三方（定義）；TSMC 專屬 tape-out 審核流程查無 |
| 5 | 光罩資料準備：OPC／ILT | 官方（OPC）＋第三方廠商聲明（ILT／cuLitho） |
| 6 | 光罩製作（寫入、空白光罩） | 查無（N2 專屬寫入機、EUV mask blank 等） |
| 7 | 光罩檢測／修補／pellicle | 論文＋第三方 |
| 8 | 光罩數量、尺寸 | 光罩數量查無；尺寸（6 吋→12 吋計畫）官方 |

---

## 1. 設計-fab 交接介面：OIP、PDK、DRM、EDA 認證

**做什麼**：TSMC 以 OIP 把設計工具（EDA）、IP、設計服務夥伴串起來；EDA 廠對每個新製程做「認證」，並拿到 TSMC 的設計規則手冊（DRM）與製程設計套件（PDK）。

**檢查點／會卡在哪**：EDA 工具對該製程「Certified」才算可用；官方狀態表分 Certified／Work in Progress。

**N2 特有**：Cadence 的流程於 2023-04 通過 N2 DRM 認證，原文寫雙方（the companies）交付 N2 PDK，未寫交付對象；2024 年底 N2P 的 PDK 版本為 0.9（早期版）。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| OIP 的定位 | "The TSMC Open Innovation Platform® is a comprehensive design technology infrastructure that encompasses all critical IC implementation areas to lower design barriers, improve design cycle times, and accelerate first-time silicon success." | https://www.tsmc.com/english/dedicatedFoundry/oip | 官方（公司說法） |
| EDA 認證範圍（類別即各關卡的檢查項目） | "The advanced process node certifications cover several silicon-centric categories, including physical implementations (APR for High Density/HPC, Custom Design), timing and power signoffs (STA, Transistor-level STA), electromigration and IR Drop (Gate-level and transistor-level EMIR), physical verifications (DRC, LVS, Dummy Fill), RC extractions (RC), simulators, and thermal." | https://www.tsmc.com/english/dedicatedFoundry/oip/eda_alliance | 官方（公司說法） |
| 認證涵蓋製程（N2 本體已不單列） | "The core of the certification program covers the tool solutions to the latest advanced process technologies (A14, A16, N2P, N3C) and 3DFabric offering." | 同上（頁面狀態表日期 "As of 10/01/2026"） | 官方 |
| Cadence 流程通過 N2 DRM 認證；PDK 由「雙方」交付，原文未寫交付對象（2023-04） | "Cadence Design Systems, Inc. announced its digital and custom/analog flows have been certified to support TSMC's new Design Rule Manual (DRM) for the foundry's advanced N3E and N2 nodes. The companies also delivered N3E and N2 process design kits (PDKs) to facilitate mobile, AI and hyperscale computing IC design innovation at these nodes." | https://www.cimdata.com/en/industry-summary-articles/item/21465-cadence-digital-and-custom-analog-design-flows-certified-for-tsmc-s-latest-n3e-and-n2-process-technologies （CIMdata 轉載，頁面日期 2023-04-27） | EDA 廠（轉載） |
| N2 PDK 完整認證（Cadence 類比流程，2024-04） | "The Cadence Custom/Analog Design Flow is fully certified for TSMC's latest N2 Process Design Kit (PDK)" | https://us.design-reuse.com/news/56128/cadence-tsmc.html （轉載，日期 2024-04-24） | EDA 廠（轉載） |
| N2P PDK 為 0.9 版（早期版本） | "These programs have already been certified for the N2P process development kit (PDK) version 0.9, deemed adequate as mass production using this fabrication process is slated for the second half of 2026, about two years from now." | https://www.tomshardware.com/tech-industry/tsmc-announces-its-customers-can-now-design-performance-enhanced-2nm-chips-with-super-high-performance-capacitors （2024-11-22） | 第三方（媒體） |
| N2 已量產（TSMC 官網 2026 版） | "TSMC's 2nm (N2) technology has started volume production in 4Q25 as planned." | https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm | 官方 |

**查無**：N2 的 PDK 各版本（0.1／0.5／1.0）釋出時程與 PDK 內容清單——TSMC 官網需登入 TSMC-Online。已搜關鍵字：TSMC N2 PDK release version、N2 PDK v0.1/v1.0、TSMC-Online PDK download。
**查無（部分）**：官方 EDA 狀態表的逐格 Certified／WIP 無法從文字判讀（以顏色／符號呈現，原始 HTML 只留下圖例）；N2P 的 Cadence／Synopsys／Siemens 各工具狀態不在本檔結論內。

---

## 2. 設計端 DTCO：N2 NanoFlex 標準元件

**做什麼**：設計者在同一個設計區塊內混用「矮」「高」標準元件，取得面積／功耗／效能的取捨。

**檢查點／會卡在哪**：元件高度組合要與時序、佈線、功耗收斂配合；EDA 工具需支援（見關卡 3）。

**N2 特有**：NanoFlex 是 N2 的 DTCO 特色，2025 年演進為 NanoFlex Pro（用於 A14）。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| NanoFlex 定義（TSMC，2024-04-24） | "TSMC's upcoming N2 technology will come with TSMC NanoFlex, the company's next breakthrough in design-technology co-optimization. TSMC NanoFlex provides designers with flexibility in N2 standard cells, the basic building blocks of chip design, with short cells emphasizing small area and greater power efficiency, and tall cells maximizing performance." | https://pr.tsmc.com/english/news/3136 | 官方（新聞稿） |
| 同一設計區塊內可混用 | "Customers are able to optimize the combination of short and tall cells within the same design block, tuning their designs to reach the optimal power, performance, and area tradeoffs for their application." | 同上 | 官方 |
| NanoFlex Pro（2025-04-23） | "Leveraging the Company's experience in design-technology co-optimization for nanosheet transistor, TSMC is also evolving its TSMC NanoFlex™ standard cell architecture to NanoFlex™ Pro, enabling greater performance, power efficiency and design flexibility." | https://pr.tsmc.com/english/news/3228 | 官方 |
| 第三方描述（IEEE Spectrum，IEDM 2024 報導，2024-12-12） | "Called Nanoflex, TSMC's tech allows different logic cells built with different nanosheet widths on the same chip." | https://spectrum.ieee.org/tsmc-n2 | 第三方（媒體） |

**查無**：TSMC 官方 NanoFlex 專頁（https://nanoflex.tsmc.com/english/dedicatedFoundry/technology/Nanoflex.htm 回 HTTP 403，tsmc.com 版路徑回 404），故無官方 NanoFlex 示意圖可下載。已搜關鍵字：TSMC NanoFlex diagram、NanoFlex short cell tall cell figure。

---

## 3. 設計實作與 sign-off

**做什麼**：RTL→合成→佈局佈線（APR）→時序／功耗 sign-off→實體驗證（DRC／LVS／dummy fill）→ESD／可靠度檢查。

**檢查點／會卡在哪**：TSMC 認證表列出的項目（Timing、Power、EMIR、DRC、Dummy Fill、LVS/LPE、RC、PERC 等）；EDA 廠新聞稿點名 N2 需要新功能。

**N2 特有**：混合元件列（hybrid cell row，Cadence 原文標明用於 N3E，非 N2 專屬）、元件 pin 對齊、pattern-based pin access、後端 ESD（PERC）規則。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| 數位 sign-off 需支援的新設計特徵（Cadence 2023-04；hybrid cell row 原文標明用於 N3E） | "The full Cadence digital implementation and signoff flow supports a variety of new design features, including native hybrid cell row optimization from synthesis to signoff ECO for optimal PPA at N3E, cell pin alignment and connection support." | https://www.cimdata.com/en/industry-summary-articles/item/21465-cadence-digital-and-custom-analog-design-flows-certified-for-tsmc-s-latest-n3e-and-n2-process-technologies | EDA 廠 |
| N2 物理驗證 sign-off 認證（Siemens，2023-09-27） | "Siemens' industry-leading Calibre® nmPlatform tool for integrated circuit (IC) verification sign-off is now fully certified for TSMC's most advanced N2 process, including Calibre® nmDRC software, Calibre® YieldEnhancer™ software, Calibre® PERC™ software and Calibre® nmLVS software" | https://news.siemens.com/en-us/tsmc-oip-2023/ | EDA 廠 |
| N2 流程認證與 tape-out（Synopsys，2023-09-25） | "Synopsys, Inc. (Nasdaq: SNPS) today announced that its digital and custom/analog design flows are certified for TSMC's N2 process technology, enabling faster delivery of advanced-node SoCs with higher quality. Both flows are seeing strong momentum, with the digital design flow achieving multiple tape-outs and the analog design flow adopted for several design starts." | https://us.design-reuse.com/news/54884/synopsys-tsmc-2nm-certified-digital-and-analog-design-flows.html | EDA 廠（轉載） |
| N2 全晶片 sign-off 工具（同上） | "As part of the certified EDA flows, Synopsys provides interoperable process design kits (iPDKs) and Synopsys IC Validator™ physical verification for full-chip physical signoff." | 同上 | EDA 廠 |
| N2P 的 pin access 與 DRC／LVS／ESD（Synopsys，2025-04-23） | "Pattern-based pin access methodology has been enhanced for TSMC N2P and A16™ nodes to deliver competitive area results." ／ "Synopsys IC Validator™ signoff physical verification solution, including Design Rule Checks (DRC) and Layout Versus Schematic (LVS) checking, is certified for A16™ and N2P processes." | https://news.synopsys.com/2025-04-23-Synopsys-and-TSMC-Usher-In-Angstrom-Scale-Designs-with-Certified-EDA-Flows-on-Advanced-TSMC-A16-and-N2P-Processes | EDA 廠 |
| sign-off 通用定義 | "signoff (also written as sign-off) checks is the collective name given to a series of verification steps that the design must pass before it can be taped out." | https://en.wikipedia.org/wiki/Signoff_(electronic_design_automation) | 第三方（百科） |
| 經紀商清單：DRC 清零、waiver 要核准（非 N2 專屬、非 TSMC 官方，可靠度低） | "Run the TSMC-specified DRC deck in full batch mode. Zero DRC violations is required. Waived violations must be documented with foundry-approved waiver forms." | https://www.vlsishuttle.com/en/mpw/tsmc-mpw-schedule-2026 | 第三方（MPW 經紀商） |

**查無**：N2 專屬的 DRC 規則條數、N2 DRM 公開內容（需 NDA）；TSMC 官方的 tape-out 前置 checklist。已搜關鍵字：TSMC tape-out review checklist、TSMC DRM N2 design rules、TSMC tape-out submission TSMC-Online。

---

## 4. Tape-out：定義與交付物

**做什麼**：將最終版圖資料庫（GDSII／OASIS）交給 foundry，作為光罩製作的起點。

**檢查點／會卡在哪**：sign-off 通過；foundry 收件後仍會做自己的檢查並修改光罩資料（第三方描述）；MPW／CyberShuttle 需符合固定截止日。

**N2 特有**：N2 可走 CyberShuttle（TSMC 官網稱涵蓋至 A14）。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| tape-out 的定義（含 mask 資料傳送） | "The tapeout is specifically the point at which the graphic for the photomask of the circuit is sent to the fabrication facility." | https://en.wikipedia.org/wiki/Tape-out | 第三方（百科） |
| foundry 在 tape-out 後還會修改光罩資料 | "in current practice, the foundry will perform checks and make modifications to the mask design specific to the manufacturing process before actual tapeout." | 同上 | 第三方（百科） |
| TSMC 光罩服務是「設計者與 fab 的介面」 | "As the world's largest mask making operation, TSMC's mask service is the interface between designers and our world class fabs." | https://www.tsmc.com/english/dedicatedFoundry/services/mask_services | 官方 |
| CyberShuttle（多專案共用光罩） | "CyberShuttle® services overcome this barrier by enabling multiple designs to share tooling costs through a multi-project mask set. This significantly reduces mask NRE costs for product prototyping and circuit characterization." | https://www.tsmc.com/english/dedicatedFoundry/services/cybershuttle | 官方 |
| CyberShuttle 涵蓋範圍與時程取得 | "the broadest technology range (from 0.5μm to A14), with the most frequent launch schedule (up to 10 shuttles per month)" ／ "login to TSMC-Online or contact your local TSMC representative for the latest CyberShuttle® schedule." | 同上 | 官方 |

**查無**：GDSII／OASIS 作為 TSMC N2 收件格式的 TSMC 官方明文（TSMC 公開頁面只說「GDS data」，見關卡 5）；N2 專屬 tape-out 流程、檔案命名、審核天數。已搜關鍵字：TSMC tape-out GDSII OASIS N2、TSMC tape-out review、TSMC-Online tape-out。
**矛盾／差異**：tape-out 的觸發點定義不統一（第三方搜尋摘要指出有「首次送出全光罩資料庫」與「設計完成可準備光罩」兩種用法；僅屬搜尋摘要，未逐字取得原文）。

---

## 5. 光罩資料準備：OPC／ILT

**做什麼**：把客戶 GDS 轉成可製作的光罩資料，含光學鄰近修正（OPC）。

**檢查點／會卡在哪**：OPC 模型要涵蓋製程工具、材料與 DFM 要求；計算量極大。

**N2 特有**：TSMC 公開說法未點名 N2；cuLitho 與曲線光罩為 TSMC 近年投產項目（2024），TSMC 作者論文提到 SRAF 與 curvy OPC 設計的檢測。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| TSMC 對先進光罩做 GDS 的 OPC 轉換 | "For advanced technology masks, TSMC routinely conducts optical proximity check (OPC) conversions of GDS data." | https://www.tsmc.com/english/dedicatedFoundry/services/mask_services | 官方 |
| OPC 模型涵蓋範圍 | "Silicon process tools and process materials, as well as design-for-manufacturing (DFM) requirements, are covered by the OPC models to facilitate the largest production window." | 同上 | 官方 |
| 資料庫優勢 | "The most complete database of silicon-validated OPC optimized with TSMC's wafer processing technologies" | 同上 | 官方 |
| cuLitho 進入 TSMC 量產（2024-03-18，NVIDIA 稿含 TSMC CEO 引言） | "We are moving NVIDIA cuLitho into production at TSMC, leveraging this computational lithography technology to drive a critical component of semiconductor scaling." | https://nvidianews.nvidia.com/news/tsmc-synopsys-nvidia-culitho | 廠商聲明（NVIDIA 稿） |
| 計算量規模（NVIDIA 聲明） | "A typical mask set for a chip — a key step in its production — could take 30 million or more hours of CPU compute time, necessitating large data centers within semiconductor foundries." | 同上 | 廠商聲明 |
| 曲線（curvilinear）與 Manhattan 流程 | "In testing cuLitho on shared workflows, the companies jointly realized a 45x speedup of curvilinear flows and a nearly 60x improvement on more traditional Manhattan-style flows." | 同上 | 廠商聲明 |
| 檢測端提到 SRAF／curvy OPC（TSMC 作者論文） | "Combining with the ML model, proper detectors were designed for each specific feature, such as SRAF and curvy OPC design, and the performance of auto defect classification (ADC) with the model has been proven." | DOI 10.1117/12.3032058（SPIE Photomask Japan 2024）；https://doi.org/10.1117/12.3032058 | 論文（abstract 經 Semantic Scholar 取得，SPIE 全文頁擋 bot） |

**查無**：TSMC 公開說明 N2 是否使用 ILT／曲線光罩（只有 TSMC 作者論文提到 curvy OPC 的檢測，未說用在 N2）；OPC 迭代次數、資料量（GB）。已搜關鍵字：TSMC N2 OPC ILT curvilinear mask、TSMC inverse lithography N2。
**注意**：NVIDIA 稿中的加速倍率是 NVIDIA 與合作夥伴聯合測試的聲明，非獨立驗證。

---

## 6. 光罩製作（寫入、空白光罩）

**做什麼**：以電子束寫入機把資料寫成光罩；TSMC 有自有光罩廠（"TSMC mask shop"）。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| TSMC 自有光罩廠（論文用語，N5／N3 量產） | "high-volume manufacturing of advanced chips including N5 and N3 was realized due to the defect-free masks provided by the TSMC mask shop." | https://doi.org/10.1117/12.2688174 （SPIE Photomask Technology 2023；abstract 取自 Semantic Scholar） | 論文 |
| 官方：全球最大光罩製造 | "World's largest mask-manufacturing capability" | https://www.tsmc.com/english/dedicatedFoundry/services/mask_services | 官方 |
| 光罩品質保固 | "Masks have quality warranties" | 同上 | 官方 |

**查無**：TSMC 光罩廠使用的電子束寫入機型號／多束寫入（MBMW）採用現況、N2 光罩寫入時間、EUV mask blank 供應商。已搜關鍵字：TSMC multi-beam mask writer N2、TSMC mask shop e-beam writer、TSMC EUV mask blank。僅查到：IMS 稱其 MBMW-301 針對 2nm 以下節點（廠商說法，未點名 TSMC 使用；TSMC 早年曾加入 IMS 多束寫入機開發，為舊資料）。

---

## 7. 光罩檢測、修補與 pellicle

**做什麼**：光罩寫完要做缺陷檢測（以 EUV 光源做 actinic 檢測）、缺陷修補後以 AIMS 類工具評估可印性，再貼 pellicle 保護。

**檢查點／會卡在哪**：EUV 光罩的缺陷判定原本需靠晶圓印製評估（約 3 天）；pellicle 讓光罩可重複使用但會遮擋傳統檢測。

**N2 特有**：TSMC 論文只明說 N5／N3 及「beyond N3」，**未點名 N2**。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| 官方：光罩例行檢查項目 | "TSMC regularly conducts mask checks for electro-static discharge (ESD) damage, scratches, particle deposition, pellicle frames and aging to keep each mask in the best possible condition." | https://www.tsmc.com/english/dedicatedFoundry/services/mask_services | 官方 |
| 舊流程：缺陷以晶圓印製評估要約 3 天 | "Currently, every potential defect must be judged by wafer printing assessment for almost 3 days, which can be both time-consuming and expensive, and even commercial approaches are incapable of meeting the demands of high-volume manufacturing." | https://doi.org/10.1117/12.2688176 （SPIE Photomask Technology 2023，TSMC 作者） | 論文 |
| Actinic 光罩審查系統（AMRS） | "With this solution, all EUV repaired and potential defects, including 18nm HP L/S, ML defects, and even through EUV pellicle defects, can be addressed in technology nodes N5, N3, and beyond N3, on the brand-new actinic review platform." | 同上 | 論文 |
| AMRS 規格 | "utilizing a stable LPP EUV source with over 95% available time and a specialized TSMC-made SMO to achieve high throughput for more than 80 sites/hr." | 同上 | 論文 |
| 以 EUV inspector 做 pellicle 檢測 | "The application of EUV inspector unleashed pellicle inspection to prolong mask operation periods in wafer foundries." | https://doi.org/10.1117/12.3032058 （SPIE Photomask Japan 2024） | 論文 |
| GPU＋AI 缺陷檢測 | "Furthermore, tsmc developed a GPU-based inspection system, which allowed for flexible algorithm development compared to FPGA." | 同上 | 論文 |
| 自製 EUV pellicle 改善（媒體轉述 TSMC 2024 年中報告） | "Back in mid-2024, TSMC reported dramatic improvements of its in-house developed EUV pellicle performance, including a four times longer lifespan, four and a half times more wafer output per pellicle, and an 80x reduction in defects." | https://www.tomshardware.com/tech-industry/semiconductors/how-tsmc-managed-to-increase-efficiency-of-asmls-euv-tools-system-level-optimizations-and-in-house-pellicles-chipmaker-boosted-euv-driven-wafer-production-by-30x-over-six-years-while-reducing-power-consumption-by-24-percent （2025-09-17） | 第三方（媒體轉述；TSMC 原始報告未取得） |

**查無**：TSMC 官方關於自製 pellicle 的原始文件（上述數字僅有媒體轉述）；N2 專屬光罩缺陷規格、光罩修補（e-beam repair）設備、pellicle 穿透率（搜尋摘要提到另一 SPIE 論文有「82–95% transmittance」，未取得該論文原文，不採用）。已搜關鍵字：TSMC EUV pellicle transmittance N2、TSMC mask repair、TSMC mask defect specification N2。

---

## 8. 光罩數量與尺寸

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| 現行 EUV 光罩為 6 吋，TSMC＋ASML 計畫轉 12 吋（2026-09） | "While High NA EUV will be adopted for production using the current, 6-inch masks, the transition to larger, 12-inch masks is expected to further increase fab productivity, lower chipmaking costs and remove stitching constraints, benefiting the entire semiconductor industry." | https://pr.tsmc.com/english/news/3338 | 官方（TSMC／ASML 聯合稿） |
| 12 吋光罩時程 | "The initiative targets establishing a 12-inch mask pilot line by 2031, supporting full lithography system readiness for advanced node production by 2033." | 同上 | 官方 |

**查無（光罩數量）**：N2 一套光罩的總數、EUV 層數、光罩組成本——TSMC 官方與 SPIE／IEDM 來源皆未見。搜尋曾出現第三方部落格與參考表的估計（EUV 25–30+ 層；光罩約 100+ 張、光罩組 US$15M–30M+），但有來源不明且互相矛盾（另一報導稱 N2 的 EUV 層數與 3nm 相近），**未逐字驗證，不建議採用**。已搜關鍵字：TSMC N2 EUV layers mask count、2nm mask set cost、N2 number of masks。

---

## 官方示意圖候選清單

| # | 檔名（已下載） | 圖直接 URL | 所在頁面 URL | 頁碼／位置 | 圖說 | 授權／版權標示 |
|---|---|---|---|---|---|---|
| 1 | `eda-reference-flow-chart.jpg`（3154×1488） | https://www.tsmc.com/sites/dcom/2026-10/EDA_Ref-Flow_chart_20261012.jpg | https://www.tsmc.com/english/dedicatedFoundry/oip/eda_alliance | 網頁，位於頁面中段「Design Reference Flows」之後；非 PDF | 頁面無圖說，img alt 為 "Reference flow roadmap after OIP"。圖內容：2008–2026 年各節點設計方案階梯圖（APR／Custom／RF／Si-Photonics／3DIC／Migration），含 N2 HPC／N2 Mobile／N2 Custom Design（2023 欄）、N2P（2024 欄）。**此圖是 N2 設計參考流程的上線時程，不是逐關卡的流程圖** | 圖上無浮水印或授權文字；頁尾 "Copyright© Taiwan Semiconductor Manufacturing Company Limited 2010-2026, All Rights Reserved." |
| 2 | `mask-services-header.jpg`（500×360） | https://www.tsmc.com/sites/dcom/inline-images/pic_maskservices.jpg | https://www.tsmc.com/english/dedicatedFoundry/services/mask_services | 網頁，頁首主圖；非 PDF | 頁面無圖說，img alt 為 "Mask Services"。圖內容：無塵室作業員手持光罩盒中的光罩（照片，非流程圖） | 圖上無浮水印；頁尾同上 All Rights Reserved |

**官方圖狀況說明**
- 只找到上述 2 張與本主題直接相關者，均下載成功。未達上限 8 張。
- **查無**：官方的「設計→tape-out→光罩」逐關卡流程圖。TSMC 官網 Mask Services、CyberShuttle、OIP 頁面均無此類圖。
- **失敗／不可用**：NanoFlex 官方專頁 https://nanoflex.tsmc.com/english/dedicatedFoundry/technology/Nanoflex.htm 回 403，無法取圖；pr.tsmc.com 的 2024／2025 Technology Symposium 新聞稿頁面僅有附件 PDF（3 頁，內含文字摘要），未見示意圖，故未收。
- 未下載（非本範圍）：TSMC N2 頁的 https://www.tsmc.com/sites/dcom/2026-07/Process-Technology-Nodes_260709.png（製程節點路線圖，屬「節點演變與藍圖」agent 範圍）。

## 公司說法與第三方證據對照

- **N2 EDA 認證時程**：EDA 廠（Synopsys 2023-09-25、Siemens 2023-09-27、Cadence 2023-04／2024-04）宣稱 N2 認證完成；TSMC 官網 EDA 認證頁（as of 10/01/2026）已不再單列 N2，僅列 N2P 等。兩者不矛盾（不同時點），但官方頁面無法直接佐證 N2 的逐格狀態。
- **N2P 量產時間**：Tom's Hardware（2024-11-22）寫 "mass production using this fabrication process is slated for the second half of 2026"；TSMC 官網 2026 版 N2 頁只說 N2 本體已於 4Q25 量產，N2P 量產時間於本次取得的 TSMC 頁面中未見——**待查證**。
- **tape-out 定義**：第三方（百科）與 TSMC 官方頁面用語不同；TSMC 頁面用「interface between designers and our world class fabs」，未使用 "tape-out" 一詞。

## 搜尋紀錄（供驗收「查無」項目）

已搜過的關鍵字組合：TSMC N2 NanoFlex DTCO OIP EDA certification PDK；TSMC N2 tape-out EDA certification Synopsys Cadence；TSMC mask making EUV pellicle mask inspection N2 mask shop；Cadence Innovus Genus certified TSMC N2 DRM；Siemens Calibre nmDRC nmLVS certified TSMC N2；TSMC CyberShuttle tape-out schedule N2；tape-out definition GDSII OASIS mask data preparation；TSMC N2 IEDM 2025 paper；NVIDIA cuLitho TSMC production；TSMC N2 EUV layers mask count；TSMC SPIE actinic inspection pellicle；Synopsys TSMC N2P A16 NanoFlex certified；TSMC annual report mask shop；TSMC OIP Design Enablement；TSMC ASML 12-inch EUV photomask；TSMC multi-beam mask writer IMS；TSMC tape-out review checklist。

未取得的來源：SPIE 全文頁（對 bot 回空頁，僅經 Semantic Scholar 取 abstract）；AnandTech（Cloudflare 驗證擋下）；TSMC 年報（未讀到光罩廠相關段落）；TSMC OIP／Technology Symposium 投影片（需登入）。
