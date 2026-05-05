"""
公理5 V2: 叙事 — 序列是意义组织的充分条件（精化版）
第一轮攻击后修正：
- 数据库/知识图谱是序列的替代形式，但也是一种组织形式
- 数学公理体系是共时性（synchronic）组织，不是历时性（diachronic）序列
- 公理不否认其他意义组织形式，只声称"序列是有效的充分条件"
"""

from .axiom_base import Axiom, Attack, Severity


class NarrativeAxiomV2(Axiom):
    name = "axiom5_narrative_v2"
    statement = (
        "序列是意义组织的充分条件 — 时序因果是意义涌现的一种通道，"
        "非时序组织（数学/地图）同样有效但不通过序列产生意义"
    )

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击（更精准）
            Attack(
                type="reverse",
                description="知识图谱：网状结构产生意义，但不是在时序中产生的",
                severity=Severity.MEDIUM,
                evidence="Wikipedia的超链接网络产生了系统性知识，无需阅读顺序",
                expected_impact="'意义'不依赖时序序列——序列只是意义产生的充分条件之一",
            ),
            # 跨域攻击（保留）
            Attack(
                type="cross_domain",
                description="数学公理的同时性（synchronic）真理：公理并列成立，无先后序列",
                severity=Severity.HIGH,
                evidence="欧几里得公理体系：五条公理同时为真，没有时间演化",
                expected_impact="真理不依赖序列——序列是经验意义的充分条件，不是逻辑真理的必要条件",
            ),
        ]
