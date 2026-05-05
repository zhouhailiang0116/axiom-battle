"""
公理5: 叙事 — 序列即因果
攻击方式：
- 反向：非叙事知识存在吗？
- 跨域：数学/物理中的因果不依赖叙事
- 反事实：无时间序列的事件集合
"""

from .axiom_base import Axiom, Attack, Severity


class NarrativeAxiom(Axiom):
    name = "axiom5_narrative"
    statement = "序列即因果 — 有序列才有因果，有因果才有意义"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="数据库/知识图谱：非序列信息存储，依然有效",
                severity=Severity.HIGH,
                evidence="Wikipedia的知识不是叙事，而是网状结构",
                expected_impact="信息组织不依赖叙事序列",
            ),
            Attack(
                type="reverse",
                description="地图/图表：空间信息不需要序列",
                severity=Severity.MEDIUM,
                evidence="地铁地图同时呈现所有节点，无先后顺序",
                expected_impact="空间数据是非序列的",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="数学公理体系：公理之间没有时间序列",
                severity=Severity.HIGH,
                evidence="欧几里得几何公理是并列关系，同时为真，无先后",
                expected_impact="因果可以不依赖时间序列",
            ),
            Attack(
                type="cross_domain",
                description="量子力学：事件在测量前无确定序列",
                severity=Severity.MEDIUM,
                evidence="双缝实验中观测行为本身改变事件序列",
                expected_impact="量子事件颠覆了叙事序列的确定性",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="快照宇宙：所有事件同时存在，无序列",
                severity=Severity.CRITICAL,
                evidence="永恒主义哲学：过去/现在/未来同等真实",
                expected_impact="叙事公理预设了时间流动，不是底层公理",
            ),
        ]
