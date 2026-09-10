"""估值數值核心模組的數值與邊界案例測試。

對應 `docs/v1.3.0-spec.md` 第 4、5、9.2、12 節（COR-01～03、FR-15～17、12.1、12.2、
12.5）。所有數值案例以完整精度重算，不拿展示用的四捨五入整數價格當中間輸入。
"""

from __future__ import annotations

import importlib.util
import inspect
import math
import sys
from pathlib import Path
from types import ModuleType

import pytest

# --- 動態載入模組 ---
# 上層目錄含連字號（research-report-kit、equity-valuation-discipline），
# 不是合法的 Python package 名稱，因此把 scripts/ 目錄加進 sys.path 後
# 以一般模組名稱 import，讓型別檢查器能正常解析屬性。
_SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / "plugins"
    / "research-report-kit"
    / "skills"
    / "equity-valuation-discipline"
    / "scripts"
)
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

_spec = importlib.util.spec_from_file_location(
    "valuation_math", _SCRIPTS_DIR / "valuation_math.py"
)
assert _spec is not None and _spec.loader is not None
vm: ModuleType = importlib.util.module_from_spec(_spec)
sys.modules["valuation_math"] = vm
_spec.loader.exec_module(vm)


# ============================================================
# COR-01：折現率配對
# ============================================================


def test_cost_of_equity_is_not_named_wacc() -> None:
    """股權成本函式必須明確命名，不得叫 wacc；wacc 是另一個獨立函式。"""
    assert hasattr(vm, "cost_of_equity")
    assert hasattr(vm, "wacc")
    assert vm.cost_of_equity is not vm.wacc
    ke = vm.cost_of_equity(rf=0.02, beta=1.1, erp=0.06)
    assert ke == pytest.approx(0.02 + 1.1 * 0.06)


def test_wacc_reference_case() -> None:
    """§9.2 WACC 配對：E=80、D=20、ke=10%、kd=5%、T=20% -> 8.8%。"""
    result = vm.wacc(ke=0.10, kd=0.05, equity_value=80, debt_value=20, tax_rate=0.20)
    assert result == pytest.approx(0.088)
    assert result != pytest.approx(0.10)  # 不能直接填股權成本當 WACC


def test_wacc_rejects_non_positive_capital_base() -> None:
    """E+D <= 0 時折現率配對無意義，必須拒絕。"""
    with pytest.raises(ValueError):
        vm.wacc(ke=0.10, kd=0.05, equity_value=0, debt_value=0, tax_rate=0.20)


def test_wacc_rejects_negative_components() -> None:
    with pytest.raises(ValueError):
        vm.wacc(ke=0.10, kd=0.05, equity_value=-10, debt_value=20, tax_rate=0.20)


# ============================================================
# COR-02：企業價值橋接
# ============================================================


def test_equity_bridge_reference_case() -> None:
    """§9.2 股權橋接：EV=1000、超額現金=100、非營運=50、債務=300、其他=50、股數=100。"""
    equity_value, per_share = vm.equity_bridge(
        ev_operating=1000,
        excess_cash=100,
        non_operating_assets=50,
        debt=300,
        other_claims=50,
        shares=100,
    )
    assert equity_value == pytest.approx(800)
    assert per_share == pytest.approx(8)


def test_equity_bridge_round_trip() -> None:
    """反向重建：per_share * shares 必須等於原始股權價值。"""
    equity_value, per_share = vm.equity_bridge(
        ev_operating=2500,
        excess_cash=40,
        non_operating_assets=10,
        debt=600,
        other_claims=20,
        shares=193.5,
    )
    rebuilt = per_share * 193.5
    assert rebuilt == pytest.approx(equity_value, rel=1e-6)


def test_equity_bridge_rejects_zero_shares() -> None:
    """股數為 0：除以零邊界，必須拒絕而非輸出 inf。"""
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=1000,
            excess_cash=0,
            non_operating_assets=0,
            debt=0,
            other_claims=0,
            shares=0,
        )


def test_equity_bridge_rejects_negative_shares() -> None:
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=1000,
            excess_cash=0,
            non_operating_assets=0,
            debt=0,
            other_claims=0,
            shares=-10,
        )


def test_equity_bridge_rejects_non_positive_equity_value() -> None:
    """結果域邊界：股權價值 <= 0 不得無聲通過（此處選擇明確拒絕）。"""
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=100,
            excess_cash=0,
            non_operating_assets=0,
            debt=1000,
            other_claims=0,
            shares=100,
        )
    # 剛好等於 0 也必須拒絕，不是只有負值才拒絕
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=1000,
            excess_cash=0,
            non_operating_assets=0,
            debt=1000,
            other_claims=0,
            shares=100,
        )


def test_equity_bridge_uses_distinct_param_names_not_generic_price() -> None:
    """文件層約束：報告與部位模組欄位不得互換，函式簽名以明確參數名表達。

    `equity_bridge` 的參數是企業價值橋接的組成項，刻意不使用泛用的
    `price`／`p_entry`／`p_end` 之類名稱，避免呼叫端把期末市價或進場價
    誤塞進股權橋接。此測試只驗證簽名慣例，實際欄位混用的防呆屬文件層
    規範，Python 型別系統不強制。
    """
    params = set(inspect.signature(vm.equity_bridge).parameters)
    assert params.isdisjoint({"price", "p_entry", "p_end", "p_upside", "p_downside"})


# ============================================================
# COR-03：成長序列與再投資
# ============================================================


def test_growth_path_reference_case() -> None:
    """§9.2 成長序列端點：g1=20%、終端3%、N=3 線性 -> [20%, 11.5%, 3%]。"""
    path = vm.growth_path(g1=0.20, g_terminal=0.03, n=3)
    assert path == pytest.approx([0.20, 0.115, 0.03])
    assert path[0] == pytest.approx(0.20)
    assert path[-1] == pytest.approx(0.03)


def test_growth_path_endpoints_always_hold_for_longer_paths() -> None:
    path = vm.growth_path(g1=0.30, g_terminal=0.02, n=6)
    assert len(path) == 6
    assert path[0] == pytest.approx(0.30)
    assert path[-1] == pytest.approx(0.02)


def test_growth_path_n_equals_one_has_defined_behavior() -> None:
    """N=1 時第一個與最後一個元素必須是同一格，g1/g_terminal 若不同即矛盾。

    本模組的判斷：拒絕呼叫（raise），而非默默回傳 [g1] 卻違反「最後一個
    元素等於終端成長」的不變式。呼叫端若真的只要單一年度成長率，應直接
    使用 g1，不透過本函式。
    """
    with pytest.raises(ValueError):
        vm.growth_path(g1=0.20, g_terminal=0.03, n=1)


def test_growth_path_rejects_n_below_one() -> None:
    with pytest.raises(ValueError):
        vm.growth_path(g1=0.20, g_terminal=0.03, n=0)
    with pytest.raises(ValueError):
        vm.growth_path(g1=0.20, g_terminal=0.03, n=-2)


def test_reinvestment_reference_case() -> None:
    """§9.2 再投資分母：前期營收100、成長10%、k=2、NOPAT率20%。

    當期營收 110、NOPAT 22、再投資 20、FCFF 2；不是以 110*2*10% 得到 22。
    """
    reinvest = vm.reinvestment(revenue_prev=100, growth=0.10, k=2)
    assert reinvest == pytest.approx(20)
    nopat = 100 * 1.10 * 0.20
    assert nopat == pytest.approx(22)
    fcff = vm.fcff_simplified(nopat=nopat, reinvestment=reinvest)
    assert fcff == pytest.approx(2)


def test_reinvestment_k_zero_does_not_divide_by_zero() -> None:
    """k=0 的邊界：再投資公式是乘法（k × ΔRevenue），k=0 不應除以零或崩潰。"""
    reinvest = vm.reinvestment(revenue_prev=100, growth=0.10, k=0)
    assert reinvest == pytest.approx(0.0)


def test_reinvestment_does_not_use_growth_rate_as_denominator() -> None:
    """驗證再投資不是用成長率當分母：growth 很小時公式仍應正常運作。"""
    reinvest = vm.reinvestment(revenue_prev=1000, growth=0.001, k=3)
    assert reinvest == pytest.approx(3 * (1000 * 1.001 - 1000))
    assert math.isfinite(reinvest)


# ============================================================
# FCFF：完整式與簡化式分開
# ============================================================


def test_fcff_full_reference_case() -> None:
    fcff = vm.fcff_full(nopat=100, dep_amort=20, capex=35, delta_nwc=5)
    assert fcff == pytest.approx(100 + 20 - 35 - 5)


def test_fcff_simplified_reference_case() -> None:
    fcff = vm.fcff_simplified(nopat=100, reinvestment=25)
    assert fcff == pytest.approx(75)


def test_fcff_full_and_simplified_are_distinct_functions() -> None:
    """兩式不得混用；同樣輸入代入不同公式，一般不會得到相同結果。"""
    full = vm.fcff_full(nopat=100, dep_amort=20, capex=35, delta_nwc=5)
    simplified = vm.fcff_simplified(nopat=100, reinvestment=30)
    assert full != pytest.approx(simplified)


# ============================================================
# 終值邊界
# ============================================================


def test_terminal_value_normal_case() -> None:
    tv = vm.terminal_value(cf_next=100, discount_rate=0.10, g_perpetual=0.03)
    assert tv == pytest.approx(100 / 0.07)


def test_terminal_value_rejects_discount_rate_equal_to_growth() -> None:
    """§9.2 終值邊界：折現率 <= 永續成長率時必須拒絕計算，不能輸出有限合理價。"""
    with pytest.raises(ValueError):
        vm.terminal_value(cf_next=100, discount_rate=0.03, g_perpetual=0.03)


def test_terminal_value_rejects_discount_rate_below_growth() -> None:
    with pytest.raises(ValueError):
        vm.terminal_value(cf_next=100, discount_rate=0.02, g_perpetual=0.03)


def test_terminal_value_reverse_round_trip() -> None:
    """Reverse round-trip：正算終值後固定其餘輸入反解永續成長率，誤差 <= 1e-6。"""
    discount_rate = 0.095
    g_perpetual = 0.025
    cf_next = 42.0
    tv = vm.terminal_value(cf_next=cf_next, discount_rate=discount_rate, g_perpetual=g_perpetual)
    rebuilt_g = discount_rate - cf_next / tv
    assert rebuilt_g == pytest.approx(g_perpetual, abs=1e-6)


# ============================================================
# FR-07：情境報酬與期望值
# ============================================================


def test_scenario_return_and_expected_value_reference_case() -> None:
    """§9.2 期望報酬：P0=100，期末70/110/150，機率25/50/25%，股利2、成本1。

    情境報酬 -29%/11%/51%；期望報酬 11%。
    """
    r_bear = vm.scenario_return(p_end=70, dividend=2, p_entry=100, cost=1)
    r_base = vm.scenario_return(p_end=110, dividend=2, p_entry=100, cost=1)
    r_bull = vm.scenario_return(p_end=150, dividend=2, p_entry=100, cost=1)
    assert r_bear == pytest.approx(-0.29)
    assert r_base == pytest.approx(0.11)
    assert r_bull == pytest.approx(0.51)

    expected = vm.expected_value(
        probabilities=[0.25, 0.50, 0.25], values=[r_bear, r_base, r_bull]
    )
    assert expected == pytest.approx(0.11)


def test_expected_value_rejects_non_unit_sum() -> None:
    with pytest.raises(ValueError):
        vm.expected_value(probabilities=[0.3, 0.3, 0.3], values=[1, 2, 3])


def test_expected_value_rejects_negative_probability() -> None:
    with pytest.raises(ValueError):
        vm.expected_value(probabilities=[-0.1, 0.6, 0.5], values=[1, 2, 3])


def test_expected_value_rejects_empty_input() -> None:
    """空集合邊界。"""
    with pytest.raises(ValueError):
        vm.expected_value(probabilities=[], values=[])


def test_expected_value_accepts_single_element() -> None:
    """單一元素邊界：機率為 1 的單一情境合法。"""
    assert vm.expected_value(probabilities=[1.0], values=[0.42]) == pytest.approx(0.42)


def test_expected_value_tolerates_floating_point_rounding() -> None:
    """機率總和容差 1e-9：0.1+0.2+0.7 在浮點下可能不是精確 1。"""
    result = vm.expected_value(probabilities=[0.1, 0.2, 0.7], values=[1, 2, 3])
    assert result == pytest.approx(0.1 * 1 + 0.2 * 2 + 0.7 * 3)


def test_probability_adjustment_bear_plus_10pp_from_base_stays_normalized() -> None:
    """§9.2 機率調整：25/50/25，熊 +10pp 自基準移出 -> 35/40/25，總和仍 100%。"""
    adjusted = [0.25 + 0.10, 0.50 - 0.10, 0.25]
    assert adjusted == pytest.approx([0.35, 0.40, 0.25])
    assert sum(adjusted) == pytest.approx(1.0)
    # 必須能正常餵給 expected_value，不因調整後總和誤差被拒絕
    result = vm.expected_value(probabilities=adjusted, values=[-0.29, 0.11, 0.51])
    assert math.isfinite(result)


# ============================================================
# 結果域邊界：總報酬 <= -100%
# ============================================================


def test_scenario_return_can_reach_total_wipeout() -> None:
    """總報酬 = -100%：期末價格與股利歸零、無額外成本。"""
    r = vm.scenario_return(p_end=0, dividend=0, p_entry=100, cost=0)
    assert r == pytest.approx(-1.0)


def test_scenario_return_can_go_below_negative_100_percent_with_cost() -> None:
    """總報酬 < -100%：成本可使報酬跌破全損，數值本身仍須是有限實數。"""
    r = vm.scenario_return(p_end=0, dividend=0, p_entry=100, cost=20)
    assert r == pytest.approx(-1.20)
    assert math.isfinite(r)


def test_scenario_return_rejects_non_positive_entry_price() -> None:
    """除以零／負進場價邊界。"""
    with pytest.raises(ValueError):
        vm.scenario_return(p_end=100, dividend=0, p_entry=0, cost=0)
    with pytest.raises(ValueError):
        vm.scenario_return(p_end=100, dividend=0, p_entry=-50, cost=0)


def test_price_return_reference_and_boundary() -> None:
    assert vm.price_return(p_end=110, p_entry=100) == pytest.approx(0.10)
    with pytest.raises(ValueError):
        vm.price_return(p_end=100, p_entry=0)


def test_annualized_return_guards_total_return_at_or_below_negative_100_percent() -> None:
    """年化：(1+total)^(1/years) 在 total <= -100% 時底數非正，必須明確拒絕。

    不得讓 Python 算出複數、NaN 進而在後續格式化時才爆掉。
    """
    with pytest.raises(ValueError):
        vm.annualized_return(total_return=-1.0, years=1)
    with pytest.raises(ValueError):
        vm.annualized_return(total_return=-1.5, years=2)


def test_annualized_return_normal_case() -> None:
    result = vm.annualized_return(total_return=0.21, years=2)
    assert result == pytest.approx((1.21) ** 0.5 - 1)


def test_annualized_return_rejects_non_positive_years() -> None:
    with pytest.raises(ValueError):
        vm.annualized_return(total_return=0.10, years=0)


# ============================================================
# FR-15：Reward/Risk
# ============================================================


def test_reward_risk_returns_none_when_downside_not_below_entry() -> None:
    """下檔情境不低於進場價：分母 <= 0，必須回傳不適用語義，不得輸出 inf 或負值。"""
    result = vm.reward_risk(p_upside=120, p_entry=100, p_downside=100)
    assert result is None
    result_above = vm.reward_risk(p_upside=120, p_entry=100, p_downside=105)
    assert result_above is None


def test_reward_risk_normal_case() -> None:
    result = vm.reward_risk(p_upside=150, p_entry=100, p_downside=70)
    assert result == pytest.approx((150 - 100) / (100 - 70))


# ============================================================
# FR-16／12.2：損益兩平機率
# ============================================================


def test_breakeven_probability_binary_reference_case() -> None:
    """二元例：G=20%、L=10%、c=1% -> 損益兩平勝率約 36.6667%。"""
    p_be = vm.breakeven_probability_binary(gain=0.20, loss=0.10, cost=0.01)
    assert p_be == pytest.approx(0.366666666666666667, rel=1e-9)


def test_breakeven_probability_binary_threshold_above_one_is_callable_detectable() -> None:
    """門檻 > 1：表示無法達成正期望，呼叫端須能辨識（此處以 > 1 判斷）。"""
    p_be = vm.breakeven_probability_binary(gain=0.01, loss=1.00, cost=0.50)
    assert p_be > 1.0


def test_breakeven_probability_binary_rejects_zero_denominator() -> None:
    """除以零邊界：gain+loss<=0。"""
    with pytest.raises(ValueError):
        vm.breakeven_probability_binary(gain=0.0, loss=0.0, cost=0.01)


# ============================================================
# §12.1／12.5：台積電固定示範（完整精度重算，不用展示用整數價格）
# ============================================================

_SHARES_BN = 25.932  # 股數 259.32 億股 = 25.932 十億股
_P0 = 2450.0


def _eps(revenue_bn: float, net_margin: float) -> float:
    return revenue_bn * net_margin / _SHARES_BN


def _scenario_end_price(revenue_bn: float, net_margin: float, pe: float) -> float:
    return _eps(revenue_bn, net_margin) * pe


def test_section_12_1_end_prices_full_precision() -> None:
    bear_p = _scenario_end_price(6000, 0.44, 18)
    base_p = _scenario_end_price(6800, 0.48, 22)
    bull_p = _scenario_end_price(7600, 0.50, 26)
    assert bear_p == pytest.approx(1832.48496, rel=1e-8)
    assert base_p == pytest.approx(2769.08839, rel=1e-8)
    assert bull_p == pytest.approx(3809.96452, rel=1e-8)


def test_section_12_1_price_returns() -> None:
    bear_p = _scenario_end_price(6000, 0.44, 18)
    base_p = _scenario_end_price(6800, 0.48, 22)
    bull_p = _scenario_end_price(7600, 0.50, 26)

    r_bear = vm.price_return(p_end=bear_p, p_entry=_P0)
    r_base = vm.price_return(p_end=base_p, p_entry=_P0)
    r_bull = vm.price_return(p_end=bull_p, p_entry=_P0)

    assert r_bear == pytest.approx(-0.25205, abs=1e-5)
    assert r_base == pytest.approx(0.13024, abs=1e-5)
    assert r_bull == pytest.approx(0.55509, abs=1e-5)


def test_section_12_1_and_12_5_reward_risk() -> None:
    bear_p = _scenario_end_price(6000, 0.44, 18)
    base_p = _scenario_end_price(6800, 0.48, 22)
    bull_p = _scenario_end_price(7600, 0.50, 26)

    rr_bull_bear = vm.reward_risk(p_upside=bull_p, p_entry=_P0, p_downside=bear_p)
    rr_base_bear = vm.reward_risk(p_upside=base_p, p_entry=_P0, p_downside=bear_p)

    assert rr_bull_bear == pytest.approx(2.202318, abs=1e-5)
    assert rr_base_bear == pytest.approx(0.516730, abs=1e-5)


def test_section_12_1_expected_price_returns_for_three_probability_sets() -> None:
    """A(25/50/25)=0.14088023、B(45/45/10)=0.00069570、C(50/40/10)=-0.01841866。"""
    bear_p = _scenario_end_price(6000, 0.44, 18)
    base_p = _scenario_end_price(6800, 0.48, 22)
    bull_p = _scenario_end_price(7600, 0.50, 26)

    r_bear = vm.price_return(p_end=bear_p, p_entry=_P0)
    r_base = vm.price_return(p_end=base_p, p_entry=_P0)
    r_bull = vm.price_return(p_end=bull_p, p_entry=_P0)

    config_a = vm.expected_value(
        probabilities=[0.25, 0.50, 0.25], values=[r_bear, r_base, r_bull]
    )
    config_b = vm.expected_value(
        probabilities=[0.45, 0.45, 0.10], values=[r_bear, r_base, r_bull]
    )
    config_c = vm.expected_value(
        probabilities=[0.50, 0.40, 0.10], values=[r_bear, r_base, r_bull]
    )

    assert config_a == pytest.approx(0.14088023, abs=1e-5)
    assert config_b == pytest.approx(0.00069570, abs=1e-5)
    assert config_c == pytest.approx(-0.01841866, abs=1e-5)


def test_section_12_2_fixed_base_probability_breakeven() -> None:
    """固定基準機率 0.5 的損益兩平：熊約 0.424544、牛約 0.075456，誤差 <= 1e-5。"""
    bear_p = _scenario_end_price(6000, 0.44, 18)
    base_p = _scenario_end_price(6800, 0.48, 22)
    bull_p = _scenario_end_price(7600, 0.50, 26)

    r_bear = vm.price_return(p_end=bear_p, p_entry=_P0)
    r_base = vm.price_return(p_end=base_p, p_entry=_P0)
    r_bull = vm.price_return(p_end=bull_p, p_entry=_P0)

    p_bear = vm.breakeven_bear_probability(
        r_bear=r_bear, r_base=r_base, r_bull=r_bull, p_base=0.5
    )
    p_bull = 1.0 - 0.5 - p_bear

    assert p_bear == pytest.approx(0.424544, abs=1e-5)
    assert p_bull == pytest.approx(0.075456, abs=1e-5)

    # round-trip：用反解出的機率重算期望價差報酬應近似 0
    expected = vm.expected_value(
        probabilities=[p_bear, 0.5, p_bull], values=[r_bear, r_base, r_bull]
    )
    assert expected == pytest.approx(0.0, abs=1e-5)


def test_breakeven_bear_probability_rejects_equal_bear_and_bull_returns() -> None:
    """熊與牛情境報酬相同時無法反解（除以零邊界）。"""
    with pytest.raises(ValueError):
        vm.breakeven_bear_probability(r_bear=0.1, r_base=0.05, r_bull=0.1, p_base=0.5)


def test_breakeven_bear_probability_rejects_out_of_range_base_probability() -> None:
    with pytest.raises(ValueError):
        vm.breakeven_bear_probability(r_bear=-0.2, r_base=0.1, r_bull=0.5, p_base=1.5)
    with pytest.raises(ValueError):
        vm.breakeven_bear_probability(r_bear=-0.2, r_base=0.1, r_bull=0.5, p_base=-0.1)


# ============================================================
# 其他輸入域邊界：極大、極小、除以零
# ============================================================


def test_wacc_handles_very_large_capital_values() -> None:
    result = vm.wacc(
        ke=0.10, kd=0.05, equity_value=8e14, debt_value=2e14, tax_rate=0.20
    )
    assert result == pytest.approx(0.088)


def test_terminal_value_handles_very_small_cash_flow() -> None:
    tv = vm.terminal_value(cf_next=1e-9, discount_rate=0.10, g_perpetual=0.03)
    assert tv == pytest.approx(1e-9 / 0.07)
    assert math.isfinite(tv)


def test_reinvestment_handles_zero_revenue_base() -> None:
    """revenue_prev=0 邊界：不應除以零（公式本身是乘法）。"""
    reinvest = vm.reinvestment(revenue_prev=0, growth=0.10, k=2)
    assert reinvest == pytest.approx(0.0)


# ============================================================
# COR-03 fade 引擎修正版：valuation-paths.md 第 4 節（4.3～4.6）
#
# 以下所有 ground truth 皆用獨立腳本（非本模組）手算：
# revenue_t = revenue_(t-1) * (1+g_t)；nopat_t = revenue_t * margin_t；
# reinvestment_t = k * (revenue_t - revenue_(t-1))；fcff_t = nopat_t - reinvestment_t；
# pv_t = fcff_t / (1+wacc)^t；終端沿用同一組公式多算一期後代入
# TV = fcff_(N+1) / (wacc - g_term)，再折現 /(1+wacc)^N。
# ============================================================

# --- 參考案例 A：RONIC >= WACC（不需要 terminal_policy） ---
_REF_G1, _REF_G_TERM, _REF_N = 0.15, 0.04, 4
_REF_MARGINS = [0.22, 0.21, 0.20, 0.19]
_REF_K = 1.5
_REF_WACC = 0.09
_REF_EV = 3.1160003418198867
_REF_YEAR_FCFF = [0.028000000000000136, 0.07337000000000016, 0.12846011111111105, 0.18968052977777777]
_REF_YEAR_REVENUE = [1.15, 1.280333333333333, 1.378492222222222, 1.4336319111111109]
_REF_TV_AT_N = 3.945355019377778
_REF_RONIC_TERM = 0.12666666666666668


def test_fade_enterprise_value_reference_case_ronic_above_wacc() -> None:
    """成長序列第一年必須是 g1（不是舊版 i/N 造成的已衰減值），逐年明細正確。"""
    growth_rates = vm.growth_path(g1=_REF_G1, g_terminal=_REF_G_TERM, n=_REF_N)
    result = vm.fade_enterprise_value(
        growth_rates=growth_rates,
        nopat_margin_path=_REF_MARGINS,
        k=_REF_K,
        wacc=_REF_WACC,
    )
    assert len(result.years) == _REF_N
    assert result.years[0].growth == pytest.approx(_REF_G1)
    assert result.years[-1].growth == pytest.approx(_REF_G_TERM)
    for i, year in enumerate(result.years):
        assert year.revenue == pytest.approx(_REF_YEAR_REVENUE[i])
        assert year.fcff == pytest.approx(_REF_YEAR_FCFF[i])
        # 逐年明細必須與獨立呼叫 reinvestment()/fcff_simplified() 得到的結果一致，
        # 不是另抄一份公式。
        revenue_prev = 1.0 if i == 0 else result.years[i - 1].revenue
        expected_reinvest = vm.reinvestment(
            revenue_prev=revenue_prev, growth=year.growth, k=_REF_K
        )
        assert year.reinvestment == pytest.approx(expected_reinvest)
        expected_fcff = vm.fcff_simplified(nopat=year.nopat, reinvestment=year.reinvestment)
        assert year.fcff == pytest.approx(expected_fcff)
    assert result.terminal_value == pytest.approx(_REF_TV_AT_N)
    assert result.enterprise_value == pytest.approx(_REF_EV)
    assert result.ronic_terminal == pytest.approx(_REF_RONIC_TERM)
    assert result.ronic_below_wacc is False


def test_fade_enterprise_value_growth_sequence_does_not_predecay_first_year() -> None:
    """對照舊 bug：第一年成長率必須恰好等於 g1，不是 g1 已經往終端衰減一步後的值。

    舊版 `g = g1 + (g_term-g1)*i/N`，`i` 從 1 起算，第一筆就已經衰減；
    正確版第一筆必須是 g1 本身（無衰減）。
    """
    growth_rates = vm.growth_path(g1=0.30, g_terminal=0.05, n=5)
    result = vm.fade_enterprise_value(
        growth_rates=growth_rates,
        nopat_margin_path=[0.25, 0.24, 0.23, 0.22, 0.21],
        k=1.0,
        wacc=0.10,
    )
    assert result.years[0].growth == pytest.approx(0.30)
    buggy_first_year_growth = 0.30 + (0.05 - 0.30) * 1 / 5  # 舊版的（錯誤）第一年值
    assert result.years[0].growth != pytest.approx(buggy_first_year_growth)


def test_fade_enterprise_value_reinvestment_uses_revenue_delta_not_growth_denominator() -> None:
    """對照舊 bug：re-投資不得用 k*g*當年營收，必須是 k*(Revenue_t - Revenue_(t-1))。"""
    growth_rates = [0.20, 0.20]
    margins = [0.30, 0.30]
    k = 1.0  # RONIC = 0.30/1.0 = 0.30 >= wacc，不觸發 terminal_policy 要求
    wacc = 0.25  # 須嚴格大於終端成長率 0.20，terminal_value() 才不拒絕
    result = vm.fade_enterprise_value(
        growth_rates=growth_rates, nopat_margin_path=margins, k=k, wacc=wacc
    )
    # 正確：reinvestment_1 = k * (1.20 - 1.00) = 1 * 0.20 = 0.20
    assert result.years[0].reinvestment == pytest.approx(0.20)
    # 舊 bug 會算成 k * g * revenue_current = 1 * 0.20 * 1.20 = 0.24
    buggy_value = k * 0.20 * 1.20
    assert result.years[0].reinvestment != pytest.approx(buggy_value)


def test_fade_enterprise_value_rejects_length_mismatch() -> None:
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.1, 0.05],
            nopat_margin_path=[0.2, 0.2, 0.2],
            k=1.0,
            wacc=0.10,
        )


def test_fade_enterprise_value_rejects_empty_growth_rates() -> None:
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[], nopat_margin_path=[], k=1.0, wacc=0.10
        )


def test_fade_enterprise_value_rejects_negative_k() -> None:
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.1, 0.05],
            nopat_margin_path=[0.2, 0.2],
            k=-1.0,
            wacc=0.10,
        )


def test_fade_enterprise_value_rejects_terminal_discount_rate_at_or_below_growth() -> None:
    """終值邊界：沿用 terminal_value 的守衛，折現率 <= 永續成長率必須拒絕。"""
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.10, 0.10],
            nopat_margin_path=[0.20, 0.20],
            k=1.0,
            wacc=0.08,  # <= 終端成長率 0.10
        )


# --- RONIC < WACC：不得自動取零成長 ---

_LOW_RONIC_K = 2.5
_LOW_RONIC_EV = 1.9413308942631147
_LOW_RONIC_TERM = 0.076


def test_fade_enterprise_value_ronic_below_wacc_requires_explicit_policy() -> None:
    """RONIC < WACC 且未給 terminal_policy：必須拒絕，不得悄悄取零成長繼續算。"""
    growth_rates = vm.growth_path(g1=_REF_G1, g_terminal=_REF_G_TERM, n=_REF_N)
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=growth_rates,
            nopat_margin_path=_REF_MARGINS,
            k=_LOW_RONIC_K,
            wacc=_REF_WACC,
        )


def test_fade_enterprise_value_ronic_below_wacc_rejects_invalid_policy_label() -> None:
    growth_rates = vm.growth_path(g1=_REF_G1, g_terminal=_REF_G_TERM, n=_REF_N)
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=growth_rates,
            nopat_margin_path=_REF_MARGINS,
            k=_LOW_RONIC_K,
            wacc=_REF_WACC,
            terminal_policy="just_use_zero_growth",  # 不在允許集合內
        )


@pytest.mark.parametrize(
    "policy", ["continue_value_destruction", "shrink_reinvestment", "restructure"]
)
def test_fade_enterprise_value_ronic_below_wacc_accepts_explicit_policy(policy: str) -> None:
    """三種有依據情境皆須可選；函式不得自行把 g_term 改成 0（用原本輸入照算）。"""
    growth_rates = vm.growth_path(g1=_REF_G1, g_terminal=_REF_G_TERM, n=_REF_N)
    result = vm.fade_enterprise_value(
        growth_rates=growth_rates,
        nopat_margin_path=_REF_MARGINS,
        k=_LOW_RONIC_K,
        wacc=_REF_WACC,
        terminal_policy=policy,
    )
    assert result.ronic_below_wacc is True
    assert result.terminal_policy == policy
    assert result.ronic_terminal == pytest.approx(_LOW_RONIC_TERM)
    # 函式沒有把 g_term 悄悄改成 0：EV 必須等於「原本輸入原樣計算」的值，
    # 不是零成長版本的 EV。
    assert result.enterprise_value == pytest.approx(_LOW_RONIC_EV)
    zero_growth_terminal_fcff = result.years[-1].fcff  # 若被改為 0 成長，終端現金流會等於最後一年 FCFF
    assert result.terminal_fcff_next != pytest.approx(zero_growth_terminal_fcff)


# --- 展示用倍數：EV/NOPAT，分母必須是同期 NOPAT ---


def test_fade_exit_multiple_uses_same_period_nopat_not_first_year_margin() -> None:
    """對照舊 bug：分母是同期 NOPAT，不是路徑第一年（或任何一年）的利潤率。"""
    growth_rates = vm.growth_path(g1=_REF_G1, g_terminal=_REF_G_TERM, n=_REF_N)
    result = vm.fade_enterprise_value(
        growth_rates=growth_rates,
        nopat_margin_path=_REF_MARGINS,
        k=_REF_K,
        wacc=_REF_WACC,
    )
    same_period_nopat = 0.30  # 呼叫端自行提供、與 EV 同時點的 NOPAT
    multiple = vm.fade_exit_multiple(
        enterprise_value=result.enterprise_value, nopat_same_period=same_period_nopat
    )
    assert multiple == pytest.approx(result.enterprise_value / same_period_nopat)
    # 舊 bug：實際除以 nopat_margin_path[0]（0.22），而不是同期 NOPAT。
    buggy_multiple = result.enterprise_value / _REF_MARGINS[0]
    assert multiple != pytest.approx(buggy_multiple)


def test_fade_exit_multiple_rejects_non_positive_denominator() -> None:
    with pytest.raises(ValueError):
        vm.fade_exit_multiple(enterprise_value=100.0, nopat_same_period=0.0)
    with pytest.raises(ValueError):
        vm.fade_exit_multiple(enterprise_value=100.0, nopat_same_period=-5.0)


def test_fade_exit_multiple_signature_has_no_dependency_on_margin_path() -> None:
    """文件層防呆：函式簽名本身就不接受 nopat_margin_path，杜絕誤用路徑首年利潤率。"""
    params = set(inspect.signature(vm.fade_exit_multiple).parameters)
    assert params == {"enterprise_value", "nopat_same_period"}


# ============================================================
# 通用反解器：solve_scalar_parameter
# ============================================================


def test_solve_scalar_parameter_unique_root_matches_analytic_solution() -> None:
    """單調線性函式：取樣網格上只有一個候選根，且與解析解一致（不是邊界值或取樣點）。"""
    result = vm.solve_scalar_parameter(lambda x: 2 * x - 7, lo=0.0, hi=10.0)
    assert result.status == "single_candidate"
    assert result.value == pytest.approx(3.5, abs=1e-6)
    assert result.residual == pytest.approx(0.0, abs=1e-6)
    assert result.samples_used == 33  # 預設 samples，揭露取樣密度


def test_solve_scalar_parameter_multiple_roots_are_not_collapsed_to_first_root() -> None:
    """f(x) = (x-2)(x-5) 在 [0,10] 有兩個根：必須都列出，不得只回傳第一個或邊界。"""
    result = vm.solve_scalar_parameter(lambda x: (x - 2) * (x - 5), lo=0.0, hi=10.0)
    assert result.status == "multiple_candidates"
    assert result.value is None
    assert sorted(result.candidates) == pytest.approx([2.0, 5.0], abs=1e-6)


def test_solve_scalar_parameter_no_solution_in_range_is_explicit() -> None:
    """f(x) 在整個範圍內同號：必須回傳明確的「取樣網格上無候選根」狀態，不是邊界值。"""
    result = vm.solve_scalar_parameter(lambda x: x + 100, lo=0.0, hi=10.0)
    assert result.status == "no_candidate_in_range"
    assert result.value is None
    assert result.candidates == ()


def test_solve_scalar_parameter_rejects_invalid_bounds() -> None:
    with pytest.raises(ValueError):
        vm.solve_scalar_parameter(lambda x: x, lo=5.0, hi=1.0)


# --- Codex adversarial review 發現的缺陷：只憑「有變號區間」就判定 single_candidate，
# --- 沒有驗證殘差，也沒有偵測 max_iter 耗盡。以下對照兩個實測可重現案例。


def test_solve_scalar_parameter_rejects_discontinuous_jump_as_unconverged() -> None:
    """跳躍不連續函式：有變號但根本沒有真正的根，不得回報 single_candidate 假解。

    `f` 在 x=0.123 處從 -1 跳到 +1，中間沒有連續穿越 0；二分法的區間寬度
    會收斂到 tol 內，但代入收斂點的殘差恆為 ±1，遠超過殘差容差，必須被
    拒絕，回報明確的「未收斂／不連續」狀態，而不是拿邊界值冒充答案。
    """

    def f(x: float) -> float:
        return -1.0 if x < 0.123 else 1.0

    result = vm.solve_scalar_parameter(f, lo=0.0, hi=1.0)
    assert result.status == "unconverged"
    assert result.value is None
    assert result.residual is not None
    assert abs(result.residual) >= 1.0
    assert result.candidates == ()
    assert result.bounds == (0.0, 1.0)
    assert result.unresolved_intervals >= 1


def test_solve_scalar_parameter_rejects_result_when_max_iter_exhausted() -> None:
    """max_iter 耗盡、區間根本沒收斂到 tol 內時，不得回報 single_candidate。"""
    result = vm.solve_scalar_parameter(
        lambda x: x - 0.3333333, lo=0.0, hi=1.0, max_iter=1, tol=1e-12
    )
    assert result.status == "unconverged"
    assert result.status != "single_candidate"
    assert result.value is None
    assert result.unresolved_intervals >= 1


def test_solve_scalar_parameter_unique_root_has_tiny_verified_residual() -> None:
    """正常單根（三次函式，root=0.42）：仍是 single_candidate，且殘差真的接近 0。"""
    result = vm.solve_scalar_parameter(lambda x: (x - 0.42) ** 3, lo=0.0, hi=1.0)
    assert result.status == "single_candidate"
    assert result.value == pytest.approx(0.42, abs=1e-6)
    assert result.residual is not None
    assert abs(result.residual) < 1e-6
    assert result.unresolved_intervals == 0


def test_solve_scalar_parameter_multiple_roots_still_detected_after_fix() -> None:
    """既有多根行為維持不變：兩根都列出，不因新增殘差檢驗而漏掉。"""
    result = vm.solve_scalar_parameter(lambda x: (x - 2) * (x - 5), lo=0.0, hi=10.0)
    assert result.status == "multiple_candidates"
    assert result.value is None
    assert sorted(result.candidates) == pytest.approx([2.0, 5.0], abs=1e-6)


def test_solve_scalar_parameter_no_solution_in_range_still_detected_after_fix() -> None:
    """既有無變號區間行為維持不變：完全同號一律是 no_candidate_in_range，不是 unconverged。"""
    result = vm.solve_scalar_parameter(lambda x: x + 100, lo=0.0, hi=10.0)
    assert result.status == "no_candidate_in_range"
    assert result.value is None
    assert result.candidates == ()


def test_solve_scalar_parameter_residual_tol_controls_acceptance() -> None:
    """residual_tol 是獨立於 tol（區間寬度）的參數：放寬它能讓原本被拒絕的候選根過關。"""

    def f(x: float) -> float:
        return -2e-6 if x < 0.5 else 3e-6

    default_result = vm.solve_scalar_parameter(f, lo=0.0, hi=1.0)
    assert default_result.status == "unconverged"

    loose_result = vm.solve_scalar_parameter(f, lo=0.0, hi=1.0, residual_tol=5e-6)
    assert loose_result.status == "single_candidate"
    assert loose_result.value == pytest.approx(0.5, abs=1e-6)


def test_solve_scalar_parameter_residual_tol_default_is_documented_1e_minus_6() -> None:
    sig = inspect.signature(vm.solve_scalar_parameter)
    assert sig.parameters["residual_tol"].default == pytest.approx(1e-6)


# --- 第二輪 Codex review 發現的缺陷：驗證通過的根只有一個時就回報
# --- single_candidate（舊名 unique），沒有另外統計「有幾個變號區間驗證
# --- 失敗」。兩個根都是真根，但其中一個因為函式在該處斜率極陡，二分法
# --- 收斂後殘差仍超過 residual_tol 而被丟棄，此時不得宣稱「單一候選」
# --- ——必須讓呼叫端知道還有一段沒解出來。


_STEEP_THRESHOLD = 5.0
_STEEP_SLOPE = -1e8


def _one_shallow_one_steep_root(x: float) -> float:
    """兩段連續（無額外跳躍）的分段線性函式，恰有兩個真根：

    - `x <= 5.0`：`f(x) = x - 2.0`，根在 `x=2`，斜率 1，容易收斂到極小殘差。
    - `x > 5.0`：延續同一個函數值在 `x=5.0` 處的連續銜接
      （`f(5.0)=3`），改用斜率 `-1e8` 的陡峭直線，根在
      `x ≈ 5.00000003`，收斂到 `tol` 內的區間寬度後，殘差仍可能是
      `|斜率| × 殘留區間寬度 ≈ 1e8 × 1e-10 ≈ 5e-3`，遠超過預設
      `residual_tol=1e-6`。

    刻意在分段點 `x=5.0` 保持函數值連續（銜接處不製造第三個假跳躍），
    是為了讓測試只驗證「兩個真根、其中一個因陡峭而驗證失敗」這一件事；
    若像 Codex 原始重現那樣直接寫
    `(x-2.0) if x<5.0 else (x-8.0)*1e8`，分段點本身會多出一個與任何真根
    無關的真實跳躍不連續（`x=5.0` 左極限 ≈3、右值 ≈-3e8），使
    `unresolved_intervals` 變成 2 而非 1——那不是缺陷，是同一顆函式裡
    真的多藏了一段無解區間，但會讓這個測試想驗證的重點被稀釋。
    """
    if x <= _STEEP_THRESHOLD:
        return x - 2.0
    return (_STEEP_THRESHOLD - 2.0) + _STEEP_SLOPE * (x - _STEEP_THRESHOLD)


def test_solve_scalar_parameter_reports_unconverged_when_one_root_fails_residual_check() -> None:
    """一個區間驗證通過、另一個驗證失敗：不得回報 single_candidate，必須是 unconverged。"""
    result = vm.solve_scalar_parameter(_one_shallow_one_steep_root, lo=0.0, hi=10.0)
    assert result.status == "unconverged"
    assert result.value is None
    assert result.unresolved_intervals == 1
    # 已驗證通過的根（x=2）仍應揭露在 candidates 供呼叫端參考，不是整個丟棄。
    assert len(result.candidates) == 1
    assert result.candidates[0] == pytest.approx(2.0, abs=1e-6)


def test_solve_scalar_parameter_loosened_residual_tol_recovers_both_roots_as_multiple() -> None:
    """把 residual_tol 放寬到足以接受陡根：兩個變號區間都驗證通過，狀態變成 multiple_candidates。"""
    result = vm.solve_scalar_parameter(
        _one_shallow_one_steep_root, lo=0.0, hi=10.0, residual_tol=0.1
    )
    assert result.status == "multiple_candidates"
    assert result.unresolved_intervals == 0
    assert sorted(result.candidates) == pytest.approx([2.0, 5.00000003], abs=1e-6)


def test_solve_scalar_parameter_unresolved_intervals_field_exists_and_defaults_to_zero_when_clean() -> None:
    """單一真根、無其他變號區間：unresolved_intervals 必須是 0，不是預設隨便一個非零值。"""
    result = vm.solve_scalar_parameter(lambda x: 3 * x - 1, lo=0.0, hi=1.0)
    assert result.status == "single_candidate"
    assert result.unresolved_intervals == 0


def test_solve_scalar_parameter_never_reports_unique_when_any_bracket_is_unresolved() -> None:
    """對照 Codex 原始重現案例（含分段點本身的額外跳躍）：不論未解區間有幾段，
    只要 > 0，就不得回報 single_candidate；且回傳的 unresolved_intervals 必須反映真實數量。
    """

    def f(x: float) -> float:
        return (x - 2.0) if x < 5.0 else (x - 8.0) * 1e8

    result = vm.solve_scalar_parameter(f, lo=0.0, hi=10.0)
    assert result.status != "single_candidate"
    assert result.status == "unconverged"
    assert result.value is None
    assert result.unresolved_intervals >= 1


# --- Reverse round-trip：跑在 fade 引擎上（§12.5 数值验收精神） ---

_RT_G1_TRUE = 0.18
_RT_G_TERM = 0.05
_RT_N = 5
_RT_MARGINS = [0.25, 0.24, 0.23, 0.22, 0.21]
_RT_K = 2.0
_RT_WACC = 0.10
_RT_EV_TRUE = 2.7143297603348433


def _fade_ev_for_g1(g1: float) -> float:
    growth_rates = vm.growth_path(g1=g1, g_terminal=_RT_G_TERM, n=_RT_N)
    return vm.fade_enterprise_value(
        growth_rates=growth_rates,
        nopat_margin_path=_RT_MARGINS,
        k=_RT_K,
        wacc=_RT_WACC,
    ).enterprise_value


def test_fade_engine_reverse_round_trip_recovers_g1_within_tolerance() -> None:
    """正算 EV 後固定其餘輸入反解 g1，重建 EV 誤差 <= 0.01 元或相對 1e-6（取較寬者）。"""
    target_ev = _fade_ev_for_g1(_RT_G1_TRUE)
    assert target_ev == pytest.approx(_RT_EV_TRUE, rel=1e-9)

    result = vm.solve_scalar_parameter(
        lambda g1: _fade_ev_for_g1(g1) - target_ev, lo=0.0, hi=0.40
    )
    assert result.status == "single_candidate"
    assert result.unresolved_intervals == 0
    assert result.value is not None

    rebuilt_ev = _fade_ev_for_g1(result.value)
    tolerance = max(0.01, abs(target_ev) * 1e-6)
    assert abs(rebuilt_ev - target_ev) <= tolerance
    # g1 本身也應該被準確重建（同一單調函式下反解應收斂到原值附近）。
    assert result.value == pytest.approx(_RT_G1_TRUE, abs=1e-4)


def test_fade_engine_reverse_round_trip_reports_no_solution_when_target_out_of_range() -> None:
    """目標 EV 超出搜尋範圍內可達成的區間：必須回傳「範圍內無解」，不得用邊界值充數。"""
    unreachable_target = 100.0  # 遠超過 g1 in [0, 0.40] 可達到的 EV 上限
    result = vm.solve_scalar_parameter(
        lambda g1: _fade_ev_for_g1(g1) - unreachable_target, lo=0.0, hi=0.40
    )
    assert result.status == "no_candidate_in_range"
    assert result.value is None


# ============================================================
# v1.3.1：第三輪 Codex review 發現的缺陷一——狀態名稱宣稱得比方法能證明的多
#
# 純變號偵測看不到偶重根（觸底但不變號），也可能把兩個相距極近的單根
# 漏掉其中一個，卻仍用 "unique"／"no_solution_in_range" 這種強斷言字眼。
# 以下三個案例皆為實測可重現的盲點，對應修法：(a) 狀態改名為只宣稱
# 「取樣網格上找到的證據」；(b) 新增 |f| 局部極小偵測補足偶重根盲點。
# ============================================================


def test_solve_scalar_parameter_finds_even_multiplicity_root_via_local_minimum() -> None:
    """`(x-0.42)**2` 在 x=0.42 觸底但不變號：純變號偵測會誤報無解，
    新增的局部極小偵測必須能找到它，狀態誠實回報為 single_candidate
    （不是宣稱唯一，只是這個網格上只找到一個候選）。
    """
    result = vm.solve_scalar_parameter(lambda x: (x - 0.42) ** 2, lo=0.0, hi=1.0)
    assert result.status == "single_candidate"
    assert result.value == pytest.approx(0.42, abs=1e-6)
    assert result.residual is not None
    assert abs(result.residual) < 1e-6
    assert result.unresolved_intervals == 0
    assert result.samples_used == 33


def test_solve_scalar_parameter_finds_both_even_and_simple_root() -> None:
    """`(x-0.42)**2*(x-0.75)`：0.75 是一般變號根，0.42 是偶重根，兩者都
    必須進入 candidates，狀態是 multiple_candidates，不得漏掉偶重根、
    誤報只有 0.75 一個唯一解。
    """
    result = vm.solve_scalar_parameter(
        lambda x: (x - 0.42) ** 2 * (x - 0.75), lo=0.0, hi=1.0
    )
    assert result.status == "multiple_candidates"
    assert result.value is None
    assert result.unresolved_intervals == 0
    assert sorted(result.candidates) == pytest.approx([0.42, 0.75], abs=1e-6)


def test_solve_scalar_parameter_close_roots_in_same_sampling_cell_best_effort_recovery() -> None:
    """`(x-0.500)*(x-0.505)`：兩個單根相距僅 0.005，在預設 samples=33
    （網格寬約 0.03125）下落在同一取樣格內，純變號偵測只會找到 x=0.500
    （恰好落在取樣點上，觸發既有變號分支），漏掉 x=0.505（對照舊版
    bug 重現：`status="unique"`、`candidates=(0.5,)`）。

    加了局部極小偵測後，這個特定案例其實兩根都被找到了：x=0.500 仍由
    既有變號分支（取樣點恰好對到根）找到；x=0.505 則是黃金分割搜尋在
    以 x=0.500 為中心展開的搜尋區間內，因為 x=0.505 在該區間內更靠近
    中心、|f| 在其附近更小，搜尋被拉向 0.505 而非 0.500 收斂到的結果。
    這是「盡力而為」機制在此組態下剛好成功的例子，**不是**保證——換一組
    根距、換一組取樣起點，仍可能像 `_minimize_abs_f` docstring 描述的
    那樣只找到其中一個。因此狀態仍必須誠實回報為 multiple_candidates，
    不是 single_candidate 冒充唯一解。
    """
    result = vm.solve_scalar_parameter(
        lambda x: (x - 0.500) * (x - 0.505), lo=0.0, hi=1.0
    )
    assert result.status == "multiple_candidates"
    assert result.value is None
    assert result.unresolved_intervals == 0
    assert sorted(result.candidates) == pytest.approx([0.500, 0.505], abs=1e-6)


def test_solve_scalar_parameter_local_minimum_that_is_truly_positive_is_rejected() -> None:
    """`|f|` 的局部極小值本身就明顯 > residual_tol：代表那裡真的沒有根，
    不得被局部極小偵測誤判成候選根。
    """
    result = vm.solve_scalar_parameter(lambda x: (x - 0.5) ** 2 + 1.0, lo=0.0, hi=1.0)
    assert result.status == "no_candidate_in_range"
    assert result.value is None
    assert result.candidates == ()


# ============================================================
# v1.3.1：第三輪 Codex review 發現的缺陷二——NaN／inf 無聲穿過公開函式
#
# NaN 與任何數字比較（含 <=）恆為 False，既有的邊界檢查攔不住 NaN；
# 每個公開函式都必須在輸入非有限、或運算結果溢位為非有限時明確拒絕。
# ============================================================

_NAN = float("nan")
_INF = float("inf")


def test_cost_of_equity_rejects_nan_and_inf_inputs() -> None:
    with pytest.raises(ValueError):
        vm.cost_of_equity(rf=_NAN, beta=1.1, erp=0.06)
    with pytest.raises(ValueError):
        vm.cost_of_equity(rf=0.02, beta=_INF, erp=0.06)


def test_wacc_rejects_nan_inputs() -> None:
    with pytest.raises(ValueError):
        vm.wacc(ke=_NAN, kd=0.05, equity_value=80, debt_value=20, tax_rate=0.20)
    with pytest.raises(ValueError):
        vm.wacc(ke=0.10, kd=0.05, equity_value=80, debt_value=20, tax_rate=_NAN)


def test_wacc_rejects_inputs_that_overflow_to_infinite_result() -> None:
    """輸入本身有限，但運算結果溢位為 inf：一樣必須拒絕，不得無聲輸出 inf。

    `kd=1e308` 與 `tax_rate=-1e308` 皆是合法的有限浮點數，但
    `kd * (1 - tax_rate)` 約為 `1e308 * 1e308 = 1e616`，遠超過
    float64 上限（約 1.8e308），會溢位成 `inf`。
    """
    with pytest.raises(ValueError):
        vm.wacc(ke=0.05, kd=1e308, equity_value=90, debt_value=10, tax_rate=-1e308)


def test_equity_bridge_rejects_nan_inputs() -> None:
    """對照 Codex 原始重現：equity_bridge(100, 0, 0, NaN, 0, 10) 曾無聲回傳 (nan, nan)。"""
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=100,
            excess_cash=0,
            non_operating_assets=0,
            debt=_NAN,
            other_claims=0,
            shares=10,
        )
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=1000,
            excess_cash=0,
            non_operating_assets=0,
            debt=0,
            other_claims=0,
            shares=_NAN,
        )


def test_equity_bridge_rejects_inf_inputs() -> None:
    with pytest.raises(ValueError):
        vm.equity_bridge(
            ev_operating=_INF,
            excess_cash=0,
            non_operating_assets=0,
            debt=0,
            other_claims=0,
            shares=10,
        )


def test_growth_path_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.growth_path(g1=_NAN, g_terminal=0.03, n=3)
    with pytest.raises(ValueError):
        vm.growth_path(g1=0.20, g_terminal=_INF, n=3)


def test_reinvestment_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.reinvestment(revenue_prev=_NAN, growth=0.10, k=2)
    with pytest.raises(ValueError):
        vm.reinvestment(revenue_prev=100, growth=_INF, k=2)


def test_fcff_full_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.fcff_full(nopat=_NAN, dep_amort=20, capex=35, delta_nwc=5)
    with pytest.raises(ValueError):
        vm.fcff_full(nopat=100, dep_amort=20, capex=_INF, delta_nwc=5)


def test_fcff_simplified_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.fcff_simplified(nopat=_NAN, reinvestment=25)
    with pytest.raises(ValueError):
        vm.fcff_simplified(nopat=_INF, reinvestment=25)


def test_terminal_value_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.terminal_value(cf_next=_NAN, discount_rate=0.10, g_perpetual=0.03)
    with pytest.raises(ValueError):
        vm.terminal_value(cf_next=100, discount_rate=_INF, g_perpetual=0.03)


def test_scenario_return_rejects_nan_and_inf_inputs() -> None:
    """對照 Codex 原始重現：scenario_return 系列曾無聲回傳 nan。"""
    with pytest.raises(ValueError):
        vm.scenario_return(p_end=70, dividend=2, p_entry=100, cost=_NAN)
    with pytest.raises(ValueError):
        vm.scenario_return(p_end=_INF, dividend=2, p_entry=100, cost=1)


def test_price_return_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.price_return(p_end=_NAN, p_entry=100)
    with pytest.raises(ValueError):
        vm.price_return(p_end=_INF, p_entry=100)


def test_annualized_return_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.annualized_return(total_return=_NAN, years=2)
    with pytest.raises(ValueError):
        vm.annualized_return(total_return=0.21, years=_INF)


def test_reward_risk_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.reward_risk(p_upside=_NAN, p_entry=100, p_downside=70)
    with pytest.raises(ValueError):
        vm.reward_risk(p_upside=150, p_entry=100, p_downside=_INF)


def test_expected_value_rejects_nan_in_probabilities_or_values() -> None:
    with pytest.raises(ValueError):
        vm.expected_value(probabilities=[_NAN, 0.5, 0.5], values=[1, 2, 3])
    with pytest.raises(ValueError):
        vm.expected_value(probabilities=[0.25, 0.5, 0.25], values=[1, _INF, 3])


def test_breakeven_probability_binary_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.breakeven_probability_binary(gain=_NAN, loss=0.10, cost=0.01)
    with pytest.raises(ValueError):
        vm.breakeven_probability_binary(gain=_INF, loss=0.10, cost=0.01)


def test_breakeven_bear_probability_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.breakeven_bear_probability(r_bear=_NAN, r_base=0.05, r_bull=0.1, p_base=0.5)
    with pytest.raises(ValueError):
        vm.breakeven_bear_probability(r_bear=-0.2, r_base=0.1, r_bull=_INF, p_base=0.5)


def test_fade_enterprise_value_rejects_nan_in_growth_rates_or_margins() -> None:
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[_NAN, 0.05], nopat_margin_path=[0.2, 0.2], k=1.0, wacc=0.10
        )
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.1, 0.05], nopat_margin_path=[0.2, _INF], k=1.0, wacc=0.10
        )
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.1, 0.05], nopat_margin_path=[0.2, 0.2], k=_NAN, wacc=0.10
        )
    with pytest.raises(ValueError):
        vm.fade_enterprise_value(
            growth_rates=[0.1, 0.05], nopat_margin_path=[0.2, 0.2], k=1.0, wacc=_NAN
        )


def test_fade_exit_multiple_rejects_nan_and_inf() -> None:
    with pytest.raises(ValueError):
        vm.fade_exit_multiple(enterprise_value=_NAN, nopat_same_period=0.30)
    with pytest.raises(ValueError):
        vm.fade_exit_multiple(enterprise_value=_INF, nopat_same_period=0.30)


def test_solve_scalar_parameter_rejects_nan_and_inf_bounds() -> None:
    with pytest.raises(ValueError):
        vm.solve_scalar_parameter(lambda x: x, lo=_NAN, hi=1.0)
    with pytest.raises(ValueError):
        vm.solve_scalar_parameter(lambda x: x, lo=0.0, hi=_INF)
