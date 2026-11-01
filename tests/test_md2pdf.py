"""md2pdf.py 的測試：純函式單元測試，加上需要 pandoc＋chromium 的端到端測試（缺依賴時 skip）。"""

from __future__ import annotations

import importlib.util
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

_SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "research-report-kit"
    / "skills"
    / "research-report-output"
    / "scripts"
)
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

_spec = importlib.util.spec_from_file_location("md2pdf", _SCRIPTS_DIR / "md2pdf.py")
assert _spec is not None and _spec.loader is not None
md2pdf: ModuleType = importlib.util.module_from_spec(_spec)
sys.modules["md2pdf"] = md2pdf
_spec.loader.exec_module(md2pdf)


def test_toc_does_not_double_escape_ampersand() -> None:
    _, toc = md2pdf.build_toc("<h2>5.3 O&amp;M 服務</h2>")
    assert "5.3 O&amp;M 服務" in toc
    assert "&amp;amp;" not in toc


def test_toc_does_not_double_escape_less_than() -> None:
    _, toc = md2pdf.build_toc("<h3>A &lt; B</h3>")
    assert ">A &lt; B<" in toc
    assert "&amp;lt;" not in toc


# ---------------------------------------------------------------- 端到端：相對路徑圖片
def _write_png(path: Path, width: int, height: int) -> None:
    """不靠 Pillow 寫一張純色 RGB PNG。"""
    raw = b"".join(b"\x00" + bytes([200, 30, 30]) * width for _ in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def _pdf_image_sizes(pdf: Path) -> list[tuple[int, int]]:
    """列出 PDF 內所有影像 XObject 的像素尺寸（含 Form XObject 內層）。"""
    from pypdf import PdfReader

    sizes: list[tuple[int, int]] = []

    def walk(resources: Any) -> None:
        xobjects = (resources or {}).get("/XObject")
        if not xobjects:
            return
        for ref in xobjects.get_object().values():
            obj = ref.get_object()
            if obj.get("/Subtype") == "/Image":
                sizes.append((int(obj["/Width"]), int(obj["/Height"])))
            elif obj.get("/Subtype") == "/Form":
                walk(obj.get("/Resources"))

    for page in PdfReader(pdf).pages:
        walk(page.get("/Resources"))
    return sizes


requires_renderer = pytest.mark.skipif(
    shutil.which("pandoc") is None or importlib.util.find_spec("playwright") is None,
    reason="需要 pandoc 與 playwright（chromium 未安裝時測試會失敗並附 md2pdf 錯誤訊息）",
)


@requires_renderer
def test_relative_image_is_embedded_at_original_size(tmp_path: Path) -> None:
    # 報告目錄名含空白與中文：檔案 URI 必須正確編碼，否則 Windows 上載不到
    report_dir = tmp_path / "報告 目錄"
    (report_dir / "fig").mkdir(parents=True)
    _write_png(report_dir / "fig" / "chart.png", 120, 120)
    md = report_dir / "report.md"
    md.write_text(
        "---\ntitle: 測試\n---\n\n## 第一節\n\n![圖](fig/chart.png)\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(_SCRIPTS_DIR / "md2pdf.py"), str(md)],
        capture_output=True, text=True, encoding="utf-8", check=False,
    )

    assert result.returncode == 0, result.stderr
    # 破圖時 Chromium 只嵌入 14×16 的破圖圖示
    assert (120, 120) in _pdf_image_sizes(report_dir / "report.pdf")
    # 中間 HTML 不留在報告目錄
    assert sorted(p.name for p in report_dir.iterdir()) == ["fig", "report.md", "report.pdf"]
