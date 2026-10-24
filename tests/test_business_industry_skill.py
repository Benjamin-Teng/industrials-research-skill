"""結構測試：Layer 1 企業與產業分析 skill（business-industry-analysis）。

方法檔是 Layer 1 的單一來源；本檔守的是它的章節結構、紅線只定義一次、治理自成一體，
以及 SKILL.md 的 SEC 指令樣板不展開、不印出 User-Agent 環境變數。
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "research-report-kit"
SKILL_DIR = PLUGIN / "skills" / "business-industry-analysis"
SKILL = SKILL_DIR / "SKILL.md"
METHOD = SKILL_DIR / "references" / "business-industry-method.md"
OUTPUT_DIR = PLUGIN / "skills" / "research-report-output"
D_TEMPLATE = OUTPUT_DIR / "templates" / "D-business-industry.md"
OUTPUT_SKILL = OUTPUT_DIR / "SKILL.md"
OUTPUT_SPEC = OUTPUT_DIR / "references" / "output-spec.md"
CUSTOMIZE = OUTPUT_DIR / "references" / "customize-your-framework.md"
TEMPLATES = OUTPUT_DIR / "templates"
SAMPLE = PLUGIN / "examples" / "sample-report.md"
PCR_SKILL = PLUGIN / "skills" / "product-cycle-rotation" / "SKILL.md"

VALUATION_REFS = (
    r"equity-valuation-discipline|valuation-paths|expectations-and-decisions|"
    r"calibration-and-governance|prepublish-checklist|valuation_math"
)

METHOD_CHAPTERS = (
    "## 一、定位與範圍",
    "## 二、研究流程八步驟",
    "## 三、商業模式類型與單位經濟量尺路由表",
    "## 四、不評價股價的紅線",
    "## 五、資料標示與紀律",
    "## 六、治理",
    "## 七、引用文獻",
)
UA_FORMS = (
    '-A "$SEC_USER_AGENT"',
    "-UserAgent $env:SEC_USER_AGENT",
    '[ -n "$SEC_USER_AGENT" ] && echo set || echo missing',
    "if ($env:SEC_USER_AGENT) {'set'} else {'missing'}",
)
UA_PRINT = re.compile(r"(echo|printf|Write-Output|Write-Host)\s+[^|;&\n]*\$\{?(env:)?SEC_USER_AGENT")
UA_BARE = re.compile(r"^\s*[\"']?\$\{?(env:)?SEC_USER_AGENT\}?[\"']?\s*$")
DEBUG_DUMP = re.compile(r"^\s*(set -x|Set-PSDebug|printenv|env\s*$|Get-ChildItem\s+env:)")
CURL_VERBOSE = re.compile(r"\bcurl\b[^|]*\s(-[A-Za-z]*v[A-Za-z]*|--verbose|--trace\S*)(\s|$)")

FENCE_PREFIXES = ("```", "~~~")
HEADING = re.compile(r"^(#{1,6}) ")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def front_matter(path: Path) -> dict:
    text = read(path)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path.name} 缺少 front matter"
    return yaml.safe_load(match.group(1)) or {}


def section(text: str, heading: str) -> str:
    """回傳 heading 行之後、下一個同級或更高級標題之前的內容（不含 heading 行）。

    只認第 0 欄的標題；圍欄（含縮排圍欄）內的行不算標題。
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


def code_lines(text: str) -> list[str]:
    """所有圍欄內的行（含縮排圍欄），不含圍欄行本身。"""
    in_fence = False
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith(FENCE_PREFIXES):
            in_fence = not in_fence
        elif in_fence:
            lines.append(line)
    return lines


def inline_code(text: str) -> list[str]:
    return re.findall(r"`([^`\n]+)`", text)


def assert_no_ua_exposure(case: unittest.TestCase, lines: list[str], allowed: tuple[str, ...] = UA_FORMS) -> None:
    for line in lines:
        if "SEC_USER_AGENT" in line and "$" in line:  # 不含 $ 的是變數名稱或設定式，不會展開值
            case.assertTrue(any(f in line for f in allowed), line)
            case.assertIsNone(UA_PRINT.search(line), line)
            case.assertIsNone(UA_BARE.search(line), line)
        case.assertIsNone(DEBUG_DUMP.search(line), line)
        case.assertIsNone(CURL_VERBOSE.search(line), line)


class TestHelpers(unittest.TestCase):
    def test_section_skips_fences_and_excludes_heading(self) -> None:
        body = section("## A\nx\n```bash\n# note\n```\ny\n## B\nz\n", "## A")
        self.assertNotIn("## A", body)
        self.assertIn("y", body)
        self.assertNotIn("z", body)

    def test_section_and_code_lines_handle_indented_fences(self) -> None:
        text = "## A\n- item\n   ```bash\n   # note\n   curl -v x\n   ```\nafter\n## B\n"
        self.assertIn("after", section(text, "## A"))
        self.assertEqual([line.strip() for line in code_lines(text)], ["# note", "curl -v x"])

    def test_section_raises_when_heading_missing(self) -> None:
        with self.assertRaises(AssertionError):
            section("## A\nx\n", "## B")

    def test_exposure_guard_catches_known_leaks(self) -> None:
        for bad in (
            'echo "${SEC_USER_AGENT}"',
            "Write-Host $env:SEC_USER_AGENT",
            "$env:SEC_USER_AGENT",
            'curl -sSv -A "$SEC_USER_AGENT" u',
            "set -x",
            "printenv",
        ):
            with self.subTest(bad=bad), self.assertRaises(AssertionError, msg=bad):
                assert_no_ua_exposure(self, [bad])
        assert_no_ua_exposure(self, ['curl -sS -A "$SEC_USER_AGENT" u | grep -v x'])


class TestMethodSingleSource(unittest.TestCase):
    def test_method_declares_layer1_methodology(self) -> None:
        self.assertIn("`methodology_version: business-industry-v1`", read(METHOD))

    def test_method_chapters_in_order(self) -> None:
        text = read(METHOD)
        positions = [text.index(h) for h in METHOD_CHAPTERS]
        self.assertEqual(positions, sorted(positions))

    def test_red_line_list_is_complete(self) -> None:
        body = section(read(METHOD), "### 4.2 報告中不出現的內容")
        self.assertEqual(len(re.findall(r"^\d+\. ", body, re.MULTILINE)), 5)

    def test_red_line_boundary_table_has_eight_cases(self) -> None:
        body = section(read(METHOD), "### 4.3 只陳述事實與機制的邊界情況")
        rows = [r for r in body.splitlines() if r.startswith("|") and "---" not in r]
        self.assertEqual(len(rows) - 1, 8)

    def test_red_line_is_defined_once(self) -> None:
        for phrase in ("媒體標題中的股價敘事", "以價格衍生的量法"):
            hits = [p for p in PLUGIN.rglob("*.md") if p.name != "CHANGELOG.md" and phrase in read(p)]
            self.assertEqual(hits, [METHOD], phrase)

    def test_label_table_has_all_layer1_states(self) -> None:
        body = section(read(METHOD), "### 5.1 標示對照表")
        for label in (
            "`l1`",
            "`l2`",
            "`l3`",
            "口述",
            "第三方逐字稿",
            "推論",
            "未揭露",
            "未查到",
            "未核對",
            "屬技術報告範圍",
        ):
            self.assertIn(label, body)

    def test_observation_zone_holds_open_standard_item(self) -> None:
        self.assertRegex(
            section(read(METHOD), "### 6.3 觀察區"),
            r"(?m)^- \*\*OB-1\*\* 開放標準削弱指令集護城河",
        )

    def test_observation_zone_lists_all_eight_items(self) -> None:
        body = section(read(METHOD), "### 6.3 觀察區")
        ids = re.findall(r"(?m)^- \*\*(OB-\d+)\*\*", body)
        self.assertEqual(ids, [f"OB-{n}" for n in range(1, 9)])

    def test_governance_sets_its_own_cadence(self) -> None:
        self.assertIn("每季至多一代", section(read(METHOD), "### 6.5 升版節奏"))

    def test_governance_stands_alone(self) -> None:
        self.assertIsNone(re.search(VALUATION_REFS, section(read(METHOD), "## 六、治理")))

    def test_method_and_skill_are_self_contained(self) -> None:
        for path in (METHOD, SKILL):
            for line in read(path).splitlines():
                if re.search(VALUATION_REFS, line):
                    self.assertIn("若有安裝", line, f"{path.name}: {line}")

    def test_excluded_frameworks_stay_out(self) -> None:
        for path in (METHOD, SKILL):
            for word in ("微笑曲線", "Slywotzky", "價值遷移"):
                self.assertNotIn(word, read(path))


class TestSkillEntry(unittest.TestCase):
    def test_description_follows_repo_convention(self) -> None:
        d = front_matter(SKILL)["description"]
        for word in ("時使用", "觸發詞包含", "個股深度研究", "商業模式", "SWOT", "護城河", "產業鏈", "利潤池"):
            self.assertIn(word, d)
        self.assertLessEqual(len(d), 400)

    def test_compatibility_lists_optional_tools(self) -> None:
        compat = front_matter(SKILL)["metadata"]["compatibility"]
        self.assertIn("pdftotext", compat)
        self.assertIn("pandoc", compat)

    def test_sec_templates_read_env_var_without_printing(self) -> None:
        text = read(SKILL)
        self.assertIn('-A "$SEC_USER_AGENT"', text)
        self.assertIn("-UserAgent $env:SEC_USER_AGENT", text)
        assert_no_ua_exposure(self, code_lines(text) + inline_code(text))

    def test_host_fallbacks_cover_both_hosts(self) -> None:
        body = section(read(SKILL), "### 沒有 SEC_USER_AGENT 時")
        for word in ("Claude Code", "Codex", "未查到", "::: caveat"):
            self.assertIn(word, body)

    def test_finmind_period_rules_present(self) -> None:
        for word in ("revenue_year", "revenue_month", "MOPS"):
            self.assertIn(word, read(SKILL))

    def test_pdf_tables_use_raw_mode(self) -> None:
        self.assertIn("-raw", read(SKILL))

    def test_skill_points_to_red_line_chapter(self) -> None:
        self.assertIn("`references/business-industry-method.md` 第四章", read(SKILL))

    def test_content_checklist_heading_exists(self) -> None:
        self.assertIn("\n## 交付前內容層檢查\n", read(SKILL))


if __name__ == "__main__":
    unittest.main()
