"""
公理6 V2: 边界 — 有意义边界的条件是差异存在（精化版）
第一轮攻击后修正：
- 监狱的局限是强制边界，不是差异性边界
- "道生一"的无差异状态：没有差异就没有边界，也没有意义
- 边界赋予意义的前提：边界是差异的体现，不是强制的限制
"""

from .axiom_base import Axiom, Attack, Severity


class BoundaryAxiomV2(Axiom):
    name = "axiom6_boundary_v2"
    statement = (
        "差异赋予边界意义 — 边界是差异的边界，"
        "无差异的边界是强制，有差异的边界是赋义"
    )

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="强制边界（监狱/极权）：边界存在但不是'赋予意义'而是'剥夺意义'",
                severity=Severity.HIGH,
                evidence="监狱中的'边界'（高墙）是强制限制，不产生意义",
                expected_impact="需要区分'差异性边界'和'强制性边界'——只有差异性边界才赋义",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="互联网：边界（推荐算法/防火墙）有时剥夺意义而非赋予意义",
                severity=Severity.MEDIUM,
                evidence="信息茧房减少了异质信息摄入，边界筛选不产生意义",
                expected_impact="数字边界不必然赋义——需要感知者主动参与才赋义",
            ),
        ]
