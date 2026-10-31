"""md2pdf.py 的單元測試（只測不需要 pandoc／chromium 的純函式）。"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

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
