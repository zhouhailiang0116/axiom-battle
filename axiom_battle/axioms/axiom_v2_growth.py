"""
公理1 V2: 生长 — 系统向功能边界生长或收缩（精化版）
第一轮攻击后修正：
- 加入能量前提条件（应对"零能量静止"攻击）
- "生长"扩展为"有序化"，包含向内收缩
- "边界"限定为"功能边界"而非纯物理边界
"""

from .axiom_base import Axiom, Attack, Severity


class GrowthAxiomV2(Axiom):
    name = "axiom1_growth_v2"
    statement = (
        "系统在开放能量流中存在时，向功能边界生长或收缩——"
        "有序化即抵达边界，扩张或内聚都是生长的形式"
    )

    def attack(self) -> list[Attack]:
        return [
            # 精化后的反向攻击（更精准）
            Attack(
                type="reverse",
                description="向内收缩是有序化，但是否'抵达'了边界？",
                severity=Severity.MEDIUM,
                evidence="冥想时意识内聚，有序度增加，但没有'抵达'物理边界",
                expected_impact="收缩是有序化，但不等于抵达边界——需要区分'有序化'和'边界抵达'",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="数学：函数在奇点处发散，永远'生长'却永远不抵达边界",
                severity=Severity.MEDIUM,
                evidence="y=1/x 在 x→0 时趋向无穷，生长无限持续但从未收敛",
                expected_impact="'向边界生长'在数学发散情况下不成立",
            ),
            # 反事实攻击（已修复，但留一个残余）
            Attack(
                type="counterfactual",
                description="如果能量流存在但边界不存在（无边宇宙）",
                severity=Severity.HIGH,
                evidence="宇宙加速膨胀模型：空间无限扩大，边界不存在",
                expected_impact="无边宇宙中生长概念失效——需要预设边界存在",
            ),
        ]
