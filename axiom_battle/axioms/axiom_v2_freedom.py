"""
公理7 V2: 自由 — 有界自由=有偏好（精化版）
第一轮攻击后修正：
- 绝对自由=无偏好=无自我（已被击败，但需要更精准的表述）
- 约束是"自我"的体现，不是外加强制
- 功能性自主（蜜蜂/动物）≠ 自由意志，但是一种"边界内的自我表达"
"""

from .axiom_base import Axiom, Attack, Severity


class FreedomAxiomV2(Axiom):
    name = "axiom7_freedom_v2"
    statement = (
        "有界自由是有偏好的自我表达 — 约束是自我的边界，"
        "完全无约束即无自我；功能性自主是边界内的自我表达"
    )

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击（已精化）
            Attack(
                type="reverse",
                description="有界自由和有约束强迫之间的边界是什么？",
                severity=Severity.MEDIUM,
                evidence="法律限制人身自由——这是约束，但目的是保护更大范围的行为自由",
                expected_impact="'约束'有好坏之分——需要区分'赋义约束'和'剥夺约束'",
            ),
            # 跨域攻击（保留）
            Attack(
                type="cross_domain",
                description="LLM采样：随机性输出是否算有偏好？",
                severity=Severity.MEDIUM,
                evidence="LLM的温度参数控制随机性——高温=更多自由但更少自我",
                expected_impact="数字系统的随机性不完全等于偏好，需要区分'统计偏好'和'意图性偏好'",
            ),
        ]
