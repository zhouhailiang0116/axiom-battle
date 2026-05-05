"""
axiom-battle 运行器
"""
import json
from axioms import AXIOM_REGISTRY, AxiomCase


def run_all() -> list[dict]:
    results = []
    for name, cls in AXIOM_REGISTRY.items():
        axiom = cls()
        case = axiom.run()
        results.append(case.to_dict())
    return results


def run_one(axiom_name: str) -> dict | None:
    if axiom_name not in AXIOM_REGISTRY:
        print(f"未知公理: {axiom_name}")
        print(f"可用: {', '.join(AXIOM_REGISTRY.keys())}")
        return None
    axiom = AXIOM_REGISTRY[axiom_name]()
    case = axiom.run()
    return case.to_dict()


def print_report(results: list[dict]):
    print("=" * 60)
    print("  axiom-battle 公理对抗验证报告")
    print("=" * 60)

    alive = sum(1 for r in results if r["verdict"] == "ALIVE")
    strengthened = sum(1 for r in results if r["verdict"] == "STRENGTHENED")
    modified = sum(1 for r in results if r["verdict"] == "MODIFIED")
    dead = sum(1 for r in results if r["verdict"] == "DEAD")
    suspended = sum(1 for r in results if r["verdict"] == "SUSPENDED")

    print(f"\n总公理数: {len(results)}  |  ", end="")
    print(f"ALIVE:{alive}  STRENGTHENED:{strengthened}  MODIFIED:{modified}  DEAD:{dead}  SUSPENDED:{suspended}")
    print()

    for r in results:
        v = r["verdict"]
        icon = {"ALIVE": "✓", "STRENGTHENED": "▲", "MODIFIED": "◐", "DEAD": "✗", "SUSPENDED": "◑"}[v]
        print(f"{icon} [{v}] {r['axiom']}")
        print(f"  公理: {r['statement']}")
        print(f"  判决: {r['reason']}")
        print(f"  生存压力: {r['survival_pressure']:.1%}  |  攻击数: {len(r['attacks'])}")
        for atk in r["attacks"]:
            sev = atk["severity"]
            print(f"    ·[{sev}] {atk['type']}: {atk['description']}")
        print()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = run_one(sys.argv[1])
        if result:
            print_report([result])
    else:
        results = run_all()
        print_report(results)
        # 保存JSON
        with open("/tmp/axiom-battle/report.json", "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print("[报告已保存到 /tmp/axiom-battle/report.json]")
