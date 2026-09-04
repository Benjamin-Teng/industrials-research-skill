#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2pdf.py — 把研究報告 Markdown 轉成「機構研究報告風」PDF（繁體中文）

用法:
    python3 md2pdf.py 報告.md                 # 產出 報告.pdf（同目錄）
    python3 md2pdf.py 報告.md -o out.pdf
    python3 md2pdf.py 報告.md --no-toc        # 不產目錄頁
    python3 md2pdf.py 報告.md --keep-html     # 保留中繼 HTML 供除錯

Markdown 需以 YAML front matter 開頭（欄位見 SKILL.md）：

    ---
    title: 〈公司名〉〈代號〉個股深度研究報告
    subtitle: 一句話講清楚核心論點與方法
    type: 個股深度研究            # 個股深度研究 / 產業供應鏈研究 / 輪動掃描週報
    ticker: TWSE:0000
    version: v1.0
    date: 2026-08-06
    price_asof: 2026-08-05 正常盤收盤
    footer_right: 個人研究筆記 · 非投資建議   # 選填，頁尾右欄
    disclaimer: 〈封面免責條款全文〉          # 選填，覆蓋預設值
    author: 〈你的名字或機構〉
    framework: 〈你的方法論文件名 vX.Y〉
    rating: 〈分批布局／觀察／回避〉
    kpi:
      - {label: 現價, value: "NT$28.5", note: "2026-08-05 收盤"}
      - {label: 三情境區間, value: "34–41", note: 熊／基準／牛, tone: bull}
      - {label: 期望值 EV, value: "37", note: 機率加權}
      - {label: 熊情境下檔, value: "-18%", note: 論點失效時, tone: bear}
    ---

支援的區塊語法（pandoc fenced_divs）：
    ::: bull      多方論點框
    ::: bear      空方／風險框
    ::: caveat    Caveats／資料限制框
    ::: note      一般提示框
    ::: page      強制分頁（空 div 即可）

依賴：pandoc、playwright(chromium)、pypdf、PyYAML
"""

import argparse
import warnings

warnings.filterwarnings("ignore")

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML：pip install pyyaml --break-system-packages")

ASSETS = Path(__file__).resolve().parent.parent / "assets"
CSS_PATH = ASSETS / "report.css"

BOX_CLASSES = {"bull", "bear", "caveat", "note"}
DISCLAIMER = ("本報告為個人研究筆記，非投資建議，不構成任何證券之要約或招攬。"
              "所有估值與情境為作者依公開資訊所做之推估，可能與實際結果重大不同。"
              "報告內市場數據以封面所列基準日為準，其後之價格變動未反映於本文結論。")


# ---------------------------------------------------------------- front matter
def split_front_matter(text: str):
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end():]


# ---------------------------------------------------------------- md -> html
def md_to_html(md_body: str) -> str:
    if not shutil.which("pandoc"):
        sys.exit("找不到 pandoc，請先安裝（apt-get install -y pandoc）")
    fmt = ("markdown+pipe_tables+fenced_divs+task_lists+footnotes"
           "+tex_math_dollars+raw_html+strikeout+auto_identifiers")
    p = subprocess.run(
        ["pandoc", "-f", fmt, "-t", "html5", "--no-highlight", "--wrap=none"],
        input=md_body, capture_output=True, text=True,
    )
    if p.returncode != 0:
        sys.exit(f"pandoc 轉檔失敗：\n{p.stderr}")
    return p.stdout


def normalise_divs(body: str) -> str:
    """把 ::: bull 之類的 fenced div 轉成 .box.bull；::: page 轉成分頁。"""
    for name in BOX_CLASSES:
        body = re.sub(rf'<div class="{name}"', f'<div class="box {name}"', body)
    body = re.sub(r'<div class="page">\s*</div>', '<div class="page-break"></div>', body)
    return body


def slugify(text: str, used: set) -> str:
    base = re.sub(r"[^\w一-鿿-]+", "-", text.strip()).strip("-").lower() or "sec"
    slug, i = base, 2
    while slug in used:
        slug, i = f"{base}-{i}", i + 1
    used.add(slug)
    return slug


def build_toc(body: str):
    """為 h2/h3 補 id，並回傳 (帶 id 的 body, toc html)。"""
    used, items = set(), []

    def repl(m):
        lvl, attrs, inner = m.group(1), m.group(2), m.group(3)
        text = re.sub(r"<[^>]+>", "", inner).strip()
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else slugify(text, used)
        if not idm:
            attrs = f' id="{hid}"' + attrs
        items.append((lvl, hid, text))
        return f"<h{lvl}{attrs}>{inner}</h{lvl}>"

    body = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", repl, body, flags=re.S)
    if not items:
        return body, ""
    lis = "".join(
        f'<li class="lv{lvl}"><a href="#{hid}">{html.escape(txt)}</a></li>'
        for lvl, hid, txt in items
    )
    return body, f'<section class="toc"><h2>目錄</h2><ul>{lis}</ul></section>'


# ---------------------------------------------------------------- cover / kpi
def kpi_html(kpis) -> str:
    if not kpis:
        return ""
    cards = []
    for k in kpis:
        tone = k.get("tone", "")
        note = f'<div class="note">{html.escape(str(k.get("note", "")))}</div>' if k.get("note") else ""
        cards.append(
            f'<div class="kpi {tone}">'
            f'<div class="label">{html.escape(str(k.get("label", "")))}</div>'
            f'<div class="value">{html.escape(str(k.get("value", "")))}</div>{note}</div>'
        )
    return f'<div class="kpi-grid">{"".join(cards)}</div>'


def cover_html(meta: dict) -> str:
    rows = [
        ("標的", meta.get("ticker")),
        ("市場", {"TW": "台股", "US": "美股", "TW+US": "台股＋美股"}.get(
            str(meta.get("market", "")).strip(), meta.get("market"))),
        ("報告類型", meta.get("type")),
        ("版本", meta.get("version")),
        ("發布日期", meta.get("date")),
        ("市場數據基準日", meta.get("price_asof")),
        ("評等／結論", meta.get("rating")),
        ("基線版標註", meta.get("baseline_of")),
        ("適用框架", meta.get("framework")),
        ("作者", meta.get("author")),
    ]
    trs = "".join(
        f'<tr><td class="k">{k}</td><td class="v">{html.escape(str(v))}</td></tr>'
        for k, v in rows if v
    )
    sub = (f'<div class="cover-sub">{html.escape(str(meta["subtitle"]))}</div>'
           if meta.get("subtitle") else "")
    baseline = (f'<div class="cover-baseline">⚠ 基線版報告：{html.escape(str(meta["baseline_of"]))}'
                f'——本版結論以此事件前／未納入該事件之資訊為基準，事件後須依預定時點修訂</div>'
                if meta.get("baseline_of") else "")
    typ = (f'<div class="cover-type">{html.escape(str(meta["type"]))}</div>'
           if meta.get("type") else "")
    return f"""<section class="cover">
  <div class="cover-top"><div class="cover-kicker">Industry &amp; Equity Research</div></div>
  {typ}
  <h1>{html.escape(str(meta.get("title", "研究報告")))}</h1>
  {sub}
  {baseline}
  <div class="cover-meta">
    <table>{trs}</table>
    <div class="cover-disclaimer">{meta.get("disclaimer", DISCLAIMER)}</div>
  </div>
</section>"""


def wrap(css: str, inner: str) -> str:
    return (f"<!DOCTYPE html><html lang=\"zh-Hant\"><head><meta charset=\"utf-8\">"
            f"<style>{css}</style></head><body>{inner}</body></html>")


# ---------------------------------------------------------------- render
FOOTER_TPL = """
<div style="width:100%;font-size:7.5pt;color:#8a94a0;padding:0 16mm;
            font-family:'Noto Sans CJK TC',sans-serif;
            display:flex;justify-content:space-between;border-top:.5px solid #e3e6ea;
            padding-top:2mm;">
  <span>{left}</span>
  <span>第 <span class="pageNumber"></span> / <span class="totalPages"></span> 頁</span>
  <span>{right}</span>
</div>"""


def render_pdf(html_str: str, out: Path, footer: str | None):
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_str)
        tmp = f.name
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{tmp}", wait_until="networkidle")
            page.emulate_media(media="print")
            page.pdf(
                path=str(out), format="A4", print_background=True,
                display_header_footer=bool(footer),
                header_template="<div></div>",
                footer_template=footer or "<div></div>",
                margin={"top": "16mm", "bottom": "18mm" if footer else "16mm",
                        "left": "16mm", "right": "16mm"},
            )
            browser.close()
    finally:
        os.unlink(tmp)


def merge(parts, out: Path):
    from pypdf import PdfWriter
    w = PdfWriter()
    for p in parts:
        w.append(str(p))
    with open(out, "wb") as fh:
        w.write(fh)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="研究報告 Markdown → 機構風 PDF")
    ap.add_argument("md")
    ap.add_argument("-o", "--out")
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--keep-html", action="store_true")
    a = ap.parse_args()

    src = Path(a.md).resolve()
    out = Path(a.out).resolve() if a.out else src.with_suffix(".pdf")
    meta, body_md = split_front_matter(src.read_text(encoding="utf-8"))
    css = CSS_PATH.read_text(encoding="utf-8")

    body = normalise_divs(md_to_html(body_md))
    body, toc = build_toc(body)
    body = kpi_html(meta.get("kpi")) + body

    front_parts = []
    if not a.no_cover:
        front_parts.append(cover_html(meta))
    if not a.no_toc and toc:
        front_parts.append(toc)

    tmpdir = Path(tempfile.mkdtemp())
    footer = FOOTER_TPL.format(
        left=html.escape(str(meta.get("title", ""))[:42]),
        right=html.escape(str(meta.get("footer_right", "個人研究筆記 · 非投資建議"))),
    )
    pdfs = []
    if front_parts:
        f_html = wrap(css, "".join(front_parts))
        f_pdf = tmpdir / "front.pdf"
        render_pdf(f_html, f_pdf, None)
        pdfs.append(f_pdf)
        if a.keep_html:
            (src.parent / (src.stem + ".front.html")).write_text(f_html, encoding="utf-8")

    b_html = wrap(css, body)
    b_pdf = tmpdir / "body.pdf"
    render_pdf(b_html, b_pdf, footer)
    pdfs.append(b_pdf)
    if a.keep_html:
        (src.parent / (src.stem + ".body.html")).write_text(b_html, encoding="utf-8")

    if len(pdfs) == 1:
        shutil.copy(pdfs[0], out)
    else:
        merge(pdfs, out)
    shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"✓ 已產出 {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
