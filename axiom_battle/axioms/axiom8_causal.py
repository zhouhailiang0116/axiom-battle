"""
公理8: 因果 — 因果链是唯一不可还原的层次
攻击方式：
- 反向：统计相关是否足以推翻因果？
- 跨域：量子纠缠非定域性
- 反事实：没有因果链的世界
"""

from .axiom_base import Axiom, Attack, Severity


class CausalAxiom(Axiom):
    name = "axiom8_causal"
    statement = "因果链是唯一不可还原的层次 — 统计相关可以欺骗，置换检验可以揭穿"

    def attack(self) -> list[Attack]:
        return [
            Attack(
                type="reverse",
                description="统计相关在足够多数据下可以稳定复现，置换检验也通过",
                severity=Severity.HIGH,
                evidence="Luria-Delbruck模型：突变累积是随机的，但多次实验后分布仍然稳定",
                expected_impact="'统计相关可以欺骗'不是因果独有的弱点",
            ),
            Attack(
                type="reverse",
                description="因果链本身可以被统计学捕捉（结构方程模型SEM）",
                severity=Severity.MEDIUM,
                evidence="Pearl的do-calculus把因果还原为概率图模型",
                expected_impact="因果公理预设了因果>统计的层级，但数学上可以统一",
            ),
            Attack(
                type="cross_domain",
                description="量子纠缠：Bell实验证明存在非定域关联",
                severity=Severity.CRITICAL,
                evidence="贝尔不等式违背：纠缠粒子对的状态关联超过任何定域隐变量解释",
                expected_impact="量子层面：因果链不成立，但关联真实存在",
            ),
            Attack(
                type="cross_domain",
                description="宇宙学：宇宙视界外的区域没有因果联系，但仍是同一个宇宙",
                severity=Severity.MEDIUM,
                evidence="可观测宇宙半径460亿光年，外部区域与我们无因果链",
                expected_impact="宇宙整体性不依赖因果链",
            ),
            Attack(
                type="counterfactual",
                description="如果所有因果链同时断裂（宇宙重启）",
                severity=Severity.CRITICAL,
                evidence="大爆炸奇点：宇宙从t=0开始，在那之前没有时间/因果概念",
                expected_impact="因果公理预设了时间存在，不是最底层的公理",
            ),
            Attack(
                type="counterfactual",
                description="纯数学世界：数学对象之间有逻辑关系但没有因果关系",
                severity=Severity.HIGH,
                evidence="素数分布和物理常数之间存在精妙的数学关系",
                expected_impact="数学世界独立于因果公理存在",
            ),
        ]
