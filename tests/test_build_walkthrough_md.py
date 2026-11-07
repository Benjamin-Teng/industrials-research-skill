"""build_walkthrough_md.py（互動頁 → md）的測試。

純函式測試不需要瀏覽器；`build()` 的測試用 Playwright，頁面一律先複製到 tmp_path，
不在 plugin 目錄底下產生任何檔案。
"""

from __future__ import annotations

import os
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


def copy_skeleton(
    tmp_path: Path, empty_plain_step: int | None = None, replacements: tuple[tuple[str, str], ...] = ()
) -> Path:
    """把骨架複製到 tmp_path；empty_plain_step 指定哪一步的 plain 改成空字串。

    replacements 是 (原字串, 新字串)，每組都必須剛好命中一次。
    """
    text = SKELETON.read_text(encoding="utf-8")
    if empty_plain_step is not None:
        pattern = rf"(\{{ n: {empty_plain_step}, act:.*?\n\s+plain: )'[^']*'"
        text, count = re.subn(pattern, r"\1''", text, count=1, flags=re.DOTALL)
        assert count == 1, "找不到要清空的 plain"
    for old, new in replacements:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    tmp_path.mkdir(parents=True, exist_ok=True)
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
        assert f"![](pdf-img/demo/{name}.png)" in text
        assert (tmp_path / "pdf-img" / "demo" / f"{name}.png").stat().st_size > 0
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


def test_failed_rebuild_leaves_existing_output_untouched(tmp_path):
    """重產跑到第 2 步才失敗：原有的 md 與圖片逐位元組不變，暫存區清乾淨。"""
    out = tmp_path / "out"
    (out / "pdf-img" / "demo").mkdir(parents=True)
    old = {
        out / "demo.md": b"OLD MD",
        out / "pdf-img" / "demo" / "s01-1.png": b"OLD PNG",
        out / "pdf-img" / "demo" / "s09-9.png": b"STALE",
    }
    for path, data in old.items():
        path.write_bytes(data)
    broken = copy_skeleton(tmp_path / "src", empty_plain_step=2)
    with launch("chromium") as browser, pytest.raises(ValueError, match="step 2.1: plain 為空"):
        build(broken, out, "demo.md", browser=browser)
    assert {p: p.read_bytes() for p in old} == old
    assert sorted(p.name for p in out.rglob("*") if p.is_file()) == sorted(p.name for p in old)
    assert not (out / "_build_tmp").exists() and not (broken.parent / "_pdfwork").exists()


def test_successful_rebuild_replaces_old_output(tmp_path):
    """重產只替換這份 md 自己的圖片子目錄；pdf-img 底下其他檔案不動。"""
    out = tmp_path / "out"
    (out / "pdf-img" / "demo").mkdir(parents=True)
    (out / "demo.md").write_bytes(b"OLD MD")
    (out / "pdf-img" / "demo" / "s09-9.png").write_bytes(b"STALE")
    (out / "pdf-img" / "s01-1.png").write_bytes(b"OTHER")  # 不屬於 demo.md 的檔案
    with launch("chromium") as browser:
        md = build(copy_skeleton(tmp_path / "src"), out, "demo.md", browser=browser)
    assert md == (out / "demo.md").resolve() and "第一幕" in md.read_text(encoding="utf-8")
    assert sorted(p.name for p in (out / "pdf-img" / "demo").iterdir()) == STEP_IMAGES
    assert (out / "pdf-img" / "s01-1.png").read_bytes() == b"OTHER"
    assert not (out / "_build_tmp").exists()


STEP_IMAGES = ["s01-1.png", "s01-2.png", "s02-1.png", "s03-1.png"]


def test_new_version_leaves_old_version_images_untouched(tmp_path):
    """同一個資料夾先產 v1.0 再產 v1.1：v1.0 的 md 與圖片逐位元組不變，v1.1 的圖在自己的子目錄。"""
    out = tmp_path / "out"
    v10, v11 = "demo_v1.0_20261101.md", "demo_v1.1_20261107.md"
    old_dir, new_dir = out / "pdf-img" / "demo_v1.0_20261101", out / "pdf-img" / "demo_v1.1_20261107"
    changed = copy_skeleton(tmp_path / "src11", replacements=(("'成本：−5%'", "'成本：−6%'"),))
    with launch("chromium") as browser:
        build(copy_skeleton(tmp_path / "src10"), out, v10, browser=browser)
        old_md = (out / v10).read_bytes()
        old_imgs = {p.name: p.read_bytes() for p in old_dir.iterdir()}
        build(changed, out, v11, browser=browser)
    assert (out / v10).read_bytes() == old_md
    assert "![](pdf-img/demo_v1.0_20261101/s01-1.png)" in old_md.decode("utf-8")
    assert {p.name: p.read_bytes() for p in old_dir.iterdir()} == old_imgs
    assert sorted(old_imgs) == STEP_IMAGES
    assert sorted(p.name for p in new_dir.iterdir()) == STEP_IMAGES
    assert "![](pdf-img/demo_v1.1_20261107/s01-1.png)" in (out / v11).read_text(encoding="utf-8")
    assert (new_dir / "s01-1.png").read_bytes() != old_imgs["s01-1.png"]  # 確認兩版的圖確實不同


@pytest.mark.parametrize("name", ["sub/demo.md", "demo.txt", "有 空白.md", "demo(1).md"])
def test_md_name_must_be_plain_file_name(tmp_path, name):
    """md 檔名會變成圖片子目錄名與 md 內的圖片路徑，不得含目錄、空白或括號。"""
    with pytest.raises(ValueError, match="md 檔名"):
        build(tmp_path / "unused.html", tmp_path, name)
    assert not (tmp_path / "_build_tmp").exists()


# 來源缺值：骨架第 1 步的 sources 是 ['demo_ar', 'demo_generic']
AR = "demo_ar: { t: 'official', label: '示範：公司年報（虛構）', url: 'https://example.com/annual-report' }"


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        ((AR, "demo_ar: { t: 'official', url: 'https://example.com/annual-report' }"), "step 1.1: 來源 demo_ar 缺 label"),
        ((AR, "demo_ar: { t: 'official', label: '示範：公司年報（虛構）' }"), "step 1.1: 來源 demo_ar 缺 url"),
        (
            (AR, "demo_ar: { t: 'official', label: '示範：公司年報（虛構）', url: 'annual-report.html' }"),
            "step 1.1: 來源 demo_ar 的 url 不是 http(s)",
        ),
        (("sources: ['demo_ar', 'demo_generic'] }", "sources: ['demo_ar', 'demo_nope'] }"), "step 1.1: 來源 demo_nope 不在 SRC"),
    ],
    ids=["missing-label", "missing-url", "non-http-url", "unknown-key"],
)
def test_source_defect_raises(tmp_path, replacement, message):
    broken = copy_skeleton(tmp_path / "src", replacements=(replacement,))
    with launch("chromium") as browser, pytest.raises(ValueError, match=re.escape(message)):
        build(broken, tmp_path / "out", "x.md", browser=browser)
    assert not (tmp_path / "out" / "x.md").exists()


def test_supplier_caption_kept_verbatim(tmp_path):
    """META.supCaveat 只出現在頁面的廠商區；md 要有那一段說明的完整原文。"""
    caveat = "也沒有任何一家明確指出供應示範產品"
    page = copy_skeleton(
        tmp_path / "src",
        replacements=(("    subject: '示範公司',\n", f"    subject: '示範公司',\n    supCaveat: '{caveat}',\n"),),
    )
    with launch("chromium") as browser:
        text = build(page, tmp_path / "out", "demo.md", browser=browser).read_text(encoding="utf-8")
    full = (
        "● 有公開資料顯示供貨給示範公司或與示範公司合作（供應商獎、官方名單、雙方新聞稿或媒體報導）"
        f"　○ 該類主要廠商。名單依類別列出，沒有逐家證明用在這一步，{caveat}。"
    )
    assert f"> {full}" in text


def _seed_old_output(out: Path) -> dict[Path, bytes]:
    (out / "pdf-img" / "demo").mkdir(parents=True)
    old = {out / "demo.md": b"OLD MD", out / "pdf-img" / "demo" / "s01-1.png": b"OLD PNG"}
    for path, data in old.items():
        path.write_bytes(data)
    return old


def _fail_md_replace(monkeypatch, exc: BaseException) -> None:
    """讓「新 md 換入正式位置」這一步拋出 exc，其餘 os.replace 照常。"""
    real = os.replace

    def fake(src, dst, *a, **kw):
        if Path(dst).name == "demo.md":
            raise exc
        return real(src, dst, *a, **kw)

    monkeypatch.setattr(build_walkthrough_md.os, "replace", fake)


def test_interrupt_during_publish_restores_old_output(tmp_path, monkeypatch):
    """發布中途 KeyboardInterrupt：舊 md 與舊圖都還原，例外照樣往上拋，暫存區清掉。"""
    out = tmp_path / "out"
    old = _seed_old_output(out)
    _fail_md_replace(monkeypatch, KeyboardInterrupt())
    with launch("chromium") as browser, pytest.raises(KeyboardInterrupt):
        build(copy_skeleton(tmp_path / "src"), out, "demo.md", browser=browser)
    assert {p: p.read_bytes() for p in old} == old
    assert sorted(p.name for p in out.rglob("*") if p.is_file()) == sorted(p.name for p in old)
    assert not (out / "_build_tmp").exists()


def test_restore_failure_keeps_backup_and_reports_path(tmp_path, monkeypatch, capsys):
    """發布失敗、還原也失敗：保留暫存區與備份，stderr 印出備份路徑，原例外照樣拋出。"""
    out = tmp_path / "out"
    _seed_old_output(out)
    _fail_md_replace(monkeypatch, OSError("replace 失敗"))
    real_rename = Path.rename

    def fake_rename(self, target):
        if self.name == "pdf-img" and self.parent.name == "backup":  # 還原那一步
            raise OSError("還原失敗")
        return real_rename(self, target)

    monkeypatch.setattr(Path, "rename", fake_rename)
    with launch("chromium") as browser, pytest.raises(OSError, match="replace 失敗"):
        build(copy_skeleton(tmp_path / "src"), out, "demo.md", browser=browser)
    backup = out / "_build_tmp" / "backup"
    assert (backup / "pdf-img" / "s01-1.png").read_bytes() == b"OLD PNG"
    assert (out / "demo.md").read_bytes() == b"OLD MD"
    assert str(backup) in capsys.readouterr().err


def test_backup_kept_even_when_marker_file_cannot_be_written(tmp_path, monkeypatch):
    """發布失敗、還原失敗、標記檔也寫不進去，三者同時發生：備份仍然保留，原例外照拋。"""
    out = tmp_path / "out"
    _seed_old_output(out)
    _fail_md_replace(monkeypatch, OSError("replace 失敗"))
    real_rename, real_write = Path.rename, Path.write_text

    def fake_rename(self, target):
        if self.name == "pdf-img" and self.parent.name == "backup":
            raise OSError("還原失敗")
        return real_rename(self, target)

    def fake_write(self, *a, **kw):
        if self.name == "RESTORE_FAILED.txt":
            raise OSError("磁碟已滿")
        return real_write(self, *a, **kw)

    monkeypatch.setattr(Path, "rename", fake_rename)
    monkeypatch.setattr(Path, "write_text", fake_write)
    with launch("chromium") as browser, pytest.raises(OSError, match="replace 失敗"):
        build(copy_skeleton(tmp_path / "src"), out, "demo.md", browser=browser)
    assert (out / "_build_tmp" / "backup" / "pdf-img" / "s01-1.png").read_bytes() == b"OLD PNG"


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """先用共用機制確認 Chromium 可用（缺時 skip，REQUIRE_BROWSER=1 時 fail），再在獨立 process 跑 CLI。"""
    with launch("chromium"):
        pass
    return subprocess.run(
        [sys.executable, "-B", "-X", "utf8", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=cwd,
        check=False,
    )


def test_cli_runs_without_browser_argument(tmp_path):
    """CLI 自己啟動 Playwright（獨立 process，不受測試共用的 Playwright 影響）。"""
    page = copy_skeleton(tmp_path)
    r = _run_cli([str(page), str(tmp_path), "cli.md"], tmp_path)
    assert r.returncode == 0, r.stderr
    assert "steps=3 beats=4" in r.stdout
    assert (tmp_path / "cli.md").is_file()


def test_cli_accepts_relative_paths(tmp_path):
    copy_skeleton(tmp_path)
    r = _run_cli(["walkthrough.html", ".", "rel.md"], tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "rel.md").is_file() and (tmp_path / "pdf-img" / "rel" / "s01-1.png").is_file()
