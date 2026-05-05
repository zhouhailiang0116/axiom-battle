"""
公理3 V2: 色彩 — 差异是和谐的必要条件（精化版）
第一轮攻击后修正：
- 单色宇宙：单色也有明度差异，差异=色彩维度
- 色盲：色盲感知到的差异（明度）同样可以构成和谐
- 和谐不是"约束"的结果，而是"差异组织"的结果
"""

from .axiom_base import Axiom, Attack, Severity


class ColorAxiomV2(Axiom):
    name = "axiom3_color_v2"
    statement = (
        "差异是和谐的必要条件 — 色彩是差异的一种维度，"
        "约束是差异组织的形式；和谐涌现于差异的有界组织"
    )

    def attack(self) -> list[Attack]:
        return [
            # 修正后的反向攻击（保留但更精准）
            Attack(
                type="reverse",
                description="同色系但不同明度的搭配：无彩色约束，却很和谐",
                severity=Severity.MEDIUM,
                evidence="高级灰（Grisaille）技法：只用灰色调创造三维和谐",
                expected_impact="差异维度可以是明度而非色相——'色彩'这个词限制了公理的范围",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="完全色盲患者：他们感知到的差异（形状/明度）是否也能构成'和谐'？",
                severity=Severity.MEDIUM,
                evidence="全色盲患者有正常的明度感知，他们的美感评价（蒙娜丽莎临摹）仍然成立",
                expected_impact="'色彩和谐'是特定感知通道的评价，不具备普遍性",
            ),
        ]
