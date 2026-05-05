"""
axiom_arena — 公理对抗历史记录与排名
每次 axiom_battle 运行后记录结果，支持：
- 记录每次判决（ALIVE/DEAD/MODIFIED/STRENGTHENED）
- 追踪每个公理的生存压力历史
- 排名公理强弱
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


class AxiomArena:
    """
    公理角斗场 — 记录和管理所有 axiom 对抗历史

    用法：
        arena = AxiomArena("/tmp/axiom_arena_log.jsonl")
        arena.record("axiom1_growth", "death", 0.0, "零能量攻击致命")
        arena.record("axiom1_growth", "modified", 0.5, "加约束后存活")
        for id_, data in arena.ranking():
            print(f"{id_}: {data['name']} avg={data['avg_intensity']:.3f}")
    """

    def __init__(self, log_path: str = "/tmp/axiom_arena_log.jsonl"):
        self.log_path = Path(log_path)
        self.events: list[dict] = []
        if self.log_path.exists():
            with open(self.log_path) as f:
                self.events = [json.loads(line) for line in f if line.strip()]

    def record(
        self,
        axiom_id: str,
        event: str,  # "alive" | "death" | "strengthen" | "modify" | "suspend"
        survival_pressure: float,
        reason: str = "",
        attack_summary: str = "",
    ) -> None:
        """记录一次对抗事件"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "axiom_id": axiom_id,
            "event": event,
            "survival_pressure": round(survival_pressure, 4),
            "reason": reason,
            "attack_summary": attack_summary,
        }
        self.events.append(entry)
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def ranking(self) -> list[tuple[str, dict]]:
        """
        返回所有公理的综合排名
        返回: [(axiom_id, {name, event_count, avg_intensity, latest_event, deaths, alive_count}), ...]
        按 avg_intensity 降序
        """
        scores: dict[str, dict] = defaultdict(
            lambda: {
                "name": "",
                "pressures": [],
                "events": [],
                "deaths": 0,
                "alive_count": 0,
                "modified_count": 0,
            }
        )

        for ev in self.events:
            aid = ev["axiom_id"]
            scores[aid]["pressures"].append(ev["survival_pressure"])
            scores[aid]["events"].append(ev["event"])
            if ev["event"] == "death":
                scores[aid]["deaths"] += 1
            elif ev["event"] == "alive":
                scores[aid]["alive_count"] += 1
            elif ev["event"] in ("modify", "strengthen"):
                scores[aid]["modified_count"] += 1

        result = []
        for axiom_id, data in scores.items():
            if data["pressures"]:
                avg = sum(data["pressures"]) / len(data["pressures"])
            else:
                avg = 1.0
            result.append((axiom_id, {
                "name": axiom_id,
                "event_count": len(data["events"]),
                "avg_intensity": round(avg, 4),
                "latest_event": data["events"][-1] if data["events"] else "none",
                "deaths": data["deaths"],
                "alive_count": data["alive_count"],
            }))

        result.sort(key=lambda x: x[1]["avg_intensity"], reverse=True)
        return result

    def top(self, n: int = 3) -> list[str]:
        """最强n个公理ID"""
        return [aid for aid, _ in self.ranking()[:n]]

    def bottom(self, n: int = 3) -> list[str]:
        """最弱n个公理ID"""
        return [aid for aid, _ in self.ranking()[-n:]]

    def summary(self) -> dict:
        """Arena总体摘要"""
        r = self.ranking()
        alive = sum(1 for _, d in r if d["deaths"] == 0)
        dead = sum(1 for _, d in r if d["deaths"] > 0)
        avg_all = sum(d["avg_intensity"] for _, d in r) / len(r) if r else 0
        return {
            "total_axioms": len(r),
            "survived": alive,
            "has_died": dead,
            "avg_survival_pressure": round(avg_all, 4),
            "ranking": r,
        }
