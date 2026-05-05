"""
公理4: 布局 — 空间即论证
攻击方式：
- 反向：空间无关论证存在吗？
- 跨域：时间序列 vs 空间布局
- 反事实：零维空间中论证还存在吗？
"""

from .axiom_base import Axiom, Attack, Severity


class LayoutAxiom(Axiom):
    name = "axiom4_layout"
    statement = "空间即论证 — 布局是论证的结构化呈现"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="纯声音论证：广播/播客没有空间布局，论证依然完整",
                severity=Severity.HIGH,
                evidence="哲学播客可以在没有视觉空间的情况下完成复杂论证",
                expected_impact="论证不依赖空间布局",
            ),
            Attack(
                type="reverse",
                description="线性文本：一维文字流，依赖阅读顺序而非空间",
                severity=Severity.MEDIUM,
                evidence="论文的逻辑流是一维的，不依赖页面空间安排",
                expected_impact="空间布局是辅助，不是论证本质",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="时间布局：音乐的时间结构是否也算一种'空间论证'？",
                severity=Severity.MEDIUM,
                evidence="赋格曲的主题陈述/展开/再现 = 音乐论证",
                expected_impact="时间序列可以替代空间布局",
            ),
            Attack(
                type="cross_domain",
                description="数学：证明步骤是时间序列，不是空间布局",
                severity=Severity.MEDIUM,
                evidence="数学证明的'布局'是逻辑顺序，不存在于物理空间",
                expected_impact="论证的本质是逻辑，不是空间",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="零维点：没有空间延伸，论证还成立吗？",
                severity=Severity.CRITICAL,
                evidence="纯语言（无书写）可以在思想层面完成论证，不依赖空间",
                expected_impact="空间布局不是论证的必要条件",
            ),
        ]
