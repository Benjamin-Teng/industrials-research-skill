---
name: business-industry-analysis
description: "研究單一個股，且沒有要求估值、目標價、報酬風險比或買賣判斷時使用：說明公司靠什麼賺錢、產業利潤由誰掌握，不評價股價。觸發詞包含個股深度研究、幫我研究、商業模式、營收拆解、單位經濟、逐營收來源 SWOT、護城河、產業鏈上下游、利潤池、同業與替代方案、產業結構、這家公司靠什麼賺錢、產業利潤誰拿走。"
metadata:
  compatibility: 選用依賴：pandoc（把 SEC 的 HTML 申報文件轉成純文字）與 pdftotext（poppler-utils 或 Xpdf，抽台股年報 PDF 表格）。缺件時的退路見「資料取得」。
---

# 企業與產業分析（Layer 1）

## 定位與分工

本 skill 是 Layer 1：回答「這家公司靠什麼賺錢」與「產業利潤由誰掌握」，**完全不評價股價**。方法、紅線、標示與治理的單一來源是 `references/business-industry-method.md`。

- **格式與交付**交給 `research-report-output` 的 D 型骨架（企業與產業研究）。
- **估值**屬 `equity-valuation-discipline`（若有安裝）。和它一併載入時，D 型報告仍以 `references/business-industry-method.md` 第四章為準。
- **產業掃描與 channel check** 屬 `product-cycle-rotation`。
- 本 skill 不取價，也不呼叫 `price-routing`。

> **使用者方法論優先**：若使用者的 project／repo 中有自訂的企業與產業分析框架文件，**那份文件是 source of truth**，本 skill 退為預設值。設定方式見 `research-report-output` 的 `references/customize-your-framework.md`。

## 什麼請求走這裡

單一個股的研究請求，沒有要求估值、目標價、報酬風險比或買賣判斷，就走這裡，產出 D 型報告。路由規則只寫在 `research-report-output` SKILL.md「工作流程」第 2 步，以那裡為準。

## 工作流程

第一步之前，先讀 `references/business-industry-method.md` 第四章，確認報告的範圍。

1. 研究契約與資料時點疊加：`references/business-industry-method.md` 2.1
2. 重建營收來源並指派商業模式類型：`references/business-industry-method.md` 2.2
3. 依類型選單位經濟量尺：`references/business-industry-method.md` 2.3
4. 逐營收來源 SWOT：`references/business-industry-method.md` 2.4
5. 縱向產業鏈與利潤池：`references/business-industry-method.md` 2.5
6. 橫向同業與替代方案：`references/business-industry-method.md` 2.6
7. 產業結構與護城河：`references/business-industry-method.md` 2.7
8. 交接給 Layer 4：`references/business-industry-method.md` 2.8

## 資料取得

### 一手資料來源

- 美股：10-K／20-F、10-Q／6-K、8-K、法說簡報與逐字稿
- 台股：年報、公開資訊觀測站（MOPS）、法說簡報、重大訊息、月營收

### SEC 文件全文

WebFetch 一次只讀到 10-K／10-Q 的前段，MD&A 與附註常被截斷，所以用指令下載全文，轉成純文字後分段讀或用 grep 找附註。美股本土公司申報 10-K，外國發行人（例如 ARM）申報 20-F，樣板取清單中最新的一份 10-K 或 20-F。在台股上市、同時申報 20-F 的公司，主要來源仍是 MOPS。

- User-Agent 的唯一來源是環境變數 `SEC_USER_AGENT`，指令直接讀它，值留在環境變數裡。格式依 SEC〈Accessing EDGAR Data〉的範例：`Sample Company Name AdminContact@<sample company domain>.com`。
- PowerShell 樣板需要 PowerShell 7 以上：`-UserAgent` 預設會驗證 product token 格式，SEC 的聯絡字串通不過，錯誤訊息還會回顯完整的值，所以樣板加 `-SkipHeaderValidation`，而 Windows PowerShell 5.1 沒有這個參數。樣板開頭先檢查，不支援就停止，改用 bash 樣板（Git Bash 或 WSL）或下節的網頁工具退路。
- 請求速率上限是每秒 10 次請求（SEC 公告）；樣板每次請求之間等 1 秒。
- 端點：`data.sec.gov/submissions/CIK` 加 10 碼補零的 CIK 取 filing 清單 JSON（路徑格式由實測支持）；`www.sec.gov/Archives/edgar/data/` 底下取申報文件。
- 原始檔存在目前工作目錄下的 `sec_raw/`，每次執行建一個新的子目錄，不沿用前次的檔案。
- 每次下載都檢查成功與 HTTP 200，轉純文字也檢查結束狀態；任一步失敗就印「下載失敗：<步驟>」並停止，不讀其他目錄的舊檔。
- 清單裡找不到 10-K 或 20-F，或 accession、主文件欄位是空的，樣板印出提示後停在那裡，不下載任何文件。
- 先只檢查環境變數有沒有設定：

```bash
[ -n "$SEC_USER_AGENT" ] && echo set || echo missing
```

```powershell
if ($env:SEC_USER_AGENT) {'set'} else {'missing'}
```

bash 樣板，依序做四件事：下載 filing 清單 JSON、下載主文件、轉純文字、找附註。

```bash
CIK10=0001664703                 # 10 碼補零的 CIK（範例）
sec_fetch() {
  local D code rc N ACC DOC
  mkdir -p sec_raw && D=$(mktemp -d sec_raw/run.XXXXXX)
  if [ -z "$D" ] || [ ! -d "$D" ]; then echo "建立工作目錄失敗"; return 1; fi
  code=$(curl -sS --fail -A "$SEC_USER_AGENT" -w '%{http_code}' -o "$D/sub.json" "https://data.sec.gov/submissions/CIK$CIK10.json"); rc=$?
  if [ "$rc" -ne 0 ] || [ "$code" != 200 ]; then echo "下載失敗：filing 清單"; return 1; fi
  sleep 1
  # 清單裡的 form、accessionNumber、primaryDocument 三個陣列同序（新到舊），用位置對齊
  pick() { grep -o "\"$1\":\[[^]]*\]" "$D/sub.json" | head -1 | sed 's/^[^[]*\[//; s/\]$//' | tr -d '"' | tr ',' '\n'; }
  N=$(pick form | grep -n -m1 -E '^(10-K|20-F)$' | cut -d: -f1)
  if [ -n "$N" ]; then ACC=$(pick accessionNumber | sed -n "${N}p"); DOC=$(pick primaryDocument | sed -n "${N}p"); fi
  if [ -z "$ACC" ] || [ -z "$DOC" ]; then
    echo "找不到 10-K／20-F，改走『沒有 SEC_USER_AGENT 時』的退路，取不到的段落標未查到"; return 1
  fi
  code=$(curl -sS --fail -A "$SEC_USER_AGENT" -w '%{http_code}' -o "$D/doc.htm" "https://www.sec.gov/Archives/edgar/data/$((10#$CIK10))/${ACC//-/}/$DOC"); rc=$?
  if [ "$rc" -ne 0 ] || [ "$code" != 200 ]; then echo "下載失敗：主文件"; return 1; fi
  pandoc -f html -t plain --wrap=none "$D/doc.htm" -o "$D/doc.txt" || { echo "下載失敗：轉純文字"; return 1; }
  echo "$D"; grep -n -i "item 7" "$D/doc.txt" | head
}
sec_fetch
```

PowerShell 樣板，步驟與停止條件相同：

```powershell
$cik10 = '0001664703'            # 10 碼補零的 CIK（範例）
& {
  if (-not (Get-Command Invoke-WebRequest).Parameters.ContainsKey('SkipHeaderValidation')) {
    '需要 PowerShell 7 以上；Windows PowerShell 5.1 請改用 bash 樣板（Git Bash 或 WSL），或走網頁工具退路'; return
  }
  try {
    New-Item -ItemType Directory -Force sec_raw -ErrorAction Stop | Out-Null
    $d = New-Item -ItemType Directory -Path (Join-Path 'sec_raw' ([guid]::NewGuid())) -ErrorAction Stop
  } catch { '建立工作目錄失敗'; return }
  if (-not $d -or -not (Test-Path -LiteralPath $d.FullName -PathType Container)) { '建立工作目錄失敗'; return }
  try { $r = Invoke-WebRequest -Uri "https://data.sec.gov/submissions/CIK$cik10.json" -UserAgent $env:SEC_USER_AGENT -SkipHeaderValidation -OutFile "$d/sub.json" -PassThru -ErrorAction Stop } catch { '下載失敗：filing 清單'; return }
  if ($r.StatusCode -ne 200) { '下載失敗：filing 清單'; return }
  Start-Sleep -Seconds 1
  $f = (Get-Content "$d/sub.json" -Raw | ConvertFrom-Json).filings.recent
  $i = (0..($f.form.Count - 1) | Where-Object { $f.form[$_] -in '10-K', '20-F' } | Select-Object -First 1)
  if ($null -eq $i -or -not $f.accessionNumber[$i] -or -not $f.primaryDocument[$i]) {
    '找不到 10-K／20-F，改走『沒有 SEC_USER_AGENT 時』的退路，取不到的段落標未查到'; return
  }
  $u = "https://www.sec.gov/Archives/edgar/data/$([int64]$cik10)/$($f.accessionNumber[$i] -replace '-','')/$($f.primaryDocument[$i])"
  try { $r = Invoke-WebRequest -Uri $u -UserAgent $env:SEC_USER_AGENT -SkipHeaderValidation -OutFile "$d/doc.htm" -PassThru -ErrorAction Stop } catch { '下載失敗：主文件'; return }
  if ($r.StatusCode -ne 200) { '下載失敗：主文件'; return }
  pandoc -f html -t plain --wrap=none "$d/doc.htm" -o "$d/doc.txt"
  if ($LASTEXITCODE -ne 0) { '下載失敗：轉純文字'; return }
  $d.FullName
  Select-String -Path "$d/doc.txt" -Pattern 'Item 7' | Select-Object -First 5
}
```

純文字很長，用 `grep -n` 或 `Select-String` 找到附註的行號，再用 `sed -n '起,迄p'` 或 `Get-Content -Skip` 分段讀。

### 沒有 SEC_USER_AGENT 時

- Claude Code：用 WebFetch 讀網頁，用 Read 分頁讀 PDF。
- Codex：用它的網頁工具，或讀使用者提供的本機檔。
- 兩邊都取不到的段落：依 `references/business-industry-method.md` 5.1 標「未查到」，並用 `::: caveat` 寫明哪些已一手驗證、哪些沒有。
- 設定方式：見 `research-report-output` 的 `references/customize-your-framework.md` 第六節。

### 台股年報 PDF 表格

- 表格用 `pdftotext -raw` 重抽並核對合計；`-layout` 模式欄位會錯位。
- 沒有 pdftotext 時，依上節的退路讀 PDF。
- 無法核對合計的表格，標「未核對」，該數字不進基準判斷。

### FinMind

- 月營收的 `date` 是發布月，所屬月份用 `revenue_year`／`revenue_month` 定位。
- 做 TTM、季增、年增之前，先確認每列的期間長度：財報列只標期末日，同一序列裡可能混有上半年累計、單季與相減推算的單季。
- 半年報與興櫃公司的財務數字，回 MOPS PDF 對帳。

## 交付前內容層檢查

逐項勾過才交付：

- [ ] 紅線依 `references/business-industry-method.md` 第四章，零違規
- [ ] 每個數字都有 `references/business-industry-method.md` 5.1 的標示與完整會計期間
- [ ] 六塊內容齊全：商業模式與單位經濟、營收拆解與逐來源 SWOT、縱向產業鏈與利潤分布、橫向同業與替代方案、產業結構與護城河、交接
- [ ] 已做公司自述與申報數據的對帳
- [ ] 比較基準沒查到的，已標「比較基準未查」
- [ ] 交接清單不含任何價格或估值數值
- [ ] 格式層依 research-report-output 的 F-rules 自查（F-a 至 F-f）；數字密集的段落與表格儲存格已拆表或分行（`fa_check.py` 回報 0 hit(s)）
- [ ] TL;DR、KPI 卡與每個表格儲存格的數字都寫出文件名與期間，不只放層級標籤
- [ ] `l3` 只做記錄與交叉比對，不支撐任何結論或基準假設；搜尋結果摘要最高標 `l2`，讀到原文才標 `l1`
- [ ] market 為 TW 時，申報文件以 MOPS、年報與 TWSE／TPEx 公告為主；同一公司另有 20-F 時只作交叉核對
