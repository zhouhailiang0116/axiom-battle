#!/usr/bin/env python3
"""
axiom-battle 完整运行器 v2
集成 axiom 攻击框架 + 冲突仲裁 + 历史Arena追踪
支持 v1 公理 vs v2 公理对比
"""
import json
import sys
from pathlib import Path

from axiom_battle.axioms import AXIOM_REGISTRY, AXIOM_REGISTRY_V2
from axiom_battle.causal_arbitrator import ConflictResolver, AxiomClaim

# Arena 使用绝对路径
import os as _os
_ARENA_PATH = "/tmp/axiom_arena_log.jsonl"
from axiom_battle.axiom_arena import AxiomArena as _AxiomArena


def run_attacks(registry: dict, label: str) -> list[dict]:
    arena = _AxiomArena(_ARENA_PATH)
    """运行公理攻击验证"""
    results = []
    for name, cls in registry.items():
        case = cls().run()
        results.append(case.to_dict())
        # 记录到Arena
        arena.record(
            axiom_id=name,
            event={
                "ALIVE": "alive",
                "STRENGTHENED": "strengthen",
                "MODIFIED": "modify",
                "DEAD": "death",
                "SUSPENDED": "suspend",
            }.get(case.verdict, "alive"),
            survival_pressure=case.survival_pressure,
            reason=case.verdict_reason,
            attack_summary=f"{label}: {len(case.attacks)} attacks",
        )
    return results


def run_conflicts() -> dict:
    """运行公理冲突仲裁"""
    resolver = ConflictResolver()
    claims = [
        AxiomClaim(5, "concentrate", "peak", 0.95, "叙事高潮需要聚焦"),
        AxiomClaim(7, "free", "max_freedom", 0.88, "用户意图应完全自由"),
        AxiomClaim(3, "constrain", "palette", 0.80, "配色需要约束和谐"),
        AxiomClaim(6, "free", "boundaryless", 0.75, "边界应该被打破"),
    ]
    conflicts = resolver.detect_conflict(claims)
    final_intensity = resolver.arbitrate(conflicts)
    return {
        "conflicts": [str(cf) for cf in conflicts],
        "conflict_reports": [cf.report() for cf in conflicts if cf.winner],
        "final_intensity": final_intensity,
    }


def print_round(results: list[dict], label: str):
    alive = sum(1 for r in results if r["verdict"] == "ALIVE")
    strengthened = sum(1 for r in results if r["verdict"] == "STRENGTHENED")
    modified = sum(1 for r in results if r["verdict"] == "MODIFIED")
    dead = sum(1 for r in results if r["verdict"] == "DEAD")
    suspended = sum(1 for r in results if r["verdict"] == "SUSPENDED")

    print(f"\n{'='*60}")
    print(f"  【{label}】 总公理数: {len(results)}")
    print(f"  ALIVE:{alive}  STRENGTHENED:{strengthened}  MODIFIED:{modified}  DEAD:{dead}  SUSPENDED:{suspended}")
    print()

    for r in results:
        v = r["verdict"]
        icon = {"ALIVE": "✓", "STRENGTHENED": "▲", "MODIFIED": "◐", "DEAD": "✗", "SUSPENDED": "◑"}[v]
        print(f"{icon} [{v:>10}] {r['axiom']}")
        print(f"  公理: {r['statement'][:60]}...")
        print(f"  判决: {r['reason']}")
        for atk in r["attacks"]:
            print(f"    ·[{atk['severity']:>8}] {atk['type']}: {atk['description'][:50]}")


def print_arena_summary():
    print(f"\n{'='*60}")
    print("  【Arena 历史排名】")
    summary = arena.summary()
    print(f"  存活: {summary['survived']}/{summary['total_axioms']}  |  曾死亡: {summary['has_died']}  |  平均生存压力: {summary['avg_survival_pressure']:.1%}")
    print()
    for axiom_id, data in summary["ranking"]:
        status = "💀" if data["deaths"] > 0 else "✅"
        print(f"  {status} {axiom_id:<22}  avg={data['avg_intensity']:.1%}  events={data['event_count']}  latest={data['latest_event']}")


if __name__ == "__main__":
    arena = _AxiomArena(_ARENA_PATH)

    # v1 公理对抗
    print("=" * 60)
    print("  axiom-battle 公理对抗验证报告 v2")
    print("  第二轮：v1 攻击 vs v2 精化")
    v1_results = run_attacks(AXIOM_REGISTRY, "v1")
    print_round(v1_results, "v1 第一轮攻击")

    # v2 公理对抗
    v2_results = run_attacks(AXIOM_REGISTRY_V2, "v2")
    print_round(v2_results, "v2 第二轮攻击（精化后）")

    # v1 vs v2 对比
    print(f"\n{'='*60}")
    print("  【v1 vs v2 对比】")
    print()
    print(f"  {'公理':<25} {'v1判决':>10} {'v2判决':>10} {'变化':>10}")
    print(f"  {'-'*55}")
    v1_by_name = {r["axiom"]: r for r in v1_results}
    v2_by_name = {r["axiom"]: r for r in v2_results}
    for name in sorted(v1_by_name.keys()):
        v1 = v1_by_name[name]
        v2 = v2_by_name.get(name)
        v1d = v1["verdict"]
        v2d = v2["verdict"] if v2 else "N/A"
        if v1d == v2d:
            change = "—"
        elif v1d == "DEAD" and v2d in ("ALIVE", "MODIFIED", "STRENGTHENED"):
            change = "✅修复"
        elif v1d in ("ALIVE", "MODIFIED") and v2d == "DEAD":
            change = "❌退化"
        else:
            change = f"{v1d}→{v2d}"
        print(f"  {name:<25} {v1d:>10} {v2d:>10} {change:>10}")

    # 冲突仲裁
    conflict_results = run_conflicts()
    print(f"\n{'='*60}")
    print("【冲突仲裁】")
    for cr in conflict_results["conflict_reports"]:
        print(f"  {cr}")

    print(f"\n最终强度系数:")
    for axiom_id, intensity in sorted(conflict_results["final_intensity"].items()):
        bar = "█" * int(intensity * 10)
        print(f"  axiom{axiom_id}: {bar} {intensity:.2f}")

    # Arena摘要
    print_arena_summary()

    # 保存报告
    output = {
        "v1_results": v1_results,
        "v2_results": v2_results,
        "conflict_results": conflict_results,
        "arena_summary": arena.summary(),
    }
    report_path = "/tmp/axiom-battle/axiom_battle_v2_report.json"
    with open(report_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[报告已保存到 {report_path}]")
