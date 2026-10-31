"""fa_check.py 的單元測試（F-a 數字密集檢查）。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

_SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "research-report-kit"
    / "skills"
    / "research-report-output"
    / "scripts"
)

_spec = importlib.util.spec_from_file_location("fa_check", _SCRIPTS_DIR / "fa_check.py")
assert _spec is not None and _spec.loader is not None
fa_check: ModuleType = importlib.util.module_from_spec(_spec)
sys.modules["fa_check"] = fa_check
_spec.loader.exec_module(fa_check)


def _levels(text: str) -> list[str]:
    return [h.level for h in fa_check.check_text(text)]


# --- 數字計法 ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("營收 603,231 百萬", 1),
        ("EPS 12.358 元", 1),
        ("毛利率 87.2% 與 87.2％", 2),
        ("金額 $1,898M", 1),
        ("NT$3.72 億", 1),
        ("倍數 2.5x", 1),
        ("跌幅 −3.9%", 1),
        ("合約價 +93–98%", 1),
        ("區間 5～8 倍", 1),
        ("1Q +93–98% → 2Q +58–63%", 2),
    ],
)
def test_counted_numbers(text: str, expected: int) -> None:
    assert fa_check.count_numbers(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "日期 2026-10-24",
        "日期 2026/10/24",
        "年月 2026-10 法說會",
        "日期 2026 年 10 月 24 日",
        "西元年 2025",
        "西元年 2025 年",
        "期別 FY2025",
        "期別 Q3",
        "期別 2026Q2",
        "期別 1Q26",
        "期別 2H26",
        "期別 H1",
        "期別 9M",
        "期別 TTM",
        "文件 10-K 10-Q 8-K 20-F 6-K",
        "規則 R2.1 RD.3 OB-2 F-a",
        "第 5.1 節",
        "資料層級 l1 l2 l3",
        "版本 v1.0",
        '<span class="l2" data-x="12">標籤</span>',
        "網址 https://example.com/a/2024/123456",
        "腳註[12]",
    ],
)
def test_excluded_numbers(text: str) -> None:
    assert fa_check.count_numbers(text) == 0


def test_leading_section_number_not_counted() -> None:
    assert fa_check.count_numbers("5.1 營運概況") == 0


def test_serial_cell_not_counted() -> None:
    assert fa_check.count_numbers("12", serial_cell=True) == 0


# --- 段落分級 ---------------------------------------------------------------


def _para(n: int, sentences: int = 1) -> str:
    parts = []
    nums = [f"{i + 11}.5%" for i in range(n)]
    per = max(1, n // sentences) if n else 1
    chunks = [nums[i : i + per] for i in range(0, n, per)] if n else [[]]
    while len(chunks) > sentences:
        chunks[-2].extend(chunks.pop())
    for c in chunks:
        parts.append("指標 " + " 與 ".join(c) + "。")
    return "".join(parts)


@pytest.mark.parametrize(
    ("n", "sentences", "expected"),
    [
        (2, 2, []),
        (3, 1, []),
        (5, 1, []),
        (5, 2, ["YELLOW"]),
        (6, 1, []),
        (6, 2, ["ORANGE"]),
        (9, 2, ["ORANGE"]),
        (10, 1, ["RED"]),
        (10, 2, ["RED"]),
    ],
)
def test_paragraph_levels(n: int, sentences: int, expected: list[str]) -> None:
    text = _para(n, sentences)
    assert fa_check.count_numbers(text) == n
    assert _levels(text) == expected


def test_derivation_symbol_keeps_orange() -> None:
    text = "A 為 11.5% → B 為 12.5% 與 13.5% 與 14.5% 與 15.5% 與 16.5%。"
    assert _levels(text) == ["ORANGE"]
    assert _levels(text.replace("→", "＝")) == ["ORANGE"]


def test_decimal_not_split_as_sentence() -> None:
    text = "毛利率 12.5% 與 13.5% 與 14.5% 與 15.5%。"
    assert _levels(text) == []


def test_list_items_are_separate_units() -> None:
    text = "- 項目 11.5% 與 12.5%\n- 項目 13.5% 與 14.5%\n- 項目 15.5%\n"
    assert _levels(text) == []
    text = "- 項目 11.5% 與 12.5% 與 13.5% 與 14.5% 與 15.5%。再一句。\n"
    assert _levels(text) == ["YELLOW"]


def test_ordered_list_marker_not_counted() -> None:
    assert _levels("1. 項目 11.5% 與 12.5%\n") == []
    assert fa_check.check_text("1. 項目 11.5%\n") == []


# --- 表格 -------------------------------------------------------------------

_HEAD = "| # | 發現 | 數據 |\n|---|---|---|\n"


def test_cell_single_line_three_numbers_hits() -> None:
    hits = fa_check.check_text(_HEAD + "| 1 | 結論 | 11.5% 12.5% 13.5% |\n")
    assert [h.level for h in hits] == ["CELL"]
    assert hits[0].line == 3


def test_cell_br_lines_two_each_passes() -> None:
    row = "| 1 | 結論 | A：11.5% 12.5%<br>B：13.5% 14.5%<br>C：15.5% 16.5% |\n"
    assert _levels(_HEAD + row) == []


def test_cell_br_line_with_three_hits() -> None:
    row = "| 1 | 結論 | A：11.5% 12.5%<br>B：13.5% 14.5% 15.5% |\n"
    assert _levels(_HEAD + row) == ["CELL"]


def test_table_header_skipped() -> None:
    head = "| 1Q 11.5% 12.5% 13.5% | b |\n|---|---|\n| x | y |\n"
    assert _levels(head) == []


# --- 略過區域 ---------------------------------------------------------------

_DENSE = "指標 11.5% 12.5% 13.5% 14.5% 15.5% 16.5% 17.5% 18.5% 19.5% 20.5%。"


def test_front_matter_skipped() -> None:
    assert _levels(f"---\nnote: {_DENSE}\n---\n\n正文\n") == []


def test_code_block_skipped() -> None:
    assert _levels(f"```\n{_DENSE}\n```\n") == []


def test_html_comment_skipped() -> None:
    assert _levels(f"<!-- {_DENSE}\n{_DENSE} -->\n") == []


def test_heading_and_blockquote_skipped() -> None:
    assert _levels(f"# {_DENSE}\n\n> {_DENSE}\n") == []


def test_dense_paragraph_outside_skipped_regions_hits() -> None:
    assert _levels(f"---\na: 1\n---\n\n```\nx\n```\n\n{_DENSE}\n") == ["RED"]


# --- CLI --------------------------------------------------------------------


def test_main_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    clean = tmp_path / "clean.md"
    clean.write_text("毛利率 12.5%。\n", encoding="utf-8")
    assert fa_check.main([str(clean)]) == 0
    assert capsys.readouterr().out.strip().endswith("fa_check: 0 hit(s)")

    dirty = tmp_path / "dirty.md"
    dirty.write_text(_DENSE + "\n", encoding="utf-8")
    assert fa_check.main([str(dirty)]) == 1
    out = capsys.readouterr().out.strip().splitlines()
    assert "dirty.md:1: RED 10 " in out[0]
    assert out[-1] == "fa_check: 1 hit(s)"

    assert fa_check.main([str(tmp_path / "missing.md")]) == 2


# --- 可見長度（是否跨行）------------------------------------------------------


def test_long_single_sentence_four_numbers_yellow() -> None:
    text = (
        "- **應收與存貨絕對額擴大**：2026-06-30 應收帳款 494,992 仟元、存貨 670,624 仟元，"
        "2025-12-31 分別為 230,652 與 473,101 仟元（合併資產負債表，`l1`）。"
    )
    assert fa_check.count_numbers(text) == 4
    assert _levels(text) == ["YELLOW"]


def test_short_single_sentence_four_numbers_info() -> None:
    text = "營收 11.5% 毛利 12.5% 淨利 13.5% 現金 14.5%。"
    assert fa_check.visible_length(text) <= fa_check.ONE_LINE_CHARS
    assert _levels(text) == []


def test_long_single_sentence_seven_numbers_orange() -> None:
    text = "本季營收年增 11.5%、毛利率 12.5%、營業利益率 13.5%、淨利率 14.5%、存貨週轉 15.5 次、應收週轉 16.5 次、資本支出占比 17.5%。"
    assert fa_check.count_numbers(text) == 7
    assert fa_check.visible_length(text) > fa_check.ONE_LINE_CHARS
    assert _levels(text) == ["ORANGE"]


def test_visible_length_strips_markup() -> None:
    assert (
        fa_check.visible_length(
            '**粗**`碼`<span class="x">字</span>[連結](http://a.b/c)'
        )
        == 5
    )


# --- Codex 第 2 輪回歸 ----------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "NT$2025 萬 US$1999M 2030 億",
        "NT$2,025 萬 US$1,999M 2,030 億",
        "2025％ 1999％ 2030％",
        "2025% 1999% 2030%",
        "2025 元 1999 倍 2030x",
    ],
)
def test_year_like_values_with_currency_or_unit_counted(text: str) -> None:
    assert fa_check.count_numbers(text) == 3


def test_standalone_years_still_excluded() -> None:
    assert fa_check.count_numbers("2025, 2026 與 2030 年") == 0
    assert fa_check.count_numbers("2025 年營收") == 0


def test_mismatched_fences_do_not_close() -> None:
    text = "```text\n~~~\n```\n\n" + _DENSE + "\n"
    assert _levels(text) == ["RED"]
    still_open = "```text\n~~~\n" + _DENSE + "\n"
    assert _levels(still_open) == []


def test_shorter_inner_fence_does_not_close() -> None:
    text = "````md\n```\n" + _DENSE + "\n```\n````\n\n" + _DENSE + "\n"
    assert [h.line for h in fa_check.check_text(text)] == [7]


def test_cell_leading_decimal_counted() -> None:
    assert _levels(_HEAD + "| 1 | 結論 | 12.5 13.5 14.5 |\n") == ["CELL"]
    assert _levels(_HEAD + "| 1 | 結論 | 5.1 12.5 13.5 |\n") == ["CELL"]


def test_paragraph_leading_decimals_counted() -> None:
    assert fa_check.count_numbers("12.5 13.5 14.5") == 3


def test_pipeless_table_matches_piped_table() -> None:
    piped = "| 指標 | 值 |\n|---|---|\n| 成長 | 11% 12% 13% |\n"
    bare = "指標 | 值\n--- | ---\n成長 | 11% 12% 13%\n"
    assert _levels(bare) == _levels(piped) == ["CELL"]
    assert [h.line for h in fa_check.check_text(bare)] == [3]
    assert _levels("指標 | 值\n:-- | --:\n成長 | 11% 12%\n") == []


def test_pipeless_table_header_skipped_and_ends_at_blank() -> None:
    text = "1Q 11% 12% 13% | b\n--- | ---\nx | y\n\n" + _DENSE + "\n"
    assert _levels(text) == ["RED"]


# --- Codex 第 3 輪回歸 ----------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    ["NT$ 2025 US$ 1999 NT$ 2030", "US$ 2,025 ¥ 1999 € 2030", "$ 2025 $ 1999 $ 2030"],
)
def test_currency_with_space_counted(text: str) -> None:
    assert fa_check.count_numbers(text) == 3


def test_currency_with_space_in_cell_hits() -> None:
    assert _levels(_HEAD + "| 1 | 結論 | NT$ 2025 US$ 1999 NT$ 2030 |\n") == ["CELL"]


def test_indented_fake_closing_fence_does_not_close() -> None:
    text = "```\n    ```\n" + _DENSE + "\n```\n\n" + _DENSE + "\n"
    assert [h.line for h in fa_check.check_text(text)] == [6]


def test_fence_indent_up_to_three_closes() -> None:
    text = "   ```\nx\n   ```\n\n" + _DENSE + "\n"
    assert [h.line for h in fa_check.check_text(text)] == [5]


def test_four_space_indented_fence_is_not_opener() -> None:
    assert _levels("    ```\n\n" + _DENSE + "\n") == ["RED"]


def test_pipeless_short_row_stays_in_table() -> None:
    hits = fa_check.check_text("a | b\n--- | ---\n11% 12% 13%\n")
    assert [(h.line, h.level) for h in hits] == [(3, "CELL")]


def test_table_ends_at_block_structure() -> None:
    text = "a | b\n--- | ---\nx | y\n# 標題\n" + _DENSE + "\n"
    assert _levels(text) == ["RED"]
