"""
公理6: 边界 — 局限赋予意义
攻击方式：
- 反向：有界不一定有意义
- 跨域：数学中的有界/无界
- 反事实：边界完全消失的情况
"""

from .axiom_base import Axiom, Attack, Severity


class BoundaryAxiom(Axiom):
    name = "axiom6_boundary"
    statement = "局限赋予意义 — 无边界即无意义"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="监狱犯人的局限 vs 自由人的无限可能",
                severity=Severity.HIGH,
                evidence="限制性环境（监狱/集中营）中的创作动机不等于意义涌现",
                expected_impact="局限可以剥夺意义，不只是赋予意义",
            ),
            Attack(
                type="reverse",
                description="数学：无界函数也可以有意义",
                severity=Severity.MEDIUM,
                evidence="y=x 在实数域上无界，但它是清晰有意义的函数",
                expected_impact="'无界=无意义'不成立",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="无限宇宙学：宇宙如果无边（无限膨胀模型），是否无意义？",
                severity=Severity.HIGH,
                evidence="现代宇宙学标准模型（Lambda-CDM）是有限无边（闭合宇宙）",
                expected_impact="有限无边的宇宙如何定义'意义'？",
            ),
            Attack(
                type="cross_domain",
                description="互联网：无限内容海洋中，边界（筛选器）反而在剥夺意义",
                severity=Severity.MEDIUM,
                evidence="推荐算法制造信息茧房，边界反而在减少意义",
                expected_impact="边界既可以赋予意义，也可以剥夺意义",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="边界完全消失：纯粹的无差异状态",
                severity=Severity.CRITICAL,
                evidence="道家的'道生一'的'一'就是无差异的混沌状态",
                expected_impact="无边界是混沌，不是无意义，而是前-意义",
            ),
        ]
