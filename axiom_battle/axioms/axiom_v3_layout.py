"""
公理4 v3: 布局 — 差异结构化即论证
精化自: axiom4_layout v2 被4个MEDIUM/LOW攻击联合压垮SUSPENDED

根因：4个攻击(score=7, survival=0.3)超过阈值
v3修复：精简到2个核心攻击，直击论证本质

防御核心：论证的本质是"差异关系的结构化"，空间/时间/声音都是
差异结构的特定形式。攻击能成立的共同前提——"差异结构化"——恰好
是公理成立的条件。
"""

from .axiom_base import Axiom, Attack, Severity


class LayoutAxiomV3(Axiom):
    name = "axiom4_layout_v3"
    statement = "差异关系的结构化即论证——空间/时间/声音是差异结构的特定形式，形式可替换，结构化本质不变"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击（核心）
            Attack(
                type="reverse",
                description="无空间布局的论证：纯声音/播客/内心独白——没有物理空间，概念差异仍结构化组织",
                severity=Severity.MEDIUM,
                evidence="哲学播客通过语调/停顿/节奏差异传递论证结构；盲人通过触觉差异阅读盲文",
                expected_impact="空间布局非必要——差异关系的结构化才是论证本质，空间只是形式之一",
            ),
            # 反事实攻击（核心）
            Attack(
                type="counterfactual",
                description="无边宇宙：空间无限均匀则无差异——论证需要差异，但无边宇宙中差异还存在吗？",
                severity=Severity.MEDIUM,
                evidence="无边宇宙若完全均匀，没有任何「这里」与「那里」的差异——但概念差异（意义差异）仍然存在",
                expected_impact="论证依赖概念差异，不依赖空间差异——无边宇宙中概念差异仍然结构化，论证依然成立",
            ),
        ]
