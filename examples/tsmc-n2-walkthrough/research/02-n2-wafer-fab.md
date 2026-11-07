# 台積電 N2 晶圓製造技術：一手證據彙整

查證日期：2026-11-01（所有條目共用，下文簡稱「查證日」）。
性質：只交證據、不下結論。引文為原文語言逐字（≤3 句）。

## 0. 先讀這裡：證據邊界

1. **台積電官方從未公開 N2 的逐步製程流程。** 官方（官網、新聞稿、年報、IEDM 2024 論文摘要）只談：結構（nanosheet GAA）、NanoFlex、PPA、SRAM 密度、MoL／BEOL／RDL／MiM。Si/SiGe 超晶格、dummy gate、inner spacer、通道釋放、替代金屬閘極等逐步內容，**查無台積電 N2 官方揭露**。
2. 因此下文各步驟分兩欄標示：**【台積電專屬】** 與 **【業界通用 nanosheet 製程（非台積電資料）】**。通用資料來自學術論文與 IBM 專利，只說明 nanosheet 通用原理，不可當成「台積電 N2 實際做法」。
3. IEDM 2024 論文全文（IEEE Xplore，付費）未取得。台積電論文細節（6-Vt、dipole、barrier-free W、1P1E、SHP-MiM 數值）取自 Tom's Hardware、SemiWiki 等**媒體轉述**，來源類型標「媒體」，需要時應回頭對照論文全文。
4. 「N2 EUV 層數」查無官方數字；網路上有 24 層、25-30+ 層等說法皆未附台積電來源，**不採用**。

## 1. 電晶體結構與原理

### 1.1 台積電官方定位【台積電專屬】

- 官方用詞：「first-generation nanosheet transistor」（第一代奈米片電晶體）、「nanosheet」；IEDM 論文摘要用「gate-all-around nanosheet (NS) transistors」。
- 引文：「N2 technology features industry-leading first-generation nanosheet transistor technology, with full-node strides in performance and power consumption to address the increasing need for energy-efficient computing.」
  - 來源 URL：https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm （全文在頁面內嵌 JSON，列表頁只顯示截斷版）
  - 查證日 2026-11-01；來源類型：官方
- 引文：「N2 technology features TSMC's first generation of nanosheet transistor technology with full-node strides in performance and power consumption. Volume production started in 2025 as planned.」
  - 來源 URL：https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf （5.1.1 Business Scope）
  - 查證日 2026-11-01；來源類型：官方（年報）
- 引文：「Q&R also completed the process reliability qualification and product quality certification for N2 technology, the first nanosheet technology.」
  - 來源 URL：同上年報 2025 ch5
  - 查證日 2026-11-01；來源類型：官方（年報）
- 量產時點：「TSMC's 2nm (N2) technology has started volume production in 4Q25 as planned.」
  - 來源 URL：https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm ；查證日 2026-11-01；官方
- IEDM 論文（台積電研究網頁收錄的摘要）：「This industry-leading N2 logic technology features energy-efficient gate-all-around nanosheet (NS) transistors, middle-of-line and backend-of-line interconnects with densest SRAM macro of ~38Mb/mm2.」
  - 來源 URL：https://research.tsmc.com/page/logic/97.html ；論文：G. Yeap et al., IEDM 2024 Late News, Paper 2.1；查證日 2026-11-01；來源類型：論文（官方研究頁摘要）

### 1.2 nanosheet 相對 FinFET 的差異與原理【業界通用，非台積電資料；其中第一筆為 IEEE Spectrum 對台積電報導】

- 通道形狀（IEEE Spectrum，報導台積電 IEDM 演講）：「Today's transistor, the FinFET, has a vertical fin of silicon at its heart. Nanosheet or gate-all-around transistors have a stack of narrow ribbons of silicon instead.」
  - 來源 URL：https://spectrum.ieee.org/tsmc-n2 ；查證日 2026-11-01；來源類型：媒體
- 閘極靜電控制與通道寬度（同上）：「The difference not only provides better control of the flow of current through the device, it also allows engineers to produce a larger variety of devices, by making wider or narrower nanosheets.」
  - 來源 URL：https://spectrum.ieee.org/tsmc-n2 ；查證日 2026-11-01；媒體
- FinFET 的寬度離散（同上）：「FinFETs could only provide that variety by multiplying the number of fins in a device—such as a device with one or two or three fins.」
  - 來源 URL：https://spectrum.ieee.org/tsmc-n2 ；查證日 2026-11-01；媒體
- 靜電與驅動電流（學術論文，通用）：「GAA-FET has superior electrostatic controllability and improved short-channel effects suppression」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；來源類型：論文（通用）
- 驅動電流與面積（學術論文，通用）：「The fully surrounding gate can suppress short-channel effects, thus reducing device leakage, while vertically stacked sheets can deliver higher drive current without increasing the layout area」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC12844779/ ；查證日 2026-11-01；論文（通用）
- 晶向與 N/P 匹配（學術論文，通用）：「When the transistor architecture changes from FinFET to GAA-FET, the main conduction surface orientation is changed from the crystallographic plane (110) to (100), which results in an increase in the electron mobility but a decrease in the hole mobility」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 與 FinFET 的整合相似度：「GAA-SNSTs are a natural extension of FinFETs, significantly reusing legacy integration and manufacturing knowledge」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC11173960/ ；查證日 2026-11-01；論文（通用）

### 1.3 台積電 N2 電晶體層級的已揭露數字【台積電專屬，媒體轉述 IEDM 論文】

- 引文：「Collectively, these refinements yield I/CV speed gains of about 70% and 110% for N-type and P-type nanosheet transistors, respectively.」（內容：優化片厚、接面、摻質活化、應力工程並降低 Ceff）
  - 來源 URL：https://www.tomshardware.com/tech-industry/tsmc-shares-deep-dive-details-about-its-cutting-edge-2nm-process-node-at-iedm-2024-35-percent-less-power-or-15-percent-more-performance ；查證日 2026-11-01；媒體（轉述 IEDM 2024）
  - 基準：Tom's 該段未寫明 I/CV 的比較對象，**待回查論文全文**。
- 引文：「N2 nanosheet technology exhibits substantially better performance/Watt than FinFET at the low Vdd range of 0.5V- 0.6V. ... a 20% speed gain and 75% lower stand-by power at 0.5V operation.」
  - 來源 URL：https://semiwiki.com/events/351309-tsmc-unveils-the-worlds-most-advanced-logic-technology-at-iedm/ ；查證日 2026-11-01；媒體（轉述 IEDM 2024 演講）
- 引文：「As GAA nanosheet transistors feature tighter threshold voltage variation (Vt-sigma), N2 achieves about a 20mV reduction in minimum operational voltage (Vmin) for High Current (HC) macros and a 30–35mV reduction for High Density (HD) macros compared to FinFET-based designs.」
  - 來源 URL：Tom's Hardware（同 1.3 第一筆）；查證日 2026-11-01；媒體
- NanoFlex（官方）：「TSMC NanoFlex provides designers with flexibility in N2 standard cells, the basic building blocks of chip design, with short cells emphasizing small area and greater power efficiency, and tall cells maximizing performance.」
  - 來源 URL：https://pr.tsmc.com/english/news/3136 （2024-04-24 新聞稿）；查證日 2026-11-01；官方
- NanoFlex 與片寬（媒體）：「Called Nanoflex, TSMC's tech allows different logic cells built with different nanosheet widths on the same chip.」
  - 來源 URL：https://spectrum.ieee.org/tsmc-n2 ；查證日 2026-11-01；媒體
- 片數／片厚／片寬／閘極長度／堆疊層數：**查無**（台積電官方與上列媒體皆未給）。已搜關鍵字：「TSMC N2 nanosheet width thickness number of sheets」「TechInsights TSMC N2 teardown nanosheet cross-section」；TechInsights 拆解報告為付費，未取得內容。

## 2. 製程步驟（依序）

標示規則：每步都分【台積電專屬】與【業界通用】。台積電專屬為「查無」者，不代表台積電沒做，只代表沒有公開資料。

### 步驟 1　Si/SiGe 超晶格磊晶

- 做什麼：在矽基板上交替磊晶 Si 與 SiGe 層，Si 層日後成為通道片、SiGe 為犧牲層。
- 原理：利用 SiGe 與 Si 對特定蝕刻的選擇性，之後可只移除 SiGe 而留下懸空的 Si 片。
- 【台積電專屬】：**查無**。已搜：「TSMC N2 Si/SiGe superlattice epitaxy」「TSMC nanosheet epi stack」「N2 IEDM 2024 superlattice」，僅得媒體提到片厚在優化，無磊晶細節。
- 【業界通用】引文：「The dominant scheme for fabricating vertically stacked Si nanosheets includes the epitaxial growth of the Si/SiGe multilayer structure on the Si substrate and the channel release process that involves the selective removal of the sacrificial SiGe layers.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用，非台積電）
- 通用實驗參數例（僅作量級示例，非 N2）：「three cycles of the Si/SiGe multilayer were deposited on an eight-inch Si substrate using a reduced pressure chemical vapor deposition (RPCVD) apparatus, where the thickness of the Si and SiGe layers was around 9 nm, and the Ge composition in the SiGe layers was 30%」
  - 來源 URL：同上；查證日 2026-11-01；論文（通用）
- 關卡／難點：磊晶是 nanosheet 的獨有關鍵模組：「several key process modules are distinctive to GAA-SNSTs and control device performance, including epitaxial deposition Si/SiGe super-lattice, inner spacer module, and channel release process.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC11173960/ ；查證日 2026-11-01；論文（通用）
- 是否為台積電公開資料：否（通用資料）。

### 步驟 2　鰭／堆疊圖形化

- 做什麼：以硬遮罩與異向性蝕刻把超晶格切成條狀（fin-like）堆疊。
- 原理：沿用 FinFET 的鰭圖形化流程。
- 【台積電專屬】：**查無**（含是否用 EUV 圖形化此層）。已搜：「TSMC N2 EUV layers」「TSMC N2 fin patterning」。
- 【業界通用】引文：「The designed test pattern was transferred to the Si/SiGe multilayer structure by anisotropic etching using the inductively coupled plasma (ICP) machine.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點：**查無專屬資料**；通用面見步驟 6（堆疊後應力導致形變）。
- 是否為台積電公開資料：否。

### 步驟 3　Dummy gate 與閘極側壁

- 做什麼：先做犧牲（dummy）閘極定義位置，之後在高溫 S/D 步驟後再以真正的金屬閘極替換。
- 原理：避免高 k／金屬閘極承受 S/D 高溫（replacement metal gate 流程）。
- 【台積電專屬】：**查無**。已搜：「TSMC N2 dummy gate」「TSMC N2 replacement metal gate」。
- 【業界通用】引文（流程圖說明）：「( e ) source and drain epitaxial growth; ( f ) dielectric deposition and planarization; ( g ) dummy gate removal and silicon nanowires formation; ( h ) filling and planarization of high-K metal gates」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC7221596/ （Figure 1 圖說）；查證日 2026-11-01；論文（通用）
- 關卡／難點（通用）：「the effective gate length of the GAA NSFET is determined not only by the critical dimension (CD) of the dummy gate but also by the thickness of the inner spacer」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC12844779/ ；查證日 2026-11-01；論文（通用）
- 是否為台積電公開資料：否。

### 步驟 4　Inner spacer（腔體蝕刻、介電沉積、回蝕）

- 做什麼：在 S/D 凹槽處把 SiGe 層側向蝕出淺腔，填入介電質並回蝕，形成閘極與 S/D 之間的內側隔離。
- 原理（通用）：「The inner spacer is proposed to reduce the parasitic capacitance between the gate and the source/drain, while providing a physical separation to protect the source/drain epitaxy from etch erosion during channel release.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC11173960/ ；查證日 2026-11-01；論文（通用）
- 製程組成（同上）：「The inner spacer module consists of cavity etch of the sacrificial SiGe layers followed by dielectric deposition and etch back.」
- 【台積電專屬】：**查無**。已搜：「TSMC N2 inner spacer」「TSMC nanosheet inner spacer low-k」。台積電研究網頁有 2D 材料 nanosheet 論文提到 inner spacer 模組，但那是 MoS2 研究元件，非 N2：https://research.tsmc.com/page/logic/59.html （僅提醒，不作 N2 證據）。
- 關卡／難點（通用，量化例）：「The process achieved good interlayer uniformity of cavity depth (cavity depth ≤ 5 ± 0.3 nm), while also obtaining a near-ideal rectangular SiGe etch front shape (inner spacer shape = 0.84) and little Si loss (0.44 nm@ each side).」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC11173960/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點（通用，選擇比）：「the average SiGe/Si etching selectivity is ~56, the inner spacer shape index is 0.92 and the local etching distance variation is only 0.65 nm across different layers.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC12844779/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點（通用，介電質回蝕）：「Silicon nitride inner spacer etch has a high etch selectivity ratio, exceeding 100:1 to Si and more than 30:1 to SiO 2 .」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC7221596/ ；查證日 2026-11-01；論文（通用）
- 是否為台積電公開資料：否。

### 步驟 5　源汲極（S/D）磊晶

- 做什麼：在 inner spacer 形成後，於凹槽內磊晶成長 S/D。
- 原理：S/D 對通道提供摻質與（PMOS 常見）應力；inner spacer 負責保護它免於釋放步驟損傷。
- 【台積電專屬】：N2 論文摘要提及「dopant activation、junction、stress engineering」屬優化項（見 1.3 的 I/CV 引文），但**S/D 磊晶材料、結構細節：查無**。已搜：「TSMC N2 source drain epi」。
- 【業界通用】引文：「( e ) source and drain epitaxial growth;」（流程）：來源 https://pmc.ncbi.nlm.nih.gov/articles/PMC7221596/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點（通用）：「the quality of source/drain epitaxy would be impacted by the damaged end of the Si nanosheet, thus raising the contact resistance」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC12844779/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點（通用，應力副作用）：「The effect of the source/drain compressive stress on the mechanical stability of stacked Si nanosheets (NS) during the process of channel release has been investigated.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 是否為台積電公開資料：否（僅「應力工程」為台積電專屬的籠統敘述，媒體轉述）。

### 步驟 6　Dummy gate 移除與通道釋放（SiGe 選擇性蝕刻）

- 做什麼：移除 dummy gate 後，以選擇性蝕刻去除 SiGe 犧牲層，讓 Si 片懸空，閘極得以環繞。
- 原理（通用）：「fluorine neutral species preferentially react with SiGe due to the higher Si-Si bond energy (2.31 eV) compared to the Si-Ge bond energy (2.12 eV) [ 28 ], achieving a high selective removal of SiGe layers.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 【台積電專屬】：**查無**（含是否採用乾式／濕式、選擇比）。已搜：「TSMC N2 channel release」「TSMC nanosheet release SiGe etch」。2024 年報僅提研究面的「nanosheet release process」用於 MoS2 研究元件，非 N2 量產：https://investor.tsmc.com/static/annualReports/2024/english/pdf/2024_tsmc_ar_e_ch5.pdf
- 關卡／難點一，釋放後形變（通用）：「The finite element simulation showed that the stress caused serious deformation of the nanosheets, which was also confirmed by the experiment.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 關卡／難點二，片距不均連動 Vt（同上）：「The unequal spacing between nanosheets results in differences in the thickness of the subsequently deposited work function metal, which results in differences in device threshold voltages」
- 關卡／難點三，選擇比與 Si 損耗：「a selectivity of 168:1 for Si 0.7 Ge 0.3 versus Si」；多寬度需求：「channel release of nanosheets with a multi-width from 30 nm to 80 nm with little Si loss」（同上；NanoFlex 需要多片寬同時釋放，此為通用文獻的對應說法，不是台積電聲明）。
- 關卡／難點四，濕蝕刻不適用高深寬比：同文以 capillary effect 說明（原文：「Wet etching is unstable in a high-aspect-ratio structure due to the influence of the capillary effect」）。來源同上；論文（通用）
- 是否為台積電公開資料：否。

### 步驟 7　替代金屬閘極：高 k／金屬閘極、功函數金屬、多重臨界電壓

- 做什麼：在懸空片外圍以 ALD 包覆高 k 介電與功函數金屬，再填金屬閘極；以不同厚度／組成／偶極（dipole）調出多種 Vt。
- 原理（通用）：「the high K dielectric and metal gate (HKMG) were uniformly wrapped on the nanosheets by atomic layer deposition (ALD) technology.」
  - 來源 URL：https://pmc.ncbi.nlm.nih.gov/articles/PMC9920338/ ；查證日 2026-11-01；論文（通用）
- 【台積電專屬】N2 Vt 規格（媒體轉述 IEDM）：「The technology also includes six voltage threshold levels (6-Vt) spanning a 200mV range, achieved using TSMC's third-generation dipole-based integration with both n-type and p-type dipoles.」
  - 來源 URL：https://www.tomshardware.com/tech-industry/tsmc-shares-deep-dive-details-about-its-cutting-edge-2nm-process-node-at-iedm-2024-35-percent-less-power-or-15-percent-more-performance ；查證日 2026-11-01；媒體
- 【台積電專屬】另一媒體同義：「With six Vt offerings spanning 200mV, N2 provides unprecedented design flexibility」
  - 來源 URL：https://semiwiki.com/events/351309-tsmc-unveils-the-worlds-most-advanced-logic-technology-at-iedm/ ；查證日 2026-11-01；媒體
- 台積電早期 multi-Vt 研究（非 N2，節點未明，同為台積電研究網頁摘要）：「For the first time, multiple-Vt (multi-Vt) device options with Vt range> 250 mV are achieved in standard cells at dimensions beyond 7nm technology node.」
  - 來源 URL：https://research.tsmc.com/english/research/logic/transistor-structure/publish-time-1.html ；查證日 2026-11-01；論文（官方研究頁摘要）；論文標題與年份待查證，不能當作 N2 證據。
- 功函數金屬材料、層數、厚度：台積電 **查無**。
- 關卡／難點（通用，IBM 專利文字，Google Patents 轉載；專利受讓人 International Business Machines Corporation）：「Isotropic etching can remove the first work function metal from between the nanosheets of the FET that requires the second work function metal.」「The isotropic etch will etch away the work function metal from between the sheets of the target FET, but at the same time it will follow the layer of work function metal to the adjacent FET, creating an undercut.」
  - 來源 URL：https://patents.google.com/patent/US10410933B2/en ；查證日 2026-11-01；來源類型：專利（通用，非台積電）
- 是否為台積電公開資料：部分（6-Vt 與 dipole 為台積電論文內容，經媒體轉述）。

### 步驟 8　中段（MoL）：接點與閘極接點

- 做什麼：S/D 接點與閘極接點（VG）將電晶體引到金屬層。
- 【台積電專屬】（媒體轉述 IEDM 2024）：「N2's MoL now uses barrier-free tungsten wiring, which reduces vertical gate contact (VG) resistance by 55% and increases the ring oscillator's frequency by about 6.2%.」
  - 來源 URL：https://www.tomshardware.com/tech-industry/tsmc-shares-deep-dive-details-about-its-cutting-edge-2nm-process-node-at-iedm-2024-35-percent-less-power-or-15-percent-more-performance ；查證日 2026-11-01；媒體
  - 比較基準：Tom's 未寫比較對象（推定為前一世代 MoL 方案），**待回查論文**。
- 台積電官方圖（論文 Fig.11 圖內文字）：「MoL/BEOL offering ~20% RC reduction and optimized rules for densest designs」（見第 4 節圖檔 iedm2024-fig11）。
- 關卡／難點：**查無**台積電專屬揭露；通用的 S/D 接點電阻議題見步驟 5。
- 是否為台積電公開資料：是（論文），媒體轉述。

### 步驟 9　後段（BEOL）、遠後段、Cu RDL、超高效能 MiM 電容

- 官方（官網）：「TSMC also developed low-resistance redistribution layer (RDL) and super high-performance metal-insulator-metal (MiM) capacitors to further boost performance.」
  - 來源 URL：https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_2nm ；查證日 2026-11-01；官方
- 官方（年報）：「The Company also developed low resistance redistribution layer (RDL) and super high performance metal-insulator-metal (MiM) capacitors to further boost performance for the 2nm process family.」
  - 來源 URL：https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf ；查證日 2026-11-01；官方（年報）
- 論文摘要（官方研究頁）：「N2 platform technology, equipped a new Cu scalable-RDL (sRDL), flat passivation and TSVs, co-optimizes holistically with 3DFabricTM technology enabling system integration/ scaling for AI/mobile/HPC product designs.」
  - 來源 URL：https://research.tsmc.com/page/logic/97.html ；查證日 2026-11-01；論文
- 【台積電專屬】數值（媒體轉述 IEDM）：「N2 employs all-new middle-of-line (MoL), back-end-of-line (BEOL), and far-BEOL wiring to cut resistance by 20% and improve performance efficiency.」；「N2 cuts metal (My) and via (Vy) resistance by 10%.」；「super high-performance MiM (SHP-MiM) capacitors providing around 200fF/mm² of capacitance, which helps achieve higher maximum operating frequencies (Fmax) by reducing transient voltage droop.」
  - 來源 URL：Tom's Hardware（同步驟 7）；查證日 2026-11-01；媒體
  - 交叉佐證：論文 Fig.11 圖內文字「~> 200fF/mm² SHP-MiM with Cu RDL for robust power delivery」（圖檔 iedm2024-fig11，台積電論文圖，經 Tom's 轉載）
- 金屬層間距（M1 pitch 等）：**查無**。已搜：「TSMC N2 metal pitch M1 pitch CPP」「TechInsights N2」；僅得無來源的社群數字，不採用。
- 3D 整合（相關但屬他人範圍）：「SoIC bond pitch of 4.5 μm」（Tom's，媒體）。
- 關卡／難點：**查無**專屬揭露。
- 是否為台積電公開資料：是。

### 步驟 10　微影：EUV 的用法

- 【台積電專屬】（媒體轉述 IEDM）：「the first metal layer (M1) is now created in one EUV exposure pass followed by a single etch step (1P1E), reducing complexity, lowering mask counts, and improving overall process efficiency. TSMC says that using EUV 1P1E for M1 cuts standard cell capacitance by nearly 10% and saves several EUV masks.」
  - 來源 URL：https://www.tomshardware.com/tech-industry/tsmc-shares-deep-dive-details-about-its-cutting-edge-2nm-process-node-at-iedm-2024-35-percent-less-power-or-15-percent-more-performance ；查證日 2026-11-01；媒體
- 官方（年報）：「The lithography R&D team made progress in enhancing process yield and performance, continuously improving the application efficiency of EUV scanners, reducing overlay errors, mitigating material defects, and developing and applying new mask pellicles and blanks.」（談 2025 年 2nm 支援，無層數）
  - 來源 URL：https://investor.tsmc.com/static/annualReports/2025/english/pdf/2025_tsmc_ar_e_ch5.pdf ；查證日 2026-11-01；官方（年報）
- EUV 總層數：**查無官方數字**。已搜：「TSMC N2 number of EUV layers」「N2 EUV masks count」；搜尋結果中的 24 層、25-30+ 層皆無台積電出處，未採用。
- High-NA：官方年報僅說「began developing lithography technology for high numerical-aperture (High-NA) EUV scanners」，未指定用於 N2（2025 年報同段）。

## 3. PPA 數字（逐字，含比較基準與矛盾）

所有數字逐字照抄；基準為各來源自己寫的版本。

| 來源 | 逐字原文 | 比較基準（原文） | 類型 |
|---|---|---|---|
| 官方新聞稿 2022-06-16 | 「10-15% speed improvement at the same power, or 25-30% power reduction at the same speed」 | 「over N3」 | 官方 |
| 官方新聞稿 2023-04-26 | 「up to 15% speed improvement over N3E at the same power, and up to 30% power reduction at the same speed, and greater than 1.15X chip density」 | N3E | 官方 |
| IEDM 2024 論文摘要 | 「15% speed gain or 30% power reduction with >1.15x chip density increase」 | 「previous 3nm node [2]」（未寫 N3E） | 論文 |
| IEDM 2024 Fig.3 | 「N2 NanoFlex HD cells gain 14~15% speed@power vs. N3E FinFlex 2-1 fin cell across Vdd range: 35% power saving at higher voltage and 24% power saving at lower voltage」 | N3E FinFlex 2-1 fin cell；Arm A715 | 論文圖說 |
| 官方（官網 N2P） | 「approximate 18% performance boost, reduces power consumption by approximately 36%, and increase transistor density by around 20% compared to N3E」 | N3E | 官方 |
| 官方（HPC 頁 N2P） | 「18% speed improvement at the same power, a 36% power reduction at the same speed, 1.2 times logic density, and 1.15 times chip density over N3E」 | N3E | 官方（見註） |

各筆來源 URL（查證日皆為 2026-11-01）：

1. 2022 新聞稿：https://pr.tsmc.com/english/news/2939 （原文另有「N2 will feature nanosheet transistor architecture to deliver a full-node improvement in performance and power efficiency」）
2. 2023 新聞稿：https://pr.tsmc.com/english/news/3021
3. 論文摘要：https://research.tsmc.com/page/logic/97.html （原文另含「SRAM macro of ~38Mb/mm2」「N2P, 5% speed enhanced version of N2 with full GDS compatibility」）
4. Fig.3：圖檔 iedm2024-fig3（第 4 節）；媒體文字版：https://www.blog.baldengineering.com/2024/10/tsmc-2nm-platform-technology-featuring.html
5. 官網 N2P：https://www.tsmc.com/english/dedicatedFoundry/technology/platform_smartphone_tech_advancedTech
6. HPC 頁 N2P：https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_advancedTech 。註：本機 HTTP 抓取被站方 403，未規避；此筆文字由網頁讀取工具的摘要取得，**逐字待核對**。

### 3.1 矛盾與口徑差（兩邊都列）

- **基準不一致**：2022 新聞稿比 N3；2023 新聞稿比 N3E；IEDM 2024 論文摘要寫「previous 3nm node」並以 [2] 引文，Fig.3 又用 N3E FinFlex 2-1 fin 為基準。
- **功耗降幅**：新聞稿「up to 30%」；2022 稿「25-30%」；論文摘要「30%」；論文 Fig.3「24%／35%」（電壓不同）。Tom's 寫「24 to 35% power reduction or 15% performance improvement at the same voltage」，與新聞稿文字不同，屬媒體整合說法。
- **效能**：新聞稿「up to 15%」，2022 稿「10-15%」，論文 Fig.3「14~15%」。
- **密度**：官方一律「greater than 1.15X chip density」（晶片密度）；IEEE Spectrum 稱「increasing density by 15 percent」。官方未在 N2 頁給純邏輯密度數字；N2P 頁才給「1.2 times logic density」。
- **混合密度定義**：搜尋結果提到官方腳註將 1.15x 定義為 50% logic、30% SRAM、20% analog 的混合設計；該腳註原文**未在本次直接取得**，標「待查證」，此說法僅見於搜尋結果摘要（某媒體對 N2 量產的報導），出處未確認、未驗證，勿引用。
- **SRAM**：論文「densest SRAM macro of ~38Mb/mm2」；Fig.13 標 37.9 Mb/mm²，7nm 25.0、5nm 32.2、3nm 34.1；IEEE Spectrum 稱「38 megabits per square millimeter, or an 11 percent boost over the previous technology, N3」。
- **後續變體（供比對，非 N2 本身）**：A16 vs N2P「8-10% speed improvement at the same Vdd」「15-20% power reduction」「up to 1.10X chip density」（https://pr.tsmc.com/english/news/3136）；A14 vs N2「up to 15% speed improvement at the same power, or up to 30% power reduction at the same speed, along with more than 20% increase in logic density」（https://pr.tsmc.com/english/news/3228）；N2U vs N2P「speed gains of 3-4% or power reduction of 8-10% and a 1.02-1.03X logic density improvement」，排定 2028 年量產（https://pr.tsmc.com/english/news/3302）。

## 4. 官方示意圖候選清單

說明：台積電官網的 N2 頁面**沒有 N2 專屬示意圖**（頁面只有節點總圖與 3nm 晶圓廠照片）。電晶體剖面圖（nanosheet TEM／示意）、製程步驟圖：**查無官方公開圖**；已搜：台積電官網與新聞稿頁內所有圖檔、research.tsmc.com 頁。可得的 N2 專屬圖為 IEDM 2024 論文圖，經 Tom's Hardware 轉載（圖說標示「Image credit: TSMC via IEDM」）。**這 4 張不是台積電自家網站托管，著作權屬台積電／IEEE，使用前請自行確認授權。**

| 檔名 | 圖的直接 URL | 所在頁面 | 圖號／頁碼 | 圖說 | 版權標示 |
|---|---|---|---|---|---|
| tsmc-process-technology-nodes-roadmap.png | https://www.tsmc.com/sites/dcom/2026-07/Process-Technology-Nodes_260709.png | https://www.tsmc.com/english/dedicatedFoundry/technology/logic | 無頁碼 | 製程節點總圖，含 2nm、A16、A14、A12 的 TEM 縮圖；非 N2 專屬 | 台積電官網，頁尾「Copyright© Taiwan Semiconductor Manufacturing Company Limited 2010- , All Rights Reserved.」 |
| iedm2024-fig11-n2-cu-rdl-mim-beol-stack.png | https://cdn.mos.cms.futurecdn.net/8giiqkGMACbw4YDKxtFc3J.png | Tom's Hardware 該文（見 2 步驟 7 URL） | 論文 Fig.11 | 「N2 new Cu RDL and passivation provide seamless integration with 3DFabric (SoIC, INFO and CoWoS) tech」；剖面標示 Cu RDL、SHP-MiM、MoL/BEOL、NS 電晶體層 | 「Image credit: TSMC via IEDM」 |
| iedm2024-fig3-n2-nanoflex-vs-n3e-power-speed.png | https://cdn.mos.cms.futurecdn.net/vgpBopYdqTqUPrs68GXiDJ.png | 同上 | 論文 Fig.3 | 「N2 NanoFlex HD cells gain 14~15% speed@power vs. N3E FinFlex 2-1 fin cell across Vdd range: 35% power saving at higher voltage and 24% power saving at lower voltage」 | 同上 |
| iedm2024-fig1-n2-perf-per-watt-per-mm2.png | https://cdn.mos.cms.futurecdn.net/s7i7uhEMLjDGSSwiVTbirH.png | 同上 | 論文 Fig.1 | 「N2 NanoFlex accelerates energy-efficient compute」（Perf/Watt/mm² 自 N28 至 N2，>140X） | 同上 |
| iedm2024-fig13-n2-sram-macro-density.png | https://cdn.mos.cms.futurecdn.net/TCEQ2jfkUU8uGkzjGAi2iH.png | 同上 | 論文 Fig.13 | 「N2 offers highest SRAM macro density ~38Mb/mm2」（7nm 25.0、5nm 32.2、3nm 34.1、2nm 37.9） | 同上 |

下載位置：（本機路徑，未隨附），共 5 張（<=10），全部成功，已逐張開檢確認內容與上表一致。

其他有用但未下載（無關圖或需付費）：

- 台積電 2024 技術論壇新聞稿 PDF（文字，非圖）：https://pr.tsmc.com/system/files/newspdf/attachment/34a0127e5c396217a02a97ee58c481b168437a1a/2024%20Tech%20Symposium%20%28E%29_final_wmn.pdf
- SemiWiki 轉載圖 N2-NanoFlex-HD-cell-benefits.png（與 Fig.3 同內容，略）：https://semiwiki.com/wp-content/uploads/2024/12/N2-NanoFlex-HD-cell-benefits.png
- IEDM 官方 press kit 與 IEEE Xplore 論文全文：未取得（press kit 頁面未取得 PDF 連結，Xplore 需訂閱）。nanosheet 剖面 TEM 圖應在論文內，建議使用者以機構權限取得。

## 5. 步驟證據強度一覽

| 步驟 | 台積電專屬證據 | 通用資料 |
|---|---|---|
| 電晶體結構 | 官方（官網、年報、論文摘要）；片數、片寬、片厚查無 | 論文、IEEE Spectrum |
| 1 Si/SiGe 磊晶 | 查無 | 論文 |
| 2 鰭／堆疊圖形化 | 查無 | 論文 |
| 3 Dummy gate | 查無 | 論文 |
| 4 Inner spacer | 查無 | 論文 |
| 5 S/D 磊晶 | 查無（僅「應力工程」籠統提及，媒體） | 論文 |
| 6 通道釋放 | 查無 | 論文 |
| 7 HKMG／WFM／多 Vt | 論文轉述（6-Vt、dipole；媒體） | 論文、IBM 專利 |
| 8 MoL | 論文轉述（barrier-free W、VG −55%；媒體） | 無 |
| 9 BEOL／RDL／MiM | 官方（RDL、SHP-MiM）；數值為媒體轉述論文 | 無 |
| 10 EUV | 論文轉述（M1 1P1E；媒體）；總層數查無 | 無 |

## 6. 已搜關鍵字與已知缺口

- 已搜：TSMC N2 nanosheet IEDM 2024；N2 NanoFlex；N2 inner spacer／channel release／superlattice／dummy gate／RMG／S/D epi；N2 EUV layers；N2 metal pitch；TechInsights N2 teardown；tsmc.com N2／N2P／A16／A14 頁；2022-2026 年各屆技術論壇新聞稿；2024、2025 年報第 5 章。
- 缺口一：IEDM 2024 論文全文未取得，Vt／MoL／EUV 細節皆為媒體轉述。
- 缺口二：台積電 2025 年北美技術論壇的 N2 官方簡報頁（含混合密度腳註）未取得。
- 缺口三：MDPI Electronics 2022 IBM GAA nanosheet 流程綜述（https://www.mdpi.com/2079-9292/11/21/3589 ）被站方 403，未規避，未使用。
- 缺口四：台積電官方 N2 電晶體剖面圖、製程步驟圖：查無。
