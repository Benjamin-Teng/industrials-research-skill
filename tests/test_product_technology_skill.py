"""結構測試：產品技術拆解 skill（product-technology-walkthrough）。

方法檔是這個 skill 的單一來源；本檔守的是它的章節結構、來源分級、禁用來源清單只定義一次、
示意圖審查標準，以及 SKILL.md 與 Codex 介面的交接點。
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "research-report-kit"
PTW = PLUGIN / "skills" / "product-technology-walkthrough"
METHOD = PTW / "references" / "product-technology-method.md"

FENCE_PREFIXES = ("```", "~~~")
HEADING = re.compile(r"^(#{1,6}) ")

HEADINGS = [
    "## 一、定位與範圍",
    "## 二、主線與兩條線",
    "## 三、蒐集：來源效力",
    "## 四、整合",
    "## 五、生成",
    "## 六、示意圖審查",
    "## 七、限制",
    "## 八、治理",
]
LEVELS = ["公司正式文件", "公司技術文件", "供應商或合作夥伴聲明", "間接來源", "媒體轉述"]


def section(text: str, heading: str) -> str:
    """回傳 heading 行之後、下一個同級或更高級標題之前的內容（不含 heading 行）。

    只認第 0 欄的標題；圍欄內的行不算標題。
    """
    level = len(heading) - len(heading.lstrip("#"))
    in_fence = False
    collecting = False
    body: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith(FENCE_PREFIXES):
            in_fence = not in_fence
        match = None if in_fence else HEADING.match(line)
        if collecting:
            if match and len(match.group(1)) <= level:
                break
            body.append(line)
        elif match and line == heading:
            collecting = True
    if not collecting:
        raise AssertionError(f"找不到標題：{heading}")
    return "\n".join(body) + "\n"


def numbered_items(text: str) -> list[str]:
    """以 `1.` 這類編號開頭的行。"""
    return [line for line in text.splitlines() if re.match(r"^\d+\.", line)]


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path.name} 缺少 front matter"
    return yaml.safe_load(match.group(1)) or {}


def test_method_has_chapters_once():
    text = METHOD.read_text(encoding="utf-8")
    for h in HEADINGS:
        assert text.count(h + "\n") == 1, h


def test_source_levels_are_five_in_order():
    items = numbered_items(section(METHOD.read_text(encoding="utf-8"), "### 3.1 來源分級"))
    assert len(items) == 5
    assert all(name in item for name, item in zip(LEVELS, items, strict=True))


def test_banned_source_list_defined_only_in_method():
    hits = [
        p
        for p in PLUGIN.rglob("*.md")
        if "不能當來源" in p.read_text(encoding="utf-8") and p.name != "CHANGELOG.md"
    ]
    assert hits == [METHOD]
    assert "社群貼文" in section(METHOD.read_text(encoding="utf-8"), "### 3.3 不能當來源的清單")


def test_review_checklist_has_seven_items():
    assert len(numbered_items(section(METHOD.read_text(encoding="utf-8"), "## 六、示意圖審查"))) >= 7


def test_methodology_version_string():
    assert "product-technology-v1" in METHOD.read_text(encoding="utf-8")


def test_skill_description():
    fm = frontmatter(PTW / "SKILL.md")
    assert fm["name"] == "product-technology-walkthrough"
    assert len(fm["description"]) <= 400
    assert "不評價股價" in fm["description"]
    for banned in ("DCF", "目標價", "報酬風險比"):
        assert banned not in fm["description"]


def test_skill_has_codex_handoff_section():
    body = (PTW / "SKILL.md").read_text(encoding="utf-8")
    assert "證據檔" in section(body, "## Codex 端")


def test_openai_yaml_states_collect_and_integrate():
    y = (PTW / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "collect" in y
    assert "integrate" in y
