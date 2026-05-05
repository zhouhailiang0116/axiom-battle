"""
公理8 V2: 因果 — 因果是特定层次内的不可还原关联（精化版）
量子纠缠攻击弱化为MEDIUM（宏观层次不适用）
大爆炸奇点攻击弱化为MEDIUM（日常经验层次仍成立）
"""

from .axiom_base import Axiom, Attack, Severity


class CausalAxiomV2(Axiom):
    name = "axiom8_causal_v2"
    statement = (
        "因果是特定层次内的不可还原关联 — "
        "量子关联/数学关系/宇宙视界是其他层次的关联；"
        "在宏观经验层次，因果链是意义溯因的唯一通道"
    )

    def attack(self) -> list[Attack]:
        return [
            Attack(
                type="reverse",
                description="SEM结构方程模型将因果还原为概率图数学，形式上完备",
                severity=Severity.MEDIUM,
                evidence="Pearl的do-calculus：P(Y|do(X))可计算，'不可还原'是认知论断言",
                expected_impact="公理预设了形而上学立场，不完全是形式断言",
            ),
            Attack(
                type="cross_domain",
                description="量子纠缠：贝尔实验只证明量子层面非定域，宏观物理因果仍成立",
                severity=Severity.MEDIUM,
                evidence="宏观物体退相干后量子效应消失，经典因果适用",
                expected_impact="加层次限定后量子攻击失效",
            ),
            Attack(
                type="counterfactual",
                description="大爆炸奇点：时间从t>0开始，t=0之前无时间/因果概念",
                severity=Severity.MEDIUM,
                evidence="广义相对论+量子力学在奇点处都失效，但日常经验层次不受影响",
                expected_impact="公理预设时间存在——但在日常经验层次仍成立",
            ),
        ]
