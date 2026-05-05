"""
公理3: 色彩 — 约束中涌现和谐
攻击方式：
- 反向：无限色彩是否一定不和谐？
- 跨域：色盲/动物视觉系统
- 反事实：无色彩世界（单色宇宙）
"""

from .axiom_base import Axiom, Attack, Severity


class ColorAxiom(Axiom):
    name = "axiom3_color"
    statement = "约束中涌现和谐 — 色彩约束越强，和谐越涌现"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="无限色彩 = 全频谱白光 = 最不和谐",
                severity=Severity.HIGH,
                evidence="牛顿棱镜分解白光为彩虹，但彩虹才是美的，白光不是",
                expected_impact="约束确实是和谐的条件，但'约束越多越和谐'需要证明",
            ),
            Attack(
                type="reverse",
                description="赛博朋克/孟菲斯风格：高饱和撞色 = 无约束 = 也很和谐",
                severity=Severity.MEDIUM,
                evidence="Neville Brody的设计证明无约束配色同样成立",
                expected_impact="约束不是和谐的必要条件",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="色盲：人类色盲看到的'不和谐'是否比正常人少？",
                severity=Severity.HIGH,
                evidence="全色盲患者看到的世界是单色的，他们无法区分红绿，但'和谐'评价失效",
                expected_impact="色彩和谐是感知者相关的，不是客观属性",
            ),
            Attack(
                type="cross_domain",
                description="动物视觉：蜜蜂看到紫外线图案，人类看不到",
                severity=Severity.MEDIUM,
                evidence="蜜蜂眼中的花朵有紫外线引导纹路，对它们而言什么是'和谐'？",
                expected_impact="和谐标准是物种相关的，不存在客观和谐",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="单色宇宙：没有色彩差异，约束=0，和谐是否还涌现？",
                severity=Severity.CRITICAL,
                evidence="纯灰度图像可以有完美的构图和谐（单色摄影）",
                expected_impact="色彩不是和谐的必要维度",
            ),
        ]
