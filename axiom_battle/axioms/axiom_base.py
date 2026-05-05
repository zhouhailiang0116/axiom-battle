"""
悟道体系 axiom-battle 公理基类

每个公理必须实现：attack() → list[Attack]

设计原则：
- 攻击是预先写好的对抗案例（人工事先设计），引擎负责跑和判决
- 判决规则可通过 JudgmentPolicy 插件替换（可配置）
- 公理可声明 depends_on 建立依赖图（公理间依赖关系）
"""

from abc import ABC, abstractmethod
from typing import Literal, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum, IntEnum

Verdict = Literal["ALIVE", "STRENGTHENED", "MODIFIED", "DEAD", "SUSPENDED"]


class Severity(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Attack:
    type: Literal["reverse", "cross_domain", "counterfactual"]
    description: str
    severity: Severity
    evidence: str = ""
    expected_impact: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "description": self.description,
            "severity": self.severity.name,
            "evidence": self.evidence,
            "expected_impact": self.expected_impact,
        }


# ── 判决策略（可插拔）────────────────────────────────────────────────────

class JudgmentPolicy:
    """
    判决策略接口，可替换默认的 severity 加权策略。

    默认策略：severity 加权打分
      - CRITICAL=4, HIGH=3, MEDIUM=2, LOW=1
      - score = Σ(severity × weight)
      - survival = max(0, 1 - score/10)

    自定义用法：
        # 全局替换默认策略
        def my_policy(attacks):
            return "DEAD", "always dead", 0.0
        Axiom.default_policy = staticmethod(my_policy)

        # 子类替换
        class MyAxiom(Axiom):
            default_policy = staticmethod(my_policy)
    """

    @staticmethod
    def evaluate(attacks: list[Attack]) -> tuple[Verdict, str, float]:
        if not attacks:
            return "ALIVE", "无有效攻击", 1.0

        critical = sum(1 for a in attacks if a.severity == Severity.CRITICAL)
        high = sum(1 for a in attacks if a.severity == Severity.HIGH)
        medium = sum(1 for a in attacks if a.severity == Severity.MEDIUM)

        score = critical * 4 + high * 3 + medium * 2
        survival = max(0.0, 1.0 - score / 10.0)

        if critical >= 2:
            return "DEAD", f"被{critical}个致命攻击摧毁", survival
        elif critical == 1 and high >= 2:
            return "DEAD", f"1个致命+{high}个高危联合摧毁", survival
        elif critical == 1:
            return "MODIFIED", "被致命攻击击穿，需要修正表述", survival
        elif high >= 2:
            return "STRENGTHENED", f"{high}个高危攻击证明公理耐冲击", survival
        elif high == 1 and medium >= 2:
            return "MODIFIED", "1个高危+2个中危联合作用，需要精化", survival
        elif survival < 0.5:
            return "SUSPENDED", "生存压力过大，暂挂", survival
        else:
            return "ALIVE", f"通过攻击考验，生存压力{survival:.1%}", survival


@dataclass
class AxiomCase:
    axiom_name: str
    axiom_statement: str
    attacks: list[Attack] = field(default_factory=list)
    verdict: Verdict = "ALIVE"
    verdict_reason: str = ""
    survival_pressure: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "axiom": self.axiom_name,
            "statement": self.axiom_statement,
            "attacks": [a.to_dict() for a in self.attacks],
            "verdict": self.verdict,
            "reason": self.verdict_reason,
            "survival_pressure": round(self.survival_pressure, 3),
        }


class Axiom(ABC):
    """
    公理基类

    每个公理声明：
        name: str              公理标识（如 "axiom1_growth"）
        statement: str          公理陈述文本
        depends_on: list[str]   依赖的其他公理（默认空）

    每个公理实现：
        attack() -> list[Attack]

    可选：
        default_policy: 替换默认判决策略（类属性）

    用法：
        class MyAxiom(Axiom):
            name = "my_axiom"
            statement = "我的公理"
            depends_on = ["axiom1_growth"]

            def attack(self) -> list[Attack]:
                return [...]

        case = MyAxiom().run()
        print(case.verdict)  # "ALIVE" / "DEAD" / ...
    """

    name: str = ""
    statement: str = ""
    # 公理依赖图：声明本公理依赖哪些其他公理
    # 例：axiom5_narrative 依赖 axiom4_layout（空间结构是序列意义的前提）
    depends_on: list[str] = field(default_factory=list)
    # 可选的替换判决策略（类属性）
    default_policy: Optional[type] = None

    @abstractmethod
    def attack(self) -> list[Attack]:
        """生成三种攻击：反向/跨域/反事实"""
        pass

    def evaluate(self, attacks: list[Attack]) -> tuple[Verdict, str, float]:
        if self.default_policy is not None:
            return self.default_policy.evaluate(attacks)
        return JudgmentPolicy.evaluate(attacks)

    def run(self) -> AxiomCase:
        attacks = self.attack()
        verdict, reason, survival = self.evaluate(attacks)
        return AxiomCase(
            axiom_name=self.name,
            axiom_statement=self.statement,
            attacks=attacks,
            verdict=verdict,
            verdict_reason=reason,
            survival_pressure=survival,
        )


# ── 公理依赖图工具 ──────────────────────────────────────────────────────

def build_dependency_graph(registry: Dict[str, type]) -> Dict[str, list[str]]:
    """
    从公理注册表构建依赖图。

    用法：
        from axiom_battle.axioms import AXIOM_REGISTRY
        graph = build_dependency_graph(AXIOM_REGISTRY)
        # graph["axiom4_layout"] = ["axiom5_narrative", ...]

    Returns:
        {被依赖公理名: [依赖它的公理列表]}
    """
    graph: Dict[str, list[str]] = {}
    for name, cls in registry.items():
        deps = getattr(cls, "depends_on", [])
        for dep in deps:
            graph.setdefault(dep, []).append(name)
    return graph


def topological_sort(registry: Dict[str, type]) -> list[str]:
    """
    公理拓扑排序（依赖顺序）。

    依赖的公理排在前面，被依赖的排在后面。
    存在循环依赖时抛出 ValueError。
    """
    graph = build_dependency_graph(registry)
    visited: Dict[str, bool] = {}
    result: list[str] = []

    def visit(name: str):
        if visited.get(name) is False:
            raise ValueError(f"循环依赖检测到: {name}")
        if visited.get(name) is True:
            return
        visited[name] = False
        for dependent in graph.get(name, []):
            visit(dependent)
        visited[name] = True
        result.append(name)

    for name in registry:
        if visited.get(name) is not True:
            visit(name)
    return result
