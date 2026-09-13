"""估值數值核心模組。

對應 `docs/v1.3.0-spec.md` 第 4、5 節（COR-01～03）與第 12 節（FR-15～17）。
純函式集合，不建 class、不建 framework，只用標準函式庫（`math`）。每個函式
只做一件事；輸入或結果落在數學定義域外時，一律明確拒絕（`raise ValueError`）
或回傳明確的「不適用」哨兵（如 `None`），不得無聲輸出 `inf`／`NaN`／複數。

單位與口徑慣例：
- 折現率、成長率、機率一律以小數表示（10% 寫成 `0.10`），不是百分比整數。
- 價格、金額欄位不預設幣別；呼叫端自行維持幣別、名目／實質與期限一致
  （COR-01）。
- 價格類參數一律使用語意明確的名稱（`p_entry`／`p_end`／`p_upside`／
  `p_downside`），刻意不使用泛用的 `price`，避免報告與部位模組欄位互換
  （見 spec §9.2 最後一列）；此為文件層約束，Python 型別系統不強制檢查。
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

__all__ = [
    "FadeResult",
    "FadeYearDetail",
    "ParameterSolveResult",
    "annualized_return",
    "breakeven_bear_probability",
    "breakeven_probability_binary",
    "cost_of_equity",
    "equity_bridge",
    "expected_value",
    "fade_enterprise_value",
    "fade_exit_multiple",
    "fcff_full",
    "fcff_simplified",
    "growth_path",
    "price_return",
    "reinvestment",
    "reward_risk",
    "scenario_return",
    "solve_scalar_parameter",
    "terminal_value",
    "wacc",
]


def _require_finite(name: str, value: float) -> float:
    """輸入或輸出必須是有限實數（模組內部使用，NaN／inf 靜默穿透防呆）。

    `NaN` 與任何數字比較（含 `<=`、`<`）恆為 `False`，本模組既有的邊界
    檢查（如 `shares <= 0`）無法攔住 `NaN`；`inf` 也會使後續四則運算悄悄
    產生看似合理但錯誤的結果。因此每個公開函式在使用參數前、回傳結果前，
    都必須呼叫本函式明確擋下 `NaN`／`inf`，不得讓資料源缺漏（以 `NaN`
    表示）無聲流入估值與報告。

    參數：
        name: 參數或回傳值名稱，用於錯誤訊息定位。
        value: 待檢查的數值。

    回傳：`value` 本身（未變動），方便在運算式中內嵌呼叫。

    Raises:
        ValueError: `value` 非有限（`NaN` 或 `inf`）。
    """
    if not math.isfinite(value):
        raise ValueError(f"{name} 必須是有限數（非 NaN／inf），收到 {value!r}")
    return value


def cost_of_equity(rf: float, beta: float, erp: float) -> float:
    """股權成本 `k_e = r_f + beta_L * ERP`（COR-01）。

    參數：
        rf: 無風險利率（小數）。
        beta: 槓桿後股票 beta。
        erp: 股權風險溢酬（小數）。

    回傳：股權成本（小數）。這是股權投資人要求的報酬率，**不是** WACC；
    只有在全股權融資等特定假設下才會等於 WACC（COR-01）。

    Raises:
        ValueError: 任一輸入或回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("rf", rf)
    _require_finite("beta", beta)
    _require_finite("erp", erp)
    return _require_finite("cost_of_equity 回傳值", rf + beta * erp)


def wacc(ke: float, kd: float, equity_value: float, debt_value: float, tax_rate: float) -> float:
    """加權平均資金成本（COR-01）。

    `WACC = E/(D+E) * ke + D/(D+E) * kd * (1 - T)`，用市場或目標資本結構權重。
    FCFF 須配 WACC 折現得到營運企業價值；FCFE／股利／剩餘利益須配 `ke`
    （股權成本），不得混用。

    參數：
        ke: 股權成本（小數）。
        kd: 稅前債務成本（小數）。
        equity_value: 股權市值（或目標權重用的股權價值），須 >= 0。
        debt_value: 債務市值（或目標權重用的債務價值），須 >= 0。
        tax_rate: 邊際稅率（小數），用於債務稅盾。

    回傳：WACC（小數）。

    Raises:
        ValueError: `equity_value` 或 `debt_value` 為負，或兩者相加 <= 0
            （資本結構未定義，折現率配對無意義），或任一輸入／回傳值
            非有限（`NaN`／`inf`）。
    """
    _require_finite("ke", ke)
    _require_finite("kd", kd)
    _require_finite("equity_value", equity_value)
    _require_finite("debt_value", debt_value)
    _require_finite("tax_rate", tax_rate)
    if equity_value < 0 or debt_value < 0:
        raise ValueError("股權價值與債務價值不得為負")
    total = equity_value + debt_value
    if total <= 0:
        raise ValueError("股權加債務價值必須 > 0，否則資本權重未定義")
    weight_equity = equity_value / total
    weight_debt = debt_value / total
    result = weight_equity * ke + weight_debt * kd * (1 - tax_rate)
    return _require_finite("wacc 回傳值", result)


def equity_bridge(
    ev_operating: float,
    excess_cash: float,
    non_operating_assets: float,
    debt: float,
    other_claims: float,
    shares: float,
) -> tuple[float, float]:
    """企業價值橋接到每股股權價值（COR-02）。

    `Equity_0 = EV_operating,0 + ExcessCash_0 + NonOperatingAssets_0 - Debt_0
    - OtherClaims_0`，`V_0 = Equity_0 / Shares_0`。

    呼叫端須自行確認每一加減項是否已計入營運現金流內（租賃、少數股權、
    JV、SBC、可轉債口徑一致），本函式不做該層驗證。

    參數：
        ev_operating: 營運企業價值（折現模型算出的 EV，不含超額現金等）。
        excess_cash: 超額現金與約當現金。
        non_operating_assets: 非營運資產（如可供出售投資、閒置土地）。
        debt: 有息負債（含租賃負債，依口徑）。
        other_claims: 其他請求權（少數股權、優先股等，未併入 debt 者）。
        shares: 流通在外股數，須 > 0。

    回傳：`(equity_value, per_share)`。

    Raises:
        ValueError: `shares <= 0`（除以零或股數無意義），或算出的股權
            價值 `<= 0`（結果域邊界：負股權或零股權不得無聲通過，此處
            選擇明確拒絕，呼叫端須重新檢視輸入或改用其他方法標記狀態），
            或任一輸入／回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("ev_operating", ev_operating)
    _require_finite("excess_cash", excess_cash)
    _require_finite("non_operating_assets", non_operating_assets)
    _require_finite("debt", debt)
    _require_finite("other_claims", other_claims)
    _require_finite("shares", shares)
    if shares <= 0:
        raise ValueError("股數必須 > 0")
    equity_value = ev_operating + excess_cash + non_operating_assets - debt - other_claims
    if equity_value <= 0:
        raise ValueError(
            f"股權價值 {equity_value} <= 0：模型隱含股權無價值或資不抵債，"
            "不得無聲輸出每股價值，須另行以明確狀態標記後再決策"
        )
    per_share = equity_value / shares
    _require_finite("equity_value 回傳值", equity_value)
    _require_finite("per_share 回傳值", per_share)
    return equity_value, per_share


def growth_path(g1: float, g_terminal: float, n: int) -> list[float]:
    """線性成長率序列（COR-03）。

    第一個元素恆等於 `g1`，最後一個元素恆等於 `g_terminal`，中間線性內插。

    `n == 1` 的行為：本模組選擇 **拒絕**（`raise ValueError`），而不是
    默默回傳 `[g1]`。理由：單一元素序列無法同時滿足「第一個等於 g1」與
    「最後一個等於 g_terminal」兩個不變式（除非 `g1 == g_terminal`），
    為避免呼叫端誤用悄悄違反不變式，一律拒絕；只需要單一年度成長率的
    呼叫端應直接使用 `g1`，不透過本函式。

    參數：
        g1: 第一年成長率（小數）。
        g_terminal: 終端（最後一年）成長率（小數）。
        n: 序列長度（預測年數），須 >= 2。

    回傳：長度為 `n` 的成長率序列。

    Raises:
        ValueError: `n < 1`，或 `n == 1`（見上述說明），或 `g1`／
            `g_terminal` 非有限（`NaN`／`inf`）。
    """
    _require_finite("g1", g1)
    _require_finite("g_terminal", g_terminal)
    if n < 1:
        raise ValueError("序列長度 n 必須 >= 1")
    if n == 1:
        raise ValueError(
            "n == 1 時無法同時滿足首尾不變式，本函式拒絕計算；"
            "只需要單一年度成長率請直接使用 g1"
        )
    step = (g_terminal - g1) / (n - 1)
    path = [g1 + step * i for i in range(n)]
    for idx, value in enumerate(path):
        _require_finite(f"growth_path 回傳值[{idx}]", value)
    return path


def reinvestment(revenue_prev: float, growth: float, k: float) -> float:
    """再投資金額（COR-03）：`Reinvestment_t = k * (Revenue_t - Revenue_(t-1))`。

    `k` 定義為每增加一元營收所需的新增資本。**不得**用成長率當分母，也
    不得以 `k * growth * revenue_prev` 之類公式混淆；本函式先算出當期
    營收，再取營收差額乘以 `k`。

    參數：
        revenue_prev: 前期營收。
        growth: 當期營收成長率（小數）。
        k: 資本強度（每增一元營收所需資本）。

    回傳：當期再投資金額。`k == 0` 或 `revenue_prev == 0` 時公式本身是
    乘法，回傳 `0.0`，不會除以零。

    Raises:
        ValueError: 任一輸入或回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("revenue_prev", revenue_prev)
    _require_finite("growth", growth)
    _require_finite("k", k)
    revenue_current = revenue_prev * (1 + growth)
    result = k * (revenue_current - revenue_prev)
    return _require_finite("reinvestment 回傳值", result)


def fcff_full(nopat: float, dep_amort: float, capex: float, delta_nwc: float) -> float:
    """完整式 FCFF（COR-03）：`FCFF_t = NOPAT_t + D&A_t - Capex_t - dNWC_t`。

    這是預設應使用的完整自由現金流公式。**不得**與 `fcff_simplified`
    混用——若已用 `fcff_simplified` 的再投資總額扣過 capex／營運資金，
    不能在這裡再扣一次。

    參數：
        nopat: 稅後淨營業利益。
        dep_amort: 折舊攤銷（加回項）。
        capex: 資本支出。
        delta_nwc: 營運資金變動。

    回傳：FCFF。

    Raises:
        ValueError: 任一輸入或回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("nopat", nopat)
    _require_finite("dep_amort", dep_amort)
    _require_finite("capex", capex)
    _require_finite("delta_nwc", delta_nwc)
    return _require_finite("fcff_full 回傳值", nopat + dep_amort - capex - delta_nwc)


def fcff_simplified(nopat: float, reinvestment: float) -> float:
    """簡化式 FCFF（COR-03）：`FCFF_t = NOPAT_t - Reinvestment_t`。

    `reinvestment` 須是涵蓋淨資本支出與營運資金變動的總再投資金額
    （例如 `reinvestment()` 函式的輸出）。**不得**再額外扣一次已含於
    再投資的 capex 或營運資金變動——那會與 `fcff_full` 混用，重複扣減。

    參數：
        nopat: 稅後淨營業利益。
        reinvestment: 總再投資金額。

    回傳：FCFF。

    Raises:
        ValueError: 任一輸入或回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("nopat", nopat)
    _require_finite("reinvestment", reinvestment)
    return _require_finite("fcff_simplified 回傳值", nopat - reinvestment)


def terminal_value(cf_next: float, discount_rate: float, g_perpetual: float) -> float:
    """終值（COR-03）：`TV = CF_(t+1) / (r - g)`。

    折現率必須嚴格大於永續成長率；相等或更小時終值在數學上發散或為負，
    必須拒絕計算，不得輸出任何有限數字當作「合理價」。

    參數：
        cf_next: 終值起算下一期現金流（與 `discount_rate` 期別一致）。
        discount_rate: 折現率（小數），FCFF 對應 WACC，FCFE 對應 ke。
        g_perpetual: 永續成長率（小數）。

    回傳：終值。

    Raises:
        ValueError: `discount_rate <= g_perpetual`，或任一輸入／回傳值
            非有限（`NaN`／`inf`）。
    """
    _require_finite("cf_next", cf_next)
    _require_finite("discount_rate", discount_rate)
    _require_finite("g_perpetual", g_perpetual)
    if discount_rate <= g_perpetual:
        raise ValueError(
            "折現率必須大於永續成長率，否則終值無限大或為負，拒絕計算"
        )
    return _require_finite("terminal_value 回傳值", cf_next / (discount_rate - g_perpetual))


def scenario_return(p_end: float, dividend: float, p_entry: float, cost: float) -> float:
    """簡化買入並持有、股利不再投資模型的情境報酬（FR-07 `R_H,i`）。

    `R_H,i = (P_H,i + D_H,i - P_0 - C_H,i) / P_0`。股利與成本（含適用
    稅負）不得重複扣除；涉及中途加減碼或股利再投資時，須改用明確現金
    流計算，不適用本函式。

    參數：
        p_end: 持有期末價格。
        dividend: 持有期間每股股利。
        p_entry: 進場價格，須 > 0。
        cost: 每股成本與適用稅負。

    回傳：情境總報酬（小數），可低於 -100%（成本可使損失超過本金）。

    Raises:
        ValueError: `p_entry <= 0`，或任一輸入／回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("p_end", p_end)
    _require_finite("dividend", dividend)
    _require_finite("p_entry", p_entry)
    _require_finite("cost", cost)
    if p_entry <= 0:
        raise ValueError("進場價必須 > 0")
    result = (p_end + dividend - p_entry - cost) / p_entry
    return _require_finite("scenario_return 回傳值", result)


def price_return(p_end: float, p_entry: float) -> float:
    """價差報酬（FR-15 `r_i^price`）：`P_H,i / P_0 - 1`，不含股利與成本。

    參數：
        p_end: 持有期末價格。
        p_entry: 進場價格，須 > 0。

    回傳：價差報酬（小數）。這是「期望價差報酬」，不是成本後總報酬，
    不得直接稱為 `R_H,i`。

    Raises:
        ValueError: `p_entry <= 0`，或任一輸入／回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("p_end", p_end)
    _require_finite("p_entry", p_entry)
    if p_entry <= 0:
        raise ValueError("進場價必須 > 0")
    return _require_finite("price_return 回傳值", p_end / p_entry - 1.0)


def annualized_return(total_return: float, years: float) -> float:
    """將持有期總報酬換算為等效年化報酬：`(1 + total)^(1/years) - 1`。

    `total_return <= -100%` 時 `1 + total_return <= 0`，對非整數次方根
    在實數域無定義（Python 會算出複數），必須明確拒絕，不得讓呼叫端在
    後續格式化字串時才因複數或 NaN 而崩潰。

    參數：
        total_return: 持有期總報酬（小數）。
        years: 持有期年數，須 > 0。

    回傳：年化報酬（小數）。

    Raises:
        ValueError: `years <= 0`，或 `1 + total_return <= 0`，或任一輸入／
            回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("total_return", total_return)
    _require_finite("years", years)
    if years <= 0:
        raise ValueError("年數必須 > 0")
    base = 1.0 + total_return
    if base <= 0:
        raise ValueError(
            "總報酬 <= -100%，年化報酬在實數域無定義（開次方根的底數非正）"
        )
    return _require_finite("annualized_return 回傳值", base ** (1.0 / years) - 1.0)


def reward_risk(p_upside: float, p_entry: float, p_downside: float) -> float | None:
    """報酬風險比（FR-15 R/R）：`(P_upside - P_entry) / (P_entry - P_downside)`。

    用於牛／熊或基準／熊等配對；數值越高代表每單位所列損失對應較多報酬。

    當下檔情境價格不低於進場價（`p_entry - p_downside <= 0`）時，分母
    不具「風險」意義，回傳 `None` 表示「不適用／未覆蓋下檔」，**不得**
    回傳 `inf` 或負值冒充 R/R（FR-15：無虧損分支時應標「未覆蓋下檔，
    R/R 無法據此評估」）。

    參數：
        p_upside: 上檔情境價格（如牛情境或基準情境）。
        p_entry: 進場價格。
        p_downside: 下檔情境價格（如熊情境）。

    回傳：R/R（正常情況），或 `None`（下檔情境不低於進場價時）。

    Raises:
        ValueError: 任一輸入或（非 `None` 時的）回傳值非有限（`NaN`／`inf`）。
    """
    _require_finite("p_upside", p_upside)
    _require_finite("p_entry", p_entry)
    _require_finite("p_downside", p_downside)
    denominator = p_entry - p_downside
    if denominator <= 0:
        return None
    return _require_finite("reward_risk 回傳值", (p_upside - p_entry) / denominator)


def expected_value(probabilities: list[float], values: list[float]) -> float:
    """機率加權期望值：`sum(p_i * v_i)`（FR-07 `E[V0]`／`E[R_H]`，FR-16）。

    機率必須非負、總和為 1（容差 `1e-9`，容忍浮點捨入），否則拒絕計算；
    不得默默正規化或忽略不合法的機率輸入。

    參數：
        probabilities: 各情境機率（小數），長度須與 `values` 一致且 >= 1。
        values: 各情境數值（報酬、股權價值等任意同單位數值）。

    回傳：機率加權期望值。

    Raises:
        ValueError: `probabilities` 或 `values` 為空、長度不一致、含負
            機率、機率總和偏離 1 超過 `1e-9`，或任一機率／數值／回傳值
            非有限（`NaN`／`inf`）。
    """
    probs = list(probabilities)
    vals = list(values)
    if len(probs) == 0 or len(vals) == 0:
        raise ValueError("機率與數值不得為空集合")
    if len(probs) != len(vals):
        raise ValueError("機率與數值長度必須一致")
    for idx, p in enumerate(probs):
        _require_finite(f"probabilities[{idx}]", p)
    for idx, v in enumerate(vals):
        _require_finite(f"values[{idx}]", v)
    if any(p < 0 for p in probs):
        raise ValueError("機率不得為負")
    total = math.fsum(probs)
    if not math.isclose(total, 1.0, abs_tol=1e-9):
        raise ValueError(f"機率總和必須為 1（容差 1e-9），目前為 {total}")
    result = math.fsum(p * v for p, v in zip(probs, vals, strict=True))
    return _require_finite("expected_value 回傳值", result)


def breakeven_probability_binary(gain: float, loss: float, cost: float) -> float:
    """二元結果損益兩平勝率（FR-16／12.2）：`(L + c) / (G + L)`。

    僅適用於確實只有贏／輸兩類結果的簡化模型；不得直接套用到包含基準、
    到期退出或其他分支的多情境模型（12.2）。

    參數：
        gain: 平均獲利率（小數，正值）。
        loss: 平均損失率（小數，正值，以正數表示幅度）。
        cost: 平均成本率（小數）。

    回傳：損益兩平勝率（小數）。**可能 > 1**，代表在此獲利／損失／成本
    組合下無法達成正期望；呼叫端須自行檢查回傳值是否 > 1 並據此判斷，
    本函式不做截斷。

    Raises:
        ValueError: `gain + loss <= 0`（分母無意義），或任一輸入／回傳值
            非有限（`NaN`／`inf`）。
    """
    _require_finite("gain", gain)
    _require_finite("loss", loss)
    _require_finite("cost", cost)
    denominator = gain + loss
    if denominator <= 0:
        raise ValueError("獲利與損失總和必須 > 0，損益兩平勝率未定義")
    return _require_finite("breakeven_probability_binary 回傳值", (loss + cost) / denominator)


def breakeven_bear_probability(
    r_bear: float, r_base: float, r_bull: float, p_base: float
) -> float:
    """固定基準機率下，反解使期望價差報酬為 0 的熊情境機率（12.2）。

    求解 `p_bear * r_bear + p_base * r_base + p_bull * r_bull = 0`，其中
    `p_bull = 1 - p_base - p_bear`。代入整理得：

    `p_bear = -(p_base * r_base + (1 - p_base) * r_bull) / (r_bear - r_bull)`

    這只是固定價格情境與固定基準機率下的數學邊界，不是估計出的實際
    勝率；回傳的 `p_bear`（與對應的 `p_bull = 1 - p_base - p_bear`）
    仍可能落在 `[0, 1]` 之外，呼叫端須自行檢查合理性。

    參數：
        r_bear: 熊情境報酬（小數）。
        r_base: 基準情境報酬（小數）。
        r_bull: 牛情境報酬（小數）。
        p_base: 固定的基準情境機率（小數），須介於 0 與 1 之間。

    回傳：使期望值為 0 的熊情境機率。

    Raises:
        ValueError: `p_base` 不在 `[0, 1]`，或 `r_bear == r_bull`（除以零，
            熊牛情境報酬相同時無法反解），或任一輸入／回傳值非有限
            （`NaN`／`inf`）。
    """
    _require_finite("r_bear", r_bear)
    _require_finite("r_base", r_base)
    _require_finite("r_bull", r_bull)
    _require_finite("p_base", p_base)
    if not 0.0 <= p_base <= 1.0:
        raise ValueError("基準機率必須介於 0 與 1 之間")
    denominator = r_bear - r_bull
    if denominator == 0:
        raise ValueError("熊與牛情境報酬相同，無法反解損益兩平機率")
    result = -(p_base * r_base + (1 - p_base) * r_bull) / denominator
    return _require_finite("breakeven_bear_probability 回傳值", result)


# ============================================================
# COR-03 fade 引擎修正版
#
# 對應 `references/valuation-paths.md` 第 4 節（4.1～4.6）。修正舊版
# `justified_multiple()` 的三個獨立錯誤：
#   1. 成長序列用 `i/N` 迴圈，第一筆就已經往終端衰減（4.3）——改吃
#      `growth_path()` 產出的明確序列，第一年恆等於 g1。
#   2. 再投資用 `k*g` 乘「當年營收」，與 `k` 的定義（每增一元營收所需
#      資本）不符（4.2）——改呼叫 `reinvestment()`，以 Revenue_t −
#      Revenue_(t-1) 為準。
#   3. 展示倍數宣稱分母是出場年 NOPAT，實際除以路徑第一年利潤率
#      （4.4）——`fade_exit_multiple()` 的簽名本身就不接受利潤率路徑，
#      分母必須由呼叫端另行傳入同期 NOPAT。
# 另外，RONIC < WACC 時不再自動把終端成長改成 0（4.5）：改成回傳
# `ronic_below_wacc` 標記，並要求呼叫端在三種有依據情境中明示選擇。
# ============================================================


@dataclass(frozen=True)
class FadeYearDetail:
    """fade 路徑單一年度的逐年明細（COR-03 4.4：優先輸出逐年明細）。

    屬性：
        year: 相對於出場年的第幾年（1 為出場年後第一年）。
        growth: 該年營收成長率（小數）。
        revenue: 該年營收（相對出場年營收正規化為 1.0 的倍數）。
        nopat_margin: 該年 NOPAT 利潤率（小數）。
        nopat: 該年 NOPAT（= revenue * nopat_margin）。
        reinvestment: 該年再投資金額（= k * (Revenue_t - Revenue_(t-1))）。
        fcff: 該年 FCFF（= nopat - reinvestment，簡化總再投資式）。
        discount_factor: 折回出場年（t=0）的折現因子。
        present_value: 該年 FCFF 的現值。
    """

    year: int
    growth: float
    revenue: float
    nopat_margin: float
    nopat: float
    reinvestment: float
    fcff: float
    discount_factor: float
    present_value: float


@dataclass(frozen=True)
class FadeResult:
    """`fade_enterprise_value()` 的回傳值：企業價值與逐年明細（COR-03 4.4）。

    屬性：
        enterprise_value: fade 路徑折回出場年（t=0）的營運企業價值總和
            （明確預測期現值 + 終值現值）。**這是 EV，不是每股價值**；
            要得到每股價值須先呼叫 `equity_bridge()` 完成股權橋接
            （COR-02）。
        years: 明確預測期逐年明細，長度與輸入的成長序列一致。
        terminal_value: 終端年（第 N 年）當下的終值（未折現）。
        terminal_value_present_value: 終值折回出場年（t=0）的現值。
        terminal_fcff_next: 終值起算用的下一期（第 N+1 年）FCFF。
        ronic_terminal: 終端 RONIC（= 終端 NOPAT 利潤率 / k）。
        ronic_below_wacc: 終端 RONIC 是否低於 WACC（COR-03 4.5）。
        terminal_policy: 呼叫端明示選擇的終端情境標籤；`ronic_below_wacc`
            為 `False` 時可為 `None`。
    """

    enterprise_value: float
    years: tuple[FadeYearDetail, ...]
    terminal_value: float
    terminal_value_present_value: float
    terminal_fcff_next: float
    ronic_terminal: float
    ronic_below_wacc: bool
    terminal_policy: str | None


_TERMINAL_POLICIES = frozenset(
    {
        "continue_value_destruction",  # 繼續破壞價值：維持成長，但再投資報酬低於資金成本
        "shrink_reinvestment",  # 縮減投資：降低再投資率，成長隨之下降
        "restructure",  # 重整：資產處分或業務退出，改走 asset_nav 對照
    }
)


def fade_enterprise_value(
    growth_rates: Sequence[float],
    nopat_margin_path: Sequence[float],
    k: float,
    wacc: float,
    terminal_policy: str | None = None,
) -> FadeResult:
    """Fade 模型企業價值：明確成長序列 + 總淨再投資簡化式（COR-03）。

    現金流公式固定為簡化總再投資式 `FCFF_t = NOPAT_t - Reinvestment_t`
    （見 `references/valuation-paths.md` 4.1），因為 fade 模型只用單一
    資本強度參數 `k`，沒有逐年拆分的 D&A／capex／ΔNWC 可用；`k` 須涵蓋
    淨資本支出與營運資金變動的合計（4.4：「成長資本項目須分清淨 capex
    與營運資金」是對 `k` 校準過程的要求，不是要求本函式另外接受拆分
    項目）。**不得**在函式外把這裡算出的 FCFF 再用 `fcff_full()` 重複扣
    一次 capex／NWC（4.1 的「兩式擇一」要求）。

    參數：
        growth_rates: 明確年度成長序列（小數），建議用
            `growth_path(g1, g_terminal, n)` 產生，第一個元素即為 `g1`、
            最後一個元素即為終端成長率 `g_terminal`。長度即為 fade 年數
            `N`，須 >= 1。
        nopat_margin_path: 長度與 `growth_rates` 相同的 NOPAT 利潤率路徑
            （出場年+1 … 終端，小數）。
        k: 單位成長資本強度（每增加一元年營收所需資本），須 >= 0。
        wacc: 折現率（小數），FCFF 對應 WACC（COR-01）。
        terminal_policy: 終端情境標籤，須是
            `{"continue_value_destruction", "shrink_reinvestment",
            "restructure"}` 之一，或 `None`。當終端 RONIC < WACC 時為
            **必填**——本函式不會自動把終端成長改成 0 繼續算，呼叫端
            必須明示三種有依據情境中選了哪一種（4.5）；實際的「縮減
            投資」或「重整」數值影響，須由呼叫端改用對應的
            `growth_rates`／`k`／`nopat_margin_path` 重新呼叫本函式，
            `terminal_policy` 只負責記錄選擇、防止悄悄代選。

    回傳：`FadeResult`。

    Raises:
        ValueError: `growth_rates` 為空、與 `nopat_margin_path` 長度不
            一致、`k < 0`、`terminal_policy` 不在允許集合內、終端 RONIC
            < WACC 卻未提供 `terminal_policy`、終值折現率 <= 終端成長率
            （透過 `terminal_value()` 拒絕），或任一輸入非有限
            （`NaN`／`inf`）。
    """
    if len(growth_rates) == 0:
        raise ValueError("成長序列不得為空")
    if len(growth_rates) != len(nopat_margin_path):
        raise ValueError("成長序列與 NOPAT 利潤率路徑長度必須一致")
    for idx, g in enumerate(growth_rates):
        _require_finite(f"growth_rates[{idx}]", g)
    for idx, margin in enumerate(nopat_margin_path):
        _require_finite(f"nopat_margin_path[{idx}]", margin)
    _require_finite("k", k)
    _require_finite("wacc", wacc)
    if k < 0:
        raise ValueError("k（資本強度）不得為負")
    if terminal_policy is not None and terminal_policy not in _TERMINAL_POLICIES:
        raise ValueError(
            f"terminal_policy 必須是 {sorted(_TERMINAL_POLICIES)} 之一，或 None"
        )

    years: list[FadeYearDetail] = []
    revenue = 1.0
    for idx, (g, margin) in enumerate(zip(growth_rates, nopat_margin_path, strict=True), start=1):
        revenue_prev = revenue
        revenue = revenue_prev * (1 + g)
        nopat = revenue * margin
        reinvest = reinvestment(revenue_prev=revenue_prev, growth=g, k=k)
        fcff = fcff_simplified(nopat=nopat, reinvestment=reinvest)
        discount_factor = _require_finite("discount_factor", 1.0 / (1 + wacc) ** idx)
        years.append(
            FadeYearDetail(
                year=idx,
                growth=g,
                revenue=revenue,
                nopat_margin=margin,
                nopat=nopat,
                reinvestment=reinvest,
                fcff=fcff,
                discount_factor=discount_factor,
                present_value=_require_finite("present_value", fcff * discount_factor),
            )
        )

    g_term = growth_rates[-1]
    margin_term = nopat_margin_path[-1]
    ronic_term = margin_term / k if k > 0 else math.inf
    ronic_below_wacc = ronic_term < wacc

    if ronic_below_wacc and terminal_policy is None:
        raise ValueError(
            "終端 RONIC < WACC：必須在 terminal_policy 明示三種有依據情境之一 "
            f"{sorted(_TERMINAL_POLICIES)}（繼續破壞價值／縮減投資／重整），"
            "不得由函式自動把終端成長改成 0 繼續算"
        )

    revenue_final = years[-1].revenue
    revenue_next = revenue_final * (1 + g_term)
    reinvest_next = reinvestment(revenue_prev=revenue_final, growth=g_term, k=k)
    nopat_next = revenue_next * margin_term
    fcff_next = fcff_simplified(nopat=nopat_next, reinvestment=reinvest_next)

    # 終值一律沿用 terminal_value()：折現率 <= 終端成長率時拒絕計算，
    # 且終端年成長、再投資、利潤率與下一期現金流由同一組公式算出，
    # 保證彼此一致（COR-03 4.6）。
    terminal_value_at_n = terminal_value(cf_next=fcff_next, discount_rate=wacc, g_perpetual=g_term)
    terminal_value_pv = _require_finite(
        "terminal_value_present_value", terminal_value_at_n / (1 + wacc) ** len(years)
    )

    enterprise_value = _require_finite(
        "enterprise_value", math.fsum(year.present_value for year in years) + terminal_value_pv
    )

    return FadeResult(
        enterprise_value=enterprise_value,
        years=tuple(years),
        terminal_value=terminal_value_at_n,
        terminal_value_present_value=terminal_value_pv,
        terminal_fcff_next=fcff_next,
        ronic_terminal=ronic_term,
        ronic_below_wacc=ronic_below_wacc,
        terminal_policy=terminal_policy,
    )


def fade_exit_multiple(enterprise_value: float, nopat_same_period: float) -> float:
    """展示用 EV/NOPAT 倍數，分母須是與 `enterprise_value` 同時點的 NOPAT（COR-02、COR-03 4.4）。

    這是 **EV/NOPAT**，不是 P/NOPAT；要得到每股價值，須先用
    `equity_bridge()` 完成股權橋接（COR-02）。

    本函式刻意 **不** 接受 `nopat_margin_path` 之類的路徑輸入——舊版
    `justified_multiple()` 宣稱分母是出場年 NOPAT，實際卻除以路徑第一年
    的利潤率（`nopat_margin_path[0]`），是獨立於成長序列 bug 之外的第二
    個錯誤。把「同期 NOPAT」限定為呼叫端必須自行算好、明確傳入的單一
    數字，讓這類誤用在型別層面就不成立。

    參數：
        enterprise_value: 企業價值（通常是 `fade_enterprise_value()` 的
            `enterprise_value`，即折回出場年的 EV）。
        nopat_same_period: 與 `enterprise_value` 同一時點（通常是出場年）
            的 NOPAT，須 > 0。

    回傳：EV/NOPAT 倍數。

    Raises:
        ValueError: `nopat_same_period <= 0`，或任一輸入／回傳值非有限
            （`NaN`／`inf`）。
    """
    _require_finite("enterprise_value", enterprise_value)
    _require_finite("nopat_same_period", nopat_same_period)
    if nopat_same_period <= 0:
        raise ValueError("同期 NOPAT 必須 > 0，否則 EV/NOPAT 倍數無意義")
    return _require_finite("fade_exit_multiple 回傳值", enterprise_value / nopat_same_period)


# ============================================================
# 通用反解器：用於 FR-03／§12.5 的 reverse round-trip
# ============================================================


@dataclass(frozen=True)
class ParameterSolveResult:
    """`solve_scalar_parameter()` 的回傳值（FR-03：反解狀態必須明確）。

    狀態由「已驗證的根數 R」與「驗證失敗的變號區間數 `unresolved_intervals`
    （U）」共同決定，**核心規則：只要 U > 0，就不得宣稱唯一解**——即使
    剛好只有一個候選根通過驗證，只要還有其他變號區間沒解出來，那個
    「唯一」就是假的（第二輪 Codex review 發現的缺陷：陡峭的第二個真根
    因收斂後殘差略超過 `residual_tol` 被丟棄，若只看「通過驗證的根數」
    會誤判成單一候選）。

    **第三輪 Codex review 發現的更根本缺陷：狀態名稱宣稱得比方法能證明的
    多。** 本函式的求解方法是「等距取樣 + 偵測變號」，這種方法在數學上
    只能證明「取樣網格上偵測到幾個通過驗證的候選根」，**不能**證明「這是
    定義域內唯一的根」或「這個範圍內確實無解」——但舊版狀態名稱
    `"unique"`／`"no_solution_in_range"` 卻做出了方法本身不支持的強斷言。
    三個實測盲點：

    1. 偶重根（如 `(x-0.42)**2`）在根處觸底但不變號，純變號偵測完全看
       不到，會誤報成「範圍內無解」。
    2. 偶重根與一般根混在同一函式中時，偶重根一樣會被漏掉，只剩看得到
       的那個根被誤報成「唯一」。
    3. 兩個相距極近的單根可能落在同一取樣格內，其中一個會被完全漏掉，
       剩下的一個一樣被誤報成「唯一」。

    因應方式：狀態名稱全面改為只宣稱「這個取樣網格上找到的證據」，不再
    宣稱「唯一」或「無解」；同時新增「偵測 `|f|` 局部極小」的機制作為變號
    偵測的補充，讓（1）（2）能被找到（見 `samples_used` 與下方偶重根偵測
    說明），（3）則是取樣密度的固有限制，**盡力而為、不保證**，呼叫端可
    調高 `samples` 降低（但不能消除）漏根機率。

    **v1.3.2（第四輪 Codex review）修正的兩個獨立缺陷：**

    1. **收斂旗標遺漏**：`_minimize_abs_f` 耗盡 `max_iter` 仍未收斂時，舊版
       照樣回傳當下中點，而候選驗收只檢查殘差、沒檢查自變數是否收斂——
       偶重根附近 `|f|` 本來就平坦，殘差天生就小，未收斂的候選因此被
       誤判成可用答案（實測：`0.001*(x-0.42)**2`、`max_iter=1`、
       `tol=1e-12` 會回傳 `single_candidate`，值誤差達 0.0018，卻宣稱
       16 位精度）。修法：`_minimize_abs_f` 改回傳
       `(root_estimate, converged)`，候選必須**同時**通過「區間已收斂」
       與「殘差 <= residual_tol」才計入 `candidates`；未收斂的候選改計入
       `unresolved_intervals`，讓狀態落到 `"unconverged"`，不得是
       `"single_candidate"` 或 `"no_candidate_in_range"`。
    2. **`f` 回傳非有限值被靜默吞掉**：取樣陣列 `fs` 舊版未檢查有限性就
       直接拿去做變號與局部極小判斷，`NaN` 與任何比較恆為 `False`，於是
       「`f` 在某段範圍算不出來」與「`f` 正常算過、確實無解」在回傳值上
       完全無法區分。修法：所有對 `f` 的求值一律經過內部 `_eval`
       wrapper 計數，新增 `non_finite_evaluations` 欄位；任一相鄰取樣點
       對只要有一端非有限，即視為「這段區間未被有效評估」計入
       `unresolved_intervals`（讓狀態落到 `"unconverged"`），不得被當成
       「沒有變號」或「不是局部極小」靜默略過。

    **要主張「唯一解」，呼叫端必須另外論證** `f` 在該範圍內連續且嚴格
    單調（或用其他數學方法證明），不能只憑本函式回傳 `"single_candidate"`
    就宣稱唯一——這是文件層約束，Python 型別系統不強制檢查。

    | 條件 | status | value | candidates |
    |---|---|---|---|
    | `U > 0`（不論 R 幾個） | `"unconverged"` | `None` | 已驗證的根（R，可能是空的） |
    | `U == 0`、`R == 1` | `"single_candidate"` | 該根 | 該根（單一元素 tuple） |
    | `U == 0`、`R > 1` | `"multiple_candidates"` | `None` | 全部 R 個根 |
    | `U == 0`、`R == 0` | `"no_candidate_in_range"` | `None` | `()` |

    屬性：
        status: 見上表，四種之一：
            - `"single_candidate"`：在取樣網格上只找到一個通過驗證的
              候選根，且沒有任何變號區間驗證失敗。**單一候選不等於
              唯一解**——只代表這個取樣密度下沒有偵測到第二個候選，
              不代表定義域內數學上只有這一個根。
            - `"no_candidate_in_range"`：在取樣網格上未偵測到任何候選根
              （既無變號區間，`|f|` 的局部極小也都沒能通過殘差檢驗）。
              **不證明範圍內無解**，只代表這個取樣密度下找不到；呼叫端
              可放寬範圍或調高 `samples` 再試。
            - `"unconverged"`：**只要有任何一個變號區間沒能通過驗證**
              （`unresolved_intervals > 0`），無論已驗證的根有幾個，都
              回報這個狀態——常見成因是 `f` 不連續，或某段區間函式斜率
              太陡導致收斂後殘差仍超過 `residual_tol`，或 `max_iter`
              不足。這與 `no_candidate_in_range` 是不同的失敗模式：前者
              是「這個範圍內疑似有解，但求解不可靠」，後者是「這個取樣
              密度下沒偵測到任何候選」。
            - `"multiple_candidates"`：找到一個以上通過檢驗的候選根，且
              沒有未解出的區間，須由呼叫端自行選根並揭露依據。
        value: `status == "single_candidate"` 時為該根；其餘狀態一律
            `None`。**不得**在非 `single_candidate` 狀態時填入邊界值或
            候選根冒充答案。
        residual: `status == "single_candidate"` 時，該根代入 `f` 的殘差
            （保證 `abs(residual) <= residual_tol` 且為有限數）。`status ==
            "unconverged"` 時，回傳所有被拒候選中「最接近通過檢驗」的
            殘差（依絕對值最小者），供呼叫端判斷離收斂有多遠；其餘狀態
            為 `None`。
        candidates: 已通過驗證的根。`"single_candidate"` 時為單一元素
            tuple；`"multiple_candidates"` 時為全部通過驗證的根；
            `"unconverged"` 時為**部分結果**——已驗證通過的根（可能為
            空，也可能不只一個），讓呼叫端至少看得到「哪些是可信的」，
            而不是整段丟棄；`"no_candidate_in_range"` 時為空 tuple。
        bounds: 搜尋範圍 `(lo, hi)`，供揭露「解的搜尋範圍」（即已檢查過
            的邊界）。
        unresolved_intervals: 計入以下三種「沒能得出可信結論」的情況（即
            上表的 U）：

            (a) 變號偵測分支中，偵測到變號但候選根沒能同時通過「區間已
                收斂」與「殘差 <= residual_tol」；
            (b) 偶重根偵測分支中，黃金分割搜尋耗盡 `max_iter` 仍未收斂
                （即使代入後殘差恰好很小——平坦函式的殘差本來就小，
                不收斂就不能信這個殘差，v1.3.2 修正）；
            (c) 任一相鄰取樣點對中至少一端求值非有限，導致這段區間根本
                沒被有效評估（v1.3.2 修正，見 `non_finite_evaluations`）。

            呼叫端與測試可直接用這個數字斷言「有幾段沒解出來」，不必從
            `status` 反推。`status != "unconverged"` 時恆為 `0`。**注意**
            偶重根偵測分支中「已收斂但殘差真的超標」（真的沒有根）**不**
            計入此數——那屬於「盡力而為找不到」，是與上述三種不同的情況。
        samples_used: 本次求解實際使用的取樣點數（即呼叫時的 `samples`
            參數值）。揭露「這個結論是在多細的網格上得到的」，讓呼叫端
            判斷取樣密度是否足夠，或該不該調高 `samples` 重跑。
        non_finite_evaluations: 呼叫 `f` 求值時，回傳非有限值（`NaN`／
            `inf`）的次數（v1.3.2 新增）。**恆 >= 0**，即使 `status` 不是
            `"unconverged"` 也可能 > 0（求值過程中出現過的非有限雜訊，
            但最終沒有影響任何判斷分支的結論時仍會被計入）；但只要有
            任何一段搜尋區間因非有限求值而未被有效評估，就必然同時反映
            在 `unresolved_intervals > 0`（狀態落到 `"unconverged"`）——
            呼叫端可用「`non_finite_evaluations > 0` 但 `status` 仍正常」
            與「兩者同時出現」區分「求值過程中出現過雜訊、但不影響結論」
            與「有一段範圍根本沒被評估」。全域皆非有限時（所有取樣點都
            非有限），`non_finite_evaluations` 至少等於取樣點數，且狀態
            必為 `"unconverged"`，與「乾淨地沒找到」
            （`"no_candidate_in_range"`，`non_finite_evaluations == 0`）
            明確可分辨。
    """

    status: str
    value: float | None
    residual: float | None
    candidates: tuple[float, ...]
    bounds: tuple[float, float]
    unresolved_intervals: int
    samples_used: int
    non_finite_evaluations: int


def _bisect_root(
    f: Callable[[float], float], lo: float, hi: float, tol: float, max_iter: int
) -> tuple[float, bool]:
    """在已知變號的 `[lo, hi]` 內以二分法收斂到 `f(x) ≈ 0` 的 `x`（模組內部使用）。

    回傳 `(root_estimate, converged)`。`converged` 僅代表「區間寬度已縮小
    到 `tol` 內」，**不**保證 `f(root_estimate)` 真的接近 0——`f` 不連續
    時區間一樣會收斂，但收斂點兩側的函數值可能仍相差很大。是否真的是
    根，由呼叫端另外驗證殘差（`solve_scalar_parameter` 的 `residual_tol`）。
    `max_iter` 耗盡仍未收斂時，回傳當下的中點與 `converged=False`。

    **迭代中任一求值非有限（`NaN`／`inf`）時立即回傳 `converged=False`**：
    `NaN` 與任何數字比較恆為 `False`，若不攔截，符號比較會靜默走到
    `else` 分支繼續「收斂」，最後交出一個沒有根據的候選（v1.3.2 第五輪
    Codex review 重現：端點有限、中段 `NaN` 的無根函式在 `samples=2` 下
    被回報成 `single_candidate`）。呼叫端據此把該區間計入
    `unresolved_intervals`。
    """
    f_lo = f(lo)
    if f_lo == 0.0:
        return lo, True
    f_hi = f(hi)
    if f_hi == 0.0:
        return hi, True
    if not (math.isfinite(f_lo) and math.isfinite(f_hi)):
        return (lo + hi) / 2.0, False
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if not math.isfinite(f_mid):
            return mid, False
        if f_mid == 0.0:
            return mid, True
        if (f_lo < 0.0) == (f_mid < 0.0):
            lo, f_lo = mid, f_mid
        else:
            hi, f_hi = mid, f_mid
        if (hi - lo) < tol:
            return (lo + hi) / 2.0, True
    return (lo + hi) / 2.0, False


_GOLDEN_RATIO = (math.sqrt(5.0) - 1.0) / 2.0  # 約 0.618，黃金分割搜尋比例


def _minimize_abs_f(
    f: Callable[[float], float], lo: float, hi: float, tol: float, max_iter: int
) -> tuple[float, bool]:
    """在 `[lo, hi]` 內以黃金分割搜尋逼近 `|f(x)|` 的局部極小點（模組內部使用）。

    用於偵測偶重根（`f` 在根處觸底但不變號，一般的變號偵測看不到）：
    純量取樣若剛好在某個局部極小附近夾出一段區間，就用本函式把 `|f|`
    壓到最小，收斂點若殘差夠小即視為候選根。

    **假設 `|f|` 在 `[lo, hi]` 內大致單峰**（只有一個低谷）。這假設在
    「取樣格夠細、兩個真根夠遠」時成立；但若一個取樣格內同時藏有兩個
    以上的根（例如兩個相距極近的單根），`|f|` 在格內會是「谷—峰—谷」
    的雙峰形狀，黃金分割搜尋只會收斂到其中一個低谷附近（通常是取樣點
    本身最接近的那個），**不保證**能分辨並找出全部——這是本函式明確
    的已知限制，不是實作疏漏；呼叫端可調高 `samples` 縮小取樣格降低
    發生機率，但無法完全消除。

    回傳 `(root_estimate, converged)`。`converged` 僅代表「區間寬度已縮小
    到 `tol` 內」，**不**保證 `f(root_estimate)` 真的接近 0——是否合格由
    呼叫端以 `residual_tol` 另外驗證（與 `_bisect_root` 的 `converged`
    語意一致）。`max_iter` 耗盡仍未收斂時，`converged` 為 `False`；
    呼叫端**不得**把未收斂的候選點當成可用答案，即使代入後殘差恰好夠
    小——平坦（偶重根附近）函式的殘差本來就小，光看殘差無法分辨「已經
    逼近真根」與「還沒開始收斂但剛好取樣點附近殘差不大」（v1.3.2 修正
    第四輪 Codex review 發現的缺陷：見 `ParameterSolveResult` docstring）。
    **迭代中任一求值非有限時立即回傳 `converged=False`**（與 `_bisect_root`
    同一條規則）：`abs(NaN) < x` 恆為 `False`，若不攔截會靜默走到 `else`
    分支繼續縮區間，最後交出一個沒有根據的候選。
    """
    a, b = lo, hi
    c = b - _GOLDEN_RATIO * (b - a)
    d = a + _GOLDEN_RATIO * (b - a)
    fc = abs(f(c))
    fd = abs(f(d))
    converged = (b - a) < tol
    for _ in range(max_iter):
        if not (math.isfinite(fc) and math.isfinite(fd)):
            return (a + b) / 2.0, False
        if converged:
            break
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - _GOLDEN_RATIO * (b - a)
            fc = abs(f(c))
        else:
            a, c, fc = c, d, fd
            d = a + _GOLDEN_RATIO * (b - a)
            fd = abs(f(d))
        converged = (b - a) < tol
    if not (math.isfinite(fc) and math.isfinite(fd)):
        return (a + b) / 2.0, False
    return (a + b) / 2.0, converged


def solve_scalar_parameter(
    f: Callable[[float], float],
    lo: float,
    hi: float,
    *,
    samples: int = 33,
    tol: float = 1e-10,
    residual_tol: float = 1e-6,
    max_iter: int = 200,
) -> ParameterSolveResult:
    """在 `[lo, hi]` 範圍內反解使 `f(x) = 0` 的 `x`（FR-03、§12.5 reverse round-trip 用）。

    用途：把「用已知參數正算出一個目標值（價格、EV……），再固定其餘
    輸入反解某一個未知參數」的反解流程做成通用工具，讓 `solve for g1`、
    `solve for wacc`、`solve for k` 等共用同一套「明確範圍、明確殘差、
    明確多解／無解／未收斂狀態」邏輯，不必每個參數各寫一份反解程式。

    做法：先在 `[lo, hi]` 內等距取 `samples` 個樣本點偵測 `f` 的變號
    區間，每個變號區間各自以二分法收斂到區間寬度 `tol` 內。**偵測到變號
    不等於找到根**——`f` 可能在該區間不連續（有變號但沒有真正穿越 0），
    所以每個候選根都必須另外驗證：`abs(f(root)) <= residual_tol` **且**
    該值為有限數（`math.isfinite`），兩項皆通過才計入合格的根；沒通過
    的候選根一律捨棄，不得計入 `candidates` 或當作答案。

    **偶重根偵測（補充變號偵測的盲點）**：純變號偵測看不到「觸底但不
    變號」的偶重根（如 `(x-a)**2` 在 `x=a`）。因此在變號偵測之外，另外
    掃描取樣點序列找 `|f|` 的局部極小（`|f(x_i)| <= |f(x_{i-1})|` 且
    `<= |f(x_{i+1})|`），對每個局部極小以黃金分割搜尋（`_minimize_abs_f`）
    在其相鄰取樣點構成的區間內把 `|f|` 壓到最小；壓到的最小值須**同時**
    通過「區間已收斂到 `tol` 內」與「殘差 `<= residual_tol`」才併入候選
    根（走與變號分支相同的去重流程）——`_minimize_abs_f` 耗盡 `max_iter`
    仍未收斂時即使殘差恰好夠小也**不得**接受，改計入
    `unresolved_intervals`（v1.3.2 修正：平坦的偶重根附近殘差本來就小，
    光看殘差無法分辨「已經逼近真根」與「還沒開始收斂」）；若已收斂但
    收斂到一個明顯為正的極小值，代表這個局部極小處真的沒有根，直接
    捨棄，**不計入 `unresolved_intervals`**——這條分支的性質是「盡力
    而為找不到」，不是「偵測到疑似解但驗證失敗」，兩者在語意上不同，
    故不共用同一個失敗計數器。此機制也能帶出一部分「同一取樣格內兩個
    相距極近的單根」，但**不保證**——那是取樣密度的固有限制，見
    `_minimize_abs_f` 的說明；**不得**因為這個機制找到了某個候選根，就
    反過來宣稱結果是唯一解。

    **非有限求值的處理（v1.3.2 修正）**：`f` 是呼叫端傳入的外部函式，
    它在某個 `x` 算出 `NaN`／`inf` 是一種**需要回報的搜尋結果**，不是
    參數錯誤，本函式**不會** raise；但也**不得**讓非有限值靜默參與變號
    或局部極小判斷——`NaN` 與任何數字比較（含 `<`、`<=`）恆為 `False`，
    若不主動檢查，非有限的取樣點會被誤判成「沒有變號」或「不是局部
    極小」而悄悄略過，使「這段範圍根本沒被評估」與「這段範圍評估過、
    確實無解」在回傳值上無法區分。修法：所有對 `f` 的求值一律經過內部
    wrapper 計數進 `non_finite_evaluations`；取樣階段任一相鄰取樣點對
    只要有一端非有限，就視為「這段區間未被有效評估」計入
    `unresolved_intervals`（連帶跳過該窗口的局部極小判斷），讓狀態落到
    `"unconverged"`，不得是 `"single_candidate"` 或 `"no_candidate_in_range"`。

    `tol` 與 `residual_tol` 管的是兩件不同的事：`tol` 管二分法／黃金分割
    搜尋的自變數 `x` 是否收斂（區間夠不夠窄）；`residual_tol` 管收斂點
    代入 `f` 之後是否真的接近 0（找到的是不是「真的根」）。兩者都通過
    才算數——單獨區間收斂不代表找到根（不連續函式的例子），單獨殘差小
    也不代表已經收斂（極端情況下可能剛好取樣點落在殘差很小但區間還很
    寬的位置，`max_iter` 過小時尤其容易發生）。

    **不假設 `f` 在整個範圍內單調，且本函式的結論僅限於「在這個取樣網格
    上看到的證據」——狀態名稱刻意不使用「唯一」「無解」等需要連續性與
    單調性論證才能成立的強斷言**（見 `ParameterSolveResult` docstring）。
    只要有任何一個變號區間沒能通過驗證，就不得宣稱單一候選——即使剛好
    只有一個候選根通過驗證，只要還有其他變號區間驗證失敗（不論是不
    連續、還是該處斜率太陡使收斂後殘差仍超過 `residual_tol`），那個
    「單一候選」就是假的。判定規則（`R` 為通過驗證的根數，`U` 為
    `unresolved_intervals`）：

    - `U > 0`（不論 `R` 是 0、1 或更多）→ `"unconverged"`。
    - `U == 0` 且 `R == 1` → `"single_candidate"`（**不等於唯一解**，見
      `ParameterSolveResult` docstring）。
    - `U == 0` 且 `R > 1` → `"multiple_candidates"`，列出所有候選根，
      不得只挑第一個或最後一個當答案。
    - `U == 0` 且 `R == 0`（完全沒有偵測到候選根）→
      `"no_candidate_in_range"`，這只代表「在這個取樣網格上」找不到，
      不代表全域無解。

    `"unconverged"` 與 `"no_candidate_in_range"` 對呼叫端的意義不同，
    **不得**混用：前者代表範圍內疑似有解、但求解不可靠（該檢查 `f` 是否
    連續，或調大 `max_iter`／`tol`／`residual_tol`），後者代表這個取樣
    密度下沒偵測到任何候選（該放寬範圍或調高 `samples`）。

    參數：
        f: 一元函式，通常是 `lambda x: 正算函式(x) - 目標值` 的殘差函式。
        lo, hi: 搜尋範圍，須 `hi > lo`。
        samples: 等距取樣點數（含端點），須 >= 2；越多越不容易漏掉相近
            的多個根，但計算成本線性增加。
        tol: 二分法／黃金分割搜尋收斂的區間寬度容差。
        residual_tol: 候選根代入 `f` 後的殘差容差；超過此值視為未通過
            檢驗。預設 `1e-6` 是絕對容差，假設 `f` 的量級與本模組常見的
            報酬率／成長率相近；若 `f` 的量級明顯不同（例如以完整價格
            為單位，數百上千元，或函式在根附近斜率極大），呼叫端應自行
            放寬或縮小 `residual_tol` 以符合該量級下的「重建誤差可接受
            範圍」——這是呼叫端該調整的輸入，不是本函式該放寬的規則。
        max_iter: 每個變號區間或偶重根候選的二分法／黃金分割搜尋最大
            疊代次數。

    回傳：`ParameterSolveResult`。

    Raises:
        ValueError: `hi <= lo`、`samples < 2`，或 `lo`／`hi`／`tol`／
            `residual_tol` 非有限（`NaN`／`inf`）。
    """
    _require_finite("lo", lo)
    _require_finite("hi", hi)
    _require_finite("tol", tol)
    _require_finite("residual_tol", residual_tol)
    if hi <= lo:
        raise ValueError("搜尋範圍上界必須大於下界")
    if samples < 2:
        raise ValueError("取樣點數必須 >= 2")

    non_finite_evaluations = 0

    def _eval(x: float) -> float:
        """`f` 求值的唯一入口（模組內部使用）：取樣、二分法、黃金分割
        三條路徑都必須經過這裡，讓非有限求值一律被計數，不被任何一條
        路徑靜默忽略（v1.3.2 修正第四輪 Codex review 發現的缺陷二）。
        """
        nonlocal non_finite_evaluations
        value = f(x)
        if not math.isfinite(value):
            non_finite_evaluations += 1
        return value

    xs = [lo + (hi - lo) * i / (samples - 1) for i in range(samples)]
    fs = [_eval(x) for x in xs]

    roots: list[float] = []
    rejected_residuals: list[float] = []
    unresolved = 0

    def _add_root_if_new(candidate: float) -> None:
        merge_tol = max(tol * 10, 1e-9)
        for existing in roots:
            if math.isclose(existing, candidate, abs_tol=merge_tol):
                return
        roots.append(candidate)

    def _consider(candidate: float, converged: bool) -> None:
        nonlocal unresolved
        residual = _eval(candidate)
        passes = converged and math.isfinite(residual) and abs(residual) <= residual_tol
        if passes:
            _add_root_if_new(candidate)
            return
        unresolved += 1
        if math.isfinite(residual):
            rejected_residuals.append(residual)

    # 分支一：變號偵測 + 二分法。相鄰取樣點對只要有一端非有限，就無法
    # 判斷這段區間是否變號——不得靜默當成「沒有變號」略過，必須計入
    # unresolved_intervals，讓狀態落到 unconverged（v1.3.2 修正）。
    for i in range(len(xs) - 1):
        f_a, f_b = fs[i], fs[i + 1]
        if not (math.isfinite(f_a) and math.isfinite(f_b)):
            unresolved += 1
            continue
        if f_a == 0.0:
            _consider(xs[i], converged=True)
            continue
        if (f_a < 0.0) != (f_b < 0.0):
            root, converged = _bisect_root(_eval, xs[i], xs[i + 1], tol, max_iter)
            _consider(root, converged)
    if math.isfinite(fs[-1]) and fs[-1] == 0.0:
        _consider(xs[-1], converged=True)

    # 分支二：|f| 局部極小偵測 + 黃金分割搜尋（補足偶重根盲點）。三個
    # 樣本點只要有一個非有限就整個窗口跳過（已由分支一對應的相鄰點對
    # 計入 unresolved_intervals，這裡不重複計數）。已收斂但殘差真的
    # 超標的候選單純捨棄，不計入 unresolved_intervals（見上方
    # docstring）；未收斂的候選一律計入 unresolved_intervals，不得因為
    # 殘差恰好夠小就接受（v1.3.2 修正缺陷一）。
    for i in range(1, len(xs) - 1):
        f_prev, f_cur, f_next = fs[i - 1], fs[i], fs[i + 1]
        if not (math.isfinite(f_prev) and math.isfinite(f_cur) and math.isfinite(f_next)):
            continue
        mag_prev, mag_cur, mag_next = abs(f_prev), abs(f_cur), abs(f_next)
        # 兩側都嚴格較大才算「真的凹下去」的局部極小；只要求 <=（非嚴格）
        # 會把完全平坦的區段（|f| 到處相等，例如不連續函式兩側各自的常數
        # 平台）也當成候選，只要 residual_tol 剛好比平台高度寬鬆就會產生
        # 大量與根無關的假候選（見 v1.3.1 修正紀錄）。要求兩側嚴格排除了
        # 平坦區段，也排除了「平台一路銜接到跳躍點」這種單側嚴格的情況，
        # 只保留真正兩側都下降的凹點——即偶重根「觸底不變號」的典型形狀。
        if mag_cur < mag_prev and mag_cur < mag_next:
            candidate, converged = _minimize_abs_f(_eval, xs[i - 1], xs[i + 1], tol, max_iter)
            residual = _eval(candidate)
            if not math.isfinite(residual):
                unresolved += 1
                continue
            if not converged:
                unresolved += 1
                continue
            if abs(residual) <= residual_tol:
                _add_root_if_new(candidate)
            # else：已收斂但殘差真的超標，代表這裡真的沒有根，捨棄且
            # 不計入 unresolved_intervals（既有行為，見上方 docstring）。

    if unresolved > 0:
        best_residual = min(rejected_residuals, key=abs) if rejected_residuals else None
        return ParameterSolveResult(
            status="unconverged",
            value=None,
            residual=best_residual,
            candidates=tuple(roots),
            bounds=(lo, hi),
            unresolved_intervals=unresolved,
            samples_used=samples,
            non_finite_evaluations=non_finite_evaluations,
        )
    if len(roots) == 1:
        root = roots[0]
        return ParameterSolveResult(
            status="single_candidate",
            value=root,
            residual=_eval(root),
            candidates=(root,),
            bounds=(lo, hi),
            unresolved_intervals=0,
            samples_used=samples,
            non_finite_evaluations=non_finite_evaluations,
        )
    if len(roots) > 1:
        return ParameterSolveResult(
            status="multiple_candidates",
            value=None,
            residual=None,
            candidates=tuple(roots),
            bounds=(lo, hi),
            unresolved_intervals=0,
            samples_used=samples,
            non_finite_evaluations=non_finite_evaluations,
        )
    return ParameterSolveResult(
        status="no_candidate_in_range",
        value=None,
        residual=None,
        candidates=(),
        bounds=(lo, hi),
        unresolved_intervals=0,
        samples_used=samples,
        non_finite_evaluations=non_finite_evaluations,
    )
