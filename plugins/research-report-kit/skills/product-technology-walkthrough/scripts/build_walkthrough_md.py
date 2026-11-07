"""從互動頁逐拍擷取剖面截圖與文字，組成 research-report-output 格式的 md。

用法：python build_walkthrough_md.py <互動頁.html> <輸出資料夾> <md 檔名>

- 互動頁是沒有 `<!doctype html>` 外殼的片段；本腳本包上外殼後放進 `<互動頁所在資料夾>/_pdfwork`
  開啟，完成（或失敗）後刪除 `_pdfwork`。
- 截圖存到 `<輸出資料夾>/pdf-img/sNN-B.png`（NN 是兩位數步號，B 從 1 起算的拍號），md 以相對路徑引用。
- front matter、閱讀說明、KPI、幕導語全部取自頁面的 `window.walkthrough.meta`；文字只擷取頁面上
  實際顯示的內容，不另外改寫。
- 擷取一律用 `textContent`：收合的 `<details>` 或隱藏元素用 innerText 讀會回空字串而且不報錯。
  必填欄位擷取到空字串時 raise，不產出缺值的 md。
- 圖片、表格欄數與數字密度由 research-report-output 的 `fa_check.py`、`md2pdf.py` 接手檢查與轉檔。
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

_FA_CHECK = Path(__file__).resolve().parents[2] / "research-report-output" / "scripts" / "fa_check.py"


def _load_fa_check() -> ModuleType:
    """以檔案路徑載入同 plugin 的 fa_check（目錄名含連字號，無法用一般 import）。"""
    if not _FA_CHECK.is_file():
        raise FileNotFoundError(
            f"找不到 {_FA_CHECK}：本腳本需要同一個 plugin 內的 research-report-output skill，請先安裝。"
        )
    spec = importlib.util.spec_from_file_location("_ptw_fa_check", _FA_CHECK)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入 {_FA_CHECK}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # fa_check 用 dataclass，需先登錄才能執行
    spec.loader.exec_module(module)
    return module


_fa = _load_fa_check()
ONE_LINE_CHARS: int = _fa.ONE_LINE_CHARS
count_numbers = _fa.count_numbers
visible_length = _fa.visible_length

# 外殼與 N2 的 build_pdf_md.py 相同：meta viewport、body 去邊界、讓 [hidden] 一定生效
_SHELL_HEAD = (
    '<!doctype html><html><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    "<style>body{margin:0}[hidden]{display:none!important}</style></head><body>"
)
_SHELL_TAIL = "</body></html>"

# 來源分級 → report.css 的徽章色（只有 l1–l3 三色）
_BADGE = {1: "l1", 2: "l1", 3: "l2", 4: "l2", 5: "l3"}

_FRONT_MATTER_FIELDS = (
    "title",
    "subtitle",
    "type",
    "methodology_version",
    "market",
    "ticker",
    "version",
    "date",
    "framework",
    "footer_right",
    "disclaimer",
)

# 擷取頁面目前這一拍的文字；全部用 textContent
_EXTRACT = """() => {
  const t = id => (document.getElementById(id)?.textContent || '').trim();
  const txt = n => (n ? n.textContent : '').trim();
  const sup = [...document.querySelectorAll('#suppliers .supg')].map(g => ({
    name: txt(g.querySelector('b')),
    list: [...g.querySelectorAll('.sup')].map(x => txt(x)) }));
  return {
    eyebrow: t('eyebrow'), title: t('title'), plain: t('plain'), now: t('now'),
    capA: t('capA'), capB: t('capB'), paCut: t('paCut'), paText: t('paText'), pbCut: t('pbCut'), pbText: t('pbText'),
    beatLabel: t('beatlabel'),
    badges: [...document.querySelectorAll('#badges .badge')].map(b => txt(b)),
    detail: [...document.querySelectorAll('#detail p')].map(p => txt(p)),
    sources: [...document.querySelectorAll('#sources li')].map(li => ({
      tag: txt(li.querySelector('.t')),
      label: li.querySelector('a') ? txt(li.querySelector('a')) : txt(li),
      url: li.querySelector('a')?.href || '' })),
    sup,
    supNote: sup.length ? '' : t('suppliers') };
}"""


def wrap_fragment(html: str) -> str:
    """把互動頁片段包成完整文件（發布時由 claude.ai 包，本機開啟與截圖要自己包）。"""
    return _SHELL_HEAD + html + _SHELL_TAIL


def _yaml_str(value: Any) -> str:
    """JSON 字串是合法的 YAML 雙引號純量，一律加引號，冒號、引號、井號都不會被誤解。"""
    return json.dumps(str(value), ensure_ascii=False)


def front_matter(meta: dict[str, Any]) -> str:
    """front matter 的欄位值全部取自 `meta`；缺欄位或空值 raise，不用預設值頂替。"""
    for key in (*_FRONT_MATTER_FIELDS, "kpi"):
        if not meta.get(key):
            raise ValueError(f"META.{key} 缺值")
    lines = ["---"]
    lines += [f"{key}: {_yaml_str(meta[key])}" for key in _FRONT_MATTER_FIELDS]
    lines.append("kpi:")
    for card in meta["kpi"]:
        pairs = ", ".join(f"{k}: {_yaml_str(card[k])}" for k in ("label", "value", "note") if card.get(k))
        lines.append("  - {" + pairs + "}")
    lines += ["---", ""]
    return "\n".join(lines)


def badge_class(level: int) -> str:
    """來源分級（1 最高）對應 report.css 的徽章色。"""
    try:
        return _BADGE[level]
    except KeyError:
        raise ValueError(f"來源分級必須是 1–5，收到 {level!r}") from None


def split_sentences(paragraph: str) -> list[str]:
    """一句一項：F1 對多句且數字多的段落會命中，拆句後每項只剩一句。

    以句號、分號斷句；分號結尾的句子改成句號。
    """
    items = []
    for piece in re.split(r"(?<=[。；])", paragraph):
        piece = piece.strip()
        if piece:
            items.append(piece.rstrip("；") + ("。" if piece.endswith("；") else ""))
    return items


def split_items(text: str) -> list[str]:
    """F1：數字 ≥3 且超過一行時，在逗號、冒號、頓號處拆成子項，一行一個重點。

    判定沿用 fa_check 自己的函式。回傳不含項目符號與縮排的字串；不拆時回傳 `[text]`。
    """
    if count_numbers(text) >= 3 and visible_length(text) > ONE_LINE_CHARS:
        parts = [p for p in re.split(r"(?<=[，：、])", text) if p.strip()]
        return [p.rstrip("，、") for p in parts]
    return [text]


def _require(value: str, n: int, b: int, field: str) -> None:
    if not value:
        raise ValueError(f"step {n}.{b}: {field} 為空")


def _capture(page: Any, steps: list[dict[str, Any]], tag_levels: dict[str, int], img_dir: Path) -> list[dict[str, Any]]:
    """逐步逐拍走訪頁面，回傳每一步的文字與各拍的截圖檔名。"""
    out: list[dict[str, Any]] = []
    for step in steps:
        n = step["n"]
        record: dict[str, Any] | None = None
        for b in range(step["beats"]):
            page.evaluate("([n, b]) => walkthrough.go(n, b)", [n, b])
            page.wait_for_timeout(450)
            d = page.evaluate(_EXTRACT)
            if d["beatLabel"] != f"{b + 1}／{step['beats']}":
                raise ValueError(f"step {n}.{b + 1}: 頁面沒有跳到這一拍（拍標籤 {d['beatLabel']!r}）")
            for field in ("title", "plain", "now"):
                _require(d[field], n, b + 1, field)
            if record is None:
                _check_step_level(d, n, tag_levels)
                record = {
                    "n": n,
                    "act": step["act"],
                    **{k: d[k] for k in ("eyebrow", "title", "plain", "badges", "detail", "sources", "sup", "supNote")},
                    "beats": [],
                }
                out.append(record)
            name = f"s{n:02d}-{b + 1}.png"
            page.locator("#panels").screenshot(path=str(img_dir / name))
            keys = ("now", "capA", "capB", "paCut", "paText", "pbCut", "pbText")
            record["beats"].append({"img": name, **{k: d[k] for k in keys}})
    return out


def _check_step_level(d: dict[str, Any], n: int, tag_levels: dict[str, int]) -> None:
    """步驟層級的欄位：細節段落、來源、徽章不得有空白項；沒列廠商時要有說明。"""
    if "　|" not in d["eyebrow"]:
        raise ValueError(f"step {n}.1: eyebrow 格式不符（缺「　|」分隔）：{d['eyebrow']!r}")
    if any(not p for p in d["detail"]):
        raise ValueError(f"step {n}.1: detail 有空白段落")
    if any(not s["label"] for s in d["sources"]):
        raise ValueError(f"step {n}.1: sources 有空白的來源名稱")
    if any(not s for s in d["badges"]):
        raise ValueError(f"step {n}.1: badges 有空白項")
    if not d["sup"]:
        _require(d["supNote"], n, 1, "supNote")
    for s in d["sources"]:
        if s["tag"] not in tag_levels:
            raise ValueError(f"step {n}.1: 來源類型 {s['tag']!r} 不在 walkthrough.tags 內")


def _compose(meta: dict[str, Any], tag_levels: dict[str, int], steps: list[dict[str, Any]]) -> str:
    guide = meta.get("readingGuide") or []
    if not guide:
        raise ValueError("META.readingGuide 缺值")
    act_lead = meta.get("actLead") or {}
    subject = meta.get("subject")
    if not subject:
        raise ValueError("META.subject 缺值")

    L: list[str] = [front_matter(meta), "## 閱讀說明", "", guide[0], ""]
    L += [f"- {item}" for item in guide[1:]] + [""]

    act = None
    for st in steps:
        act_part, _, label = st["eyebrow"].partition("　|")
        label = label.strip()
        if st["act"] != act:
            act = st["act"]
            lead = act_lead.get(str(act))
            if not lead:
                raise ValueError(f"META.actLead[{act}] 缺值")
            L += ["::: page", ":::", "", f"## {act_part.strip().replace('・', '　')}", "", lead, ""]
        L += [f"### {label}　{st['title']}", "", st["plain"], ""]
        for i, bt in enumerate(st["beats"], 1):
            L += [f"**第 {i} 拍**", "", bt["now"], ""]
            # 截圖已含兩張圖的標題與圖說；替代文字留空，避免 pandoc 再產生一次圖說
            L += [f"![](pdf-img/{bt['img']})", ""]
        if st["detail"]:
            L += ["#### 細節", ""]
            for p in st["detail"]:
                for sentence in split_sentences(p):
                    first, *rest = split_items(sentence)
                    L += [f"- {first}"] + [f"    - {x}" for x in rest]
            L += [""]
        L += ["#### 相關廠商", ""]
        if st["sup"]:
            # 表格：每家廠商一行（<br>），台股代號不會和同段其他數字疊加
            L += [f"> 依類別列出；● 有公開資料顯示供貨給{subject}或與{subject}合作，○ 為該類主要廠商。", ""]
            L += ["| 類別 | 廠商 |", "| --- | --- |"]
            L += [f"| {g['name']} | {'<br>'.join(g['list'])} |" for g in st["sup"]] + [""]
        else:
            L += [st["supNote"], ""]
        if st["sources"]:
            L += ["#### 資料來源", ""]
            for s in st["sources"]:
                tag = badge_class(tag_levels[s["tag"]])
                link = f"[{s['label']}]({s['url']})" if s["url"] else s["label"]
                L += [f'- <span class="tag {tag}">{s["tag"]}</span> {link}']
            L += [""]
    return "\n".join(L)


def build(page: Path, out_dir: Path, md_name: str, *, browser: Any = None) -> Path:
    """互動頁 → md 與逐拍截圖。回傳 md 路徑。

    截圖與 md 先產生在 `out_dir/_build_tmp/`，全部驗證成功才替換正式的 `pdf-img/` 與 md；
    中途失敗時，原有的 md 與圖片不變，暫存區清掉。

    `browser` 傳入已啟動的 Playwright browser 時沿用（同一個 process 只能有一個 sync Playwright）；
    省略時自己啟動 headless chromium。
    """
    page = page.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    tmp = out_dir / "_build_tmp"
    shutil.rmtree(tmp, ignore_errors=True)  # 清掉上次當機留下的
    new_img = tmp / "pdf-img"
    new_img.mkdir(parents=True)
    work = page.parent / "_pdfwork"
    work.mkdir(exist_ok=True)
    try:
        if (page.parent / "img").is_dir():
            shutil.copytree(page.parent / "img", work / "img", dirs_exist_ok=True)
        page_html = work / "page.html"
        page_html.write_text(wrap_fragment(page.read_text(encoding="utf-8")), encoding="utf-8")
        if browser is None:
            from playwright.sync_api import sync_playwright

            with sync_playwright() as pw:
                chromium = pw.chromium.launch(headless=True)
                try:
                    meta, tag_levels, steps = _run(chromium, page_html, new_img)
                finally:
                    chromium.close()
        else:
            meta, tag_levels, steps = _run(browser, page_html, new_img)
        new_md = tmp / md_name
        new_md.write_text(_compose(meta, tag_levels, steps), encoding="utf-8")
        return _publish(new_img, new_md, out_dir / "pdf-img", out_dir / md_name, tmp / "backup")
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)


def _publish(new_img: Path, new_md: Path, final_img: Path, final_md: Path, backup: Path) -> Path:
    """用新圖資料夾與新 md 替換正式版；任一步失敗就把圖片資料夾還原。"""
    backup.mkdir()
    had_old = final_img.exists()
    if had_old:
        final_img.rename(backup / "pdf-img")
    try:
        new_img.rename(final_img)
        os.replace(new_md, final_md)
    except OSError:
        if final_img.exists():
            shutil.rmtree(final_img, ignore_errors=True)
        if had_old:
            (backup / "pdf-img").rename(final_img)
        raise
    return final_md


def _run(browser: Any, page_html: Path, img_dir: Path) -> tuple[dict[str, Any], dict[str, int], list[dict[str, Any]]]:
    ctx = browser.new_context(
        viewport={"width": 1180, "height": 1000},
        reduced_motion="reduce",
        color_scheme="light",
        device_scale_factor=2,
    )
    try:
        pg = ctx.new_page()
        errors: list[str] = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(page_html.as_uri())
        pg.wait_for_function("() => window.walkthrough !== undefined")
        meta = pg.evaluate("walkthrough.meta")
        tags = pg.evaluate("walkthrough.tags")
        outline = pg.evaluate("walkthrough.steps.map(s => ({ n: s.n, act: s.act, beats: s.beats.length }))")
        tag_levels = {v["name"]: v["level"] for v in tags.values()}
        steps = _capture(pg, outline, tag_levels, img_dir)
        if errors:
            raise RuntimeError("頁面錯誤：" + "; ".join(errors))
        return meta, tag_levels, steps
    finally:
        ctx.close()


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("用法：python build_walkthrough_md.py <互動頁.html> <輸出資料夾> <md 檔名>", file=sys.stderr)
        return 2
    page, out_dir, md_name = Path(argv[1]), Path(argv[2]), argv[3]
    try:
        md = build(page, out_dir, md_name)
    except (ValueError, RuntimeError) as exc:
        print(f"停止產出：{exc}", file=sys.stderr)
        return 1
    text = md.read_text(encoding="utf-8")
    print(f"steps={len(re.findall(r'^### ', text, re.MULTILINE))} beats={len(re.findall(r'^\*\*第 ', text, re.MULTILINE))} md={md}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
