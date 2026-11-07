"""結構測試：產品技術拆解 skill（product-technology-walkthrough）。

方法檔是這個 skill 的單一來源；本檔守的是它的章節結構、來源分級、禁用來源清單只定義一次、
示意圖審查標準，以及 SKILL.md 與 Codex 介面的交接點。
"""

from __future__ import annotations

import re
import subprocess
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


REVIEW_KEYWORDS = [
    ("接點", "不交叉"),
    ("疊在", "實際畫出的物件"),
    ("上下順序", "前後步驟連續"),
    ("左右兩圖", "位置一致"),
    ("圖說", "標籤"),
    ("錯誤狀態", "合法"),
    ("375px",),
]


def test_review_checklist_has_seven_items():
    body = section(METHOD.read_text(encoding="utf-8"), "## 六、示意圖審查")
    items = numbered_items(body)
    assert len(items) >= 7
    for number, keywords in enumerate(REVIEW_KEYWORDS):
        for word in keywords:
            assert word in items[number], (number + 1, word)
    for phrase in ("獨立 agent", "逐條算座標", "連接表"):
        assert phrase in body, phrase


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
    codex = section((PTW / "SKILL.md").read_text(encoding="utf-8"), "## Codex 端")
    assert "Codex 只做蒐集與整合" in codex
    for deliverable in ("每幕證據檔", "廠商名單", "每幕審查紀錄"):
        assert deliverable in codex, deliverable
    assert re.search(r"齊備(就|即)停", codex)
    assert re.search(r"互動頁、md、PDF[^。]*交給 Claude Code", codex)


def test_openai_yaml_states_collect_and_integrate():
    y = (PTW / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert "collect" in y
    assert "integrate" in y


OUTPUT_DIR = PLUGIN / "skills" / "research-report-output"
OUTPUT_SPEC = OUTPUT_DIR / "references" / "output-spec.md"
OUTPUT_SKILL = OUTPUT_DIR / "SKILL.md"
LAYER1_METHOD = PLUGIN / "skills" / "business-industry-analysis" / "references" / "business-industry-method.md"


def test_output_spec_defines_type_e_after_d():
    spec = OUTPUT_SPEC.read_text(encoding="utf-8")
    d, e = spec.index("### D 型｜"), spec.index("### E 型｜產品技術研究")
    assert d < e and "product-technology-v1" in spec


def test_routing_mentions_type_e():
    assert "E 型" in section(OUTPUT_SKILL.read_text(encoding="utf-8"), "## 工作流程")


def test_no_four_type_wording_left():
    for p in (OUTPUT_SKILL, OUTPUT_SPEC, ROOT / "README.md"):
        t = p.read_text(encoding="utf-8")
        assert "四型" not in t and "{A,B,C,D}" not in t, p


def test_layer1_points_to_new_skill():
    m = LAYER1_METHOD.read_text(encoding="utf-8")
    assert "技術報告（另案）" not in m and "product-technology-walkthrough" in m


def test_output_spec_type_e_has_no_market_data_fields():
    body = section(OUTPUT_SPEC.read_text(encoding="utf-8"), "### E 型｜產品技術研究（methodology_version: product-technology-v1）")
    for word in ("build_walkthrough_md.py", "沒有價格與市場數據", "product-technology-method.md"):
        assert word in body, word


def test_output_spec_filename_and_checklist_cover_type_e():
    spec = OUTPUT_SPEC.read_text(encoding="utf-8")
    assert "_產品技術研究_v1.0_" in spec
    checklist = section(spec, "## 八、發布前檢查清單（格式層）")
    assert "E 型" in checklist and "product-technology-walkthrough" in checklist


def test_output_skill_description_and_modes_cover_type_e():
    text = OUTPUT_SKILL.read_text(encoding="utf-8")
    assert "產品技術" in frontmatter(OUTPUT_DIR / "SKILL.md")["description"]
    assert "**E 型保留**" in section(text, "### External（傳播）")
    assert "**E 型保留**" in section(text, "### Briefing（摘要，≤3 頁）")


def test_plugin_readme_no_four_type_wording():
    assert "四型" not in (PLUGIN / "README.md").read_text(encoding="utf-8")


EX = ROOT / "examples" / "tsmc-n2-walkthrough"
LOCAL = re.compile(r"C:\\Users|AppData|G:\\|D:[/\\]projects|[\w.+-]+@[\w-]+\.[\w.]+")


def test_example_has_expected_files():  # 先確認首例存在，下面幾條才不會在空目錄上空轉通過
    names = {p.relative_to(EX).as_posix() for p in EX.rglob("*") if p.is_file()}
    assert {"README.md", "CONFORMANCE.md"} <= names
    assert len(list(EX.glob("*.html"))) == 1
    assert len([p for p in EX.glob("*.md") if p.name not in ("README.md", "CONFORMANCE.md")]) == 1
    assert list((EX / "research").glob("*.md"))


def test_example_page_not_gitignored():
    page = next(EX.glob("*.html"))
    assert subprocess.run(["git", "check-ignore", "--no-index", "-q", str(page)], cwd=ROOT, check=False).returncode == 1


def test_example_has_only_text_files():
    allowed = {".html", ".md"}
    assert [p for p in EX.rglob("*") if p.is_file() and p.suffix.lower() not in allowed] == []


def test_example_has_no_local_paths_or_email():
    for p in EX.rglob("*"):
        if p.is_file():
            assert not LOCAL.search(p.read_text(encoding="utf-8")), p


def test_example_md_has_no_dangling_image_links():
    for p in EX.rglob("*.md"):
        assert "pdf-img/" not in p.read_text(encoding="utf-8"), p
