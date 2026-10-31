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
    # （前面有幣別符號，或後面接數字、千分位、小數、%、％、金額單位時，是數值不是年份）
    re.compile(
        r"(?<![\d,.\-/$¥€])(?<![$¥€]\s)(?<!\d,)(?:19|20)\d{2}"
        r"(?!\d|,\d|\.\d|[-/]\d|\s?(?:[%％]|萬|億|仟|千|百|元|倍|x\b|[KMB](?![A-Za-z])))"
    ),
]
# 段落行首的標題式編號（5.1 營運概況）；後面必須接文字，「12.5 13.5」不算
_LEADING_SECTION = re.compile(r"^\s*\d+(?:\.\d+)+(?=\s+[^\d\s+\-−])")

_NUM = r"\d+(?:,\d{3})*(?:\.\d+)?"
_SIGN = r"[+\-−]?"
_NUMBER = re.compile(_SIGN + _NUM + rf"(?:\s?[–～~\-]\s?{_SIGN}{_NUM})?")

_SENTENCE_SPLIT = re.compile(r"[。！？]|[.!?](?=\s|$)")
_DERIVATION = ("→", "＝", "=")

_LIST_MARK = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(?:\[[ xX]\]\s+)?")
_PIPE = re.compile(r"(?<!\\)\|")
_SEPARATOR_CELL = re.compile(r"^:?-{1,}:?$")

# --- 區塊邊界（CommonMark 0.31.2／GFM）------------------------------------------
# 除清單項外，區塊開頭都限縮排 ≤3 空白；清單項允許任意縮排以涵蓋巢狀清單。
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
_THEMATIC_BREAK = re.compile(
    r"^ {0,3}(?:(?:-[ \t]*){3,}|(?:\*[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
_SETEXT_UNDERLINE = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
_BLOCKQUOTE = re.compile(r"^ {0,3}>")
_HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup"
    "|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame"
    "|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem"
    "|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody"
    "|td|tfoot|th|thead|title|tr|track|ul"
)
# HTML 區塊第 1–6 型（可打斷段落者）；第 7 型不能打斷段落，不列入。
_HTML_BLOCK = re.compile(
    r"^ {0,3}(?:<(?:script|pre|style|textarea)(?:[ \t>]|$)"
    r"|<!--|<\?|<![A-Za-z]|<!\[CDATA\["
    rf"|</?(?:{_HTML_BLOCK_TAGS})(?:[ \t]|/?>|$))",
    re.IGNORECASE,
)


def block_kind(line: str) -> str | None:
    """回傳 line 開啟的區塊種類；不是區塊開頭時回傳 None。

    種類：blank、fence、thematic、heading、quote、list、html。
    順序有意義：分隔線先於清單項（「- - -」是分隔線）。
    setext 標題底線要看上一行是不是段落，由 check_text 另行判斷。
    """
    if not line.strip():
        return "blank"
    if _FENCE.match(line):
        return "fence"
    if _THEMATIC_BREAK.match(line):
        return "thematic"
    if _ATX_HEADING.match(line):
        return "heading"
    if _BLOCKQUOTE.match(line):
        return "quote"
    if _LIST_MARK.match(line):
        return "list"
    if _HTML_BLOCK.match(line):
        return "html"
    return None


def is_block_start(line: str) -> bool:
    """line 是否開啟新區塊（因而結束進行中的表格或段落）。"""
    return block_kind(line) is not None


def count_numbers(
    text: str, *, serial_cell: bool = False, in_cell: bool = False
) -> int:
    """回傳 text 中計入 F-a 的數字個數。

    serial_cell=True 時純序號不計；表格儲存格（in_cell 或 serial_cell）不套用行首章節編號排除。
    """
    stripped = text.strip()
    if serial_cell and re.fullmatch(r"#?\d{1,3}", stripped):
        return 0
    if not (in_cell or serial_cell):
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
    return re.sub(
        r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"), text, flags=re.DOTALL
    )


def _split_cells(line: str) -> list[str]:
    body = line.strip()
    body = body.removeprefix("|")
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def _is_separator(cells: list[str]) -> bool:
    return (
        bool(cells) and all(_SEPARATOR_CELL.match(c) for c in cells if c) and any(cells)
    )


def _table_starts(header: str, delimiter: str) -> bool:
    """header＋delimiter 是否構成 GFM 表格開頭。

    分隔列必須含管線、每格都是 :?-+:?，且欄數與表頭一致；
    因此單獨的 --- 不會被當成分隔列（那是分隔線或 setext 底線）。
    """
    if not (_PIPE.search(header) and _PIPE.search(delimiter)):
        return False
    if is_block_start(header):
        return False
    cells = _split_cells(delimiter)
    return _is_separator(cells) and len(cells) == len(_split_cells(header))


def check_text(text: str) -> list[Hit]:
    lines = _blank_comments(text).splitlines()
    hits: list[Hit] = []

    # 單位累積：(起始行號, [文字片段], 種類 para／list)
    unit: tuple[int, list[str], str] | None = None

    def flush() -> None:
        nonlocal unit
        if unit is not None:
            joined = " ".join(unit[1])
            level = _classify_paragraph(joined)
            if level != "INFO":
                hits.append(
                    Hit(unit[0], level, count_numbers(joined), _snippet(joined))
                )
        unit = None

    def check_row(lineno: int, row: str) -> None:
        for col, cell in enumerate(_split_cells(row)):
            for part in re.split(r"<br\s*/?>", cell, flags=re.IGNORECASE):
                n = count_numbers(part, serial_cell=(col == 0), in_cell=True)
                if n >= 3:
                    hits.append(Hit(lineno, "CELL", n, _snippet(part)))

    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break

    fence: tuple[str, int] | None = None  # 開啟中的 fence：(字元, 長度)
    in_table = False
    while i < len(lines):
        raw = lines[i]
        lineno = i + 1
        i += 1
        stripped = raw.strip()

        if fence is not None:
            # 結束行：同字元、長度不短於開啟行、且只有 fence 字元
            closer = _FENCE.match(raw)
            if (
                closer
                and set(raw.strip()) == {fence[0]}
                and len(raw.strip()) >= fence[1]
            ):
                fence = None
            continue

        # setext 標題：段落下緊接 === 或 ---，整個段落成為標題，不計
        if unit is not None and unit[2] == "para" and _SETEXT_UNDERLINE.match(raw):
            unit = None
            continue

        kind = block_kind(raw)
        if kind is not None:
            # 任何區塊開頭都結束進行中的表格與段落
            flush()
            in_table = False
            if kind == "fence":
                opener = _FENCE.match(raw)
                assert opener is not None
                fence = (opener.group(1)[0], len(opener.group(1)))
            elif kind == "list":
                marker = _LIST_MARK.match(raw)
                assert marker is not None
                unit = (lineno, [raw[marker.end() :]], "list")
            elif kind == "html":
                unit = (lineno, [stripped], "para")  # 標籤由 _EXCLUDE 去除，文字照計
            # blank、thematic、heading、quote：只當邊界，本行不計。
            # 刻意偏離 CommonMark：不做 blockquote 惰性續行，`>` 行之後沒有 `>` 的行
            # 一律另起段落計數——檢查器寧可多報，也不要吞掉引述後的正文。
            continue

        if in_table:
            check_row(lineno, stripped)  # 無管線的缺欄資料列也留在表內
            continue
        if i < len(lines) and _table_starts(raw, lines[i]):
            flush()
            in_table = True  # 本行是表頭，下一行是分隔列，兩者都略過
            i += 1
            continue
        if stripped.startswith("|"):
            flush()
            check_row(lineno, stripped)
            continue

        if unit is not None:
            unit[1].append(stripped)
        else:
            unit = (lineno, [stripped], "para")
    flush()
    hits.sort(key=lambda h: h.line)
    return hits


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8")
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
