"""
公理4 v2: 布局 — 差异结构化即论证
精化自: axiom4_layout v1 被"零维点"CRITICAL攻击击穿

攻击分析：
- v1致命伤：零维（纯语言思想）无空间延伸 → 空间非论证必要条件
- v2防御：论证的本质是"差异关系结构"，空间是差异结构的一种呈现形式
  零维纯语言依赖"概念差异"组织，仍是差异结构化
"""

from .axiom_base import Axiom, Attack, Severity


class LayoutAxiomV2(Axiom):
    name = "axiom4_layout_v2"
    statement = "差异关系的结构化即论证——空间布局是差异结构的一种可视化形式"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击（v2降级：HIGH→MEDIUM）
            Attack(
                type="reverse",
                description="纯声音论证：无空间布局，概念差异仍通过语音组织",
                severity=Severity.MEDIUM,
                evidence="播客/广播：时间流中组织概念，靠语调/停顿/节奏差异传递论证结构",
                expected_impact="空间布局非必要，差异组织才是本质",
            ),
            Attack(
                type="reverse",
                description="线性文本：一维文字差异（词义/逻辑差异）承载论证，不依赖空间",
                severity=Severity.LOW,
                evidence="盲人通过触觉盲文阅读，差异在触觉维度展开，无需视觉空间",
                expected_impact="差异结构可以在任意维度展开",
            ),
            # 跨域攻击（v2降级）
            Attack(
                type="cross_domain",
                description="时间布局：音乐的时间差异结构（主题-展开-再现）= 音乐论证",
                severity=Severity.MEDIUM,
                evidence="赋格曲的论证结构：主题陈述=立论，对位展开=论证，再现=总结",
                expected_impact="时间差异结构与空间差异结构等价",
            ),
            # 反事实攻击（v2新增防御层）
            Attack(
                type="counterfactual",
                description="无边宇宙：无限均匀空间没有差异，论证如何成立？",
                severity=Severity.MEDIUM,
                evidence="如果空间处处完全均匀，没有「这里」与「那里」的差异，论证结构无从建立",
                expected_impact="论证需要差异，不依赖空间本身",
            ),
        ]
