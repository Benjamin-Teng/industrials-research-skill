# 首例：台積電 N2 製程產品技術研究

`product-technology-walkthrough` skill 的第一個實際成品：跟著一片晶圓走完 N2 製程，
從設計、光罩、做出奈米片電晶體、接上導線，走到測試、封裝與出貨，最後是節點藍圖。

## 這是什麼版本

- 快照日期：2026-11-07。資料查證日是 2026-11-01，與正式版相同。
- 互動頁已對齊方法檔 5.1 的資料格式，改了哪些地方見 `CONFORMANCE.md`。
- 正式版放在作者的雲端硬碟，除了這裡的檔案，還有 PDF、逐拍截圖與官方圖檔。互動版發布成作者的
  claude.ai 私人頁面，網址不公開。

## 資料夾內容

| 檔案 | 內容 |
| --- | --- |
| `台積電N2製程_產品技術研究_v1.0_20261101.html` | 互動頁原始檔 |
| `台積電N2製程_產品技術研究_v1.0_20261101.md` | 由互動頁產生的文字版，截圖行已拿掉 |
| `research/01`～`04-*.md` | 各幕證據檔（幕與檔案的對照見 `CONFORMANCE.md`） |
| `research/05-suppliers.md` | 各步驟廠商名單 |
| `research/review-*.md` | 各幕的獨立審查紀錄 |
| `CONFORMANCE.md` | 逐章對照方法檔的不符清單與處理結論 |

## 沒有收進來的東西

repo 是公開的，第三方圖片不放進來。以下只在正式版：

- `img/`：互動頁嵌入的三張官方圖（論文 Fig.11、SoIC 對照圖、CoWoS-S 結構圖），以及蒐集階段下載的官方示意圖。
- 逐拍截圖（資料夾 `pdf-img`）：md 與 PDF 用的截圖。
- PDF 靜態版。
- `tools/`：方法檔整理前的舊版產檔腳本，已由 skill 的 `scripts/build_walkthrough_md.py` 取代。

證據檔與審查紀錄裡原本寫著本機的下載位置或截圖位置，這些地方改成「（本機路徑，未隨附）」。
其餘內容照原檔，markdownlint 的格式問題也沒有修。

## 缺圖時的樣子

這裡沒有 `img/`，所以步驟 14 與 17 的三張官方圖都會載入失敗。頁面改顯示一張卡片，寫出圖說，
附「開啟圖片來源」連結。圖下方的說明文字仍是描述原圖的版本。

## 重產 md 與截圖

流程見方法檔 5.2，第一步是互動頁轉 md 與截圖（`<skill>` 指 `plugins/research-report-kit/skills/product-technology-walkthrough`）：

```bash
uv run python <skill>/scripts/build_walkthrough_md.py <互動頁.html> <輸出資料夾> <md 檔名>
```

截圖會寫到輸出資料夾下的 `pdf-img` 資料夾。在這個資料夾重產時，三張官方圖的截圖會是替代卡片。

## 連接檢查

步驟 2、13、14 的導線、通孔與接點都標了 `data-net`，可以這樣逐拍檢查：

```bash
uv run python <skill>/scripts/schematic_topology.py <互動頁.html> --step 14 --beat 2
```

目前的結果與判讀見 `CONFORMANCE.md` 第六章。
