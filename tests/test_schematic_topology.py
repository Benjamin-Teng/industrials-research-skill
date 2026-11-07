"""schematic_topology.py（示意圖連接關係檢查）的測試。

純函式測試不需要瀏覽器；CLI 測試用 subprocess 跑腳本（同一個 process 只能有一個 sync Playwright，
測試 process 已有共用的一個），頁面一律先複製到 tmp_path，不在 plugin 目錄底下產生任何檔案。
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any, Self

import pytest
from browser_helpers import PTW, SKELETON, _unavailable, launch

TOPOLOGY = PTW / "scripts" / "schematic_topology.py"
DEMO_PLAIN_STEP = 1  # 與 test_walkthrough_skeleton.py 相同：沒有 data-net 元件
DEMO_NET_STEP = 2  # 通孔—導線—通孔，網路 n1

_spec = importlib.util.spec_from_file_location("schematic_topology", TOPOLOGY)
assert _spec is not None and _spec.loader is not None
topology = importlib.util.module_from_spec(_spec)
sys.modules["schematic_topology"] = topology
_old = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    _spec.loader.exec_module(topology)
finally:
    sys.dont_write_bytecode = _old
check = topology.check
gap = topology.gap
connection_table = topology.connection_table


def wire(id: str, net: str, x: float, y: float, w: float, h: float) -> dict[str, Any]:
    return {"id": id, "svg": "A", "part": "m", "net": net, "kind": "wire", "x": x, "y": y, "w": w, "h": h}


def via(id: str, net: str, x: float, y: float) -> dict[str, Any]:
    return {"id": id, "svg": "A", "part": "v", "net": net, "kind": "via", "x": x, "y": y, "w": 4, "h": 4}


def node(id: str, net: str, x: float, y: float, w: float, h: float) -> dict[str, Any]:
    return {"id": id, "svg": "A", "part": "n", "net": net, "kind": "node", "x": x, "y": y, "w": w, "h": h}


def kinds(issues: list[dict[str, Any]]) -> list[str]:
    return [i["kind"] for i in issues]


def test_end_contacts_ok():
    assert check([via("v1", "n1", 0, 0), wire("w1", "n1", 4, 0, 36, 4), via("v2", "n1", 40, 0)]) == []


def test_face_contacts_ok():  # 通孔從上方接在導線兩端附近
    assert check([wire("w1", "n1", 0, 4, 40, 4), via("v1", "n1", 0, 0), via("v2", "n1", 36, 0)]) == []


def test_stub_beyond_last_contact():  # 導線右端多伸出 20，超過 stub
    assert kinds(check([wire("w1", "n1", 0, 4, 60, 4), via("v1", "n1", 0, 0), via("v2", "n1", 36, 0)])) == ["懸空端點"]


def test_stub_within_limit_ok():  # 多伸出 2 剛好不超過預設 stub
    assert check([wire("w1", "n1", 0, 4, 42, 4), via("v1", "n1", 0, 0), via("v2", "n1", 36, 0)]) == []


def test_stub_past_large_node_is_dangling():  # 寬 40 的 node 蓋住導線右段，導線又從 node 右緣伸出 20
    boxes = [wire("w1", "n1", 0, 4, 100, 4), via("v1", "n1", 0, 0), node("n", "n1", 40, 0, 40, 12)]
    issues = check(boxes)
    assert kinds(issues) == ["懸空端點"]
    assert "末端伸出最外側接觸點 20" in issues[0]["detail"]


def test_node_extending_past_wire_end_is_not_a_stub():  # node 長軸範圍超出導線末端：末端在 node 內，不算懸空
    assert check([wire("w1", "n1", 0, 4, 60, 4), via("v1", "n1", 0, 0), node("n", "n1", 40, 0, 40, 12)]) == []


def test_single_contact_is_dangling():
    assert kinds(check([via("v1", "n1", 0, 0), wire("w1", "n1", 4, 0, 36, 4)])) == ["懸空端點"]


def test_vertical_wire_uses_y_axis():  # h > w 的導線沿 y 軸判斷
    ok = [via("v1", "n1", 0, 0), wire("w1", "n1", 0, 4, 4, 36), via("v2", "n1", 0, 40)]
    assert check(ok) == []
    stub = [via("v1", "n1", 0, 0), wire("w1", "n1", 0, 4, 4, 60), via("v2", "n1", 0, 40)]
    assert kinds(check(stub)) == ["懸空端點"]


def test_isolated_via():
    assert kinds(check([via("v1", "n1", 0, 0)])) == ["孤立通孔"]


def test_via_touching_other_net_is_still_isolated():
    issues = check([via("v1", "n1", 0, 0), wire("w2", "n2", 4, 0, 36, 4)])
    assert "孤立通孔" in kinds(issues) and "短路" in kinds(issues)


def test_short_and_near_between_nets():
    assert "短路" in kinds(check([wire("a", "n1", 0, 0, 10, 4), wire("b", "n2", 10, 0, 10, 4)]))
    assert "過近" in kinds(check([wire("a", "n1", 0, 0, 10, 4), wire("b", "n2", 13, 0, 10, 4)]))


def test_far_between_nets_ok():
    boxes = [wire("a", "n1", 0, 0, 10, 4), wire("b", "n2", 16, 0, 10, 4)]
    assert "過近" not in kinds(check(boxes)) and "短路" not in kinds(check(boxes))


def test_other_svg_not_compared():
    a = wire("a", "n1", 0, 0, 10, 4)
    b = {**wire("b", "n2", 0, 0, 10, 4), "svg": "B"}
    assert "短路" not in kinds(check([a, b]))


def test_node_joins_shorts_and_connectivity_but_no_end_check():
    # node 當作接觸點，讓導線兩端都有接；node 本身不做端點檢查
    ok = [node("n_a", "n1", 0, 0, 10, 10), wire("w1", "n1", 10, 4, 20, 2), node("n_b", "n1", 30, 0, 10, 10)]
    assert check(ok) == []
    assert "短路" in kinds(check([node("n_a", "n1", 0, 0, 10, 10), node("n_b", "n2", 10, 0, 10, 10)]))
    assert check([node("n_a", "n1", 0, 0, 10, 10)]) == []


def test_gap_distance():
    a, b = wire("a", "n1", 0, 0, 10, 4), wire("b", "n2", 13, 8, 10, 4)
    assert gap(a, b) == 5.0  # dx=3, dy=4
    assert gap(a, wire("c", "n2", 5, 2, 10, 4)) == 0  # 重疊
    assert gap(a, wire("d", "n2", 10, 0, 10, 4)) == 0  # 相接
    assert gap(a, {**b, "svg": "B"}) == float("inf")  # 不同圖不比較


def test_connection_table_shape():
    boxes = [via("v1", "n1", 0, 0), wire("w1", "n1", 4, 0, 36, 4), via("v2", "n1", 40, 0)]
    table = connection_table(boxes, check(boxes)).splitlines()
    assert table[0] == "| 元件 | 網路 | 接到 | 問題 |"
    assert len(table) == 2 + len(boxes)
    assert all(row.count("|") == 5 for row in table)  # 4 欄
    w1_row = next(r for r in table if r.startswith("| w1 |"))
    assert "v1" in w1_row and "v2" in w1_row


def test_connection_table_marks_issue():
    boxes = [via("v1", "n1", 0, 0)]
    table = connection_table(boxes, check(boxes))
    assert "孤立通孔" in table


def test_pure_functions_do_not_import_playwright():
    code = (
        "import importlib.util, sys;"
        f"s = importlib.util.spec_from_file_location('t', {str(TOPOLOGY)!r});"
        "m = importlib.util.module_from_spec(s); s.loader.exec_module(m);"
        "m.check([]); m.connection_table([], []);"
        "assert 'playwright' not in sys.modules"
    )
    r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, encoding="utf-8", check=False)
    assert r.returncode == 0, r.stderr


def run_cli(page: Path, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(TOPOLOGY), str(page), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )


def skeleton_copy(tmp_path: Path) -> Path:
    page = tmp_path / "page.html"
    page.write_text(SKELETON.read_text(encoding="utf-8"), encoding="utf-8")
    return page


def test_cli_exit_codes(tmp_path):  # 瀏覽器測試
    with launch():  # 缺瀏覽器時依 REQUIRE_BROWSER skip 或 fail
        pass
    page = skeleton_copy(tmp_path)
    r = run_cli(page, "--step", DEMO_NET_STEP, "--beat", 0)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "| 元件 | 網路 | 接到 | 問題 |" in r.stdout and "demo-w1" in r.stdout
    r = run_cli(page, "--step", DEMO_PLAIN_STEP, "--beat", 0)
    assert r.returncode == 2 and "沒有標註網路的元件" in r.stdout
    assert sorted(p.name for p in tmp_path.iterdir()) == ["page.html"]  # 中間檔已刪


def test_cli_whole_page_and_bad_step(tmp_path):
    with launch():
        pass
    page = skeleton_copy(tmp_path)
    r = run_cli(page)  # 逐拍：至少有一拍有標註元件、沒有問題
    assert r.returncode == 0, r.stdout + r.stderr
    assert "demo-v1" in r.stdout and "沒有標註網路的元件" in r.stdout
    r = run_cli(page, "--step", 99)
    assert r.returncode == 3 and "沒有步驟 99" in r.stderr


def test_cli_reports_problem_with_exit_1(tmp_path):
    with launch():
        pass
    page = skeleton_copy(tmp_path)
    text = page.read_text(encoding="utf-8")
    moved = "R(288, 136, 16, 94)"
    assert text.count(moved) == 1
    page.write_text(text.replace(moved, "R(288, 236, 16, 94)"), encoding="utf-8")  # 右通孔移到導線下方遠處
    r = run_cli(page, "--step", DEMO_NET_STEP, "--beat", 0)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "懸空端點" in r.stdout and "孤立通孔" in r.stdout


# ---- Playwright 例外一律轉成 exit 3（不開真的瀏覽器，用假的 sync_playwright 注入）


class _FakePage:
    def __init__(self, fail: str | None) -> None:
        self.fail = fail

    def on(self, *_: object) -> None:
        pass

    def goto(self, *_: object) -> None:
        pass

    def wait_for_function(self, *_: object) -> None:
        if self.fail == "timeout":
            from playwright.sync_api import TimeoutError as PlaywrightTimeout

            raise PlaywrightTimeout("Timeout 30000ms exceeded.")

    def evaluate(self, *_: object) -> list[Any]:
        if self.fail == "evaluate":
            from playwright.sync_api import Error as PlaywrightError

            raise PlaywrightError("Page.evaluate: ReferenceError: walkthrough is not defined")
        return [[1, 0]]


class _FakeBrowser:
    def __init__(self, fail: str | None) -> None:
        self.fail = fail
        self.closed = False

    def new_context(self, **_: object) -> Any:
        fail = self.fail

        class _Ctx:
            def new_page(self) -> _FakePage:
                return _FakePage(fail)

        return _Ctx()

    def close(self) -> None:
        self.closed = True


def _fake_sync_playwright(fail: str | None, browsers: list[_FakeBrowser]) -> Any:
    class _Chromium:
        def launch(self, **_: object) -> _FakeBrowser:
            if fail == "launch":
                from playwright.sync_api import Error as PlaywrightError

                raise PlaywrightError("BrowserType.launch: Executable doesn't exist")
            browser = _FakeBrowser(fail)
            browsers.append(browser)
            return browser

    class _Pw:
        chromium = _Chromium()

        def __enter__(self) -> Self:
            return self

        def __exit__(self, *_: object) -> None:
            pass

    return lambda: _Pw()


@pytest.mark.parametrize("fail", ["evaluate", "timeout", "launch"])
def test_playwright_errors_exit_3(fail, tmp_path, monkeypatch, capsys):
    try:
        from playwright import sync_api
    except ImportError:
        _unavailable("沒有安裝 playwright")
    browsers: list[_FakeBrowser] = []
    monkeypatch.setattr(sync_api, "sync_playwright", _fake_sync_playwright(fail, browsers))
    page = skeleton_copy(tmp_path)
    code = topology.main(["schematic_topology.py", str(page), "--step", str(DEMO_NET_STEP)])
    assert code == 3
    assert "停止檢查" in capsys.readouterr().err
    assert sorted(p.name for p in tmp_path.iterdir()) == ["page.html"]  # 中間檔已刪
    assert all(b.closed for b in browsers)  # 瀏覽器有關
