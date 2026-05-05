"""
公理2 V2: 光影 — 感知接口定义形态（精化版）
第一轮攻击后修正：
- 触觉/回声定位都是感知接口，不只是光影
- 自发光体本身就是光源，光源不需要被照亮来定义自己
- 感知者不存在时，形态以潜在方式存在（薛定谔的猫思想实验）
"""

from .axiom_base import Axiom, Attack, Severity


class LightAxiomV2(Axiom):
    name = "axiom2_light_v2"
    statement = (
        "感知接口定义形态 — 任何感知通道（光/声/触/数字）中的对比差异"
        "都能定义形态；无感知接口则形态以潜在态存在"
    )

    def attack(self) -> list[Attack]:
        return [
            # 精化后的反向攻击
            Attack(
                type="reverse",
                description="完全无感知接口（无光无声无触无数字信号）时，形态是否存在？",
                severity=Severity.HIGH,
                evidence="量子力学：粒子在未被测量前处于叠加态，形态不确定",
                expected_impact="无感知接口时形态不确定——公理需要加上'在感知接口存在时'前提",
            ),
            # 跨域攻击（已弱化）
            Attack(
                type="cross_domain",
                description="机器感知（LiDAR/超声波）定义形态时没有'感知者体验'",
                severity=Severity.MEDIUM,
                evidence="LiDAR点云定义三维形态，但'被感知'不是必要条件",
                expected_impact="形态定义可以独立于有感知体验的主体",
            ),
        ]
