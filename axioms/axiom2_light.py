"""
公理2: 光影 — 对比定义形态
攻击方式：
- 反向：无光环境下的形态是否存在？
- 跨域：数字图像 vs 物理实体
- 反事实：如果宇宙只有一种亮度会怎样？
"""

from .axiom_base import Axiom, Attack, Severity


class LightAxiom(Axiom):
    name = "axiom2_light"
    statement = "对比定义形态 — 无光即无影，无影即无形"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="触觉形态：盲人通过触觉认知物体，不需要光影",
                severity=Severity.HIGH,
                evidence="蝙蝠通过回声定位，暗室中仍能感知三维形态",
                expected_impact="光影不是形态定义的唯一途径",
            ),
            Attack(
                type="reverse",
                description="自发光体：太阳不需要被照亮来'定义形态'",
                severity=Severity.MEDIUM,
                evidence="恒星是自发光，其形态由核聚变边界定义，而非反射光",
                expected_impact="自发光体违反了'对比定义形态'的逻辑",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="数字渲染：程序化生成（ray marching）不需要物理光",
                severity=Severity.HIGH,
                evidence="SDF体积渲染可以在无光照模型下定义物体形状",
                expected_impact="数字形态可以在纯数学定义下存在",
            ),
            Attack(
                type="cross_domain",
                description="X射线/超声波：穿透性成像不依赖可见光对比",
                severity=Severity.MEDIUM,
                evidence="医学CT用X射线密度差异成像，非光影对比",
                expected_impact="'对比'不一定是光强度的对比",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="如果宇宙是完全均匀的光场（无对比），形态还存在吗？",
                severity=Severity.CRITICAL,
                evidence="德雷克方程的黑暗森林悖论：完全均匀辐射场中无形态可言",
                expected_impact="光影公理预设了不均匀性，不是底层公理",
            ),
            Attack(
                type="counterfactual",
                description="如果感知者不存在，光影还有意义吗？",
                severity=Severity.HIGH,
                evidence="月亮不被看时是否存在（洛克问题）",
                expected_impact="光影是感知者相关的，不是客观存在",
            ),
        ]
