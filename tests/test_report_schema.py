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
