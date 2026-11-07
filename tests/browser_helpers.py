"""瀏覽器測試的共用工具：啟動 Playwright、把互動頁片段包上外殼後開啟、列出每一拍。

互動頁原始檔是片段（沒有 `<!doctype html>` 外殼），發布時由 claude.ai 包上。測試前先包一層與
`build_walkthrough_md.py` 相同的外殼再開。

缺瀏覽器時預設 skip；設 `REQUIRE_BROWSER=1` 時改為 fail，避免 CI 上悄悄跳過。
"""

from __future__ import annotations

import atexit
import importlib.util
import os
import shutil
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any, NoReturn

import pytest

ROOT = Path(__file__).resolve().parents[1]
PTW = ROOT / "plugins" / "research-report-kit" / "skills" / "product-technology-walkthrough"
SKELETON = PTW / "assets" / "walkthrough-skeleton.html"
SCRIPT = PTW / "scripts" / "build_walkthrough_md.py"

# 外殼只在腳本裡寫一份：以檔案路徑載入（目錄名含連字號，無法用一般 import），測試共用同一個模組物件。
_spec = importlib.util.spec_from_file_location("build_walkthrough_md", SCRIPT)
assert _spec is not None and _spec.loader is not None
build_walkthrough_md: ModuleType = importlib.util.module_from_spec(_spec)
sys.modules["build_walkthrough_md"] = build_walkthrough_md
_old_dont_write = sys.dont_write_bytecode
sys.dont_write_bytecode = True  # 載入腳本（含它載入的 fa_check）時不在 plugin 目錄寫 __pycache__
try:
    _spec.loader.exec_module(build_walkthrough_md)
finally:
    sys.dont_write_bytecode = _old_dont_write
wrap_fragment = build_walkthrough_md.wrap_fragment


def _unavailable(reason: str) -> NoReturn:
    if os.environ.get("REQUIRE_BROWSER") == "1":
        pytest.fail(f"REQUIRE_BROWSER=1，但{reason}")
    pytest.skip(reason)


_playwright: Any = None


def _shared_playwright() -> Any:
    """同一個 process 只能有一個 sync Playwright 在跑，所以全部測試共用一個，結束時才關。"""
    global _playwright
    if _playwright is None:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            _unavailable("沒有安裝 playwright")
        _playwright = sync_playwright().start()
        atexit.register(_playwright.stop)
    return _playwright


@contextmanager
def launch(engine: str = "chromium") -> Iterator[Any]:
    """啟動 headless 瀏覽器；缺 playwright 或瀏覽器執行檔時依 REQUIRE_BROWSER skip 或 fail。"""
    pw = _shared_playwright()
    from playwright.sync_api import Error as PlaywrightError

    try:
        browser = getattr(pw, engine).launch(headless=True)
    except PlaywrightError as exc:  # 瀏覽器執行檔不存在
        _unavailable(f"{engine} 無法啟動：{exc}")
    try:
        yield browser
    finally:
        browser.close()


def open_page(
    browser: Any,
    page_path: Path,
    tmp_path: Path,
    viewport: tuple[int, int] = (375, 560),
    console_errors: list[str] | None = None,
) -> Any:
    """把互動頁複製到 tmp_path、包上外殼後開啟；頁面載入時若有 JS 例外就直接失敗。

    傳入 console_errors 時，從載入開始收集 console.error 的文字。
    """
    src = page_path.read_text(encoding="utf-8")
    if (page_path.parent / "img").is_dir():
        shutil.copytree(page_path.parent / "img", tmp_path / "img", dirs_exist_ok=True)
    tmp_path.mkdir(parents=True, exist_ok=True)
    target = tmp_path / page_path.name
    target.write_text(wrap_fragment(src), encoding="utf-8")

    page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]}, device_scale_factor=1)
    errors: list[str] = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    if console_errors is not None:
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.goto(target.as_uri())
    page.wait_for_function("() => window.walkthrough !== undefined")
    assert not errors, f"頁面載入時發生 JS 例外：{errors}"
    return page


def all_beats(page: Any) -> list[tuple[int, int]]:
    """回傳每一拍的 (步號, 拍索引)；拍索引從 0 起，與 walkthrough.go(n, b) 相同。"""
    pairs = page.evaluate("walkthrough.steps.flatMap(s => s.beats.map((_, b) => [s.n, b]))")
    return [(int(n), int(b)) for n, b in pairs]
