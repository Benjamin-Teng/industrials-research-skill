"""互動頁骨架（product-technology-walkthrough/assets/walkthrough-skeleton.html）的瀏覽器測試。

環境變數 `WALKTHROUGH_PAGE` 可換成其他互動頁（例如正式成品）：通用檢查照跑，
依賴骨架示範內容的測試 skip。
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from browser_helpers import all_beats, launch, open_page

ROOT = Path(__file__).resolve().parents[1]
PTW = ROOT / "plugins" / "research-report-kit" / "skills" / "product-technology-walkthrough"
SKELETON = PTW / "assets" / "walkthrough-skeleton.html"
PAGE = Path(os.environ["WALKTHROUGH_PAGE"]) if os.environ.get("WALKTHROUGH_PAGE") else SKELETON

# 骨架示範內容的步號
DEMO_PLAIN_STEP = 1  # 兩拍、交會到第 3 步、第 2 拍有一張不存在的圖、沒有 data-net 元件
DEMO_NET_STEP = 2  # 通孔—導線—通孔，網路 n1
DEMO_CROSS_TARGET = 3
DEMO_MISSING_PHOTO = "img/demo-missing.png"
DEMO_PHOTO_URL = "https://example.com/demo-photo-source"
DEMO_PHOTO_CAPTION = "示範圖片：這張圖不存在"

demo_only = pytest.mark.skipif(
    PAGE != SKELETON, reason="WALKTHROUGH_PAGE 已覆寫，依賴骨架示範內容的測試不適用"
)


@pytest.fixture(scope="module")
def page(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Any]:
    with launch("chromium") as browser:
        yield open_page(browser, PAGE, tmp_path_factory.mktemp("walkthrough"))


@demo_only
def test_skeleton_not_gitignored():
    r = subprocess.run(["git", "check-ignore", "--no-index", "-q", str(SKELETON)], cwd=ROOT, check=False)
    assert r.returncode == 1  # 1 = 未忽略；不加 --no-index 時已追蹤檔一律回 1


def test_every_beat_has_text_and_no_undefined(page):
    beats = all_beats(page)
    assert beats
    for n, b in beats:
        page.evaluate("([n,b]) => walkthrough.go(n,b)", [n, b])
        for sel in ("#title", "#plain", "#now"):
            assert page.text_content(sel).strip(), (n, b, sel)
        shown = page.evaluate("document.querySelector('.wrap').textContent")
        assert "undefined" not in shown and "NaN" not in shown, (n, b)


@demo_only
def test_demo_text_keeps_unicode_minus(page):
    texts = []
    for n, b in all_beats(page):
        page.evaluate("([n,b]) => walkthrough.go(n,b)", [n, b])
        texts.append(page.evaluate("document.querySelector('.wrap').textContent"))
    assert any("−5%" in t for t in texts)


@demo_only
def test_cross_chip_jumps_to_target(page):
    page.evaluate(f"walkthrough.go({DEMO_PLAIN_STEP}, 0)")
    chip = page.locator("#cross .chip")
    assert chip.count() == 1
    assert "交會" in chip.text_content()
    chip.click()
    assert page.evaluate("location.hash") == f"#s{DEMO_CROSS_TARGET}"
    assert page.text_content("#title") == page.evaluate(
        f"walkthrough.steps.find(s => s.n === {DEMO_CROSS_TARGET}).title"
    )


@demo_only
def test_missing_photo_shows_caption_card(page):
    page.evaluate(f"walkthrough.go({DEMO_PLAIN_STEP}, 1)")
    page.wait_for_function(f"() => !document.querySelector('svg image[href=\"{DEMO_MISSING_PHOTO}\"]')")
    link = page.locator(f'#svgB a[href="{DEMO_PHOTO_URL}"]')
    assert link.count() == 1
    assert "on" in (link.get_attribute("class") or "").split()
    shown = page.evaluate(
        "[...document.querySelectorAll('#svgB .el.on')].filter(e => e.style.display !== 'none')"
        ".map(e => e.textContent).join('')"
    )
    assert DEMO_PHOTO_CAPTION in shown


@demo_only
def test_dump_scene_returns_annotated_elements(page):
    page.evaluate(f"walkthrough.go({DEMO_NET_STEP}, 0)")
    items = page.evaluate("walkthrough.dumpScene()")
    assert sorted(i["id"] for i in items) == ["demo-v1", "demo-v2", "demo-w1"]
    assert {i["net"] for i in items} == {"n1"}
    assert {i["id"]: i["kind"] for i in items} == {"demo-v1": "via", "demo-w1": "wire", "demo-v2": "via"}
    for i in items:
        assert i["svg"] in ("A", "B")
        assert i["w"] > 0 and i["h"] > 0


@demo_only
def test_dump_scene_empty_on_unannotated_step(page):
    page.evaluate(f"walkthrough.go({DEMO_PLAIN_STEP}, 0)")
    assert page.evaluate("walkthrough.dumpScene()") == []


@pytest.mark.parametrize("engine", ["chromium", "webkit"])
def test_narrow_viewport(engine, tmp_path):  # 375×560；只防一般退化，不是 iOS 證據
    with launch(engine) as browser:
        pg = open_page(browser, PAGE, tmp_path, viewport=(375, 560))
        for n, b in all_beats(pg):
            pg.evaluate("([n,b]) => walkthrough.go(n,b)", [n, b])
            sw, cw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            assert sw <= cw, (engine, n, b, sw, cw)
        pg.evaluate("walkthrough.setImmersive(true)")
        for n, b in all_beats(pg):
            pg.evaluate("([n,b]) => walkthrough.go(n,b)", [n, b])
            box = pg.locator("#panels").bounding_box()
            assert box is not None and box["height"] <= 560, (engine, n, b, box)
