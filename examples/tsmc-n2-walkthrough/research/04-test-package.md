# 04 測試與封裝：N2 晶圓出廠後到可出貨晶片（證據蒐集）

- 查證日期：2026-11-01（所有 URL 皆於該日實際開啟或下載）
- 性質：只交證據，不下結論。引文為原文語言逐字，每則 ≤3 句。
- 標示規則：【TSMC 專屬】＝來源直接講台積電；【業界通用】＝非台積電專屬的一般流程說明，不可直接當成台積電做法。
- 來源類型：官方（tsmc.com、investor.tsmc.com 法說逐字稿、SEC 20-F）／論文／媒體／通用第三方。
- 證據強度圖例：官方、第三方、通用、查無。
- 重要限制：台積電官網與公開文件**沒有**逐步描述 WAT、CP（針測）、線上檢測、切割、凸塊、最終測試的內容；這幾關的台積電專屬細節為「查無」，僅能提供業界通用說明與台積電的概括性說法。

---

## 0. 全流程骨架（台積電自述範圍與外包界線）

### 0-1 台積電對自己服務範圍的描述【TSMC 專屬】

- 做什麼：台積電以晶圓製造為主，另提供光罩、3DFabric 先進封裝與測試服務。
- 由誰執行：「directly or through outsourcing arrangements」，即台積電自做或外包。
- 引文 1（20-F，2025 年度，2026-04-16 申報）：「The following processes cover assembly, packaging, and testing of the semiconductor devices. Our focus is on wafer fabrication although we also provide other services either directly or through outsourcing arrangements.」
  - URL：https://www.sec.gov/Archives/edgar/data/1046179/000162828026025362/tsm-20251231.htm
  - 來源類型：官方（SEC 20-F）
- 引文 2（同上）：「We also offer design, mask making, TSMC 3DFabric® advanced silicon stacking and packaging services, and testing services.」
- 引文 3（同上）：「The principal source of our revenue is wafer fabrication, which accounted for approximately 86% of our net revenue in 2025. The rest of our net revenue was mainly derived from packaging and testing services, mask making, design, and royalty income.」
- 引文 4（同上，設備清單）：「The principal pieces of equipment used by us to manufacture semiconductors are scanners, cleaners and track equipment, inspection equipment, etchers, furnaces, wet stations, strippers, implanters, sputterers, chemical vapor deposition (“CVD”) equipment, chemical mechanism polish (“CMP”) equipment, testers and probers.」
- 證據強度：官方。

### 0-2 台積電先進封裝頁的整體定位【TSMC 專屬】

- 引文：「TSMC advanced packaging services create the best solutions to unleash our customer's innovations by advancing the core technology, offering integrated turnkey services, leveraging intelligent packaging fab, and providing comprehensive testing solutions.」
- 引文：「TSMC 3DFabric® solutions consist of both frontend and backend technologies, including TSMC-SoIC®, CoWoS®, and InFO.」
- URL：https://www.tsmc.com/english/dedicatedFoundry/services/advanced-packaging
- 來源類型：官方
- 備註：該頁**未出現** bumping、final test、OSAT 字樣（已逐字搜尋頁面文字）。

### 0-3 後段營收占比與資本支出【TSMC 專屬】

- 引文（4Q25 法說，2026-01-15，Wendell Huang，公司會後更正註記）：「the revenue contribution last year from advanced packaging is slightly over 10% (corrected by company after the call). It's about 8% in 2024. We expect it to grow faster than the corporate average, and account for low-teens % in 2026.」
- 引文（同場資本支出）：「About 70% to 80% of the 2026 capital budget will be allocated to advanced process technologies. About 10 percent will be spent for specialty technologies, and about 10 to 20 percent will be spent for advanced packaging, testing, mask making and others (added by company after the call).」
- URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf
- 來源類型：官方（LSEG 編輯逐字稿）
- 備註：台積電不把封裝與測試分開揭露資本支出（見 2Q26 法說，第 4 節）。

---

## 1. 關卡一：線上缺陷檢測與量測（inline inspection / metrology）

- 做什麼：前段製程中，在關鍵層後以光學、電子束等設備檢查缺陷與量測尺寸，及早攔截異常。
- 由誰執行：台積電自家晶圓廠（前段）。
- 證據強度：【TSMC 專屬】查無；【業界通用】第三方／通用。

### 1-1【TSMC 專屬】查無

- 已搜關鍵字：「TSMC inline inspection N2」「TSMC inline metrology nanosheet」「TSMC wafer acceptance test WAT wafer sort N2」「TSMC N2 yield learning inspection」；tsmc.com 的 Manufacturing 相關頁面本次未逐頁開啟，不排除其中有檢測相關說明（待查證）。
- 僅有的間接證據：20-F 設備清單含 inspection equipment（見 0-1 引文 4）。

### 1-2【業界通用，且與奈米片（GAA）相關】N2 為奈米片結構，檢測難度上升

- 引文（Semiconductor Engineering，2022-08-09，Karen Heyman）：「As fabs turn to nanosheet transistors, it is becoming increasingly challenging to detect line-edge roughness and other defects due to the depths and opacities of these and other multi-layered structures.」
- 引文（同文，IBM 的 Nelson Felix）：「With nanosheet architecture, a lot of defects that could kill a transistor are not line-of-sight. They're on the underside of nanosheets, or other hard-to-access places.」
- 引文（同文，Onto Innovation 的 Nick Keller）：「In a stacked nanosheet device, the physical dimensions of each sheet need to be measured individually — especially after selective source-drain recess etch, which determines drive current, and the inner spacer etch, which determines source-to-gate capacitance」
- URL：https://semiengineering.com/nanosheet-fets-drive-changes-in-metrology-and-inspection
- 來源類型：媒體（產業，引述設備商與 IBM）
- 檢查點／會卡在哪：奈米片底面缺陷非視線可及；每層奈米片需單獨量測（源汲極凹陷蝕刻、內間隔層蝕刻後）。注意：此為產業通論，**不是**台積電 N2 的檢測做法。

### 1-3【業界通用】並非所有良率損失都能被 inline 與參數測試攔住

- 引文（UC Berkeley IEOR 130 講義，Prof. Robert C. Leachman，2014）：「Not all die yield losses are due to defects. Some mis-processing escapes detection at inline optical inspections in the fabrication process as well as at parametric test.」
- URL：https://fog.misty.com/perry/cod/references/yield_models.pdf
- 來源類型：論文／教材（學術講義）

---

## 2. 關卡二：WAT（晶圓允收測試）

- 做什麼：晶圓製造結束後，量測晶圓上測試結構（scribe line 內）的電性參數，檢查「製程」是否在規格內；不是測客戶的電路。
- 由誰執行：晶圓廠（台積電）產生資料並提供給客戶。
- 證據強度：【TSMC 專屬】查無；【業界通用】通用／第三方（來源為良率管理軟體廠商的科普文）。

### 2-1【TSMC 專屬】查無

- 已搜關鍵字：「TSMC wafer acceptance test」「TSMC WAT N2」「TSMC PCM process control monitor」。找到的僅有求才文章（cleverprep.com 對 TSMC 良率工程師的職缺描述），屬非官方轉述，未列為證據。

### 2-2【業界通用】WAT 的定義與資料內容

- 引文（Semiconductor Engineering，2020-03-10，Marie Ryan（yieldHUB））：「Wafer Acceptance Testing (WAT), also known as Process Control Monitoring (PCM) data, is data generated by the fab at the end of manufacturing and generally made available to the fabless customer for every wafer. The data will typically have between forty and one hundred tests, each test having a result for each site (or “drop-in”) on the wafer.」
- 引文（同文，WAT 與後段關聯）：「For example, the results for a WAT site can be correlated with the parametric and bin performance of that part of the wafer in wafer sort.」
- 引文（同文，用途）：「The limits in the data from fab will be for internal use by the fab. Using a YMS like yieldHUB you can set your own effective SPC limits so that you can spot lot-ids and wafers (like the one highlighted in Fig 3) before they cause yield loss or reliability issues later on.」
- URL：https://semiengineering.com/whats-wat-testing-at-the-end-of-manufacturing
- 來源類型：通用第三方（vendor 科普文）
- 檢查點：關鍵參數（如飽和電流 Isat）在晶圓內各 site 與批次間的一致性；超出管制界限的批次／晶圓。
- 不合格怎麼處理：查無（台積電的批次處置規則未公開；上文僅說客戶可用自訂 SPC 界限預警）。

---

## 3. 關卡三：CP／wafer sort（針測）

- 做什麼：以探針卡接觸晶圓上每顆 die，做快速電性測試，標出壞 die，避免它們被封裝。
- 由誰執行：【TSMC 專屬】台積電聲明提供 probe card 與測試方案（自做或外包的分界未公開）；【業界通用】OSAT（Amkor、日月光）也提供 wafer probe。
- 證據強度：【TSMC 專屬】官方（概括性）；N2 專屬細節查無；【業界通用】第三方。

### 3-1【TSMC 專屬】台積電的測試能力聲明

- 引文：「By utilizing TSMC's total testing solutions, including industry-leading probe card and thermal management technologies, we have established a test program development infrastructure. This enables co-development of test programs with customers to accelerate new product time-to-market. Furthermore, TSMC is advancing its vision for distributed in-process testing, which will be the cornerstone for 3DIC.」
- URL：https://www.tsmc.com/english/dedicatedFoundry/services/advanced-packaging
- 來源類型：官方
- 備註：該頁沒有逐字說明 CP（wafer sort）步驟本身；「probe card」是針測的核心耗材，但官網未明寫此處指針測。

### 3-2【業界通用】wafer sort 的作用

- 引文（AnySilicon，The Ultimate Guide to Wafer Sort）：「Wafer sort is a simple electrical test, that is perform on a silicon die while it’s in a wafer form. Wafer sort’s main purpose is to identify the non-functional dies and thereby avoiding assembly of those dies into packages. In many cases, wafer sort is a simple and quick test that focuses on a few electrical parameters that are most likely to fail.」
- URL：https://anysilicon.com/?p=4593
- 來源類型：通用第三方（IC 設計服務公司科普文，無發布日期）
- 檢查點：die 級電性通過／失敗分 bin；壞 die 標記後不進封裝。
- 不合格怎麼處理：壞 die 不封裝（同上）。

### 3-3【TSMC 專屬】3DFabric 的 die 級追蹤與 bin 管理（封裝廠側，與 CP 結果銜接）

- 引文：「In mass production, we employ an intelligent bin management system to accurately manage trillions of customer die combinations. This system fully utilizes the different grades of customer dies and produces more high-performance chiplets with consistent quality.」
- 引文：「TSMC developed the exclusive die-level MES adopted in its advanced packaging fabs, which provides instant die-level information, real-time dispatching and transfer instructions, comprehensive defect interception and classification, automated yield prediction and optimization.」
- URL：https://www.tsmc.com/english/dedicatedFoundry/services/apm_intelligent_packaging_fab
- 來源類型：官方
- 備註：台積電未明說 bin 等級來源是否為 CP 結果；此處僅呈現原文。

---

## 4. 關卡四：良率學習與缺陷密度（D0）

- 做什麼：以缺陷密度 D0 追蹤製程成熟度；D0 隨量產時間下降，良率隨之上升。
- 由誰執行：台積電。
- 證據強度：官方（法說、財報）＋媒體（研討會投影片轉述）；官方未公開 D0 數值。

### 4-1【業界通用】D0 與良率的關係（模型）

- 引文（UC Berkeley IEOR 130 講義，Leachman）：「Many die yield losses are the result of tiny defects.」；「Empirically, the Poisson yield model has been found to give accurate yield predictions for small die (when A ≤ 0.25 sq cm) and when the expected number of defects per die is low (when D0A < 1.0).」（原文符號在 PDF 轉文字時有缺漏，以 URL 原檔為準）
- URL：https://fog.misty.com/perry/cod/references/yield_models.pdf
- 來源類型：論文／教材
- 備註：Poisson、Murphy、Seeds、負二項等模型在大 die 上結果差很大；本檔不代入計算。

### 4-2【TSMC 專屬】2025 北美技術論壇（2025-04）：N2 D0 與 N3／N5／N7 同階段比較

台積電的原始投影片未在官網公開（查無）。以下為媒體轉述，**有矛盾，兩邊並列**。

- 媒體 A，Tom's Hardware（Anton Shilov，2025-04-25）：「TSMC exposed the defect density (D0) of its N2 process technology relative to its predecessors at the same stage of development at its North American Technology Symposium this week. According to the company, the defect density is below that of N3, N5, and N7 manufacturing nodes.」
  - 同文補充：「In addition, the slide published by ComputerBase reveals that N2 is two quarters away from mass production」
  - 同文曲線描述：「The N2 curve begins with higher initial defect levels than N5/N4 but declines sharply, closely matching the defect reduction trajectory of N3/N3P.」
  - URL：https://www.tomshardware.com/tech-industry/tsmc-discloses-n2-defect-density-lower-than-n3-at-the-same-stage-of-development
  - 來源類型：媒體
  - 注意：該文圖說註明「Data by TSMC, re-drawn by DALL-E/Chat-GPT」，其圖為重繪，**不是**台積電官方圖，故不列入下載。
- 媒體 B，TechPowerUp（2025-05-07，轉引台灣 Ctee 報導）：「(N2's) defect density (D0) performance is comparable to that of the 5 nm family, and even surpasses the 7 nm and 3 nm processes of the same period, making it one of the most technologically mature advanced nodes.」
  - URL：https://www.techpowerup.com/336439/tsmc-leadership-speaks-of-unprecedented-demand-for-2-nm-greater-than-previous-gen-nodes
  - 來源類型：媒體（二手轉述）
- 矛盾點：A 說低於 N3、N5、N7；B 說與 N5 相當、優於 N7 與 N3。兩者皆非原始投影片，未能裁決。
- 數值：查無官方 D0 數值。網路上流傳的「< 0.2/cm²」為論壇／分析推算，非台積電公布，不採用。
- 已搜關鍵字：「TSMC N2 defect density」「N2 D0 curve symposium」「TSMC N2 yield percent」。

### 4-3【TSMC 專屬】2026 北美技術論壇（2026-04）

- 引文（Semiconductor Engineering，2026-04-27）：「TSMC also claimed that N2 is ramping better in terms of defect density reduction than N3.」
- 引文（同文）：「TSMC is manufacturing the world's largest 5.5-reticle size CoWoS, with > 98% yield in 2026.」（媒體對台積電論壇內容的轉述）
- URL：https://semiengineering.com/tsmc-tech-symposium-2026-by-the-numbers/
- 來源類型：媒體
- 備註：「N2 已量產、超過 20 個客戶 tape-out」等同篇內容亦屬轉述，本檔未採用。

### 4-4【TSMC 專屬】法說會：N2 良率的措辭（逐字、附日期）

台積電法說只用「good yield」，**不給百分比或 D0**（已逐份搜尋 1Q26、2Q26、3Q26、4Q25 逐字稿關鍵字 yield／defect）。

- 2026-01-15（4Q25 法說，C.C. Wei）：「N2 successfully entered high volume manufacturing in 4Q 2025 at both our Hsinchu and Kaohsiung sides with good yield. We are seeing strong demand from smartphone and HPC/AI applications and expect a faster ramp in 2026.」
  - URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf
- 2026-04-16（1Q26 法說）：「Today, our new node, N2, has already entered high-volume manufacturing in the fourth quarter of 2025 with good yield. N2 is ramping successfully in multiple phases at both Hsinchu and Kaohsiung site, supported by strong demand from both smartphone and HPC/AI applications.」
  - URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf
- 2026-10-15（3Q26 法說，C.C. Wei 開場）：「Our new node, N2, has already entered a high-volume manufacturing in the fourth quarter of 2025, with good yield. N2 is ramping successfully in multiple phases at both Hsinchu and Kaohsiung sites. We expect our N2 family technology's annual capacity to more than double in 2027, supported by strong demand from both smartphone and HPC/AI applications.」
  - URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-10/eba4fac72873bf546b669bd2b5d973df5c93215d/TSMC%203Q26%20Transcript.pdf
- 2026-10-15（3Q26 Q&A，C.C. Wei 答新節點學習曲線）：「And so the learning curve, yes, but we are doing a reasonable job. And so all the customers are very happy today.」
- 2026-07-16（2Q26 法說）：N2 之後的 A14 才有量化良率（非 N2）：「Internal product-like vehicle demonstrated close to 90% device performance and close to 90% 256 megabits SRAM yield.」
  - URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-08/3e494f0c14dd0890f897aa044415e21d93486cc4/TSMC%202Q26%20Transcript.pdf
- 2026-01-15（4Q25 法說，亞利桑那，非 N2 專指）：「We built a fab in Arizona, and we worked hard, so today, everything, even the yield or defect density is almost equal to Taiwan.」

### 4-5【TSMC 專屬】N2 SRAM 良率（論文／研討會）

- 論文：G. Yeap et al., "2nm Platform Technology featuring Energy-efficient Nanosheet Transistors and Interconnects co-optimized with 3DIC for AI, HPC and Mobile SoC Applications"，IEDM，2024 年 12 月。
- 引文（SemiWiki，Scotten Jones，2025-02-10，轉述該論文）：「In the paper TSMC reports that a 256Mb SRAM array has >80% average yield and >90% peak yield.」
  - URL：https://semiwiki.com/semiconductor-services/techinsights/352972-iedm-2025-tsmc-2nm-process-disclosure-how-does-it-measure-up/
  - 來源類型：媒體（對論文的分析；未取得論文原文）
- 引文（Tom's Hardware，2024-10-31，回顧 2024 年研討會）：「yields for 256 Mb (32 MB) SRAM devices were surpassing 80% in certain batches. As of March 2024, the average yield for 256 Mb SRAM had reached approximately 70%, up significantly from around 35% in April 2023.」
  - URL：https://www.tomshardware.com/tech-industry/sram-scaling-isnt-dead-after-all-tsmcs-2nm-process-tech-claims-major-improvements
  - 來源類型：媒體
- 備註：兩者時點不同（2024 年 3 月 vs. IEDM 2024 論文），並非矛盾；SRAM 測試載具良率不等於產品良率（SemiWiki 同文亦言「There are other yield components beside those tested in an SRAM array」）。

---

## 5. 關卡五：晶圓切割與凸塊（dicing／bumping）

- 做什麼：凸塊為 flip chip／晶圓級封裝形成電性接點的步驟；切割（singulation）把晶圓分成單顆 die。
- 由誰執行：【TSMC 專屬】查無（台積電官網未提及 bumping 與 dicing 的執行方式）；【業界通用】OSAT 提供。
- 證據強度：【TSMC 專屬】查無；【業界通用】第三方（OSAT 官網）。

### 5-1【TSMC 專屬】查無

- 已搜關鍵字：「TSMC bumping」「TSMC wafer bumping N2」「TSMC dicing」「TSMC 3DFabric bump」「tsmc.com advanced packaging bumping」。tsmc.com 先進封裝頁面文字逐字檢查無 bumping、dicing。
- 間接線索：CoWoS-R 頁提到「C4 bump」「C4/underfill」（結構說明，非流程）；InFO-PoP 頁提到「no organic substrate or C4 bump」。

### 5-2【業界通用】OSAT 的凸塊與測試一站式服務

- 引文（Amkor Wafer Bumping 頁）：「Our China, Korea, Portugal and Taiwan bumping operations are co-located with wafer probe, assembly and final test, enabling Amkor to provide complete “turnkey” flip chip and WLCSP solutions in these key geographic locations.」
  - URL：https://amkor.com/services/wafer-bumping/
- 引文（Amkor WLCSP 頁）：「WLCSP includes wafer bumping (with or without pad layer redistribution or RDL), wafer level final test (probe), device singulation and packing in tape & reel to support a full turnkey solution.」
  - URL：https://amkor.com/packaging/wafer-level-packaging/wlcsp/
  - 2026-11-07 重新開啟，引文仍在原頁；方法檔 3.1 第 4 級（間接來源）。互動頁步驟 14 的「接墊」說明引用這一句。
- 來源類型：通用第三方（OSAT 官網，無發布日期）
- 備註：日月光（ASE）Bumping 頁（https://ase.aseglobal.com/?p=55）對本流程直接抓取回 403，**未能逐字核對**，僅有搜尋摘要提到其凸塊自 1999 年提供，故不列引文。
- 備註：TrendForce 轉述 ETNews 稱，CoW 外包設備投資聚焦於「dicing equipment for cutting wafers and interposers and bonding equipment」（見第 8 節，屬媒體傳聞）。

---

## 6. 關卡六：先進封裝（3DFabric 家族）與 N2 的關係

- 做什麼：把 N2 等先進製程晶片，與其他晶片（HBM、其他 chiplet）以 SoIC 3D 堆疊、CoWoS 2.5D、InFO 扇出型封裝整合。
- 由誰執行：台積電（先進後段廠）；部分步驟外包 OSAT（見第 8 節）。
- 證據強度：官方。

### 6-1【TSMC 專屬】3DFabric 的組成與命名（以官方為準）

- 引文：「TSMC 3DFabric® offers 3D silicon stacking and advanced packaging solutions, such as TSMC-SoIC®, CoWoS®, and InFO (Integrated Fan-Out), to enable homogeneous and heterogeneous chip integration to meet customer requirements for high performance, high compute density, and high energy efficiency, low latency, and high integration.」
- 引文：「TSMC 3DFabric® is the Company's comprehensive family of 3D silicon stacking and advanced packaging solutions. It encompasses TSMC's fine pitch, chip-to-chip connection leveraging of wafer processes and consists of both wafer-level frontend and backend technologies.」
- URL：https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/3DFabric.htm
- 來源類型：官方
- 官方命名：TSMC-SoIC®、CoWoS®（CoWoS-S／CoWoS-R／CoWoS-L）、InFO（InFO-PoP、InFO-oS、InFO_MS、MUST、InFO_AiP）、TSMC-SoW™。

### 6-2【TSMC 專屬】與 N2 的直接連結：SoIC

- 引文：「SoIC integrated chips can be subsquently assembled by using conventional packages or new TSMC 3DFabric® technology services, such as CoWoS® or TSMC-SoW™ ... Several ongoing developments will allow the SoIC family to unleash more innovations, including the SoIC Gen-2 process that enables advanced SoC (N2 and beyond) compatibility and compact universal photonics engine (COUPE) to enable Si photonic solution.」（原文 "subsquently" 拼字照抄）
- 引文（KGD 關卡）：「Integrating known good dies (KGDs) with different chip sizes, functionalities and wafer node technologies.」
- 引文（量產狀態）：「its 3nm chip stacking technology successfully entered volume production in 2025.」
- URL：https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm
- 來源類型：官方
- N2 特有之處：SoIC Gen-2 與 N2 以後的先進 SoC 相容（官方原文）；除此之外官網未列「N2 產品用哪種封裝」的對照表。

### 6-3【TSMC 專屬】SoIC 兩種堆疊方式

- 引文：「It supports both chip on wafer (CoW) and wafer-on-wafer (WoW) schemes.」；「TSMC-SoIC® platform is fully compatible with existing advanced packaging services such as CoWoS® and InFO, offering a powerful "3Dx3D" system-level solution.」
- URL：https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth.htm
- 引文（WoW 適用條件）：「SoIC-X wafer-on-wafer is suitable for high yielding nodes and the same die size applications or design.」（SoIC.htm）
- 檢查點：WoW 對良率要求較高（兩片晶圓對疊，壞 die 無法事先剔除；此為本檔對原文的條件句整理，原文僅說適用於高良率節點）。

### 6-4【TSMC 專屬】CoWoS 與 InFO

- 引文（CoWoS）：「TSMC's world-leading CoWoS® advanced 2.5D packaging technology provides the essential foundation for high-performance computing (HPC) and artificial intelligence (AI) products. By integrating multiple SoCs and high-bandwidth memory stacks, CoWoS® empowers products with high-performance compute and memory bandwidth.」
- 引文（CoWoS-L）：「TSMC's first CoWoS®-L at 3.5X-reticle size has been in volume production since 2024.」
- URL：https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm
- 引文（InFO）：「Integrated Fan-Out (InFO) technology is an innovative wafer-level system integration technology featuring a high-density redistribution layer (RDL) and through-InFO vias (TIVs) for high-density interconnect and performance across a variety of applications, including mobile and high-performance computing (HPC).」
- URL：https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm
- 來源類型：官方

### 6-5 N2 產品與具體封裝型式的對照【查無官方；僅媒體傳聞】

- 官方：台積電官網與法說未逐一說明哪個 N2 產品採哪種封裝，標「查無」。
- 媒體（傳聞，非台積電或客戶官方）：9to5Mac／TrendForce／TweakTown 等引供應鏈報導稱 Apple A20（N2）將由 InFO 改採 WMCM，Apple 伺服器晶片用 SoIC。URL 例：https://www.tweaktown.com/news/105968/apple-to-use-tsmcs-advanced-wmcm-and-soic-packaging-for-a20-server-chips-in-2026/index.html（來源類型：媒體，引述 DigiTimes 與 Commercial Times；本檔未逐字核對原文）。
- 官方（AMD 新聞稿，2025-04-14）僅說：「next-generation AMD EPYC processor, codenamed “Venice,” is the first HPC product in the industry to be taped out and brought up on the TSMC advanced 2nm (N2) process technology.」未提封裝。URL：https://www.taiwannews.com.tw/en/news/6085102（GlobeNewswire 全文轉載）。
- 已搜關鍵字：「N2 CoWoS」「AMD Venice N2 CoWoS MI450」「Apple A20 WMCM」。

### 6-6【TSMC 專屬】量產規模與大光罩尺寸

- 引文（3Q26 法說，2026-10-15，C.C. Wei）：「we are in the real world production of 5x reticle size. I don't believe that anybody can do that today, except the TSMC. And the yield is excellent.」
- 引文（1Q26 法說，2026-04-16，C.C. Wei）：「our advanced packaging capacity is very tight also. So we have to work with our OSAT partners.」
- URL：見 4-4 的 3Q26 與 1Q26 逐字稿。
- 來源類型：官方

---

## 7. 關卡七：最終測試（final test）與出貨

- 做什麼：封裝完成後的最後電性／功能測試，另可能含 burn-in 與系統級測試；通過者出貨。
- 由誰執行：【TSMC 專屬】台積電先進後段廠含「advanced testing」；【業界通用】OSAT（Amkor、日月光）提供 final test。
- 證據強度：【TSMC 專屬】官方（概括性）；N2 專屬及流程細節查無；【業界通用】第三方。

### 7-1【TSMC 專屬】Advanced Backend Fab 6：封裝與測試合一

- 引文（TSMC 新聞稿，2023-06-08）：「TSMC today announced the opening of its Advanced Backend Fab 6, the Company's first all-in-one automated advanced packaging and testing fab to realize 3DFabric™ integration of front-end to back-end process and testing services.」
- 引文：「Advanced Backend Fab 6 enables TSMC to flexibly allocate capacity for TSMC 3DFabric™ advanced packaging and silicon stacking technologies, such as SoIC, InFO, CoWoS and advanced testing, improving production yield and efficiency.」
- 引文：「TSMC estimates that the fab will have the capacity to produce more than 1 million 12-inch wafer equivalent 3DFabric process technology per year, and more than 10 million hours of testing services per year.」
- URL：https://pr.tsmc.com/english/news/3033
- 來源類型：官方（新聞稿）
- 檢查點：die 級追蹤與品質防線，原文：「establish a robust die-level big data quality defense network ... a complete production history for each die is constructed through die traceability.」

### 7-2【TSMC 專屬】封裝廠缺陷攔截與分類

- 引文：「TSMC has not only deployed APC to control and operate tools but also implemented Advanced Defect Classification (ADC) in the process flow, which automates the yield and quality defense control to intercept and classify defects. Furthermore, TSMC yield analysis engine using HITL and advanced algorithms detects defects and isolates defective material precisely.」
- URL：https://www.tsmc.com/english/dedicatedFoundry/services/apm_intelligent_packaging_fab
- 來源類型：官方

### 7-3 測試能量是瓶頸之一【TSMC 專屬，法說】

- 引文（2Q26 法說，2026-07-16，C.C. Wei）：「as time goes by, some of the customers' products need more tester. You cannot believe that. I mean, so the tester in shortage, so we have to put more CapEx in the tester or in the packaging or in other areas.」
- URL：https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/2026-08/3e494f0c14dd0890f897aa044415e21d93486cc4/TSMC%202Q26%20Transcript.pdf
- 來源類型：官方
- 會卡在哪：測試機台（tester）供不應求。

### 7-4【業界通用】OSAT 的最終測試與其他測試

- 引文（Amkor 測試服務頁）：「As the top OSAT supplier for high performance compute (HPC), artificial intelligence (AI) processors & automotive testing, we have an extensive array of test capabilities and significant experience in device testing. The performance envelope for burn-in and system level test has recently expanded to account for higher power and lower cost.」（頁面並列 Final Test、Wafer Probe、Burn-in 項目）
- URL：https://amkor.com/test-services/
- 來源類型：通用第三方（OSAT 官網）

### 7-5 出貨：查無

- 台積電官方文件未逐步描述「最終測試通過後如何出貨給客戶」，標「查無」。已搜關鍵字：「TSMC final test shipment」「TSMC turnkey backend」「TSMC 20-F wafer probing final testing」。
- 台積電「integrated turnkey service」頁（https://www.tsmc.com/english/dedicatedFoundry/services/apm_integrated_turnkey）直接抓取回 403；先進封裝頁摘要寫：「TSMC's integrated turnkey service provides a complete solution to resolve heterogeneous packing issues, e.g., chip-packaging-integration (CPI) issues, through intense collaboration with substrate, memory and materials suppliers.」（來源 https://www.tsmc.com/english/dedicatedFoundry/services/advanced-packaging，官方）。

---

## 8. 誰做：台積電 vs. OSAT

證據強度：官方（法說）＋媒體（供應鏈報導）；官方未逐步列出分工，且媒體說法彼此不完全一致。

### 8-1【TSMC 專屬，官方】台積電承認與 OSAT 合作

- 引文（1Q26 法說，2026-04-16，C.C. Wei）：「whenever we can or wherever we can, we want to make sure that their product can be, their demand of the product can be met by TSMCs front-end and high-end packaging. So we certainly -- let me say that our advanced packaging capacity is very tight also. So we have to work with our OSAT partners.」
- URL：見 4-4 的 1Q26 逐字稿。
- 來源類型：官方
- 4Q25 法說（2026-01-15）分析師提問亦言「we'll work more closely with OSAT partners on the leading edge advanced packaging」——此為分析師措辭，非公司說法。

### 8-2【TSMC 專屬，媒體】外包的段落：oS 為既有，CoW 為新近擴大

- 引文（TrendForce，2026-08-05，引 ETNews、Mydrivers、Mirror Daily）：「According to ETNews, sources say the company has decided to expand outsourcing of CoW (Chip-on-Wafer), a key step in its CoWoS packaging technology for AI chips, to OSAT companies including ASE. Unlike its previous practice of primarily outsourcing WoS (Wafer-on-Substrate), the latest move is intended to boost production capacity with key OSAT partners and help relieve packaging bottlenecks.」
- 引文（同文）：「OSAT companies including ASE, Amkor, and SPIL have long manufactured WoS packages under technology licenses from TSMC.」
- URL：https://www.trendforce.com/news/2026/08/05/news-tsmc-reportedly-expands-outsourcing-of-key-cowos-front-end-step-to-osats-amid-rising-nvidia-asic-demand/
- 來源類型：媒體（單一韓媒來源轉述，台積電未證實）
- 矛盾／並存說法（同文）：另一模式為客戶「continue outsourcing wafer fabrication to TSMC before shipping completed wafers directly to ASE or SPIL for end-to-end CoWoS packaging」，由客戶主導、非台積電主導（Mirror Daily 說法）。
- 名詞注意：同文以 WoS 表示「interposer 與基板接合」，一般業界亦稱 oS（on Substrate）；官方 3DFabric 頁面使用 CoWoS-S/R/L 命名，不使用 oS 作為產品名。

### 8-3 日月光（ASE）／Amkor 的能力與自述【業界通用】

- Amkor 自述見 5-2、7-4（含 wafer bumping、wafer probe、final test、burn-in、system level test）。
- ASE：直接抓取其凸塊頁面 403，無逐字引文，標「待查證」。

---

## 9. 關卡檢查點總覽（供畫圖參考，僅整理上文證據）

| 關卡 | 台積電專屬證據 | 業界通用證據 | 檢查點（來源節次） | 證據強度 |
|---|---|---|---|---|
| 線上檢測／量測 | 查無（僅 20-F 設備清單） | 有（奈米片檢測難度） | 底面缺陷非視線可及（1-2） | 通用／第三方 |
| WAT | 查無 | 有 | scribe line 測試結構參數一致性（2-2） | 通用／第三方 |
| CP 針測 | 概括性（probe card 能力） | 有 | die 級電性分 bin（3-2） | 官方（概括）＋通用 |
| 良率學習 D0 | 法說「good yield」、論壇 D0 曲線（轉述） | 有（Poisson 等模型） | D0 隨量產下降（4-2） | 官方＋媒體；無數值 |
| 切割／凸塊 | 查無 | 有（Amkor） | 查無 | 通用／第三方 |
| 先進封裝 | 有（3DFabric 頁） | — | KGD、CoW／WoW（6-2、6-3） | 官方 |
| 最終測試 | 有（Fab 6 advanced testing） | 有（Amkor） | tester 不足（7-3） | 官方＋通用 |
| 出貨 | 查無 | — | 查無 | 查無 |

---

## 10. 官方示意圖候選清單

授權／版權標示（共通）：tsmc.com 全站頁尾為「Copyright© Taiwan Semiconductor Manufacturing Company Limited 2010-2026, All Rights Reserved.」；3DFabric 頁另有「All diagrams, animations, and videos are for demonstrative and illustrative purposes only.」未見可再利用授權條款（Creative Commons 等）；使用者報告引用時視為需註明來源、非開放授權。各圖頁面為網頁，無頁碼或投影片編號（標「N/A（網頁）」）。

已下載（資料夾：（本機路徑，未隨附））：

| # | 檔名 | 圖片直接 URL | 所在頁面 URL | 頁碼 | 圖說（alt／可見內容） | 下載 |
|---|---|---|---|---|---|---|
| 1 | `soic-whats-whys-hows-infographic.jpg` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/SoIC/SoIC-Infographic-2003_V9.4.jpg | https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC_inDepth.htm | N/A（網頁） | 頁面標題「The Whats, Whys, and Hows of TSMC-SoIC®」；圖內標題「AN IN-DEPTH LOOK AT SYSTEM ON INTEGRATED CHIPS」，含 SoIC 與 2D／3D IC 的密度、速度、功耗對比；圖尾有「Presented by TSMC」標示（已目視） | 成功，1500x6250 |
| 2 | `intelligent-packaging-fab-diagram.png` | https://www.tsmc.com/system/files/inline-images/APM_Intelligent_Packaging_Fab_1_0.png | https://www.tsmc.com/english/dedicatedFoundry/services/apm_intelligent_packaging_fab | N/A（網頁） | alt「APM_Integrated_Packaging_Fab」；圖內為 Cyber Physical System：Automation→Big Data→ML，含 MES、Data Mart、Yield & Quality Defense、Machine Learning Platform（已目視） | 成功，1572x668 |
| 3 | `cowos-overview.png` | https://www.tsmc.com/sites/dcom/2026-07/CoWoS_01.png | https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm | N/A（網頁） | 無 alt；圖內：xPU 與 DRAM 分散→xPU＋HBM Stack 置於 Interposer；「CoWoS® 1. Increases bandwidth 2. Reduces power consumption 3. Smaller form factor」（已目視）。直接抓取需帶 Referer（無則 403） | 成功，870x1038 |
| 4 | `cowos-s-structure.png` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/cowos/CoWoS-s_01.png | 同上 cowos.htm | N/A（網頁） | CoWoS®-S 結構圖（依頁面 alt，未目視內容） | 成功，1200x449 |
| 5 | `cowos-l-structure.png` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/cowos/CoWoS-L_01.png | 同上 cowos.htm | N/A（網頁） | CoWoS®-L 結構圖（依頁面 alt，未目視內容） | 成功，1200x510 |
| 6 | `soic-holistic-3d-system-integration.jpg` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/SoIC/SoIC-3D-Integration.jpg | https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm | N/A（網頁） | alt「Holistic 3D System Integration」（未目視內容） | 成功 |
| 7 | `soic-chips.jpg` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/SoIC/SoIC-chips.jpg | 同上 SoIC.htm | N/A（網頁） | alt「SoIC Chips」（未目視內容） | 成功 |
| 8 | `info-os-structure.png` | https://3dfabric.tsmc.com/site_img/dedicatedFoundry/technology/InFO/InFO_oS.png | https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/InFO.htm | N/A（網頁） | alt「InFO_oS」，對應 InFO-oS（Integrated Fan-Out on Substrate）（未目視內容） | 成功，1200x420 |

未下載、僅記錄：

- InFO 一般 wafer-level packaging 圖 `InFO_WLCS_Packaging.png`：頁面 HTML 引用的路徑（/site_img/.../InFO_WLCS_Packaging.png）抓取回 404，下載失敗。
- SoIC-WoW 圖：https://3dfabric.tsmc.com/site_img/dedicatedFoundry/services/WLSI_SoIC-WoW_1.png（頁面 SoIC.htm 引用的相對路徑組出；本次已達 8 張上限，未下載、未測 URL 是否可用）。
- N2 D0 曲線：台積電原始投影片未於官網公開（查無）；Tom's Hardware 之圖為 AI 重繪，不列入官方圖。
- 台積電先進封裝頁的影片（`<video>` 來源 URL 頁面文字中未顯示）：未取得。

---

## 附：已搜關鍵字與已知缺口

- 查無或僅概括：台積電專屬的 inline inspection、WAT、CP 針測流程、切割、凸塊、最終測試步驟、出貨流程；N2 官方 D0／良率百分比；N2 產品與封裝型式的官方對照表。
- 已搜（英文）：TSMC N2 defect density、N2 yield percent、wafer acceptance test、wafer sort N2、TSMC bumping／dicing、TSMC final test、TSMC OSAT outsourcing CoWoS、20-F wafer probing final testing、AMD Venice N2 CoWoS、Apple A20 WMCM、nanosheet metrology inspection。
- 未做（時間與範圍）：中文關鍵字搜尋（如「台積電 CP 針測」）、TSMC 年報（annual report）中文版品質章節、ECTC／IEDM 封裝論文（SoIC KGD 測試）逐篇全文、ASE／SPIL 官網的 CoWoS 相關頁（ASE 頁 403）。這些為後續可補的缺口。
