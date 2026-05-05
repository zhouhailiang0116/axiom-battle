#!/usr/bin/env python3
"""
axiom-battle 完整运行器
集成 axiom 攻击框架 + 冲突仲裁 + 因果验证
"""
import json
import sys
from pathlib import Path

# ── 攻击框架 ──────────────────────────────────────────────────────────────
from axiom_battle.axioms import AXIOM_REGISTRY
from axiom_battle.causal_arbitrator import ConflictResolver, AxiomClaim, AXIOM_PRIORITY


def run_attacks() -> list[dict]:
    """运行公理攻击验证"""
    results = []
    for name, cls in AXIOM_REGISTRY.items():
        case = cls().run()
        results.append(case.to_dict())
    return results


def run_conflicts() -> dict:
    """运行公理冲突仲裁"""
    resolver = ConflictResolver()

    # 典型创作场景：叙事聚焦 vs 自由最大化
    claims = [
        AxiomClaim(5, "concentrate", "peak", 0.95, "叙事高潮需要聚焦"),
        AxiomClaim(7, "free", "max_freedom", 0.88, "用户意图应完全自由"),
    ]

    # 添加：色彩约束 vs 边界自由
    claims.append(
        AxiomClaim(3, "constrain", "palette", 0.80, "配色需要约束和谐"),
    )
    claims.append(
        AxiomClaim(6, "free", "boundaryless", 0.75, "边界应该被打破"),
    )

    conflicts = resolver.detect_conflict(claims)
    final_intensity = resolver.arbitrate(conflicts)

    return {
        "claims": [str(c) for c in claims],
        "conflicts": [str(cf) for cf in conflicts],
        "conflict_reports": [cf.report() for cf in conflicts if cf.winner],
        "final_intensity": final_intensity,
    }


def print_report(attack_results: list[dict], conflict_results: dict):
    print("=" * 60)
    print("  axiom-battle 公理对抗验证报告")
    print("=" * 60)

    alive = sum(1 for r in attack_results if r["verdict"] == "ALIVE")
    strengthened = sum(1 for r in attack_results if r["verdict"] == "STRENGTHENED")
    modified = sum(1 for r in attack_results if r["verdict"] == "MODIFIED")
    dead = sum(1 for r in attack_results if r["verdict"] == "DEAD")
    suspended = sum(1 for r in attack_results if r["verdict"] == "SUSPENDED")

    print(f"\n【攻击验证】总公理数: {len(attack_results)}")
    print(f"  ALIVE:{alive}  STRENGTHENED:{strengthened}  MODIFIED:{modified}  DEAD:{dead}  SUSPENDED:{suspended}")

    for r in attack_results:
        v = r["verdict"]
        icon = {"ALIVE": "✓", "STRENGTHENED": "▲", "MODIFIED": "◐", "DEAD": "✗", "SUSPENDED": "◑"}[v]
        print(f"\n{icon} [{v}] {r['axiom']}")
        print(f"  公理: {r['statement']}")
        print(f"  判决: {r['reason']}")
        print(f"  生存压力: {r['survival_pressure']:.1%}  |  攻击数: {len(r['attacks'])}")
        for atk in r["attacks"]:
            print(f"    ·[{atk['severity']}] {atk['type']}: {atk['description']}")

    print(f"\n{'=' * 60}")
    print("【冲突仲裁】")
    for cr in conflict_results["conflict_reports"]:
        print(f"  {cr}")

    print(f"\n最终强度系数:")
    for axiom_id, intensity in sorted(conflict_results["final_intensity"].items()):
        print(f"  axiom{axiom_id}: {intensity:.2f}")


if __name__ == "__main__":
    attack_results = run_attacks()
    conflict_results = run_conflicts()
    print_report(attack_results, conflict_results)

    output = {
        "attack_results": attack_results,
        "conflict_results": conflict_results,
    }
    with open("axiom_battle_report.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[报告已保存到 axiom_battle_report.json]")
