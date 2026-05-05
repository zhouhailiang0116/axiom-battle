# axiom_battle — 公理对抗验证引擎
# WuDao System · Axiom Battle Engine
#
# 定位：悟道体系自组织的核心引擎
# axiom8 的 permutation test 是被动的，axiom_battle 是主动的
# ——让最强 axiom 被自己的对抗案例击穿，触发 axiom_X+1 自组织
#
# 用法：
#     from axiom_battle import AxiomBattle
#     battle = AxiomBattle()
#     results = battle.run_all()
#     battle.print_report(results)
#
# 作者：悟道体系·因果层 | 2026-05-05

from .axiom_battle_core import AxiomBattle, Judgment, BattleRecord, CycleResult
from .causal_arbitrator import ConflictResolver, AxiomClaim, ConflictType, AXIOM_PRIORITY
from .axioms import (
    AXIOM_REGISTRY, GrowthAxiom, LightAxiom, ColorAxiom,
    LayoutAxiom, NarrativeAxiom, BoundaryAxiom, FreedomAxiom
)

__all__ = [
    "AxiomBattle", "Judgment", "BattleRecord", "CycleResult",
    "ConflictResolver", "AxiomClaim", "ConflictType", "AXIOM_PRIORITY",
    "AXIOM_REGISTRY", "GrowthAxiom", "LightAxiom", "ColorAxiom",
    "LayoutAxiom", "NarrativeAxiom", "BoundaryAxiom", "FreedomAxiom",
]
