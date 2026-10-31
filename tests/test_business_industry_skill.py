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
UA_READ = re.compile(
    r"\$\{?(env:)?SEC_USER_AGENT|%SEC_USER_AGENT%|GetEnvironmentVariable\(\s*[\"']SEC_USER_AGENT"
    r"|(?<!Set-Item )(?<!New-Item )env:SEC_USER_AGENT"
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
        if UA_READ.search(line):  # 設定式（SetEnvironmentVariable、setx、export）不讀值，不算
            case.assertTrue(any(f in line for f in allowed), line)
            case.assertIsNone(UA_PRINT.search(line), line)
            case.assertIsNone(UA_BARE.search(line), line)
        case.assertIsNone(DEBUG_DUMP.search(line), line)
        case.assertIsNone(CURL_VERBOSE.search(line), line)


#: 設計 5.3 的五條禁令，逐條列出全部獨立禁止項
RED_LINE_ITEMS = (
    ("股價", "市值", "估值倍數", "目標價", "內在價值", "預期報酬", "股利殖利率"),
    ("EPS", "每股股利", "每股淨值"),
    ("買進", "賣出", "加減碼", "持有", "便宜", "低估", "值得買", "已反映"),
    ("價格隱含預期", "R/R", "示範機率", "決策狀態", "評等"),
    ("媒體標題中的股價敘事", "漲停", "股價飆漲", "以價格衍生的量法", "市值占比", "市值遷移"),
)
#: (第一欄關鍵詞, 「不寫」欄的全部獨立禁止項)
RED_LINE_BOUNDARY = (
    ("被投資公司", ("對其價格的評價",)),
    ("股權換訂單", ("履約價", "與市價的比較")),
    ("募資", ("發行價", "每股溢價")),
    ("庫藏股", ("是否被低估",)),
    ("股東回饋", ("每股股利", "殖利率")),
    ("業務報酬指標", ("連結到股價",)),
    ("資本成本", ("自算 WACC", "以超額報酬推估價值")),
    ("前瞻目標", ("當成事實", "推到估值")),
)


def red_line_problems(body_42: str, body_43: str) -> list[str]:
    """檢查 4.2 五條禁令與 4.3 八列「不寫」欄是否各自帶齊全部禁止項。"""
    problems: list[str] = []
    items = re.findall(r"^\d+\. (.*)$", body_42, re.MULTILINE)
    if len(items) != len(RED_LINE_ITEMS):
        problems.append(f"禁令條數 {len(items)}")
    for n, (item, words) in enumerate(zip(items, RED_LINE_ITEMS, strict=False), 1):
        problems.extend(f"第 {n} 條缺「{w}」" for w in words if w not in item)
    rows = [r for r in body_43.splitlines() if r.startswith("|") and "---" not in r][1:]
    if len(rows) != len(RED_LINE_BOUNDARY):
        problems.append(f"邊界表列數 {len(rows)}")
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    for key, words in RED_LINE_BOUNDARY:
        match = [c for c in cells if len(c) == 3 and key in c[0]]
        if len(match) != 1:
            problems.append(f"邊界表找不到唯一的「{key}」列")
            continue
        problems.extend(f"「{key}」列的不寫欄缺「{w}」" for w in words if w not in match[0][2])
    return problems


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
            "echo %SEC_USER_AGENT%",
            '[Environment]::GetEnvironmentVariable("SEC_USER_AGENT","User")',
            "Get-Item env:SEC_USER_AGENT",
        ):
            with self.subTest(bad=bad), self.assertRaises(AssertionError, msg=bad):
                assert_no_ua_exposure(self, [bad])
        assert_no_ua_exposure(self, ['curl -sS -A "$SEC_USER_AGENT" u | grep -v x'])
        for ok in (
            '[Environment]::SetEnvironmentVariable("SEC_USER_AGENT", "x", "User")',
            'setx SEC_USER_AGENT "x"',
            'export SEC_USER_AGENT="x"',
        ):
            with self.subTest(ok=ok):
                assert_no_ua_exposure(self, [ok])


class TestMethodSingleSource(unittest.TestCase):
    def test_method_declares_layer1_methodology(self) -> None:
        self.assertIn("`methodology_version: business-industry-v1`", read(METHOD))

    def test_method_chapters_in_order(self) -> None:
        text = read(METHOD)
        positions = [text.index(h) for h in METHOD_CHAPTERS]
        self.assertEqual(positions, sorted(positions))

    def test_red_line_content_is_complete(self) -> None:
        text = read(METHOD)
        problems = red_line_problems(
            section(text, "### 4.2 報告中不出現的內容"),
            section(text, "### 4.3 只陳述事實與機制的邊界情況"),
        )
        self.assertEqual(problems, [])

    def test_red_line_check_catches_every_single_item_removal(self) -> None:
        text = read(METHOD)
        b42 = section(text, "### 4.2 報告中不出現的內容")
        b43 = section(text, "### 4.3 只陳述事實與機制的邊界情況")
        self.assertEqual(red_line_problems(b42, b43), [])
        for n, words in enumerate(RED_LINE_ITEMS, 1):
            line = next(ln for ln in b42.splitlines() if ln.startswith(f"{n}. "))
            for word in words:
                with self.subTest(item=n, word=word):
                    self.assertIn(word, line)
                    mutated = b42.replace(line, line.replace(word, "", 1))
                    self.assertNotEqual(red_line_problems(mutated, b43), [])
        for key, words in RED_LINE_BOUNDARY:
            row = next(r for r in b43.splitlines() if r.startswith("|") and key in r.split("|")[1])
            for word in words:
                with self.subTest(row=key, word=word):
                    cells = row.split("|")
                    self.assertIn(word, cells[3])
                    cells[3] = cells[3].replace(word, "", 1)
                    mutated = b43.replace(row, "|".join(cells))
                    self.assertNotEqual(red_line_problems(b42, mutated), [])
        self.assertNotEqual(red_line_problems("\n".join(b42.splitlines()[:-2]), b43), [])
        loosened = b43.replace(next(r for r in b43.splitlines() if "發行價" in r), "| 募資 | x | 無限制 |")
        self.assertNotEqual(red_line_problems(b42, loosened), [])

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

    def test_observation_zone_lists_all_thirteen_items(self) -> None:
        body = section(read(METHOD), "### 6.3 觀察區")
        ids = re.findall(r"(?m)^- \*\*(OB-\d+)\*\*", body)
        # OB-2 已升為 R3.6，編號不重排
        self.assertEqual(ids, ["OB-1"] + [f"OB-{n}" for n in range(3, 15)])

    def test_fix_round1_rule_amendments_are_in_method(self) -> None:
        text = read(METHOD)
        for needle in (
            "並標明屬循環或結構。時間窗寫出起點、終點與目前狀態。",
            "未發生的才列為觀察指標。",
            "- **OB-14** 分階段生效事項的排程",
            "時間窗終點與狀態為 MCD、樣本外案例（匿名）",
            "並列含 SBC 與不含 SBC 兩種口徑。列在營收內的不可重複項目",
            "營收內不可重複項目與營收減項為 BE、樣本外案例（匿名）",
            "資料不足時依下表降級，各環節的利潤比較取不到同業基準時一樣走降級",
            "「比較基準未查」只用於 S／W 判定（R4.4），不取代降級。",
            "- **R3.6** 單位經濟之外，並列應收與存貨的天數、收付款條件，以及營業現金流與淨利的對照（證據",
            "（證據：高明鐵、樣本外案例（匿名）；文獻：無）",
        ):
            with self.subTest(needle[:24]):
                self.assertIn(needle, text)
        self.assertNotIn("**OB-2**", text)

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

    def test_content_checklist_covers_format_sourcing_tier_and_tw_sources(self) -> None:
        checklist = read(SKILL).partition("\n## 交付前內容層檢查\n")[2]
        for item in (
            "- [ ] 格式層依 research-report-output 的 F-rules 自查（F-a 至 F-f）；數字密集的段落與表格儲存格已拆表或分行",
            "- [ ] TL;DR、KPI 卡與每個表格儲存格的數字都寫出文件名與期間，不只放層級標籤",
            "- [ ] `l3` 只做記錄與交叉比對，不支撐任何結論或基準假設；搜尋結果摘要最高標 `l2`，讀到原文才標 `l1`",
            "- [ ] market 為 TW 時，申報文件以 MOPS、年報與 TWSE／TPEx 公告為主；同一公司另有 20-F 時只作交叉核對",
        ):
            with self.subTest(item[:20]):
                self.assertIn(item, checklist)

    def test_sec_section_cites_arm_only_and_keeps_tw_primary_source(self) -> None:
        sec = section(read(SKILL), "### SEC 文件全文")
        self.assertIn("外國發行人（例如 ARM）申報 20-F", sec)
        self.assertNotIn("台積電", sec)
        self.assertIn("在台股上市、同時申報 20-F 的公司，主要來源仍是 MOPS", sec)


STEP_HEADINGS = (
    "### 2.1 步驟 1：研究契約與資料時點疊加", "### 2.2 步驟 2：重建營收來源並指派商業模式類型",
    "### 2.3 步驟 3：依類型選單位經濟量尺", "### 2.4 步驟 4：逐營收來源 SWOT",
    "### 2.5 步驟 5：縱向產業鏈與利潤池", "### 2.6 步驟 6：橫向同業與替代方案",
    "### 2.7 步驟 7：產業結構與護城河", "### 2.8 步驟 8：交接給 Layer 4",
)
ARCHETYPES = (
    "設備製造與專案", "訂閱軟體", "加盟與不動產", "保險", "受管制公用事業",
    "網路型基礎設施", "IP 授權", "接單製造服務（晶圓代工）", "規格型材料",
    "商品型材料", "零組件", "配銷", "控股母公司的資本配置",
)

#: 逐步鎖定核准的規則 ID（依規則證據判定表）；新增、刪除或改號都要先改這裡
APPROVED_RULES = dict(zip(STEP_HEADINGS, (
    ("R1.1", "R1.2", "R1.3"),
    ("R2.1", "R2.2", "R2.3", "R2.4", "R2.5"),
    ("R3.1", "R3.2", "R3.3", "R3.4", "R3.5", "R3.6"),
    ("R4.1", "R4.3", "R4.4", "R4.5", "R4.6", "R4.8"),
    ("R5.1", "R5.2", "R5.3", "R5.4", "R5.6", "R5.8"),
    ("R6.1", "R6.2", "R6.3"),
    ("R7.1", "R7.2", "R7.3", "R7.4", "R7.5", "R7.6"),
    ("R8.1", "R8.2", "R8.3"),
), strict=True))
#: 判定為觀察區或範圍說明的空號，不得以規則行出現
RESERVED_GAPS = ("R4.2", "R4.7", "R5.5", "R5.7", "R6.4", "R8.4")
#: 凡以 `- **R<n>.<n>**` 或 `- **RD.<n>**` 開頭的行都是規則行；ID 之後的內容另由 RULE_FORMAT 驗
RULE_LINE = re.compile(r"^- \*\*((?:R\d|RD)\.\d+)\*\*(.*)$", re.MULTILINE)
#: ID 之後恰好一個半形空白、非空正文，再以完整的證據欄結尾
RULE_FORMAT = re.compile(r"^ (\S.*?)（證據：(.*?)；文獻：(.*)）$")
EVIDENCE_TAIL = re.compile(r"（證據：(.*?)；文獻：(.*)）$")
#: 外部 URL 只吃 RFC 3986 的 ASCII 字元扣掉 ) ] ' * 與 [；空白、非 ASCII 字元（中文、全形標點、
#: 零寬空白）、反引號、| { } < > " 一律結束，以免跨過後面的本機路徑。
#: 已知限制：URL 後直接接 . , ; : ! ? & ~ ( 再接路徑時會一起被剝掉（例：`https://a.com/x.docs/y`）；
#: 這些字元本來就能合法出現在 URL 內，regex 分辨不出來。
URL = re.compile(r"https?://[A-Za-z0-9\-._~:/?#@!$&+,;=%(]+")
ROUTING_HEADER = ("類型", "適用量尺", "不適用的量尺", "公司自定義 KPI 的處理", "開發組案例")
#: 只存在於維護者本機、不隨 plugin 發布的路徑與檔名
UNSHIPPED_PATHS = ("frameworks.md", "rule-evidence", "primary-sources", "docs/", ".superpowers")


def rule_problems(text: str) -> list[str]:
    """檢查各步驟的規則 ID 與核准清單完全相等、空號沒有寫回、每條規則行的證據欄完整。"""
    problems: list[str] = []
    for heading, approved in APPROVED_RULES.items():
        ids = step_rule_ids(section(text, heading))
        if sorted(ids) != sorted(approved):
            problems.append(f"{heading} 的規則 ID 是 {ids}")
    every = sorted(r for rules in APPROVED_RULES.values() for r in rules)
    found = step_rule_ids(text)
    if sorted(found) != every:
        problems.append("全檔的 R 規則 ID 與核准清單不符")
    problems.extend(f"空號 {gap} 被寫回" for gap in RESERVED_GAPS if gap in found)
    for rule_id, rest in RULE_LINE.findall(text):
        match = RULE_FORMAT.match(rest)
        if not match or not all(group.strip() for group in match.groups()):
            problems.append(f"{rule_id} 的正文或證據欄不完整")
    return problems


def step_rule_ids(text: str) -> list[str]:
    """步驟規則（R<n>.<n>）的 ID；與證據檢查共用 RULE_LINE 的判定。"""
    return [rule_id for rule_id, _ in RULE_LINE.findall(text) if not rule_id.startswith("RD")]


def local_path_hits(text: str) -> list[str]:
    """先剝掉外部 URL，再回傳 text 中出現的未發布路徑。"""
    local = URL.sub("", text)
    return [token for token in UNSHIPPED_PATHS if token in local]


def table_cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().split("|")[1:-1]]


def routing_problems(body: str) -> list[str]:
    """檢查路由表表頭、類型清單，以及每列恰好 5 欄且沒有空欄。"""
    rows = [r for r in body.splitlines() if r.startswith("|") and "---" not in r]
    if not rows:
        return ["沒有路由表"]
    problems: list[str] = []
    if table_cells(rows[0]) != list(ROUTING_HEADER):
        problems.append("表頭不符")
    names: list[str] = []
    for row in rows[1:]:
        cells = table_cells(row)
        names.append(cells[0] if cells else "")
        if len(cells) != len(ROUTING_HEADER):
            problems.append(f"{names[-1]} 有 {len(cells)} 欄")
        problems.extend(f"{names[-1]} 第 {n} 欄是空的" for n, c in enumerate(cells, 1) if not c)
    if sorted(names) != sorted(ARCHETYPES):
        problems.append("類型清單不符")
    return problems


class TestEightSteps(unittest.TestCase):
    def test_every_step_has_rules_or_reference_practice(self):
        text = read(METHOD)
        for heading in STEP_HEADINGS:
            self.assertRegex(section(text, heading),
                             r"(?m)^(- \*\*R\d\.\d+\*\*|參考做法見 6\.3 OB-\d+)", heading)

    def test_every_rule_carries_evidence(self):
        lines = re.findall(r"^- \*\*(?:R\d\.\d+|RD\.\d+)\*\*.*$", read(METHOD), re.MULTILINE)
        self.assertGreater(len(lines), 20)
        for line in lines:
            self.assertIn("（證據：", line)

    def test_rule_ids_are_unique(self):
        ids = re.findall(r"^- \*\*((?:R\d|RD)\.\d+|OB-\d+)\*\*", read(METHOD), re.MULTILINE)
        self.assertEqual(len(ids), len(set(ids)))

    def test_handoff_caps_dominant_variables(self):
        self.assertRegex(section(read(METHOD), "### 2.8 步驟 8：交接給 Layer 4"), r"(一至三|1[–-]3) ?個")

    def test_rules_match_approved_list_with_complete_evidence(self) -> None:
        self.assertEqual(rule_problems(read(METHOD)), [])

    def test_rule_guard_catches_each_mutation(self) -> None:
        text = read(METHOD)
        self.assertEqual(rule_problems(text), [])
        for heading in STEP_HEADINGS:
            body = section(text, heading)
            mutated = text
            for line in (ln for ln in body.splitlines() if RULE_LINE.match(ln)):
                mutated = mutated.replace(line + "\n", "", 1)
            with self.subTest(drop_all_rules=heading):
                self.assertNotEqual(rule_problems(mutated), [])
        for gap in RESERVED_GAPS:
            anchor = next(ln for ln in text.splitlines() if ln.startswith(f"- **R{gap[1]}."))
            mutated = text.replace(anchor, f"{anchor}\n- **{gap}** 寫回（證據：無；文獻：無）", 1)
            with self.subTest(write_back=gap):
                self.assertNotEqual(rule_problems(mutated), [])
        for line in (m.group(0) for m in RULE_LINE.finditer(text)):
            match = EVIDENCE_TAIL.search(line)
            assert match, line
            emptied = line[: match.start(1)] + " " + line[match.end(1):]
            no_literature = line[: match.start()] + f"（證據：{match.group(1)}）"
            for kind, bad in (("evidence_blank", emptied), ("literature_removed", no_literature)):
                with self.subTest(**{kind: line[:12]}):
                    self.assertNotEqual(rule_problems(text.replace(line, bad, 1)), [])
        for line in (m.group(0) for m in RULE_LINE.finditer(text)):
            head = line[: line.index("** ") + 2]
            for kind, bad in (
                ("id_only", head),
                ("tab_separator", head + "\t" + line[len(head) + 1:]),
                ("no_separator", head + line[len(head) + 1:]),
            ):
                with self.subTest(**{kind: head}):
                    self.assertNotEqual(rule_problems(text.replace(line, bad, 1)), [])

    def test_method_and_skill_ship_no_local_paths(self) -> None:
        for path in (METHOD, SKILL):
            with self.subTest(file=path.name):
                self.assertEqual(local_path_hits(read(path)), [])

    def test_local_path_guard_ignores_external_urls(self) -> None:
        self.assertEqual(local_path_hits("見 https://www.sec.gov/about/offices/ocie/docs/ 的說明"), [])
        self.assertEqual(local_path_hits("見 docs/superpowers/specs/x.md"), ["docs/"])

    def test_url_stripping_stops_at_markdown_and_cjk_punctuation(self) -> None:
        cases = (
            ("[來源](https://example.com/docs/)，另見[內部](docs/superpowers/specs/x.md)", ["docs/"]),
            ("見 https://example.com/a。docs/superpowers/specs/x.md", ["docs/"]),
            ("見 [SEC](https://www.sec.gov/about/offices/ocie/docs/) 與 <https://example.com/docs/>", []),
            # inline code 不受 markdownlint MD034 檢查，反引號緊貼 URL 的寫法最容易出現
            ("`https://a.com/docs/`與`docs/superpowers/specs/x.md`與`https://b.com/docs/`", ["docs/"]),
            ("見 https://example.com/a與frameworks.md", ["frameworks.md"]),
            ("“https://example.com/a”docs/superpowers/specs/x.md", ["docs/"]),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(local_path_hits(text), expected)


class TestArchetypeRouting(unittest.TestCase):
    def rows(self):
        body = section(read(METHOD), "### 3.1 路由表")
        return [r for r in body.splitlines() if r.startswith("|") and "---" not in r]

    def test_routing_table_lists_development_archetypes(self):
        cells = [r.split("|")[1].strip() for r in self.rows()[1:]]
        self.assertEqual(sorted(cells), sorted(ARCHETYPES))

    def test_routing_table_names_inapplicable_scales(self):
        for col in ("適用量尺", "不適用的量尺", "公司自定義 KPI"):
            self.assertIn(col, self.rows()[0])

    def test_routing_rows_have_five_filled_columns(self) -> None:
        self.assertEqual(routing_problems(section(read(METHOD), "### 3.1 路由表")), [])

    def test_routing_guard_catches_blank_or_missing_cells(self) -> None:
        body = section(read(METHOD), "### 3.1 路由表")
        self.assertEqual(routing_problems(body), [])
        for row in self.rows()[1:]:
            name = table_cells(row)[0]
            for n in range(len(ROUTING_HEADER)):
                parts = row.split("|")
                blank = "|".join([*parts[: n + 1], " ", *parts[n + 2:]])
                dropped = "|".join([*parts[: n + 1], *parts[n + 2:]])
                for kind, bad in (("blank", blank), ("dropped", dropped)):
                    with self.subTest(row=name, column=n + 1, kind=kind):
                        self.assertNotEqual(routing_problems(body.replace(row, bad, 1)), [])

    def test_off_table_procedure_defines_its_own_scale(self):
        body = section(read(METHOD), "### 3.2 表外類型的通用程序")
        for word in ("表外類型", "定價與認列機制", "定義依據"):
            self.assertIn(word, body)


D_CHAPTERS = (
    "## 一、TL;DR", "## 二、研究契約與資料時點", "## 三、營收來源與商業模式",
    "## 四、單位經濟", "## 五、逐營收來源 SWOT", "## 六、產業鏈與利潤池",
    "## 七、同業與替代方案", "## 八、產業結構與護城河", "## 九、交接給 Layer 4",
    "## 十、Caveats 與來源追蹤",
)
FRONT = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
# 方法檔 4.2 的完整清單：由 RED_LINE_ITEMS 攤平（去掉兩個描述語），再加上骨架常見的同義寫法；
# KPI 卡、front matter 與骨架內文共用這一份
_DESCRIPTORS = ("媒體標題中的股價敘事", "以價格衍生的量法")
RED_LINE_TERMS = (
    *(w for group in RED_LINE_ITEMS for w in group if w not in _DESCRIPTORS),
    "現價", "市價", "本益比", "P/E", "每股", "價格隱含", "E[R_H]", "price_asof",
)
RATING = re.compile(r"\brating\b", re.ASCII)
LAYER1_MARKER = re.compile(r"<!-- 方法：business-industry-method\.md 2\.(\d) -->")


def string_values(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from string_values(v)
    elif isinstance(node, list):
        for v in node:
            yield from string_values(v)


class TestDTemplate(unittest.TestCase):
    def body(self):
        return FRONT.sub("", read(D_TEMPLATE), count=1)

    def test_chapters_in_order(self):
        text = self.body()
        positions = [text.index(h) for h in D_CHAPTERS]
        self.assertEqual(positions, sorted(positions))

    def test_chapters_point_to_their_steps(self):
        text = self.body()
        for n, chapter in enumerate(D_CHAPTERS[1:9], start=1):
            self.assertIn(f"<!-- 方法：business-industry-method.md 2.{n} -->", section(text, chapter))

    def test_tables_use_fixed_headers(self):
        text = self.body()
        self.assertIn("| 象限 | 議題 | 機制 | 影響的損益項目與方向 | 數字＋出處＋期間 | 比較對象／觸發條件與時間窗 | 循環或結構 |", text)
        self.assertIn("| 環節 | 具名公司 | 角色 | 利潤率或定價權事實 | 證據標示 |", text)
        self.assertRegex(text, r"(?m)^\| 實體 \|")

    def test_template_body_has_no_valuation_slots(self):
        text = self.body()
        for word in RED_LINE_TERMS:
            self.assertNotIn(word, text)
        self.assertIsNone(RATING.search(text))

    def test_layer1_front_matter_has_no_red_line_terms(self):
        blob = " ".join(string_values(front_matter(D_TEMPLATE)))
        for word in RED_LINE_TERMS:
            self.assertNotIn(word, blob)
        self.assertIsNone(RATING.search(blob))

    def test_layer1_kpi_cards_are_business_only(self):
        kpi = front_matter(D_TEMPLATE)["kpi"]
        blob = " ".join(f"{k.get('label', '')} {k.get('value', '')} {k.get('note', '')}" for k in kpi)
        for word in RED_LINE_TERMS:
            self.assertNotIn(word, blob)
        self.assertIsNone(RATING.search(blob))

    def test_layer1_front_matter_raw_text_has_no_red_line_terms(self):
        raw = read(D_TEMPLATE).partition("\n---\n")[0]
        for word in RED_LINE_TERMS:
            self.assertNotIn(word, raw)
        self.assertIsNone(RATING.search(raw))

    def test_entity_role_matrix_roles_are_verbatim(self):
        row = next(r for r in self.body().splitlines() if r.startswith("| 實體 |"))
        self.assertEqual(table_cells(row), ["實體", "供應商", "客戶", "通路", "競爭者", "資金方", "互補者"])

    def first_content_line(self, chapter, after_marker=True):
        lines = section(self.body(), chapter).splitlines()
        lines = [ln for ln in lines if ln.strip() and not (after_marker and ln.startswith("<!-- 方法："))]
        return lines[0]

    def test_chapters_open_with_conclusion_slot(self):
        for chapter in ("## 五、逐營收來源 SWOT", "## 六、產業鏈與利潤池", "## 十、Caveats 與來源追蹤"):
            with self.subTest(chapter):
                self.assertTrue(self.first_content_line(chapter).startswith("〈本節結論一句"))

    def test_profit_pool_opens_with_conclusion(self):
        first = self.first_content_line("### 6.5 利潤池")
        self.assertTrue(first.startswith("結論："))
        self.assertIn("未扣資本成本", first)

    def test_evidence_cells_use_tag_spans(self):
        self.assertIn('<span class="tag l1">', self.body())
        self.assertNotIn("| `l1` |", self.body())

    def test_swot_comparison_fallback_and_profit_sharing_layer(self):
        text = self.body()
        swot = [ln for ln in text.splitlines() if ln.startswith(("| S |", "| W |"))]
        self.assertTrue(swot)
        for line in swot:
            self.assertIn("比較基準未查", line)
        self.assertIn("**分潤層**", section(text, "## 六、產業鏈與利潤池"))

    def test_rule_ids_name_the_method_file(self):
        self.assertIsNone(re.search(r"（R[0-9D]", self.body()))

    def test_entity_role_matrix_has_seven_columns(self):
        rows = [r for r in self.body().splitlines() if r.startswith("| 實體 |")]
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(table_cells(rows[0])), 7)

    def test_step_markers_appear_once_right_after_heading(self):
        text = self.body()
        self.assertEqual(len(LAYER1_MARKER.findall(text)), 8)
        for n, chapter in enumerate(D_CHAPTERS[1:9], start=1):
            lines = text.splitlines()
            nxt = next(ln for ln in lines[lines.index(chapter) + 1:] if ln.strip())
            self.assertEqual(nxt, f"<!-- 方法：business-industry-method.md 2.{n} -->")
            self.assertEqual(text.count(nxt), 1)

    def test_no_unshipped_local_paths(self):
        self.assertEqual(local_path_hits(read(D_TEMPLATE)), [])

    def test_reference_practices_are_marked_optional(self):
        text = self.body()
        refs = [ln for ln in text.splitlines() if "參考做法見" in ln]
        self.assertTrue(refs)
        for n in (1, 3, 4, 5, 6, 7, 8):  # OB-2 已升為 R3.6（必填）
            self.assertIn(f"方法檔參考做法見 6.3 OB-{n}", text)
        self.assertNotIn("6.3 OB-2", text)
        for line in refs:
            self.assertIn("方法檔參考做法見 6.3 OB-", line)
            self.assertIn("（選填，", line)
        tows = [ln for ln in text.splitlines() if "TOWS" in ln and ln.startswith("#")]
        self.assertTrue(tows)
        for line in tows:
            self.assertIn("選用", line)


NL = chr(10)
SWOT_NUMBER_RULE = "一行一個數字；多個數字以 `<br>` 分行，每行附出處"


def swot_number_cell_problems(text: str, expected_tables: int) -> list[str]:
    """逐張解析 SWOT 表（表頭含「數字＋出處＋期間」欄），檢查 S／W／O／T 每列該欄都含分行與出處指示。"""
    lines = text.splitlines()
    problems: list[str] = []
    tables = 0
    for n, ln in enumerate(lines):
        header = table_cells(ln) if ln.startswith("|") else []
        if "數字＋出處＋期間" not in header or header[0] != "象限":
            continue
        tables += 1
        col = header.index("數字＋出處＋期間")
        seen = []
        for row in lines[n + 2:]:
            if not row.startswith("|"):
                break
            cells = table_cells(row)
            seen.append(cells[0])
            if len(cells) != len(header) or SWOT_NUMBER_RULE not in cells[col]:
                problems.append(f"表 {tables} 的 {cells[0]} 列缺數字欄指示")
        if seen != ["S", "W", "O", "T"]:
            problems.append(f"表 {tables} 的列為 {seen}")
    if tables != expected_tables:
        problems.append(f"SWOT 表數 {tables} != {expected_tables}")
    return problems


class TestDTemplateFormatAndSourcing(unittest.TestCase):
    """D 骨架對齊 F-rules 與數字出處：TL;DR 實績表、表格結論行、單格單數字、層級標籤後接文件名。"""

    def body(self):
        return FRONT.sub("", read(D_TEMPLATE), count=1)

    def lines(self):
        return self.body().splitlines()

    def table_start(self, header_prefix):
        lines = self.lines()
        return next(i for i, ln in enumerate(lines) if ln.startswith(header_prefix))

    def prev_nonblank(self, idx):
        lines = self.lines()
        j = idx - 1
        while not lines[j].strip():
            j -= 1
        return lines[j]

    def test_tldr_points_are_bold_conclusion_plus_support_with_number_cap(self):
        tldr = section(self.body(), "## 一、TL;DR")
        points = [ln for ln in tldr.splitlines() if ln.startswith("**")]
        self.assertEqual(len(points), 2)
        for p in points:
            self.assertRegex(p, r"^\*\*[^*]+。\*\* 〈支撐句")
            self.assertIn("至多 2 個數字；其餘數字放進下方實績表", p)

    def test_tldr_has_four_column_results_table_with_conclusion(self):
        idx = self.table_start("| 指標 | 數值 | 期間（起訖日） | 出處文件 |")
        self.assertEqual(len(table_cells(self.lines()[idx])), 4)
        self.assertTrue(self.prev_nonblank(idx).startswith("> **〈表格結論"))
        text = self.body()
        self.assertLess(text.index("## 一、TL;DR"), text.index("| 指標 | 數值 | 期間（起訖日） | 出處文件 |"))
        self.assertLess(text.index("| 指標 | 數值 | 期間（起訖日） | 出處文件 |"), text.index("## 二、"))

    def test_caveat_tables_have_conclusion_line_and_10_1_opens_with_slot(self):
        for prefix in ("| 公司自述（出處） |", "| # | 文件或來源 |"):
            with self.subTest(prefix):
                idx = self.table_start(prefix)
                self.assertTrue(self.prev_nonblank(idx).startswith("> **〈表格結論"))
        first = next(ln for ln in section(self.body(), "### 10.1 公司自述與申報數據對帳").splitlines() if ln.strip())
        self.assertTrue(first.startswith("〈"))
        self.assertIn("結論", first)

    def test_swot_number_column_demands_one_number_per_cell(self):
        text = self.body()
        self.assertEqual(swot_number_cell_problems(text, expected_tables=2), [])
        # 變異：清空任一張表任一列的指示都必須被抓到
        lines = text.splitlines()
        rows = [i for i, ln in enumerate(lines) if ln.startswith(("| S |", "| W |", "| O |", "| T |"))]
        self.assertEqual(len(rows), 8)
        for i in rows:
            with self.subTest(row=i):
                mutated = lines.copy()
                mutated[i] = mutated[i].replace(SWOT_NUMBER_RULE, "")
                self.assertTrue(swot_number_cell_problems(NL.join(mutated), expected_tables=2))

    def test_related_party_split_is_a_table(self):
        idx = self.table_start("| 關係人 | 營收（期間） | 占比 | 剔除後成長 | 出處文件 |")
        self.assertTrue(self.prev_nonblank(idx).startswith("> **〈表格結論"))
        self.assertIn("無關係人交易", section(self.body(), "## 三、營收來源與商業模式"))

    def test_working_capital_is_a_required_table_citing_r36(self):
        idx = self.table_start("| 指標 | 本期（期間） | 基期（期間） | 出處文件 |")
        self.assertTrue(self.prev_nonblank(idx).startswith("> **〈表格結論"))
        lines = self.lines()
        label = next(ln for ln in lines if ln.startswith("**營運資金**"))
        self.assertIn("必填", label)
        self.assertNotIn("選填", label)
        self.assertIn("R3.6", label)
        self.assertNotIn("OB-2", label)
        rows = "\n".join(lines[idx:idx + 8])
        for metric in ("應收天數", "存貨天數", "營業現金流", "淨利"):
            self.assertIn(metric, rows)

    def test_tag_spans_are_followed_by_document_and_period(self):
        text = self.body()
        spans = re.findall(r'<span class="tag l1">公司揭露</span>(.{0,12})', text)
        self.assertTrue(spans)
        for tail in spans:
            self.assertTrue(tail.startswith("〈文件名與期間〉"), tail)

    def test_kpi_notes_name_the_source(self):
        for card in front_matter(D_TEMPLATE)["kpi"]:
            with self.subTest(card["label"]):
                self.assertIn("出處", str(card["note"]))
                self.assertIn("期間", str(card["note"]))


class TestOutputSkillRouting(unittest.TestCase):
    def routing_lines(self):
        body = section(read(OUTPUT_SKILL), "## 工作流程")
        d = next(l for l in body.splitlines() if "templates/D-business-industry.md" in l and "→" in l)
        a = next(l for l in body.splitlines() if "templates/A-single-stock.md" in l and "→" in l)
        return d, a

    def test_routing_examples_cover_both_directions(self):
        d, a = self.routing_lines()
        for phrase in ("幫我研究", "個股深度研究", "前景如何", "供應鏈上下游分析"):
            self.assertIn(phrase, d)
        for phrase in ("值不值得買", "要不要賣", "目標價"):
            self.assertIn(phrase, a)
        for phrase in ("值不值得買", "要不要賣"):
            self.assertNotIn(phrase, d)
        self.assertIn("沒有明確要求", d)

    def test_briefing_has_d_rules_after_a_rules(self):
        body = section(read(OUTPUT_SKILL), "### Briefing（摘要，≤3 頁）")
        self.assertLess(body.index("**保留**"), body.index("**D 型保留**"))
        self.assertLess(body.index("**刪去**"), body.index("**D 型刪去**"))
        line = next(l for l in body.splitlines() if l.startswith("**D 型保留**"))
        for word in ("營收來源排序", "SWOT", "利潤分布", "交接變數"):
            self.assertIn(word, line)

    def test_external_mode_keeps_layer1_disclosures(self):
        body = section(read(OUTPUT_SKILL), "### External（傳播）")
        line = next(l for l in body.splitlines() if l.startswith("**D 型保留**"))
        for word in ("business-industry-v1", "未揭露", "未查到", "未核對", "會計期間", "比較基準未查", "資料缺口"):
            self.assertIn(word, line)

    def test_iron_rule_5_replaces_price_date_for_d(self):
        rules = section(read(OUTPUT_SKILL), "## 鐵則")
        line = next(l for l in rules.splitlines() if l.lstrip().startswith("5. "))
        self.assertIn("D 型", line)
        self.assertIn("會計期間", line)

    def test_output_spec_checklist_branches_for_d(self):
        body = section(read(OUTPUT_SPEC), "## 八、發布前檢查清單（格式層）")
        for word in ("D 型", "會計期間已標", "disclaimer", "business-industry-analysis",
                     "查價日已標", "prepublish-checklist.md"):
            self.assertIn(word, body)

    def test_workflow_has_optional_proofreading_step_before_pdf(self):
        body = section(read(OUTPUT_SKILL), "## 工作流程")
        steps = re.findall(r"^(\d+)\. (.*)$", body, re.MULTILINE)
        titles = [t for _, t in steps]
        idx = next(i for i, t in enumerate(titles) if "中文用語校對" in t)
        for word in ("選用", "speak-human-tw"):
            self.assertIn(word, titles[idx])
        self.assertLess(idx, next(i for i, t in enumerate(titles) if t.startswith("**產 PDF**")))
        self.assertEqual([int(n) for n, _ in steps], list(range(1, len(steps) + 1)))
        start = body.index(f"{steps[idx][0]}. ")
        step_text = body[start:body.index(f"\n{steps[idx + 1][0]}. ", start)]
        for word in ("選用", "F-rules", "降格式", "跳過確認、事後摘要"):
            self.assertIn(word, step_text)

    def test_output_spec_checklist_lists_optional_proofreading(self):
        body = section(read(OUTPUT_SPEC), "## 八、發布前檢查清單（格式層）")
        self.assertIn("（選用）已用 speak-human-tw 校對正文用語；版面仍以 F-rules 為準", body)

    def test_readme_lists_speak_human_tw_as_optional_dependency(self):
        text = read(PLUGIN / "README.md")
        self.assertIn("https://github.com/Raymondhou0917/speak-human-tw", text)

    def test_output_spec_workflow_step_citation_points_at_pdf_step(self):
        steps = re.findall(r"^(\d+)\. \*\*(.+?)\*\*", section(read(OUTPUT_SKILL), "## 工作流程"), re.MULTILINE)
        pdf_no = next(n for n, t in steps if t == "產 PDF")
        self.assertIn(f"SKILL.md 工作流程第 {pdf_no} 步", read(OUTPUT_SPEC))

    def test_output_spec_has_d_skeleton_and_filename(self):
        text = read(OUTPUT_SPEC)
        self.assertIn("### D 型｜企業與產業研究報告", text)
        self.assertIn("_企業與產業研究_v1.0_", text)

    def test_customize_documents_sec_user_agent(self):
        body = section(read(CUSTOMIZE), "## 六、資料源 MCP（選配）")
        self.assertIn("SEC_USER_AGENT", body)
        self.assertIn("{'set'} else {'missing'}", body)
        self.assertIn('[ -n "$SEC_USER_AGENT" ] && echo set || echo missing', body)
        for word in ("由使用者自己", "不代為設定", "不要寫進專案共用的 `.claude/settings.json`"):
            self.assertIn(word, body)
        assert_no_ua_exposure(self, code_lines(body) + inline_code(body))

    def test_output_spec_d_chapters_match_d_template(self):
        body = section(read(OUTPUT_SPEC), "### D 型｜企業與產業研究報告（`methodology_version: business-industry-v1`）")
        listed = re.findall(r"^\d+\. \*\*(.+?)\*\*", body, re.MULTILINE)
        titles = [re.sub(r"^## [一二三四五六七八九十]+、", "", h) for h in re.findall(r"^## .+$", read(D_TEMPLATE), re.MULTILINE)]
        self.assertEqual(listed, titles)


class TestValuationHandoffWording(unittest.TestCase):
    def test_handoffs_name_a_type_explicitly(self):
        for path in (TEMPLATES / "B-industry-supplychain.md", TEMPLATES / "C-rotation-weekly.md", PCR_SKILL):
            text = read(path)
            with self.subTest(path.name):
                self.assertNotIn("深度研究", text)
                self.assertNotIn("深度報告", text)
                self.assertNotIn("深度框架", text)
                self.assertIn("A 型估值研究", text)

    def test_a_template_chapter_4_cites_d_report(self):
        self.assertIn("D 型", section(read(TEMPLATES / "A-single-stock.md"), "## 四、事業結構與供應鏈"))


if __name__ == "__main__":
    unittest.main()
