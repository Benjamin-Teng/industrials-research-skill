#!/usr/bin/env python3
"""
fa_check.py — 檢查 Markdown 報告的 F-a（數字密集段落與表格儲存格）

用法:
    python3 fa_check.py 報告.md

規則以 references/formatting-rules.md 的 F1 為準：
    段落  ≥10 個數字 RED；6–9 ORANGE（單句且無推導符號降為 INFO）；
          3–5 且句子數 ≥2 為 YELLOW，否則 INFO。
    表格儲存格（以 <br> 分行，每行各算）≥3 個數字 CELL。

輸出每個命中一行 `<檔名>:<行號>: <級別> <數字數> <前 40 字>`（INFO 不輸出），
最後一行 `fa_check: N hit(s)`。有命中 exit 1，無命中 exit 0，讀不到檔 exit 2。
只用標準函式庫。
"""

from __future__ import annotations

import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# --- 不計入的內容：先整段換成空白，再數剩下的數字 ----------------------------

_EXCLUDE = [
    re.compile(r"https?://\S+"),
    re.compile(r"<[^>]+>"),  # <span …> 等 HTML 標籤
    re.compile(r"\[\d+\]"),  # 腳註編號
    # 日期
    re.compile(r"\d{4}\s?[-/]\s?\d{1,2}\s?[-/]\s?\d{1,2}"),
    re.compile(r"(?<![\d,.])\d{4}-(?:0[1-9]|1[0-2])(?![\d-])"),  # 年月
    re.compile(r"\d{4}\s?年\s?\d{1,2}\s?月(?:\s?\d{1,2}\s?日)?"),
    re.compile(r"\d{1,2}\s?月\s?\d{1,2}\s?日"),
    re.compile(r"\d{4}\s?年"),
    # 期別標籤
    re.compile(r"(?<![A-Za-z0-9])FY\d{2,4}(?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])\d{4}Q[1-4](?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])[1-4]Q(?:\d{2,4})?(?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])Q[1-4](?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])[12]H(?:\d{2,4})?(?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])H[12](?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9,.$])(?:3|6|9|12)M(?![A-Za-z0-9])"),
    # 文件名
    re.compile(r"(?<![A-Za-z0-9])\d{1,2}-[A-Z](?![A-Za-z0-9])"),
    # 規則與章節編號（R2.1、RD.3、OB-2、HBM3 這類字母開頭的代號）
    re.compile(r"(?<![A-Za-z0-9$])[A-Z]{1,3}[-.]?\d+(?:\.\d+)*"),
    re.compile(r"第\s?\d+(?:\.\d+)*\s?[章節]"),
    # 資料層級、版本號
    re.compile(r"(?<![A-Za-z0-9])l[123](?![A-Za-z0-9])"),
    re.compile(r"(?<![A-Za-z0-9])v\d+(?:\.\d+)*"),
    # 單獨的西元年
    re.compile(r"(?<![\d,.\-/])(?:19|20)\d{2}(?![\d,%]|\.\d|[-/]\d)"),
]
_LEADING_SECTION = re.compile(r"^\s*\d+(?:\.\d+)+(?=\s|$)")

_NUM = r"\d+(?:,\d{3})*(?:\.\d+)?"
_SIGN = r"[+\-−]?"
_NUMBER = re.compile(_SIGN + _NUM + rf"(?:\s?[–～~\-]\s?{_SIGN}{_NUM})?")

_SENTENCE_SPLIT = re.compile(r"[。！？]|[.!?](?=\s|$)")
_DERIVATION = ("→", "＝", "=")

_LIST_MARK = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?")
_FENCE = re.compile(r"^\s*(```|~~~)")
_SEPARATOR_CELL = re.compile(r"^:?-{1,}:?$")


def count_numbers(text: str, *, serial_cell: bool = False) -> int:
    """回傳 text 中計入 F-a 的數字個數。serial_cell=True 時純序號不計。"""
    stripped = text.strip()
    if serial_cell and re.fullmatch(r"#?\d{1,3}", stripped):
        return 0
    text = _LEADING_SECTION.sub(" ", text)
    for pattern in _EXCLUDE:
        text = pattern.sub(" ", text)
    return len(_NUMBER.findall(text))


def count_sentences(text: str) -> int:
    return sum(1 for s in _SENTENCE_SPLIT.split(text) if s.strip())


@dataclass(frozen=True)
class Hit:
    line: int
    level: str
    numbers: int
    snippet: str


# 一行 A4 PDF 約容納的字元數；未經校準的常數，用來近似「單位是否跨行」。
ONE_LINE_CHARS = 50

_MD_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
_MD_MARKUP = re.compile(r"\*\*|__|`|<[^>]+>")


def visible_length(text: str) -> int:
    """去掉 Markdown 標記（粗體、反引號、HTML 標籤、連結網址）後的字元數。"""
    text = _MD_LINK.sub(r"\1", text)
    text = _MD_MARKUP.sub("", text)
    return len("".join(text.split()))


def _classify_paragraph(text: str) -> str:
    n = count_numbers(text)
    if n >= 10:
        return "RED"
    sentences = count_sentences(text)
    multiline = visible_length(text) > ONE_LINE_CHARS
    if n >= 6:
        if sentences <= 1 and not multiline and not any(s in text for s in _DERIVATION):
            return "INFO"
        return "ORANGE"
    if n >= 3:
        return "YELLOW" if sentences >= 2 or multiline else "INFO"
    return "INFO"


def _snippet(text: str) -> str:
    return " ".join(text.split())[:40]


def _blank_comments(text: str) -> str:
    """把 HTML 註解換成同行數的空行，保留行號。"""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"), text, flags=re.DOTALL)


def _split_cells(line: str) -> list[str]:
    body = line.strip()
    body = body.removeprefix("|")
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def _is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(_SEPARATOR_CELL.match(c) for c in cells if c) and any(cells)


def check_text(text: str) -> list[Hit]:
    lines = _blank_comments(text).splitlines()
    hits: list[Hit] = []

    # 單位累積：(起始行號, [文字片段])
    unit: tuple[int, list[str]] | None = None

    def flush() -> None:
        nonlocal unit
        if unit is not None:
            joined = " ".join(unit[1])
            level = _classify_paragraph(joined)
            if level != "INFO":
                hits.append(Hit(unit[0], level, count_numbers(joined), _snippet(joined)))
        unit = None

    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break

    in_fence = False
    table_rows_seen = 0  # 0 = 不在表格內；1 = 剛過表頭；2 = 已過分隔列
    while i < len(lines):
        raw = lines[i]
        lineno = i + 1
        i += 1
        stripped = raw.strip()

        if _FENCE.match(raw):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            flush()
            table_rows_seen = 0
            continue
        if stripped.startswith("|"):
            flush()
            cells = _split_cells(stripped)
            if table_rows_seen == 0:
                table_rows_seen = 1  # 表頭
                continue
            if table_rows_seen == 1:
                table_rows_seen = 2
                if _is_separator(cells):
                    continue
            for col, cell in enumerate(cells):
                for part in re.split(r"<br\s*/?>", cell, flags=re.IGNORECASE):
                    n = count_numbers(part, serial_cell=(col == 0))
                    if n >= 3:
                        hits.append(Hit(lineno, "CELL", n, _snippet(part)))
            continue
        table_rows_seen = 0
        if re.match(r"^#{1,6}(\s|$)", stripped) or stripped.startswith(">"):
            flush()
            continue
        if re.fullmatch(r"(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,}", stripped):
            flush()
            continue

        marker = _LIST_MARK.match(raw)
        if marker:
            flush()
            unit = (lineno, [raw[marker.end() :]])
        elif unit is not None:
            unit[1].append(stripped)
        else:
            unit = (lineno, [stripped])
    flush()
    hits.sort(key=lambda h: h.line)
    return hits


def main(argv: list[str]) -> int:
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) != 1:
        print("用法: python3 fa_check.py <報告.md>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"fa_check: 讀不到 {path}: {exc}", file=sys.stderr)
        return 2
    hits = check_text(text)
    for h in hits:
        print(f"{path.name}:{h.line}: {h.level} {h.numbers} {h.snippet}")
    print(f"fa_check: {len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
