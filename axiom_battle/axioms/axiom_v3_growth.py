"""
公理1 v3: 生长 — 有序化即生长
精化自: axiom1_growth v2 被"无边宇宙"HIGH攻击击穿

攻击分析：
- v1/v2致命伤："向边界生长"——无边宇宙中能量流存在但无边界
- v3防御：生长不依赖空间边界，依赖"有序化方向"
  有界/无界环境都有能量梯度，梯度方向即有序化方向
  生长 = 在能量梯度方向上增加结构化/减少熵
"""

from .axiom_base import Axiom, Attack, Severity


class GrowthAxiomV3(Axiom):
    name = "axiom1_growth_v3"
    statement = "系统在开放能量流中存在时，向有序化方向生长或收缩——扩张与内聚皆为生长，边界是有序化的结果而非前提"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击（降级）
            Attack(
                type="reverse",
                description="向内收缩是有序化，但收缩后没有「抵达」任何边界",
                severity=Severity.MEDIUM,
                evidence="冥想时意识内聚，有序度增加，但没有任何物理边界被触及",
                expected_impact="收缩是有序化，但不等同于抵达边界——需要区分过程与结果",
            ),
            # 跨域攻击（降级）
            Attack(
                type="cross_domain",
                description="数学：函数在奇点处发散，永远生长却永远没有「方向」",
                severity=Severity.MEDIUM,
                evidence="y=1/x 在 x→0 时趋向无穷，生长无限持续但从未收敛到任何边界",
                expected_impact="发散函数没有极限，有序化需要一个吸引态",
            ),
            # 反事实攻击（核心防御）
            Attack(
                type="counterfactual",
                description="无边宇宙：能量流存在但空间无边界，生长向何处？",
                severity=Severity.LOW,
                evidence="无边宇宙中能量梯度依然存在（温度差/密度差），有序化沿梯度方向展开，不依赖空间边界",
                expected_impact="有序化方向来自能量梯度，不来自空间边界——边界是有序化的可能结果，不是前提",
            ),
        ]
