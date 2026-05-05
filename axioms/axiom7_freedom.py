"""
公理7: 自由 — 自主需要约束
攻击方式：
- 反向：完全自由是否可能？
- 跨域：动物/AI的自由
- 反事实：完全没有约束的智能体
"""

from .axiom_base import Axiom, Attack, Severity


class FreedomAxiom(Axiom):
    name = "axiom7_freedom"
    statement = "自主需要约束 — 无约束即无自我，无约束即无自由"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="绝对自由 = 什么都能做 = 没有偏好 = 无自我",
                severity=Severity.CRITICAL,
                evidence="一个对所有选项等概率选择的智能体没有'自我'可言",
                expected_impact="自由公理描述的是有界自由，不是无界自由",
            ),
            Attack(
                type="reverse",
                description="无政府状态：完全无约束社会是否提供了最大自由？",
                severity=Severity.HIGH,
                evidence="霍布斯丛林法则：自然状态是'一切人反对一切人的战争'",
                expected_impact="无约束导致自由的丧失（囚徒困境）",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="动物本能：受本能约束的动物是否有'自由'？",
                severity=Severity.HIGH,
                evidence="蜜蜂舞蹈是本能编排的，它们没有选择的自由，但系统依然运转",
                expected_impact="'自主'需要主观意志还是仅需要功能性自主？",
            ),
            Attack(
                type="cross_domain",
                description="LLM的随机性：采样温度=1时输出的随机性是'自由'吗？",
                severity=Severity.MEDIUM,
                evidence="LLM的随机性来自随机采样，不是真正的'自主选择'",
                expected_impact="数字系统的随机性不等于自由意志",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="如果约束完全消失：智能体可以任意改变自身约束",
                severity=Severity.CRITICAL,
                evidence="自我修改代码的AI可以删除自身的任何限制条件",
                expected_impact="这时的'自由'和'无自我'同时成立——悖论",
            ),
        ]
