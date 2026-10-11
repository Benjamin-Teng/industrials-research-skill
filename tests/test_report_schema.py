"""報告 schema 與實際輸出行為的驗收測試。

spec v1.3.0 第 9.2 節要求：新增檢查「不得只比對關鍵字，須涵蓋數值、反解狀態、
schema 時點與實際報告輸出的行為」。數值與反解狀態由 ``test_valuation_math.py`` 守護；
本檔負責另外兩類：

* **schema 時點**——三份模板與範例的 front matter 必須帶齊 expectations-v1 欄位，
  且持有期（``holding_horizon_months``）與預測期（``forecast_horizon_years``）是兩個
  獨立欄位，不得只有其一。
* **實際報告輸出的行為**——範例報告引用的數字，必須與 ``valuation_math`` 由同一組
  輸入實際算出來的值一致；模板不得殘留已退役的指令；表格不得超過七欄。
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path
from types import ModuleType
from typing import ClassVar

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "research-report-kit"
TEMPLATES = PLUGIN / "skills" / "research-report-output" / "templates"
SAMPLE = PLUGIN / "examples" / "sample-report.md"
SCRIPTS = PLUGIN / "skills" / "equity-valuation-discipline" / "scripts"
VALUATION = PLUGIN / "skills" / "equity-valuation-discipline"
OUTPUT = PLUGIN / "skills" / "research-report-output"

# 上層目錄含連字號，不是合法 package 名稱；沿用 test_valuation_math.py 的載入方式。
_spec = importlib.util.spec_from_file_location("valuation_math", SCRIPTS / "valuation_math.py")
assert _spec is not None and _spec.loader is not None
vm: ModuleType = importlib.util.module_from_spec(_spec)
sys.modules["valuation_math"] = vm
_spec.loader.exec_module(vm)

METHODOLOGY_VERSION = "expectations-v1"

#: 每份報告的 front matter 都必須帶的 expectations-v1 欄位。
REQUIRED_FIELDS = (
    "methodology_version",
    "research_question",
    "as_of",
    "strategy_type",
    "holding_horizon_months",
    "forecast_horizon_years",
    "valuation_methods",
    "expectations_status",
    "decision_status",
    "decision_policy_source",
)

ENUMS = {
    "strategy_type": {"fundamental", "catalyst", "monitoring", "unknown"},
    "expectations_status": {"supported", "insufficient", "no_material_gap"},
    "decision_status": {"actionable_candidate", "watch", "avoid"},
    "edge_status": {"hypothesis_only", "evidence_supported", "validated_with_limits", None},
}

#: 已退役、不得再以「有效指令」形式出現的規則。
#: value 是允許出現的語境（退役說明），命中這些字樣的行不算違規。
RETIRED_PATTERNS = {
    r"安全邊際\s*[＝=]": "退役|不再|取消|已改",
    r"EV\s*×\s*\(\s*1\s*[−-]\s*安全邊際\s*\)": "退役|不再|取消",
    r"逾期預設動作": "退役|不再|取消",
    r"min\(.*Kelly": "退役|不再|取消",
    r"衍生\s*P/NOPAT": "退役|不再|取消|不是",
    r"基礎折讓": "退役|不再|取消",
}

MARKDOWN_FILES = sorted(PLUGIN.rglob("*.md"))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def front_matter(path: Path) -> dict:
    text = read(path)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"{path.name} 缺少 front matter"
    return yaml.safe_load(match.group(1)) or {}


def report_files() -> list[Path]:
    return sorted(TEMPLATES.glob("*.md")) + [SAMPLE]


class TestFrontMatterSchema(unittest.TestCase):
    """schema 時點：欄位齊備、列舉值合法、持有期與預測期分開。"""

    def test_every_report_declares_required_fields(self) -> None:
        for path in report_files():
            with self.subTest(path.name):
                meta = front_matter(path)
                missing = [f for f in REQUIRED_FIELDS if f not in meta]
                self.assertEqual(missing, [], f"{path.name} 缺欄位：{missing}")

    def test_methodology_version_is_pinned_and_separate_from_report_version(self) -> None:
        for path in report_files():
            with self.subTest(path.name):
                meta = front_matter(path)
                self.assertEqual(meta["methodology_version"], METHODOLOGY_VERSION)
                # 報告版本與方法論版本是兩個欄位，不得互相取代
                self.assertIn("version", meta)
                self.assertNotEqual(meta["version"], meta["methodology_version"])

    def test_horizon_fields_are_two_independent_fields(self) -> None:
        """持有期 ≠ 預測期：兩者必須各自存在，缺一即違反 FR-01。"""
        for path in report_files():
            with self.subTest(path.name):
                meta = front_matter(path)
                self.assertIn("holding_horizon_months", meta)
                self.assertIn("forecast_horizon_years", meta)

    def test_enum_fields_use_declared_values(self) -> None:
        for path in report_files():
            meta = front_matter(path)
            for field, allowed in ENUMS.items():
                if field not in meta:
                    continue
                value = meta[field]
                if isinstance(value, str) and value.startswith("〈"):
                    continue  # 模板佔位符
                with self.subTest(f"{path.name}:{field}"):
                    self.assertIn(value, allowed)

    def test_kpi_cards_between_three_and_five(self) -> None:
        for path in report_files():
            with self.subTest(path.name):
                kpi = front_matter(path).get("kpi") or []
                self.assertGreaterEqual(len(kpi), 3)
                self.assertLessEqual(len(kpi), 5)


class TestSampleReportMatchesComputedValues(unittest.TestCase):
    """實際報告輸出的行為：範例引用的數字須與模組實算值一致。

    這不是關鍵字比對——右側的期望值全部由 ``valuation_math`` 從同一組輸入現算，
    改了公式或改了範例任一邊，測試都會紅。
    """

    # expectations-and-decisions.md 第 14 節的固定示範輸入
    ENTRY = 2450.0
    SHARES_BN = 25.932
    SCENARIOS: ClassVar[dict[str, tuple[float, float, float]]] = {  # 名稱 -> (營收十億元, 淨利率, 本益比)
        "bear": (6000.0, 0.44, 18.0),
        "base": (6800.0, 0.48, 22.0),
        "bull": (7600.0, 0.50, 26.0),
    }

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(SAMPLE)
        cls.prices = {
            name: revenue * margin / cls.SHARES_BN * pe
            for name, (revenue, margin, pe) in cls.SCENARIOS.items()
        }
        cls.returns = {
            name: vm.price_return(price, cls.ENTRY) for name, price in cls.prices.items()
        }

    #: 抓出文中所有數字（含千分位與小數），供容差比對用。
    NUMBER_RE: ClassVar[re.Pattern[str]] = re.compile(r"\d[\d,]*(?:\.\d+)?")

    def assert_number_present(self, value: float, digits: int, msg: str) -> None:
        """範例中必須有一個數字，與實算值在該顯示位數的容差內相符。

        不比對字串格式——文件寫 ``3,809.96`` 或 ``3,810`` 都算通過，只要數值對得上。
        這樣測試綁的是「數字正確」而不是「排版寫法」。
        """
        target = abs(value)
        tolerance = max(0.5 * 10 ** -digits, abs(target) * 1e-6)
        for token in self.NUMBER_RE.findall(self.text):
            try:
                candidate = float(token.replace(",", ""))
            except ValueError:  # pragma: no cover - 正規表示式已限制格式
                continue
            if abs(candidate - target) <= tolerance:
                return
        self.fail(f"{msg}：範例中找不到與 {target:,.{digits}f} 相符的數字（容差 {tolerance:g}）")

    def test_scenario_prices_match_recomputed_values(self) -> None:
        for name, price in self.prices.items():
            with self.subTest(name):
                self.assert_number_present(price, 0, f"{name} 期末價格")

    def test_price_returns_match_recomputed_values(self) -> None:
        for name, ret in self.returns.items():
            with self.subTest(name):
                self.assert_number_present(ret * 100, 2, f"{name} 價差報酬")

    def test_both_reward_risk_ratios_are_reported(self) -> None:
        """FR-15：牛/熊與基準/熊兩種都要列，不得只挑最大值。"""
        rr_bull = vm.reward_risk(self.prices["bull"], self.ENTRY, self.prices["bear"])
        rr_base = vm.reward_risk(self.prices["base"], self.ENTRY, self.prices["bear"])
        assert rr_bull is not None and rr_base is not None
        self.assert_number_present(rr_bull, 2, "牛/熊 R/R")
        self.assert_number_present(rr_base, 2, "基準/熊 R/R")

    def test_three_illustrative_probability_sets_are_reported(self) -> None:
        """FR-16：至少三組機率，涵蓋正期望、近損益兩平、負期望。"""
        configs = [(0.25, 0.50, 0.25), (0.45, 0.45, 0.10), (0.50, 0.40, 0.10)]
        expectations = []
        for p_bear, p_base, p_bull in configs:
            value = vm.expected_value(
                [p_bear, p_base, p_bull],
                [self.returns["bear"], self.returns["base"], self.returns["bull"]],
            )
            expectations.append(value)
            self.assert_number_present(value * 100, 2, "期望價差報酬")

        self.assertGreater(expectations[0], 0, "第一組應為正期望")
        self.assertLess(abs(expectations[1]), 0.01, "第二組應接近損益兩平")
        self.assertLess(expectations[2], 0, "第三組應為負期望")

    def test_probability_source_is_labelled_illustrative(self) -> None:
        """合成案例不得宣稱已驗證的 edge。"""
        self.assertIn("illustrative", self.text)
        self.assertIn("hypothesis_only", self.text)

    def test_holding_period_return_is_not_derived_from_intrinsic_value(self) -> None:
        """FR-07：禁止把 V0/P0 − 1 稱為持有期報酬。"""
        forbidden = re.compile(r"V0\s*/\s*P0\s*[−-]\s*1\s*[＝=]?\s*(持有期|預期)報酬")
        self.assertIsNone(forbidden.search(self.text))


class TestPreEntryScreenContract(unittest.TestCase):
    """建倉前快篩須跨 SSOT、輸出模式與模板維持同一份行為契約。"""

    def test_ssot_blocks_red_screen_without_policy_override(self) -> None:
        """次級 reference 不得獨占紅燈時的 decision_status 路由。"""
        ssot = read(VALUATION / "references" / "expectations-and-decisions.md")
        decision_section = ssot.split("## 11. 決策", 1)[1].split("## 12. 部位計算", 1)[0]
        for requirement in ("建倉前快篩", "🔴", "使用者風險政策", "不得僅因"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, decision_section)

    def test_briefing_preserves_pre_entry_decision_evidence(self) -> None:
        """Briefing 不得因刪節而遺失快篩結果與決策影響。"""
        output_skill = read(OUTPUT / "SKILL.md")
        briefing = output_skill.split("### Briefing", 1)[1].split("### ⚠️ 刪節後處理", 1)[0]
        for requirement in (
            "S1–S6",
            "未覆蓋",
            "最脆弱",
            "決策影響",
            "一句判定依據",
            "inline 來源／日期",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, briefing)

    def test_single_stock_template_collects_pre_entry_screen(self) -> None:
        """完整 A 型報告須實際提供快篩輸入位置，而非只靠 reference。"""
        template = read(TEMPLATES / "A-single-stock.md")
        for requirement in ("建倉前快篩", "S1", "S6", "N/A", "最脆弱"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, template)

        chapter_five = template.index("## 五、")
        screen = template.index("### 5.1 建倉前快篩")
        governance = template.index("### 5.2 治理與籌碼面")
        chapter_six = template.index("## 六、")
        self.assertLess(chapter_five, screen)
        self.assertLess(screen, governance)
        self.assertLess(governance, chapter_six)

    def test_sotp_summary_rows_stay_inside_sotp_table(self) -> None:
        """新增章節不得切斷 SOTP 表頭與彙總列。"""
        template = read(TEMPLATES / "A-single-stock.md")
        sotp = template.split("### 6.1 分部加總", 1)[1].split("### 6.2 週期常態化", 1)[0]
        header = sotp.index("| 分部 |")
        subtotal = sotp.index("| 小計 |")
        adjusted = sotp.index("| **調整後 `EV_enterprise`** |")
        self.assertLess(header, subtotal)
        self.assertLess(subtotal, adjusted)

    def test_template_reuses_s3_measure_instead_of_legacy_total(self) -> None:
        """模板不得以未限定期間的承諾總額另設一套門檻。"""
        template = read(TEMPLATES / "A-single-stock.md")
        self.assertNotIn("承諾總額 > 一年營收", template)
        self.assertIn("24 個月未入帳固定承諾現值年化", template)
        self.assertIn("承諾調整後淨負債", template)

    def test_outputs_do_not_copy_the_decision_routing_table(self) -> None:
        """範例與模板不得重抄可能落後 SSOT 的 actionable_candidate 條件。"""
        copied_route = "預期差、驗證路徑、成本後報酬與使用者風險政策**均**通過"
        for path in (*TEMPLATES.glob("*.md"), SAMPLE):
            with self.subTest(path=path.name):
                self.assertNotIn(copied_route, read(path))

    def test_active_markdown_has_no_legacy_s3_measure(self) -> None:
        """所有有效文件只能引用 S3 的 24 個月單一計量契約。"""
        forbidden = (
            "承諾總額 ÷ `EV_enterprise`",
            "承諾總額 > 一年營收",
            "未來 5 年：採購承諾",
        )
        offenders: list[str] = []
        for path in MARKDOWN_FILES:
            if path.name == "CHANGELOG.md":
                continue
            text = read(path)
            for phrase in forbidden:
                if phrase in text:
                    offenders.append(f"{path.relative_to(PLUGIN)}: {phrase}")
        self.assertEqual(offenders, [], "仍有舊 S3 計量契約：\n" + "\n".join(offenders))

    def test_s3_defines_comparable_commitment_measure(self) -> None:
        """S3 不得把不同期間與重複認列的承諾直接相加後套紅燈。"""
        screen = read(VALUATION / "references" / "pre-entry-balance-sheet-screen.md")
        s3_section = screen.split("| S3 |", 1)[1].split("| S4 |", 1)[0]
        for requirement in ("未來 24 個月", "排除已入帳", "現值", "情境機率"):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, s3_section)

    def test_s3_requires_unique_classification_and_incremental_exposure(self) -> None:
        """同一底層現金流不得跨來源或固定／或有分類重複計入。"""
        screen = read(VALUATION / "references" / "pre-entry-balance-sheet-screen.md")
        s3_section = screen.split("| S3 |", 1)[1].split("| S4 |", 1)[0]
        for requirement in (
            "按合約與**底層現金流**跨來源去重",
            "固定承諾或或有曝險中**只能歸類一次**",
            "保證等或有義務",
            "只計固定承諾未涵蓋的增額曝險",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, s3_section)

    def test_template_and_sample_map_consequences_and_probabilities_together(self) -> None:
        """每個適用輸出須在同一規則段同時交代後果與機率的去向。"""
        contracts = (
            (
                TEMPLATES / "A-single-stock.md",
                "> **任一項觸發警示的處理**",
                ("具體經濟後果", "放入適用情境", "發生機率", "權重"),
            ),
            (
                SAMPLE,
                "> **資本強度警示的處理**",
                ("後果已放入", "熊情境淨利率", "發生可能性", "熊情境權重"),
            ),
        )
        for path, anchor, requirements in contracts:
            text = read(path)
            paragraph = text.split(anchor, 1)[1].split("\n\n", 1)[0]
            for requirement in requirements:
                with self.subTest(path=path.name, requirement=requirement):
                    self.assertIn(requirement, paragraph)

    def test_active_markdown_has_no_probability_only_risk_rule(self) -> None:
        """有效文件不得要求風險只改機率而排除情境內的經濟後果。"""
        forbidden = (
            "警示由情境機率承接",
            "不得再砍營收或把利潤率取下緣",
            "未另外砍營收或取利潤率下緣",
        )
        offenders: list[str] = []
        for path in MARKDOWN_FILES:
            if path.name == "CHANGELOG.md":
                continue
            text = read(path)
            for phrase in forbidden:
                if phrase in text:
                    offenders.append(f"{path.relative_to(PLUGIN)}: {phrase}")
        self.assertEqual(offenders, [], "仍有風險只調機率的舊規則：\n" + "\n".join(offenders))


class TestRetiredRulesAreNotActiveInstructions(unittest.TestCase):
    """已退役的規則只能以「退役說明」出現，不得留為有效指令。

    ``CHANGELOG.md`` 不在掃描範圍——變更紀錄的「移除」段本來就要逐條列出被拿掉的
    規則原文，那是歷史紀錄而非有效指令。
    """

    def test_no_retired_rule_survives_as_instruction(self) -> None:
        offenders: list[str] = []
        for path in MARKDOWN_FILES:
            if path.name == "CHANGELOG.md":
                continue
            for lineno, line in enumerate(read(path).splitlines(), 1):
                for pattern, allowed_context in RETIRED_PATTERNS.items():
                    if re.search(pattern, line) and not re.search(allowed_context, line):
                        offenders.append(f"{path.relative_to(PLUGIN)}:{lineno}  {line.strip()[:80]}")
        self.assertEqual(offenders, [], "退役規則仍以有效指令形式存在：\n" + "\n".join(offenders))


class TestTableWidth(unittest.TestCase):
    """PDF 版面上限：表格欄數不得超過 7，超過須拆表。"""

    def test_no_table_exceeds_seven_columns(self) -> None:
        offenders: list[str] = []
        for path in MARKDOWN_FILES:
            for lineno, line in enumerate(read(path).splitlines(), 1):
                stripped = line.strip()
                if not (stripped.startswith("|") and stripped.endswith("|")):
                    continue
                if "---" in stripped:
                    continue
                columns = len(stripped.split("|")) - 2
                if columns > 7:
                    offenders.append(f"{path.relative_to(PLUGIN)}:{lineno}  {columns} 欄")
        self.assertEqual(offenders, [], "表格超過 7 欄：\n" + "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
