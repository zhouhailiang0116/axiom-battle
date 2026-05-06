#!/usr/bin/env python3
"""
axiom-battle CLI 入口
用法：
    axiom-battle              # 运行全部公理对抗
    axiom-battle --axiom 1   # 只跑 axiom1
    axiom-battle --v2        # 跑 v2 精化版
    axiom-battle --v3        # 跑 v3 版
    axiom-battle --list      # 列出所有公理
    axiom-battle --json      # JSON 输出
    axiom-battle --server    # 启动 REST API
"""
import sys
import argparse
from axiom_battle import AxiomBattle
from axiom_battle.axioms import AXIOM_REGISTRY, AXIOM_REGISTRY_V2, AXIOM_REGISTRY_V3


def list_axioms():
    print("\n  悟道体系 · 公理清单\n  " + "=" * 50)
    battle = AxiomBattle()
    defendants = battle.list_defendants()
    for d in defendants:
        print(f"  [{d['axiom_id']}] {d['name']:<8} status={d['status']}")
    print()


def run_battle(axiom_id=None, version="v1", json_output=False):
    registries = {"v1": AXIOM_REGISTRY, "v2": AXIOM_REGISTRY_V2, "v3": AXIOM_REGISTRY_V3}
    registry = registries.get(version, AXIOM_REGISTRY)

    if axiom_id is not None:
        key = f"axiom{axiom_id}" if axiom_id < 8 else None
        # 尝试找对应版本
        for prefix in [f"axiom{axiom_id}", f"axiom{axiom_id}_{version}"]:
            for k in registry:
                if k.startswith(prefix):
                    key = k
                    break
            if key:
                break
        if key and key in registry:
            cls = registry[key]
            case = cls().run()
            if json_output:
                import json
                print(json.dumps(case.to_dict(), ensure_ascii=False, indent=2))
            else:
                _print_case(case)
        else:
            print(f"  未找到 axiom {axiom_id} (version={version})")
            print(f"  可用：{list(registry.keys())}")
    else:
        # 运行全部
        results = []
        for name, cls in registry.items():
            case = cls().run()
            results.append(case.to_dict())
            if not json_output:
                _print_case(case)

        if json_output:
            import json
            print(json.dumps(results, ensure_ascii=False, indent=2))


def _print_case(case):
    v = case.verdict
    icon = {"ALIVE": "✓", "STRENGTHENED": "▲", "MODIFIED": "◐", "DEAD": "✗", "SUSPENDED": "◑"}.get(v, "?")
    print(f"\n{icon} [{v:>10}] {case.axiom_name}")
    print(f"  公理: {case.axiom_statement}")
    print(f"  判决: {case.verdict_reason}")
    for atk in case.attacks:
        print(f"    ·[{atk.severity.name:>8}] {atk.type}: {atk.description[:60]}")


def run_server():
    print("  启动 axiom-battle REST API...")
    print("  (需要 uvicorn: pip install 'fastapi[standard]')")
    try:
        import uvicorn
        from axiom_battle.api_server import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except ImportError:
        print("  错误: 请安装 uvicorn")
        print("  pip install 'fastapi[standard]'")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="axiom-battle",
        description="悟道体系 · 公理对抗赛引擎 — Popper证伪主义的代码化",
    )
    parser.add_argument("--list", action="store_true", help="列出所有公理")
    parser.add_argument("--axiom", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8],
                        help="只跑指定 axiom")
    parser.add_argument("--version", "-v", choices=["v1", "v2", "v3"], default="v1",
                        help="公理版本 (default: v1)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    parser.add_argument("--server", "-s", action="store_true", help="启动 REST API")
    args = parser.parse_args()

    if args.list:
        list_axioms()
    elif args.server:
        run_server()
    else:
        run_battle(axiom_id=args.axiom, version=args.version, json_output=args.json)


if __name__ == "__main__":
    main()
