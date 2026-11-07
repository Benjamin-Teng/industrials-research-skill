"""build_walkthrough_md.py（互動頁 → md）的測試。

純函式測試不需要瀏覽器；`build()` 的測試用 Playwright，頁面一律先複製到 tmp_path，
不在 plugin 目錄底下產生任何檔案。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from browser_helpers import SCRIPT, SKELETON, build_walkthrough_md, launch

front_matter = build_walkthrough_md.front_matter
split_items = build_walkthrough_md.split_items
badge_class = build_walkthrough_md.badge_class
wrap_fragment = build_walkthrough_md.wrap_fragment
build = build_walkthrough_md.build

LONG = "良率 90%，功耗降 25%，密度增 15%，" + "說明" * 30

META_SAMPLE = {
    "title": "示範產品：從材料到出貨",
    "subtitle": "骨架示範",
    "subject": "示範公司",
    "market": "TW",
    "ticker": "TWSE:0000",
    "type": "產品技術研究",
    "methodology_version": "product-technology-v1",
    "framework": "個人研究筆記（互動頁靜態版）",
    "date": "2026-11-07",
    "version": "v0.1",
    "footer_right": "個人研究筆記 · 非投資建議",
    "disclaimer": "本頁為示範：內容虛構，非投資建議。",
    "kpi": [
        {"label": "示範指標", "value": "−5%", "note": "虛構，示範用"},
        {"label": "含冒號：的標籤", "value": "2026 Q4", "note": 'He said "x"'},
    ],
}


def copy_skeleton(tmp_path: Path, empty_plain_step: int | None = None) -> Path:
    """把骨架複製到 tmp_path；empty_plain_step 指定哪一步的 plain 改成空字串。"""
    text = SKELETON.read_text(encoding="utf-8")
    if empty_plain_step is not None:
        pattern = rf"(\{{ n: {empty_plain_step},.*?\n\s+plain: )'[^']*'"
        text, count = re.subn(pattern, r"\1''", text, count=1, flags=re.DOTALL)
        assert count == 1, "找不到要清空的 plain"
    target = tmp_path / "walkthrough.html"
    target.write_text(text, encoding="utf-8")
    return target


def test_front_matter_takes_values_from_meta():
    fm = yaml.safe_load(front_matter(META_SAMPLE).strip().strip("-"))
    assert fm["type"] == "產品技術研究" and fm["methodology_version"] == "product-technology-v1"
    assert fm["title"] == META_SAMPLE["title"]
    assert fm["ticker"] == "TWSE:0000"
    assert str(fm["date"]) == "2026-11-07"
    assert fm["kpi"] == META_SAMPLE["kpi"]


def test_front_matter_missing_required_field_raises():
    broken = {k: v for k, v in META_SAMPLE.items() if k != "disclaimer"}
    with pytest.raises(ValueError, match="disclaimer"):
        front_matter(broken)


def test_split_items():
    assert split_items(LONG) == ["良率 90%", "功耗降 25%", "密度增 15%", "說明" * 30]
    assert split_items("短句 1、2、3") == ["短句 1、2、3"]


def test_badge_class_matches_n2_mapping():
    assert [badge_class(i) for i in range(1, 6)] == ["l1", "l1", "l2", "l2", "l3"]


def test_badge_class_rejects_unknown_level():
    with pytest.raises(ValueError):
        badge_class(6)


def test_wrap_fragment_is_a_full_document():
    html = wrap_fragment("<p>x</p>")
    assert html.startswith("<!doctype html>") and html.endswith("</body></html>")
    assert "<p>x</p>" in html


def test_no_hardcoded_absolute_path():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "D:/projects" not in text
    assert ".innerText" not in text  # 擷取一律用 textContent


def test_output_is_utf8_with_minus_sign(tmp_path):
    with launch("chromium") as browser:
        md = build(copy_skeleton(tmp_path), tmp_path, "demo.md", browser=browser)
    assert "−5%" in md.read_bytes().decode("utf-8")
    assert not (tmp_path / "_pdfwork").exists()


def test_output_structure_follows_skeleton(tmp_path):
    with launch("chromium") as browser:
        md = build(copy_skeleton(tmp_path), tmp_path, "demo.md", browser=browser)
    text = md.read_text(encoding="utf-8")
    fm = yaml.safe_load(text.split("---")[1])
    assert fm["methodology_version"] == "product-technology-v1"
    assert "## 閱讀說明" in text
    assert "## 第一幕　做出元件" in text and "## 第二幕　誰來供應" in text
    assert "產品線：跟著最小單位" in text  # actLead[1]
    assert "### 步驟 1／3　鋪膜與做出元件" in text
    # 骨架共 4 拍：s01-1、s01-2、s02-1、s03-1
    for name in ("s01-1", "s01-2", "s02-1", "s03-1"):
        assert f"![](pdf-img/{name}.png)" in text
        assert (tmp_path / "pdf-img" / f"{name}.png").stat().st_size > 0
    assert "示範廠商甲" in text and "<span class=\"tag l1\">公司正式文件</span>" in text
    assert "● 有公開資料顯示供貨給示範公司或與示範公司合作" in text
    assert "示範：這一步不列廠商。" in text
    # 預設收合的 <details> 內容也要抓得到
    assert "示範細節：展開後的補充說明" in text


def test_empty_required_field_raises(tmp_path):
    broken = copy_skeleton(tmp_path, empty_plain_step=1)
    with launch("chromium") as browser, pytest.raises(ValueError, match="plain 為空"):
        build(broken, tmp_path, "x.md", browser=browser)
    assert not (tmp_path / "_pdfwork").exists()


def test_cli_runs_without_browser_argument(tmp_path):
    """CLI 自己啟動 Playwright（獨立 process，不受測試共用的 Playwright 影響）。"""
    page = copy_skeleton(tmp_path)
    r = subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(SCRIPT), str(page), str(tmp_path), "cli.md"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert "steps=3 beats=4" in r.stdout
    assert (tmp_path / "cli.md").is_file()
