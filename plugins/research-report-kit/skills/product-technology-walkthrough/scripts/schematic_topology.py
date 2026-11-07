"""示意圖連接關係檢查：從互動頁逐拍傾印帶 `data-net` 的矩形，檢查導線、通孔的連接是否合理。

用法：python schematic_topology.py <互動頁.html> [--step N --beat B]

- 元件標 `data-net`（網路名）與 `data-kind`（wire／via／node，省略視為 node），且只能是 `<rect>`。
- 檢查四種問題：懸空端點、短路、過近、孤立通孔。純函式 `gap`、`check`、`connection_table` 不需瀏覽器。
- 只有 CLI 才會啟動 headless chromium，以 `walkthrough.go()` 切到每一拍，再呼叫 `dumpScene()`。
- exit code：1＝任一拍有問題；0＝沒有問題且至少一拍有標註元件；2＝受檢的拍全都沒有標註元件
  （不算通過）；3＝用法或頁面錯誤（找不到步驟、頁面 JS 例外、標了 `data-net` 卻被略過的元件）。
- `data-net` 是人標的：標錯時本工具會把錯的連接驗成對的，所以它只是審查的輔助證據，不能取代逐條人工核對。
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, TypedDict

Box = TypedDict(
    "Box",
    {
        "id": str,
        "svg": str,
        "part": str,
        "net": str,
        "kind": str,
        "x": float,
        "y": float,
        "w": float,
        "h": float,
    },
)
Issue = TypedDict("Issue", {"kind": str, "ids": list[str], "detail": str})

DANGLING = "懸空端點"
SHORT = "短路"
NEAR = "過近"
ISOLATED_VIA = "孤立通孔"

NO_NET_MESSAGE = "沒有標註網路的元件"
_SKIPPED_PREFIX = "walkthrough：data-net 只支援"


def gap(a: Box, b: Box) -> float:
    """兩矩形的最短距離；重疊或相接為 0。不同張圖（`svg` 不同）不比較，回傳 inf。"""
    if a["svg"] != b["svg"]:
        return math.inf
    dx = max(a["x"] - (b["x"] + b["w"]), b["x"] - (a["x"] + a["w"]), 0.0)
    dy = max(a["y"] - (b["y"] + b["h"]), b["y"] - (a["y"] + a["h"]), 0.0)
    return math.hypot(dx, dy)


def _touching(box: Box, boxes: list[Box], tol: float) -> list[Box]:
    """同一張圖、同網路、與 box 相距 <= tol 的其他元件。"""
    return [o for o in boxes if o is not box and o["net"] == box["net"] and gap(box, o) <= tol]


def _dangling(wire: Box, contacts: list[Box], stub: float) -> str | None:
    if len(contacts) < 2:
        return f"只有 {len(contacts)} 個接觸，導線需要兩端都接上"
    horizontal = wire["w"] >= wire["h"]
    start, length = (wire["x"], wire["w"]) if horizontal else (wire["y"], wire["h"])
    end = start + length
    lows = [c["x"] if horizontal else c["y"] for c in contacts]
    highs = [c["x"] + c["w"] if horizontal else c["y"] + c["h"] for c in contacts]
    head, tail = min(lows) - start, end - max(highs)
    if head > stub:
        return f"起端伸出最外側接觸點 {head:g}，超過 stub={stub:g}"
    if tail > stub:
        return f"末端伸出最外側接觸點 {tail:g}，超過 stub={stub:g}"
    return None


def check(boxes: list[Box], tol: float = 0.5, near: float = 6.0, stub: float = 2.0) -> list[Issue]:
    """回傳所有問題。懸空端點只看 wire；node 參與短路、過近與連通計算，不做端點檢查。"""
    issues: list[Issue] = []
    for box in boxes:
        contacts = _touching(box, boxes, tol)
        if box["kind"] == "wire":
            reason = _dangling(box, contacts, stub)
            if reason:
                issues.append({"kind": DANGLING, "ids": [box["id"]], "detail": reason})
        elif box["kind"] == "via" and not contacts:
            issues.append({"kind": ISOLATED_VIA, "ids": [box["id"]], "detail": "沒有碰到任何同網路元件"})
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            if a["net"] == b["net"]:
                continue
            d = gap(a, b)
            pair = f"{a['id']}（{a['net']}）與 {b['id']}（{b['net']}）"
            if d <= tol:
                issues.append({"kind": SHORT, "ids": [a["id"], b["id"]], "detail": f"{pair}不同網路卻相接"})
            elif d < near:
                issues.append({"kind": NEAR, "ids": [a["id"], b["id"]], "detail": f"{pair}相距 {d:g}，小於 {near:g}"})
    return issues


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def connection_table(boxes: list[Box], issues: list[Issue], tol: float = 0.5) -> str:
    """md 表格 `| 元件 | 網路 | 接到 | 問題 |`；「接到」列出同網路接觸元件的 id。"""
    rows = ["| 元件 | 網路 | 接到 | 問題 |", "| --- | --- | --- | --- |"]
    for box in boxes:
        linked = "、".join(o["id"] for o in _touching(box, boxes, tol)) or "—"
        found = "、".join(dict.fromkeys(i["kind"] for i in issues if box["id"] in i["ids"])) or "無"
        rows.append(f"| {_cell(box['id'])} | {_cell(box['net'])} | {_cell(linked)} | {found} |")
    return "\n".join(rows)


# ---------------------------------------------------------------- CLI（需要瀏覽器，延遲 import）


def _load_wrap_fragment() -> Any:
    """以檔案路徑載入同資料夾的 build_walkthrough_md（目錄名含連字號，無法用一般 import）。"""
    path = Path(__file__).resolve().with_name("build_walkthrough_md.py")
    spec = importlib.util.spec_from_file_location("build_walkthrough_md", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入 {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # 不在 plugin 目錄寫 __pycache__
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
    return module.wrap_fragment


def _scenes(page: Path, step: int | None, beat: int) -> list[tuple[int, int, list[Box]]]:
    """逐拍傾印。回傳 [(步號, 拍索引, boxes)]；頁面錯誤或步驟不存在時 raise RuntimeError。"""
    from playwright.sync_api import sync_playwright

    wrap_fragment = _load_wrap_fragment()
    # 中間檔放在頁面所在目錄，相對路徑圖片才不會破圖；用完刪除
    fd, name = tempfile.mkstemp(prefix="_topology_", suffix=".html", dir=page.parent)
    work = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(wrap_fragment(page.read_text(encoding="utf-8")))
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            try:
                ctx = browser.new_context(viewport={"width": 1180, "height": 1000}, reduced_motion="reduce")
                pg = ctx.new_page()
                errors: list[str] = []
                skipped: list[str] = []
                pg.on("pageerror", lambda e: errors.append(str(e)))
                pg.on(
                    "console",
                    lambda m: skipped.append(m.text) if m.type == "error" and m.text.startswith(_SKIPPED_PREFIX) else None,
                )
                pg.goto(work.as_uri())
                pg.wait_for_function("() => window.walkthrough !== undefined")
                outline = pg.evaluate("walkthrough.steps.flatMap(s => s.beats.map((_, b) => [s.n, b]))")
                targets = [(int(n), int(b)) for n, b in outline]
                if step is not None:
                    targets = [t for t in targets if t == (step, beat)]
                    if not targets:
                        raise RuntimeError(f"沒有步驟 {step} 的第 {beat} 拍（拍索引從 0 起算）")
                result: list[tuple[int, int, list[Box]]] = []
                for n, b in targets:
                    pg.evaluate("([n, b]) => walkthrough.go(n, b)", [n, b])
                    result.append((n, b, pg.evaluate("walkthrough.dumpScene()")))
                if errors:
                    raise RuntimeError("頁面錯誤：" + "; ".join(errors))
                if skipped:
                    raise RuntimeError("有元件標了 data-net 卻被略過，未受檢：" + "; ".join(dict.fromkeys(skipped)))
                return result
            finally:
                browser.close()
    finally:
        work.unlink(missing_ok=True)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="逐拍檢查互動頁示意圖的連接關係")
    parser.add_argument("page", type=Path, help="互動頁 .html（沒有外殼的片段）")
    parser.add_argument("--step", type=int, help="只看這一步（步號）")
    parser.add_argument("--beat", type=int, default=0, help="搭配 --step：拍索引，從 0 起算（預設 0）")
    args = parser.parse_args(argv[1:])
    if args.beat != 0 and args.step is None:
        parser.error("--beat 必須搭配 --step")
    for stream in (sys.stdout, sys.stderr):  # cp950 主控台印中文會 UnicodeEncodeError
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")
    try:
        scenes = _scenes(args.page, args.step, args.beat)
    except (RuntimeError, OSError) as exc:
        print(f"停止檢查：{exc}", file=sys.stderr)
        return 3

    any_issue = False
    any_boxes = False
    for n, b, boxes in scenes:
        print(f"### step {n} beat {b}")
        if not boxes:
            print(NO_NET_MESSAGE)
            print()
            continue
        any_boxes = True
        issues = check(boxes)
        any_issue = any_issue or bool(issues)
        print(connection_table(boxes, issues))
        for issue in issues:
            print(f"- {issue['kind']}：{issue['detail']}")
        print()
    if any_issue:
        return 1
    if any_boxes:
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
