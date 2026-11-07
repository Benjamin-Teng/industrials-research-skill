# 03 節點演變與未來藍圖（N7 → N2 → A14/A12，含 Samsung／Intel 對照）

- 查證日期：**2026-11-01**（本檔所有來源皆於該日取得；PDF 逐字稿的換行已合併，引文不改字）
- 範圍：只交證據，不下結論。論斷格式為「引文（原文）｜來源編號」；來源編號對應第 10 章來源登記表（含 URL、發布日、類型、查證日）。
- 標示規則：【已發生】＝公司已宣稱完成的事實；【預告】＝公司對未來的時程／規格宣稱；【媒體】＝非官方來源；【查無】＝列出已搜關鍵字。
- 表格欄數皆 ≤7。

## 0. 先看這幾點（會影響後續詮釋的證據衝突或修改）

1. **A16 時程出現兩種官方口徑**：台積電 4Q25 法說（2026-01-15）仍說「Volume production is on track for second half 2026」；2026-04 技術論壇後，SemiEngineering（2026-04-27）稱簡報路線圖把 A16 移到 2027，Tom's Hardware（2026-04-22）引述台積電高層「ready for production in 2026… volume production to begin in 2027」；但 tsmc.com 2026-07 版節點圖仍把 A16 標在 2026，HPC 頁仍寫「production ready in 2026」。兩邊都列在 4.A16。
2. **N2 的 PPA 口徑曾三度改寫**（2022-07 → 2023-04 → 2024-07 起），主要是功耗下限（20% → 25%）與密度定義（logic density → chip density）。見 3.N2。
3. **A14 的密度口徑也改過**：2025-04 新聞稿「more than 20% increase in logic density」→ 2025-07 起法說「about 20% chip density gain」→ 2026-04／07「close to 20% chip density gain」。
4. **背面供電最早是 N2 的選配（2024-01：N2 + backside power rail、2026 量產），2024-04 改成獨立節點 A16**；A14 上的背面供電先稱「Super Power Rail offering planned for 2029」（2025-07），2026-04 命名為 A12。
5. **N2 量產地點的官方說法變過**：2023-01 說 N2 在「Hsinchu and Taichung Science Park」，2024-01 起改為「Hsinchu and Kaohsiung」。「寶山」字樣在台積電官方文件中【查無】。
6. **N2 營收占比（法說）**：2Q26 占晶圓營收 3%，3Q26 占 8%。

## 1. 節點總表

### 表 1-A：電晶體架構、關鍵技術、首批應用（【已發生】為主）

| 節點 | 電晶體 | 關鍵新技術 | 官方首批應用領域 | 證據強度 |
|---|---|---|---|---|
| N7（含 N7+、N6） | FinFET | N7+ 為「first commercially available … EUV-enabled」商用製程；N7 本身是否用 EUV 官方頁面【查無】明文 | 手機＋HPC 兩條軌道 | 強（官方頁面存檔） |
| N5（含 N5P、N4） | FinFET | EUV（「second available EUV process」） | smartphone＋HPC | 強（官方頁面存檔） |
| N3（N3E／N3P／N3X） | FinFET | N3 FINFLEX；官方頁面未明寫 EUV 層數 | smartphone＋HPC | 強 |
| N2 | nanosheet（第一代 GAA） | NanoFlex（短／高 cell 混用） | smartphone＋HPC/AI | 強 |
| N2P | nanosheet | 與 N2 同設計規則，裝置 +5% | smartphone＋HPC | 中（量產宣告【查無】） |
| N2X | nanosheet | 超高效能標準 cell＋高速裝置 | HPC | 中（時程僅媒體） |
| N2U | nanosheet | DTCO | AI／HPC／mobile | 強（新聞稿，預告） |
| A16 | nanosheet | Super Power Rail（背面供電） | HPC（複雜訊號＋密集供電） | 強（規格）／弱（時程有衝突） |
| A14 | 第二代 nanosheet | NanoFlex Pro | smartphone＋HPC/AI | 強 |
| A13 | 第二代 nanosheet | A14 直接 shrink | AI／HPC／mobile | 強（新聞稿，預告） |
| A12 | 第二代 nanosheet | 第二代背面供電（A14 平台＋SPR） | AI／HPC | 強（新聞稿，預告）；PPA【查無】 |

### 表 1-B：官方 PPA 宣稱（每列皆含比較基準）

| 節點 | 速度（同功耗） | 功耗（同速度） | 密度 | 比較基準 | 公布日／來源 |
|---|---|---|---|---|---|
| N7 | 最高 +30% | −55% | 3× logic density | vs N16 | 現行頁面（無日期）S06 |
| N7 | ~+20% | ~−40% | 1.6× logic density | vs 10nm | 頁面存檔 2021-05-08 S10 |
| N5 | ~+15% | ~−30% | （官方頁面【查無】） | vs N7 | 頁面存檔 2021-05-08 S09 |
| N5（同一頁後版） | ~+20% | ~−40% | — | vs N7 | 頁面存檔 2023-02-03 S12（2021 版把此數字寫給 N5P） |
| N3 | 最高 +15% | 最高 −30% | 最高 +70% logic density | vs N5 | 頁面存檔 2021-07-02／2022-05-31 S11 |
| N3E | ~+20% | >−30% | ~1.6× logic density | vs N5 | 現行頁面 S06 |
| N3P | +5%（同 leakage） | −5~10% | 1.04× chip density | vs N3E | 2023-04-26 S04 |
| N3X | +5%（1.2V） | — | 同 N3P | vs N3P | 2023-04-26 S04 |
| N2 | +10~15% | −25~30% | >15% chip density | vs N3E | 法說 2024-07-18 起 S28／S32 |
| N2P | +18% | −36% | 1.2× logic／1.15× chip | vs N3E | 現行 HPC 頁（無日期）S05 |
| A16 | +8~10%（同 Vdd） | −15~20% | 最高 1.10× chip density（1.07~1.10×） | vs N2P | 2024-04-24 S03；法說 2025-07-17 S32 |
| N2U | +3~4% | −8~10% | 1.02~1.03× logic density | vs N2P | 2026-04-22 S01 |
| N2A | +15~20%（同功耗） | — | — | vs N3A | 2026-04-22 S01 |
| A14 | +10~15% | −25~30% | 接近 20% chip density（初版：>20% logic density） | vs N2 | 法說 2026-04-16 S35；新聞稿 2025-04-23 S02 |
| A13 | 「performance gains」（未給數字） | 「power efficiency」（未給數字） | 面積 −6% | vs A14 | 2026-04-22 S01 |
| A12 | 【查無】官方數字 | 【查無】 | 【查無】 | — | S01 僅稱 A14 平台＋SPR |

### 表 1-C：量產／預計量產時程（已發生 vs 預告）

| 節點 | 已發生（日期、來源） | 公司預告（現行） | 時程曾被修改？ |
|---|---|---|---|
| N7 | 2018 量產（S07）；N7+ 2019 全面量產（S10） | — | 查無修改證據 |
| N5 | 風險試產 2019-03；量產 2020 上半年（S09） | — | 查無修改證據 |
| N3 | 量產「late fourth quarter」2022（2023-01-12 法說 S22） | — | N3E 時程微調（見 3.N3） |
| N3E／N3P／N3X | N3E 2023Q4 量產（S26）；N3X 2025 量產、N3C 2026 量產（S07） | N3P 原預告 2H24（S04） | N3E：2022-07「約 N3 後 1 年」→ 2022-10「可能提早 2–3 個月」→ 2023Q4 |
| N2 | 2025Q4 量產（S07、S34） | — | 2022-07 起一貫「2025」；實際 4Q25，查無延後 |
| N2P | — | 2H26 量產（S28→S34，最後一次明說 2026-01-15） | 1Q26 起法說不再重述；量產宣告【查無】 |
| N2X | — | 官方時程【查無】；媒體稱 2027（S50） | — |
| N2U | — | 2028 量產（S01） | 首次公布 |
| A16 | — | 見 4.A16（2026／2027 兩種說法） | **有衝突** |
| A14 | — | 風險試產 2027、量產 2028（S36、S37） | 2028 一貫；風險試產 2027 為 2026-07 新增細節 |
| A13、A12 | — | 2029（S01、S36） | A12 前身為「A14 + SPR 2029」（S32） |

## 2. N7、N5（舊世代，供時間軸）

### N7【已發生】

- 引文：「In 2018, TSMC became the first foundry to start 7nm FinFET (N7) volume production.」｜S07（來源類型：官方；現行頁面）
- 引文：「Compared to its 10nm FinFET process, TSMC's 7nm FinFET features 1.6X logic density, ~20% speed improvement, and ~40% power reduction. TSMC set another industry record by launching two separate 7nm FinFET tracks: one optimized for mobile applications, the other for high performance computing applications.」｜S10（官方頁面存檔 2021-05-08）
- 引文：「N7+ technology is the first commercially available extreme ultraviolet EUV-enabled foundry manufacturing process technology in the world.」；「7nm FinFET plus (N7+) technology entered full-scale production in 2019」｜S10
- 引文：「TSMC’s 7nm (N7) technology delivers up to a 30% speed improvement, a 55% power saving, and 3 times logic density improvement over 16nm (N16).」｜S06（現行頁面，基準為 N16）
- N6（供參）：「N6 manufacturing process delivers 18% higher logic density over the N7 process.」｜S10

### N5【已發生】

- 引文：「The momentum at 5nm node was carried on well into volume production which started in the first half of 2020. Compared to 7nm FinFET (N7) technology, N5 technology offers about 15% speed improvement or about 30% reduction in power consumption.」｜S09（官方頁面存檔 2021-05-08）
- 引文：「TSMC's 5nm process technology is TSMC's second available Extreme Ultraviolet lithography (EUV) process technology, and is TSMC's newest offering with highest transistor density.」｜S09
- 引文：「Upon entering risk production in March 2019, this world-leading technology received multiple customer product tape-outs, with both mobile and high performance computing products.」｜S09
- **來源矛盾（同一官網頁面不同版本）**：2021 版把「roughly 20% speed improvement or about 40% reduction in power consumption compared with the 7nm process」寫給 N5P（S09）；2023-02-03 版改寫成「N5 technology provides about 20% faster speed than N7 technology or about 40% power reduction」（S12）。兩版並陳，原因官方未說明。
- 引文：「Extreme ultra-violet (EUV) lithography makes N5 mask layers and process complexity more manageable.」｜S06
- N4 / N4P（供參）：「N4P provides an 11% performance boost compared to N5 and entered volume production in 2023.」｜S06

## 3. N3 與 N2 家族

### N3（含 N3E／N3P／N3X）

- 【已發生】引文：「In 2022, TSMC became the first foundry to move 3nm FinFET (N3) technology into high-volume production.」｜S07
- 【已發生】引文：「Our N3 has successfully entered volume production in late fourth quarter last year as planned, with good yield.」｜S22（2023-01-12 法說）
- N3 原始 PPA【預告時代的宣稱】：「N3 technology will offer up to 70% logic density gain, up to 15% speed improvement at the same power and up to 30% power reduction at the same speed as compared with N5 technology.」｜S11（頁面存檔 2021-07-02，2022-05-31 版相同）
- N3E【已發生】：「N3E is an optimized 3nm node that provides an approximate 20% speed improvement, over 30% power savings, and approximately 1.6 times logic density increase compared to N5 technology.」｜S06；「N3E has already entered volume production in the fourth quarter of 2023.」｜S26（2024-01-18）
- N3E 時程修改：2022-07-14「volume production is scheduled for around 1 year after N3」（S20）→ 2022-10-13「we might pull in a little bit for 2 or 3 months」（S21）→ 2023-01-12「Volume production is scheduled for second half '23」（S22）→ 2023-07-20「will start volume production in the fourth quarter of this year」（S24）。
- N3P／N3X（2023-04-26 新聞稿，S04）：「N3P, scheduled to enter production in the second half of 2024, offers an additional boost to N3E with 5% more speed at the same leakage, 5-10% power reduction at the same speed, and 1.04X more chip density.」「N3X, which prioritizes performance and maximum clock frequencies for HPC applications, provides 5% more speed versus N3P at drive voltage of 1.2V, with the same improved chip density as N3P, and will enter volume production in 2025.」
- N3X 已發生：「N3X started volume production in 2025, and N3C started volume production in 2026.」｜S07
- 首批應用：「making it the ideal choice for smartphones and high-performance computing (HPC) applications.」｜S06；N3 量產初期「driven by both HPC and smartphone applications」｜S22
- EUV：台積電現行 N3 頁面與已取得的存檔頁未明寫 N3 的 EUV 使用，列【查無】（已搜：tsmc.com l_3nm 現行與 2021–2025 存檔、platform 頁「EUV」）。

### N2（第一代 nanosheet）

- 【已發生】引文：「TSMC’s 2nm (N2) technology has started volume production in 4Q25 as planned. N2 technology features industry-leading first-generation nanosheet transistor technology, with full-node strides in performance...」｜S07（現行頁面）
- 【已發生】引文：「N2 successfully entered high volume manufacturing in 4Q 2025 at both our Hsinchu and Kaohsiung sides with good yield.」｜S34（2026-01-15 法說）
- NanoFlex【已發生，2024-04-24 首度介紹】：「TSMC NanoFlex provides designers with flexibility in N2 standard cells, the basic building blocks of chip design, with short cells emphasizing small area and greater power efficiency, and tall cells maximizing performance.」｜S03
- 為何用 nanosheet（公司說法）：「After careful evaluation and extensive period of development, our 2-nanometer technology will adopt nanosheet transistor structure to provide our customers with best performance, cost and technology maturity.」｜S20（2022-07-14）
- **N2 PPA 口徑演變（基準皆 vs N3E）**：
  - 2022-07-14（S20）：「10 to 15 speed improvement at the same power or 20% to 30% power improvement at the same speed and logic density of more than 20% increase as compared with N3E」。
  - 2023-04-26（S04）：「up to 15% speed improvement over N3E at the same power, and up to 30% power reduction at the same speed, and greater than 1.15X chip density.」
  - 2024-07-18（S28）：「10% to 15% speed improvement at the same power, or 25% to 30% power improvement at the same speed, and more than 15% chip density increase as compared with N3E.」
  - 2025-01-16（S30）、2025-04-17（S31）、2025-07-17（S32）：功耗下限寫為「[25%] (corrected by company after the call)」，即法說當天口述有誤、事後更正為 25%。
- 預告時程（歷次）：2022-07-14「risk production schedule in 2024 and volume production in 2025」（S20）；2023-04-20「on track for volume production in 2025」（S23）；2025-07-17「well on track for volume production in the second half of 2025」（S32）；實際 4Q25，【查無】延後證據。
- 首批應用：「We are seeing strong demand from smartphone and HPC/AI applications and expect a faster ramp in 2026.」｜S34
- 客戶 NTO：「The TSMC 2nm (N2) technology has received multiple NTOs and entered volume production in 2025.」｜S05（現行 HPC 頁）。【媒體】SemiEngineering（2026-04-27）：「more than 20 customer tape-outs received so far and over 70 in the pipeline」｜S51。
- N2 營收占比【已發生】：「2-nanometer process technology contributed 3% of wafer revenue in the second quarter.」｜S36（2026-07-16）；「2-nanometer process technology contributed 8% of wafer revenue in the third quarter」｜S37（2026-10-15）。
- N2 對毛利率：「we expect a steep ramp-up of our 2-nanometer to dilute our gross margin by about 3 to 4 percentage points in the second half of the year.」｜S36

### N2P

- 【預告→現行】引文：「The N2P technology provides a 5% performance uplift, while maintaining the same design rules as N2, and could account for the majority of N2 adoptions. N2P delivers an 18% speed improvement at the same power, a 36% power reduction at the same speed, 1.2 times logic density, and 1.15 times chip density over N3E.」｜S05（現行頁面，基準 N3E）
- 引文（首次法說口徑，2024-07-18）：「N2P features a further 5% performance with -- at the same power of 5% to 10% power benefit at the same speed on top of the N2.」｜S28（基準 N2）
- 時程歷次：2024-07-18「volume production is scheduled for the second half 2026」（S28）；2025-01-16、04-17、07-17、10-16 同（S30–S33）；2026-01-15「volume production is scheduled for the second half of this year」（S34）。**2026-04-16、07-16、10-15 法說未再重述 N2P 時程**。N2P 實際量產宣告：【查無】（已搜：S35–S37 逐字稿 "N2P"、"2P"；tsmc.com 平台頁；pr.tsmc.com 2026 新聞稿）。

### N2X、N2U、N2A

- N2X 【已發生的規格描述／預告】引文：「N2X consists of two elements: ultra-high performance standard cell and high-speed device, which provide a combined 10% (5% each) speed boost.」｜S05。N2X 時程：官方【查無】（已搜：S35–S37 逐字稿、S01 新聞稿、tsmc.com HPC 頁）；【媒體】Tom's Hardware 2026-04-22 的表格列 N2X 量產 2027（基準 N2P）｜S50。
- N2U【預告】引文：「TSMC continues to advance its 2nm platform with the introduction of N2U, which employs design-technology co-optimization to reach speed gains of 3-4% or power reduction of 8-10% and a 1.02-1.03X logic density improvement from N2P. … N2U is scheduled for production in 2028.」｜S01（2026-04-22）
- N2A【預告】引文：「N2A provides 15-20% speed gain at the same power compared with N3A and is scheduled to complete AEC-Q100 qualification in 2028.」｜S01

## 4. A16、A14、A13、A12 與更後續節點

### A16（背面供電）

- 規格【預告時代宣稱】引文：「Compared to TSMC’s N2P process, A16 will provide 8-10% speed improvement at the same Vdd (positive power supply voltage), 15-20% power reduction at the same speed, and up to 1.10X chip density improvement for data center products.」｜S03（2024-04-24）。2025-06-02 存檔頁寫作「8%~10% speed improvement at the same Vdd, 15%~20% power reduction at the same speed, and 1.07~1.10X chip density」｜S08。法說：「additional 7% to 10% chip density gain」｜S32（2025-07-17）。
- 首批應用：「A16 is best suited for specific HPC products with complex signal routes and dense power delivery networks.」｜S32
- **時程歷次**：
  1. 2024-04-24「production in 2026」｜S03。
  2. 2024-07-18「Volume production is scheduled for second half 2026」｜S28；2025-01-16、04-17、07-17、10-16 皆同（S30–S33）。
  3. 2026-01-15「Volume production is on track for second half 2026.」｜S34（最後一次在法說明確重述）。
  4. 2026-04-16 法說只提「such as N2P and A16」，不含時程｜S35；2026-07-16、10-15 法說【查無】A16 時程（已搜 "A16"、"Super Power"）。
  5. 【媒體】2026-04-22 Tom's Hardware：「It is noteworthy that TSMC now lists A16 as a 2027 process technology, which is technically a slip from 2026.」並引述 Kevin Zhang：「A16 will be ready for production in 2026… However, actual product ramp depends on customers, and we expect volume production to begin in 2027.」｜S50。
  6. 【媒體】SemiEngineering 2026-04-27：「A16 had been advertised earlier for production in late 2026, but Figure 1 now shows it in 2027.」｜S51。
  7. 【官方，與上矛盾】tsmc.com 現行 HPC 頁：「targeting to be production ready in 2026」｜S05；tsmc.com 2026-07 版節點圖把 A16 標在 2026（圖檔 `tsmc-process-technology-nodes-2026-07.png`）。
  - 台積電 2026-04-22 新聞稿（S01）全文【查無】提及 A16。
- 2025 年報（R&D 章節）【已發生】：「TSMC's A16 technology development made significant progress in 2025 … Built upon 2nm process technology and design rules, A16 process technology adopts a backside power delivery network」「the Company initiated the development and risk production preparation for TSMC A16TM process technology」｜S40

### A14

- 【預告】新聞稿 2025-04-23 引文：「Compared with the N2 process, which is about to enter volume production later this year, A14 will offer up to 15% speed improvement at the same power, or up to 30% power reduction at the same speed, along with more than 20% increase in logic density.」；「Planned to enter production in 2028, the current A14 development is progressing smoothly with yield performance ahead of schedule.」｜S02
- 法說口徑（基準 N2）：2025-07-17「10% to 15% speed improvement at the same power or [25%] (corrected by company after the call) to 30% power improvement at the same speed and about 20% chip density gain」｜S32；2026-04-16「close to 20% chip density gain」｜S35。
- 2026-07-16 進度【已發生】：「Internal product-like vehicle demonstrated close to 90% device performance and close to 90% 256 megabits SRAM yield.」；「Risk production will start in 2027 and volume production is scheduled for 2028.」｜S36
- 2026-10-15：「Risk production is well on track for 2027, and volume production will start in 2028.」｜S37
- 客戶面：「in our A14, we have seen more and more customers actually higher than the 2-nanometer activities so far. And we expect that the A14 will be a bigger node than our current N2 technologies.」｜S37
- 【媒體】A14 不用 High-NA EUV：Kevin Zhang「They continue to find a way to drive the technology scaling without using High-NA」｜S50（2026-04-22）。

### A13、A12

- A13【預告】引文：「A13 provides 6% area savings from A14. Design rules are fully backward compatible with A14 … scheduled to enter production in 2029, one year after A14.」｜S01；2026-07-16 法說：「A13 represents a further advancement of our A14, achieving an over 6% die area」（逐字稿此處截斷）｜S36。
- A12【預告】引文：「TSMC is also previewing its A14 platform enhancement A12, which features Super Power Rail technology to provide backside power delivery for AI and HPC applications. A12 is also scheduled to enter production in 2029.」｜S01；官網：「TSMC’s A12 technology is the second generation of innovative backside power rail solution, with integrated cutting-edge nanosheet transistor, making it the best solution for AI/HPC applications.」｜S07
- A12 前身說法：「We will continue our strategy of continuous enhancement with A14, including a Super Power Rail offering planned for 2029.」｜S32（2025-07-17）。
- 【媒體】Tom's Hardware 引述 Kevin Zhang 談 A16→A12：「A16 is our first-generation technology with Super Power Rail, or backside power delivery, and A12 is the next generation. … you also need to scale the backside to achieve overall density benefits.」｜S50

### A14 之後、官方已公布的節點

- 官方已公布節點名稱只到 A12／A13（2029）。其後【查無】官方命名節點。已搜：tsmc.com 邏輯技術頁、S01–S03 新聞稿、S35–S37 逐字稿（"A10"、"1.0"、"beyond A14"）。
- 相關官方線索：2025 年報「the Company's research efforts continued to push forward with exploratory studies for nodes beyond A14」｜S40；20-F：「The increases were mainly attributed to a higher level of research activities for 10-angstrom, 14-angstrom, and 16-angstrom process technologies」｜S41；2025-04-17 法說（Wei）：「after the 2-nanometer will be 1.4 and 1.0, that has not been discussed yet.」｜S31。
- 【媒體】Tom's Hardware 作者歸納：「the lack of plans to use High-NA EUV lithography for any nodes through 2029」（非台積電原話；台積電側原話見 A14 段 Kevin Zhang 引文）｜S50。

## 5. 背面供電（Super Power Rail, SPR）原理與時程

- 原理（官方）：「It improves logic density and performance by dedicating front-side routing resources to signals, making A16 ideal for HPC products with complex signal routes and dense power delivery networks.」｜S03；「SPR also improves power delivery and reduces IR drop significantly. Most importantly, the novel backside contact scheme we developed preserves gate density, layout footprint, and device width flexibility, thus achieving best density and performance simultaneously, and we believe it is a first in the industry.」｜S08（頁面存檔 2025-06-02）；現行頁：「Super Power Rail (SPR) optimizes power delivery by freeing up front-side routing for signals, substantially reducing IR drop, and maintaining gate density and layout flexibility.」｜S05
- 官方未公開 SPR 的剖面結構圖或接觸方式細節（如直接接觸 source/drain）：【查無】（已搜：新聞稿、tsmc.com 技術頁、年報）。第三方描述見 S50 以外的媒體，未採用。
- 時程歷次【預告】：
  1. 2022-07-14（Wei）：「On the backside power delivery, actually, we call the super power rail, is part of our N2 platform offering. And at the proper time, who are introduced to the market whenever our customers need it.」｜S20
  2. 2024-01-18：「N2 with backside power rail will be available in the second half of 2025 to customers with production in 2026.」｜S26
  3. 2024-04-24：改為獨立節點 A16（S03）；2024-07-18：「We also introduced A16 as our next nanosheet-based technology, featuring Super Power Rail, or SPR, as a separate offering.」｜S28
  4. 2025-07-17：A14 加 SPR「planned for 2029」｜S32
  5. 2026-04-22：命名 A12、2029｜S01
- 採用條件（公司說法，2026-10-15）：「Whether you use the backside power, those kind of metallization scheme, is based on your need for your product, okay? So some of the accelerator might be using it. Some of the product like mobile phones, they don't use it.」｜S37

## 6. 研發投入

| 項目 | 數值 | 基準／口徑 | 來源 |
|---|---|---|---|
| 2023 R&D 費用 | NT$182,370 百萬，占淨營收 8.5% | 20-F | S41 |
| 2024 R&D 費用 | NT$204,182 百萬，占 7.1% | 20-F；年報同為 7.1% | S41、S42 |
| 2025 R&D 費用 | NT$246,427 百萬（約 US$7,855 百萬），占 6.5% | 20-F；年報同為 6.5% | S41、S40 |
| 2025 年增幅 | +NT$42,245 百萬，+20.7% | vs 2024 | S41 |
| 2026 R&D 預算 | 約為 2026 營收的 7% | 年報「Total R&D budget is estimated to be around 7% of 2026 revenue」（預告） | S40 |

- 引文（增幅原因）：「The increases were mainly attributed to a higher level of research activities for 10-angstrom, 14-angstrom, and 16-angstrom process technologies, as we continued to advance to smaller processing nodes.」｜S41
- 引文（組織）：「TSMC's research and development efforts include both centralized activities and those undertaken by individual fabs.」｜S40；2025 年報聯絡頁列「Global R&D Center — 168, Kehuan Rd., Hsinchu Science Park, Hsinchu 308-001」｜S40。年報另載與 SRC（美）、IMEC（比利時）及 30 餘所海外院校合作。
- 年報 2026 R&D 預算涵蓋專案（約占 89%）：2nm 平台、A16、A14 及更後、3DIC、下世代微影、長期研究｜S40。
- R&D 人力：官方（年報、20-F）【查無】；已搜：年報、20-F 全文「R&D personnel／employees／headcount」，及 Sustainability Report 的搜尋結果（未取得內文）。【媒體】Taiwan News 2025-03-07 引述魏哲家：「TSMC's 1nm chip development is led by its R&D personnel, with around 10,000 researchers in Taiwan. The R&D center in the US will have around 1,000 people, mainly focused on improving production line technologies at its US fabs」｜S43（口頭轉述，定義不明）。

## 7. N2 量產狀態與產能據點

- 【已發生】量產：見 3.N2（S07、S34）。
- 據點【已發生】：「N2 is ramping successfully in multiple phases at both Hsinchu and Kaohsiung sites.」｜S35（2026-04-16）、S37（2026-10-15）。官網：「TSMC currently operates six 12-inch GIGAFAB® facilities – Fab 12, Fab 14, Fab 15, Fab 18, Fab 20, and Fab 22.」｜S14；2025 年報聯絡頁列 Fab 20「1, Kehuan Rd., Hsinchu Science Park, Hsinchu 308-001」、Fab 22「1, Yuancyu N. Rd., Nanzi Dist., Kaohsiung City 811-019」｜S40。官網舊版：「TSMC Fab 20 will be the main 2nm production facility」｜S13（存檔 2025-05-22）。
- 「寶山」：官方文件【查無】。已搜：年報全文、法說逐字稿 2022Q2–2026Q3、tsmc.com GIGAFAB 與技術頁關鍵字 "Baoshan"。Fab 20 與 N2 的對應關係以 S13 為準（官方只寫 Fab 20）。
- **據點說法修改**：2023-01-12「We are also preparing for N2 volume production starting in 2025, which will be located in Hsinchu and Taichung Science Park.」｜S22 → 2024-01-18「We plan to build multiple fabs or multiple phases of 2-nanometer technologies in both Hsinchu and Kaohsiung science parks」｜S26（同場董事長 Mark Liu：「our Kaohsiung fab, the first fab used to be 28-nanometer or 7-nanometer. Now it's becoming 2-nanometer.」）。
- 產能【預告】：「We expect our N2 family technology's annual capacity to more than double in 2027」｜S37。每月晶圓數官方【查無】；【媒體】（低可信，單一來源推估）TweakTown／Borecraft 稱年底目標約 10 萬片／月，未採用數字。
- 資本支出：「the CapEx dollar required to build 1k wafer-per-month capacity of N2 is substantially higher than 1k wafer-per-month capacity for N3.」｜S34（2026-01-15）
- 亞利桑那：「around 30% of our 2-nanometer and more advanced capacity will be located in Arizona」｜S31（2025-04-17；公司事後補了「and more advanced」）。
- 台中：「actively commencing the construction of its 1.4-nanometer fab in Taichung」｜S14（現行頁）。

- 產能與製程範圍【已發生】（2026-11-07 補，供序幕卡片）：「As of 2025, the combined capacity has exceeded 13 million 12-inch equivalent wafers, offering process technologies covering the full generation and half-generation designs from 0.13 micrometers to 2 nanometers.」｜S14（https://www.tsmc.com/english/dedicatedFoundry/manufacturing/gigafab，現行頁，查證日 2026-11-07）；方法檔 3.1 第 1 級。

## 8. 競爭對手路線

### 8.1 Samsung Foundry（2nm GAA）

- SF2 規格【預告時代宣稱，2023-06-28】：「The company will begin mass production of the 2nm process for mobile applications in 2025, then expand to HPC in 2026 and automotive in 2027. Samsung’s 2nm process (SF2) has shown a 12% increase in performance, a 25% increase in power efficiency and a 5% decrease in area, when compared to its 3nm process (SF3).」｜S70（基準 SF3）
- SF2Z 與 SF1.4【預告，2024-06-13】：「The company’s latest 2nm process, SF2Z, incorporates optimized backside power delivery network (BSPDN) technology, which places power rails on the backside of the wafer to eliminate bottlenecks between the power and signal lines.」；「Mass production of SF2Z is slated for 2027.」；「Samsung reaffirmed that its preparations for SF1.4 (1.4nm) are progressing smoothly, with performance and yield targets on track for mass production in 2027.」｜S71
- 【已發生】SF2 量產：「The Business also commenced mass production of first-generation 2nm products and began shipments of 4nm HBM base-die products.」｜S72（2026-01-29，Q4 2025 業績新聞稿）。2026 展望：「It plans to ramp up production of second-generation 2nm products」｜S72。
- 後續簡報【已發生／預告】：1Q26「Initiating 2nm Gen 2 mobile product ramp-up」「1.4nm on track; pursuing large-scale 2nm customer expansion」｜S73（簡報 PDF 建立日 2026-04-29）；2Q26「2nm Gen 2 mobile ramp-up」｜S73（2026-07-29）；3Q26「earnings improvement on 2nm 2nd Gen. new mobile products」「Continued order wins centered on 2nm HPC」｜S73（2026-10-28）。
- 首顆 2nm 產品：「Based on the industry’s first 2nm GAA process, the Exynos 2600 delivers enhanced AI and gaming experiences」｜S76（三星官方產品頁，無日期）。
- **時程修改（SF1.4）**：2022-10-04 引文：「Samsung targets mass production of 2nm process technology by 2025 and 1.4nm by 2027」｜S77；2024-06-13 重申 2027（S71）；【媒體】2026-07-01 SAFE Forum：韓聯社類媒體 FNNews 報導「mass production targeted for 2029」｜S74；TrendForce 2026-07-02：「SF1.4 is now reportedly slated for mass production in 2029, while its 2nm performance-enhanced variant, SF2P+, is expected to arrive earlier, between 2027 and 2028.」｜S75。Samsung 官方新聞稿站（news.samsung.com）【查無】2026 年 SAFE／SFF 新聞稿（tag 頁最新為 SFF 2024）。
- 【媒體】SF2P vs SF2：「the transition from SF2 to SF2P cuts power consumption by 26% while boosting operating frequency by 15%」｜S75（轉述 The Elec，基準 SF2）。
- SF2Z（背面供電）現況：官方 2024 說 2027；2026 年報導中未被提及，狀態【查無】官方說法（已搜：S71–S73、S74–S75）。

### 8.2 Intel（18A、14A；RibbonFET、PowerVia）

- 18A 規格【已發生，現行官網頁，無日期】：「Delivers up to 18% higher performance at iso power, 38% lower power at iso performance, and 30% chip density improvement versus Intel 3.」｜S60（基準 Intel 3）
- 結構說明：「Intel Foundry’s industry-first PowerVia technology relocates course pitch metals and bumps to the back side of the die and embeds nano-scale through-silicon vias (nano-TSVs) in every standard cell for efficient power distribution.」；「RibbonFET is Intel Foundry's gate-all-around transistor architecture, in which the channel is fully surrounded by the gate」｜S60；「PowerVia reduces worst‑case dynamic voltage droop by as much as 10x while enabling up to 11% block‑level area compaction in routed designs.」｜S60
- 【已發生】量產：「Arizona’s Fab 52 is fully operational and set to reach high-volume production using Intel 18A later this year」｜S61（2025-10-09）；「At the start of 2026, we released our first products manufactured on Intel 18A, our most advanced leading-edge semiconductor manufacturing technology, or node, in high volume production.」｜S64（10-Q，2026-10-30 提交）
- 【已發生】18A 達到大量生產的年度（頁面時間軸畫在 2025 年的依據）：「In 2025, we ramped Intel 18A into high-volume production」｜S79（Intel 2025 年度 10-K，主要依據；終審時取得，擷取工具只確認到句子開頭）；另見「Intel 18A ramped to high-volume manufacturing in Arizona and Oregon」｜S78（2025 年第 4 季暨全年業績新聞稿，2026-01-22，條文本身未註明月份）。S61 的「later this year」只是預告，不作為達成的證據。
- 18A-P【已發生，風險試產】：「Intel 18A-P entered risk production, meeting the timeline shared with customers and partners last year」｜S62（2026-07-23）；規格：「over 9% higher performance at iso power or more than 18% lower power at iso performance」｜S60（基準 18A）。
- 14A【預告】：High-NA — 「Intel expects to use both 0.33NA EUV and 0.55NA EUV … starting with product proof points on Intel 18A in 2025 and continuing into production of Intel 14A.」｜S65（2024-04-18）；2025 路線圖圖檔把 14A 標「Industry 1st High-NA EUV」與「PowerDirect」（文字層）｜S66。
- 14A 進度【已發生】：「Released Intel 14A 0.9 process design kit (PDK) in October.」｜S63（2026-10-29）；「During Q2 2026, we committed to completing development of Intel 14A, with a number of future Intel products designed to utilize the node」；「the scale and pace of our manufacturing expansion projects will ultimately be dictated by the amount of committed demand for Intel 14A that we are able to obtain」｜S64。
- **14A 時程修改**：【媒體】Digital Trends 2026-07-24：舊預期「risk production in 2028 and volume production in 2029」，新：「14A risk production for internal products is now planned for the second half of 2027」「High-volume production is expected to begin in 2028」｜S68；Tom's Hardware 2026-07-24 引述 Lip-Bu Tan：「we remain on track for 14A risk production for our internal products in the second half of 2027, and we made the decision in Q2 to fully commit to high volume ramp in 2028」｜S67。舊版（2028／2029）的 Intel 一手來源：【查無】（已搜：S62、S63、S64、S65、S66；本次未取得 Intel 該季法說逐字稿）。
- 2024 路線圖（Intel 圖檔文字）：「Intel 14A | Industry 1st | High-NA EUV」，並稱「2024 and 2027 targets represent planned milestones and expectations」｜S66。

## 9. 官方示意圖候選清單

| # | 檔名（已下載） | 圖／頁面 | 圖說 | 授權／版權標示 |
|---|---|---|---|---|
| 1 | `tsmc-process-technology-nodes-2026-07.png`（2000×764，183,880 bytes） | 直接 URL：https://www.tsmc.com/sites/dcom/2026-07/Process-Technology-Nodes_260709.png；所在頁面：https://www.tsmc.com/english/dedicatedFoundry/technology/logic（亦見 l_2nm、l_a14、l_a12）；無頁碼 | 製程節點時間軸 1987–2030：3µm → … → 7nm、5nm、3nm、2nm、A16、A14、A12；圖上 2nm 標 2025、A16 標 2026、A14 標 2028、A12 標 2029；2nm 之後節點為虛線圈 | 頁尾「Copyright © Taiwan Semiconductor Manufacturing Company Limited 2010-2026, All Rights Reserved.」；圖本身無額外授權標示。檔名日期 260709 推測為 2026-07-09 上線，屬推測 |
| 2 | `tsmc-process-technology-nodes-2023-02-wayback.png`（1600×702，127,292 bytes） | 直接 URL（官網原址已回 403）：https://www.tsmc.com/sites/dcom/2023-03/Process-Technology-Nodes_20230220.png；本次取自 Wayback：http://web.archive.org/web/20250602205054im_/https://www.tsmc.com/sites/dcom/2023-03/Process-Technology-Nodes_20230220.png；所在頁面：https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm（存檔 2025-06-02） | 同款時間軸的 2023 版，止於 3nm（2022），可與圖 1 對照「一代一代新增的節點」 | 同上（官網版權頁尾）；經 Wayback 取得 |
| 3 | `intel-foundry-roadmap-2025.pdf`（PDF，200,803 bytes；向量圖，非點陣） | 直接 URL：https://download.intel.com/newsroom/2025/foundry/Intel-Foundry-Direct-Connect-Roadmap-Infographic.pdf；所在頁面：Intel Newsroom／Direct Connect 素材（頁面 URL 本次未取得，【查無】） | Intel Foundry 製程路線圖：14A（High-NA EUV、PowerDirect）、18A（PowerVia）、Intel 3，標示 2025–2028 | 文末「All product and service plans, roadmaps, and performance estimates are subject to change without notice.」；Intel 商標聲明 |

- TSMC 背面供電（SPR）官方示意圖：【查無】可下載的公開頁面圖檔。已搜：tsmc.com 邏輯技術頁／A16／A14／A12／HPC 平台頁／pr.tsmc.com 3136、3228、3302 之 HTML 圖片標籤；僅找到上列節點圖與非技術性的廠房／捷徑圖示。
- TSMC 2026 技術論壇簡報圖（路線圖投影片）：新聞稿 PDF（S01 附件，3 頁）【查無】內嵌圖；論壇簡報本體非公開下載，未取得。
- Samsung：SFF 2024 新聞稿（S71）的 7 張圖皆為活動現場照片，無技術示意圖，未下載。
- 已下載 3 個檔，上限 8；其餘候選無。下載皆成功，無失敗項目。

## 10. 來源登記表（查證日一律 2026-11-01）

B = `https://investor.tsmc.com/english/encrypt/files/encrypt_file/reports/`

| ID | 來源 | 發布日 | 類型 | URL |
|---|---|---|---|---|
| S01 | TSMC 新聞稿「TSMC Debuts A13 Technology at 2026 North America Technology Symposium」 | 2026-04-22（官網列 2026-04-23） | 官方 | https://pr.tsmc.com/english/news/3302 |
| S02 | TSMC 新聞稿「TSMC Unveils Next-Generation A14 Process…」 | 2025-04-23 | 官方 | https://pr.tsmc.com/english/news/3228 |
| S03 | TSMC 新聞稿「TSMC Celebrates 30th North America Technology Symposium…」 | 2024-04-24 | 官方 | https://pr.tsmc.com/english/news/3136 |
| S04 | TSMC 新聞稿「TSMC Showcases New Technology Developments at 2023 Technology Symposium」 | 2023-04-26（官網列 2023-04-27） | 官方 | https://pr.tsmc.com/english/news/3021 |
| S05 | tsmc.com HPC 平台頁（N2P/N2X/A16/A14/N3X 段） | 無日期（現行頁） | 官方 | https://www.tsmc.com/english/dedicatedFoundry/technology/platform_hpc_tech_advancedTech |
| S06 | tsmc.com Smartphone 平台頁（N2P/N3E/N5/N7 段） | 無日期（現行頁） | 官方 | https://www.tsmc.com/english/dedicatedFoundry/technology/platform_smartphone_tech_advancedTech |
| S07 | tsmc.com 邏輯技術頁（N2、N3、A12、A14、A16 摘要；N7、N5 量產年） | 無日期（現行頁） | 官方 | https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm |
| S08 | tsmc.com l_3nm 存檔（A16 SPR 全文） | 存檔 2025-06-02 | 官方（Wayback） | http://web.archive.org/web/20250602205054/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm |
| S09 | tsmc.com l_5nm 存檔（N5） | 存檔 2021-05-08 | 官方（Wayback） | http://web.archive.org/web/20210508183921/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_5nm |
| S10 | tsmc.com l_7nm 存檔（N7、N7+、N6） | 存檔 2021-05-08 | 官方（Wayback） | http://web.archive.org/web/20210508182310/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_7nm |
| S11 | tsmc.com l_3nm 存檔（N3 vs N5 PPA） | 存檔 2021-07-02（2022-05-31 版相同：http://web.archive.org/web/20220531115350/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm） | 官方（Wayback） | http://web.archive.org/web/20210702161021/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_3nm |
| S12 | tsmc.com l_5nm 存檔（N5 約 20%／40%） | 存檔 2023-02-03 | 官方（Wayback） | http://web.archive.org/web/20230203062017/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_5nm |
| S13 | tsmc.com l_7nm 存檔（含 N2 段：Fab 20 為主要 2nm 廠） | 存檔 2025-05-22 | 官方（Wayback） | http://web.archive.org/web/20250522132154/https://www.tsmc.com/english/dedicatedFoundry/technology/logic/l_7nm |
| S14 | tsmc.com GIGAFAB 頁 | 無日期（現行頁） | 官方 | https://www.tsmc.com/english/dedicatedFoundry/manufacturing/gigafab |
| S20 | 2Q22 法說逐字稿 | 2022-07-14 | 法說會 | B2022-07/185efaefea866a5e944499cda9eeecc65315449c/TSMC%202Q22%20Transcript.pdf |
| S21 | 3Q22 法說逐字稿 | 2022-10-13 | 法說會 | B2022-10/1ee31c398ae422b9f503b5f64324c11997011447/TSMC%203Q22%20Transcript.pdf |
| S22 | 4Q22 法說逐字稿 | 2023-01-12 | 法說會 | B2023-01/84f1ef6f66c6c90b05d2e581066a01a8f1c4f410/TSMC%204Q22%20Transcript.pdf |
| S23 | 1Q23 法說逐字稿 | 2023-04-20 | 法說會 | B2023-04/882aa7c981570fe00c0bba76648983b02b54cbf4/TSMC%201Q23%20Transcript.pdf |
| S24 | 2Q23 法說逐字稿 | 2023-07-20 | 法說會 | B2023-07/7ec677062ca442e429b632ccd6d4f31ad53b1ce7/TSMC%202Q23%20Transcript.pdf |
| S26 | 4Q23 法說逐字稿 | 2024-01-18 | 法說會 | B2024-03/1979f7d585d258f1026b753e4b8a98a046bc81d3/TSMC%204Q23%20Transcript.pdf |
| S28 | 2Q24 法說逐字稿 | 2024-07-18 | 法說會 | B2024-08/5122725a56670882d777a8e8bfe0ed247cc55330/TSMC%202Q24%20Transcript.pdf |
| S30 | 4Q24 法說逐字稿 | 2025-01-16 | 法說會 | B2025-01/84aeb15bbe33894365d33f52e027c5268ba95dcf/TSMC%204Q24%20Transcript.pdf |
| S31 | 1Q25 法說逐字稿 | 2025-04-17 | 法說會 | B2025-04/7630274eecc1197a4e3ea6a415f44a47204fe10a/TSMC%201Q25%20Transcript.pdf |
| S32 | 2Q25 法說逐字稿 | 2025-07-17 | 法說會 | B2025-07/1f4f86c935f1de837672a6973154e64b26bdae57/TSMC%202Q25%20Transcript.pdf |
| S33 | 3Q25 法說逐字稿 | 2025-10-16 | 法說會 | B2025-10/6860312f04fd291d0f26b46c1234f84e6332717e/TSMC%203Q25%20Transcript.pdf |
| S34 | 4Q25 法說逐字稿 | 2026-01-15 | 法說會 | B2026-01/51d09df96cd89ac19d65af39032b038dc2896a24/TSMC%204Q25%20Transcript.pdf |
| S35 | 1Q26 法說逐字稿 | 2026-04-16 | 法說會 | B2026-04/3cef85204275f94fd111485cfdf4adb3c0263c45/TSMC%201Q26%20Transcript.pdf |
| S36 | 2Q26 法說逐字稿 | 2026-07-16 | 法說會 | B2026-08/3e494f0c14dd0890f897aa044415e21d93486cc4/TSMC%202Q26%20Transcript.pdf |
| S37 | 3Q26 法說逐字稿 | 2026-10-15 | 法說會 | B2026-10/eba4fac72873bf546b669bd2b5d973df5c93215d/TSMC%203Q26%20Transcript.pdf |
| S40 | TSMC 2025 年報 | PDF 未載明發布日（R&D 表含至 2026-02-28 資料） | 年報 | https://investor.tsmc.com/sites/ir/annual-report/2025/2025%20TSMC%20Annual%20Report.E.pdf |
| S41 | TSMC 2025 Form 20-F | 提交日待查證 | 年報（SEC） | https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf |
| S42 | TSMC 2024 年報 | PDF 未載明發布日 | 年報 | https://investor.tsmc.com/sites/ir/annual-report/2024/2024-Annual%20Report-E.pdf |
| S43 | Taiwan News「TSMC CEO stresses most R&D will stay in Taiwan」 | 2025-03-07 | 媒體 | https://www.taiwannews.com.tw/news/6054003 |
| S50 | Tom's Hardware「TSMC unveils process technology roadmap through 2029…」 | 2026-04-22 | 媒體 | https://www.tomshardware.com/tech-industry/semiconductors/tsmc-unveils-process-technology-roadmap-through-2029-a12-a13-n2u-announced-a16-slips-to-2027 |
| S51 | SemiEngineering「TSMC Tech Symposium 2026, By The Numbers」 | 2026-04-27 | 媒體 | https://semiengineering.com/tsmc-tech-symposium-2026-by-the-numbers/ |
| S60 | Intel 18A 製程頁（18A／18A-P／PowerVia／RibbonFET） | 無日期（現行頁） | 官方（Intel） | https://www.intel.com/content/www/us/en/foundry/process/18a.html |
| S61 | Intel 新聞稿「Intel Unveils Panther Lake Architecture…」 | 2025-10-09 | 官方（Intel） | https://www.intel.com/content/www/us/en/newsroom/news/client-computing/intel-unveils-panther-lake-architecture-first-ai-pc-platform-built-on-18a.html |
| S62 | Intel 2Q26 業績新聞稿（8-K 附件） | 2026-07-23 | 官方（Intel／SEC） | https://www.sec.gov/Archives/edgar/data/50863/000005086326000155/q226earningsrelease.htm |
| S63 | Intel 3Q26 業績新聞稿（8-K 附件） | 2026-10-29 | 官方（Intel／SEC） | https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000188/q326earningsrelease.htm |
| S64 | Intel 10-Q（期間止 2026-09-26） | 2026-10-30 | 官方（SEC） | https://www.sec.gov/Archives/edgar/data/0000050863/000005086326000191/intc-20260926.htm |
| S65 | Intel Newsroom「With High NA EUV, Intel Foundry Opens New Frontier in Chipmaking」 | 2024-04-18 | 官方（Intel） | https://newsroom.intel.com/intel-foundry/intel-foundry-opens-new-frontier-chipmaking |
| S66 | Intel Foundry 路線圖圖檔 2025／2024 | 2025（月日未載明）／2024 | 官方（Intel） | https://download.intel.com/newsroom/2025/foundry/Intel-Foundry-Direct-Connect-Roadmap-Infographic.pdf ；https://download.intel.com/newsroom/2024/foundry/intel-foundry-node-roadmap-2024.pdf |
| S67 | Tom's Hardware「Intel commits to 14A mass production in 2028…」 | 2026-07-24 | 媒體 | https://www.tomshardware.com/pc-components/cpus/intel-commits-to-14a-mass-production-in-2028-as-its-sales-rise-25-percent-year-over-year |
| S68 | Digital Trends「Intel just pulled its 14A production schedule forward by a year」 | 2026-07-24 | 媒體 | https://www.digitaltrends.com/computing/intel-just-pulled-its-14a-production-schedule-forward-by-a-year/ |
| S78 | Intel 新聞稿「Intel Reports Fourth-Quarter and Full-Year 2025 Financial Results」 | 2026-01-22 | 官方（Intel） | https://www.intc.com/news-events/press-releases/detail/1759/intel-reports-fourth-quarter-and-full-year-2025-financial-results ；SEC 附件：https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000009/q425earningsrelease.htm |
| S79 | Intel 2025 年度 10-K（fiscal year ended 2025-12-27） | 2026 | 官方（Intel，SEC 申報） | https://www.sec.gov/Archives/edgar/data/50863/000005086326000011/intc-20251227.htm |
| S77 | Samsung Newsroom「…Plans for 1.4nm Process Technology and Investment for Production Capacity at Samsung Foundry Forum 2022」 | 2022-10-04 | 官方（Samsung） | https://news.samsung.com/global/samsung-electronics-unveils-plans-for-1-4nm-process-technology-and-investment-for-production-capacity-at-samsung-foundry-forum-2022 |
| S70 | Samsung Newsroom「…Foundry Vision in the AI Era at Samsung Foundry Forum 2023」 | 2023-06-28 | 官方（Samsung） | https://news.samsung.com/global/samsung-electronics-unveils-foundry-vision-in-the-ai-era-at-samsung-foundry-forum-2023 |
| S71 | Samsung Newsroom「Samsung Showcases AI-Era Vision and Latest Foundry Technologies at SFF 2024」 | 2024-06-13 | 官方（Samsung） | https://news.samsung.com/global/samsung-showcases-ai-era-vision-and-latest-foundry-technologies-at-sff-2024 |
| S72 | Samsung「…Announces Fourth Quarter and FY 2025 Results」 | 2026-01-29 | 官方（Samsung） | https://news.samsung.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results |
| S73 | Samsung 業績簡報 4Q25／1Q26／2Q26／3Q26（PDF 建立日 2026-01-28／04-29／07-29／10-28，發布約為隔日） | 見左 | 官方（Samsung） | https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_conference_eng.pdf（其餘將 `2025_4Q` 換成 `2026_1Q`、`2026_2Q`、`2026_3Q`） |
| S74 | FNNews「Samsung Electronics says 1.4-nanometer process is on track for mass production in 2029」 | 2026-07-01 | 媒體 | https://en.fnnews.com/news/202607011445192159 |
| S75 | TrendForce「Samsung Reportedly Expands 2nm Portfolio…」 | 2026-07-02 | 媒體 | https://www.trendforce.com/news/2026/07/02/news-samsung-reportedly-expands-2nm-portfolio-ahead-of-2029-sf1-4-mass-production-sf2p-targets-2027-28/ |
| S76 | Samsung Semiconductor Exynos 2600 產品頁 | 無日期（現行頁） | 官方（Samsung） | https://semiconductor.samsung.com/processor/mobile-processor/exynos-2600/ |

## 11. 查無與限制清單

| 項目 | 結果 | 已搜關鍵字／來源 |
|---|---|---|
| 「寶山」作為 N2 據點的官方用詞 | 查無 | Baoshan（年報、法說逐字稿 2022Q2–2026Q3、tsmc.com GIGAFAB／技術頁）；僅見 Fab 20、Fab 22、Hsinchu、Kaohsiung |
| N2P 實際量產宣告 | 查無 | N2P、2P（1Q26–3Q26 逐字稿）；pr.tsmc.com 2026 新聞稿 |
| N2X 官方時程 | 查無 | N2X（逐字稿、S01、tsmc.com HPC 頁） |
| A12 PPA 官方數字 | 查無 | A12（S01、S36、tsmc.com） |
| A14 之後官方命名節點 | 查無 | A10、1.0、beyond A14（逐字稿、年報、20-F） |
| TSMC 官方 R&D 人力數字 | 查無（僅媒體轉述魏哲家口頭說法） | 年報、20-F 全文；Sustainability Report 搜尋結果未取得內文 |
| N2 每月晶圓產能官方數字 | 查無 | 逐字稿 2025Q1–2026Q3、年報 |
| SPR 官方結構示意圖 | 查無 | 見第 9 章 |
| N3 的 EUV 使用官方明文 | 查無 | tsmc.com l_3nm 現行與存檔 |
| Samsung 2026 年官方路線圖新聞稿／SF2Z 現況 | 查無（僅媒體） | news.samsung.com Samsung Foundry Forum tag 頁；S72–S73 |
| Intel 14A 舊時程（2028 風險／2029 量產）的 Intel 一手來源 | 查無（僅媒體引述舊預期） | S62–S66；未取得 Intel 季度法說逐字稿 |
| N2 IEDM 2024 論文等學術一手數據（SRAM 密度等） | 未納入（本次僅見媒體轉述，未取得論文全文） | IEDM TSMC N2 |

其他限制：Intel 10-Q 提交日取自 SEC 索引頁；Samsung 簡報發布日以 PDF 建立日推算（建立日加一日為法說日，屬推算）；tsmc.com 現行頁面皆無發布日，已標「現行頁」並以存檔頁補足歷史時點。

## 12. 序幕用的證據（2026-11-07 補）

原本只記在審查紀錄 `review-pe-r1.md`，補進證據檔。查證日 2026-11-07，以頁面原始碼逐字比對。

| 論斷 | 逐字引文 | 來源 URL | 類型 |
|---|---|---|---|
| 節點名稱不對應任何特定尺寸 | "Nowadays, a particular node name does not reflect the size of any particular chip feature, as it once did." | https://spectrum.ieee.org/the-status-of-moores-law-its-complicated（Rachel Courtland，2013-10-28） | 媒體；方法檔 3.1 第 5 級 |
| Intel 的 Mark Bohr：指不出哪個尺寸剛好是節點名稱 | "But I’m the first to admit that I can’t point to the one dimension that’s 32 nm or 22 nm or 14 nm. Some dimensions are smaller than the stated node name, and others are larger." | 同上 | 媒體；第 5 級 |
