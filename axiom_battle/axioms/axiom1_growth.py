"""
公理1: 生长 — 系统向边界生长
攻击方式：
- 反向：边界内生长 vs 边界外生长
- 跨域：物理边界 vs 心理边界
- 反事实：静止系统是否也算一种"生长"？
"""

from .axiom_base import Axiom, Attack, Severity


class GrowthAxiom(Axiom):
    name = "axiom1_growth"
    statement = "系统向边界生长 — 生长即扩张，扩张即抵达边界"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="向内生长（收缩/内省）是否也算生长？",
                severity=Severity.HIGH,
                evidence="熵减系统（生命体）就是在向内有序化，而非扩张边界",
                expected_impact="如果收缩算生长，公理需要修正为'系统向边界生长或收缩'",
            ),
            Attack(
                type="reverse",
                description="边界处的生长是否一定会突破边界？",
                severity=Severity.MEDIUM,
                evidence="墙壁上的藤蔓会沿着墙壁蔓延，不一定会'突破'",
                expected_impact="生长不等于扩张",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="心理边界：内心秩序的建立是否算'向边界生长'？",
                severity=Severity.HIGH,
                evidence="冥想/修行是向内心边界'生长'，方向与物理空间相反",
                expected_impact="'边界'定义需要明确是物理边界还是心理边界",
            ),
            Attack(
                type="cross_domain",
                description="数学：函数向奇点生长 — 奇点是否算'边界'？",
                severity=Severity.MEDIUM,
                evidence="y=1/x 在 x→0 时函数值发散，但从未'抵达'边界",
                expected_impact="边界定义在数学语境下不成立",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="如果系统处于完全静止状态（零能量），生长是否不可能？",
                severity=Severity.CRITICAL,
                evidence="热力学第三定律：零温下系统处于基态，无热运动",
                expected_impact="生长公理依赖能量存在，不是普适公理",
            ),
        ]
