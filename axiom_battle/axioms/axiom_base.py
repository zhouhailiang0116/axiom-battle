"""
悟道体系 axiom-battle 公理基类
每个公理必须实现：attack() → dict
"""

from abc import ABC, abstractmethod
from typing import Literal, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

Verdict = Literal["ALIVE", "STRENGTHENED", "MODIFIED", "DEAD", "SUSPENDED"]


class Severity(Enum):
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


@dataclass
class AxiomCase:
    """单个公理的对抗案例"""
    axiom_name: str
    axiom_statement: str
    attacks: list[Attack] = field(default_factory=list)
    verdict: Verdict = "ALIVE"
    verdict_reason: str = ""
    survival_pressure: float = 0.0  # 0.0-1.0，越高越顽强

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
    """公理基类"""

    name: str = ""
    statement: str = ""  # 公理陈述

    @abstractmethod
    def attack(self) -> list[Attack]:
        """生成三种攻击：反向/跨域/反事实"""
        pass

    def evaluate(self, attacks: list[Attack]) -> tuple[Verdict, str, float]:
        """
        根据攻击判定公理状态
        返回: (verdict, reason, survival_pressure)
        """
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

    def run(self) -> AxiomCase:
        """完整运行对抗流程"""
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
