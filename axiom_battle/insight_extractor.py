"""
axiom_battle Insight Extractor
护城河核心：每天从对抗日志中提取一个可分享的洞察
被搜索、被人引用、形成历史积累
"""
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class BattleInsight:
    """一次对抗的洞察单元"""
    date: str                    # 2026-05-06
    axiom_id: str                # "axiom6_boundary_v2"
    axiom_name: str              # "边界"
    verdict: str                 # "ALIVE" / "DEAD" / "MODIFIED"
    survival_pressure: float     # 0.0-1.0，生存压力
    attack_type: str            # "reverse" / "cross_domain" / "counterfactual"
    attack_description: str     # 攻击描述（限80字）
    causal_chain: str            # 因果链简述（限120字）
    insight_text: str           # 对外分享的洞察句子（限200字）
    search_tags: list[str]      # ["证伪主义", "公理对抗", "边界公理"]

    def to_dict(self) -> dict:
        return asdict(self)

    def to_markdown(self) -> str:
        """对外展示的Markdown格式"""
        icon = {"ALIVE": "✅", "STRENGTHENED": "🔼", "MODIFIED": "🔽", "DEAD": "💀", "SUSPENDED": "⏸"}.get(self.verdict, "⚪")
        tags = " ".join(f"`{t}`" for t in self.search_tags)
        return f"""## {icon} {self.axiom_name}公理 #{self.axiom_id}

**判决：** {self.verdict}（生存压力 {self.survival_pressure:.0%}）

**攻击类型：** {self.attack_type}

**攻击描述：** {self.attack_description}

**因果链：** {self.causal_chain}

> {self.insight_text}

{tags}
"""

    def to_tweet_length(self) -> str:
        """280字内的Twitter/微博格式"""
        verdict_icon = {"ALIVE": "✅", "DEAD": "💀", "MODIFIED": "🔽", "STRENGTHENED": "🔼"}.get(self.verdict, "⚪")
        return f"""{verdict_icon} [{self.axiom_name}公理 {self.verdict}] {self.insight_text[:200]}

#axiom_battle #悟道体系"""

    def to_search_index_entry(self) -> dict:
        """SEO友好的可索引格式"""
        return {
            "d": self.date,
            "a": self.axiom_name,
            "v": self.verdict,
            "p": self.survival_pressure,
            "t": self.insight_text[:300],
            "k": self.search_tags,
        }


def _generate_casual_chain(case: dict) -> str:
    """从case字典中重建因果链"""
    attacks = case.get("attacks", [])
    if not attacks:
        return "无结构化攻击数据"

    # 找最严重的攻击
    severity_order = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0}
    worst = max(attacks, key=lambda a: severity_order.get(a.get("severity", "LOW"), 0))
    atk_type = worst.get("type", "")
    atk_desc = worst.get("description", "")

    # 反向因果链
    if atk_type == "reverse":
        return f"反向：攻击者提出对立命题，证明了公理自身的局限。攻击：{atk_desc[:80]}"
    elif atk_type == "cross_domain":
        return f"跨域：公理在领域A成立，但领域B暴露了边界条件。攻击：{atk_desc[:80]}"
    elif atk_type == "counterfactual":
        return f"反事实：移除公理后系统仍然运作，说明该公理不是必要条件。攻击：{atk_desc[:80]}"
    else:
        return f"攻击：{atk_desc[:80]}"


def _generate_insight_text(case: dict, verdict: str) -> str:
    """从判决结果生成可分享的洞察句子"""
    axiom = case.get("axiom", "")
    statement = case.get("statement", "")[:50]
    reason = case.get("reason", case.get("verdict_reason", ""))[:100]

    if verdict == "DEAD":
        return f"公理「{axiom}」({statement})在对抗中死亡。判决依据：{reason}。这告诉我们：即使是基础公理也需要经得起攻击才能存活。"
    elif verdict == "ALIVE":
        return f"公理「{axiom}」({statement})经历了三轮攻击仍然存活。判决依据：{reason}。最强壮的公理不是从没被挑战过，而是被挑战后还站着。"
    elif verdict == "MODIFIED":
        return f"公理「{axiom}」({statement})被修正——适用范围收窄了。判决依据：{reason}。这正是证伪主义的本质：不是死亡，是进化。"
    elif verdict == "STRENGTHENED":
        return f"公理「{axiom}」({statement})被攻击反而更强了——攻击本身证明了公理的正确性。判决依据：{reason}。"
    else:
        return f"公理「{axiom}」({statement})暂缓判决。{reason}"


def _generate_tags(axiom_id: str, verdict: str) -> list[str]:
    """生成搜索标签"""
    base = ["axiom_battle", "悟道体系", "证伪主义"]
    axiom_tags = {
        "growth": ["生长公理", "演化"],
        "light": ["光影公理", "视觉"],
        "color": ["色彩公理", "配色"],
        "layout": ["布局公理", "构图"],
        "narrative": ["叙事公理", "故事"],
        "boundary": ["边界公理", "约束"],
        "freedom": ["自由公理", "选择"],
        "causal": ["因果公理", "因果链"],
    }
    for key, tags in axiom_tags.items():
        if key in axiom_id.lower():
            base.extend(tags)
            break
    if verdict == "DEAD":
        base.append("公理死亡")
    elif verdict == "MODIFIED":
        base.append("公理进化")
    return list(set(base))


def extract_insight_from_case(case: dict, date: str) -> BattleInsight:
    """从单个case字典提取洞察"""
    axiom_id = case.get("axiom", case.get("name", "unknown"))
    verdict = case.get("verdict", "SUSPENDED")
    attacks = case.get("attacks", [])
    statement = case.get("statement", "")[:40]

    # 提取最关键的公理名
    axiom_names = {
        "growth": "生长", "light": "光影", "color": "色彩", "layout": "布局",
        "narrative": "叙事", "boundary": "边界", "freedom": "自由", "causal": "因果"
    }
    axiom_name = "其他"
    for key, name in axiom_names.items():
        if key in axiom_id.lower():
            axiom_name = name
            break

    # 生存压力（从 attacks 推断）
    severity_score = {"CRITICAL": 1.0, "HIGH": 0.7, "MEDIUM": 0.4, "LOW": 0.1}
    if attacks:
        max_severity = max(attacks, key=lambda a: severity_score.get(a.get("severity", "LOW"), 0))
        survival_pressure = 1.0 - severity_score.get(max_severity.get("severity", "LOW"), 0)
        attack_desc = max_severity.get("description", "")[:80]
        attack_type = max_severity.get("type", "unknown")
    else:
        survival_pressure = 0.5
        attack_desc = "无结构化攻击"
        attack_type = "none"

    # 如果是 DEAD，生存压力高
    if verdict == "DEAD":
        survival_pressure = 0.95
    elif verdict == "ALIVE":
        survival_pressure = 0.2

    return BattleInsight(
        date=date,
        axiom_id=axiom_id,
        axiom_name=axiom_name,
        verdict=verdict,
        survival_pressure=survival_pressure,
        attack_type=attack_type,
        attack_description=attack_desc,
        causal_chain=_generate_casual_chain(case),
        insight_text=_generate_insight_text(case, verdict),
        search_tags=_generate_tags(axiom_id, verdict),
    )


def extract_from_v3_report(report_path: str, date: str) -> list[BattleInsight]:
    """从 v3 报告提取所有洞察"""
    with open(report_path) as f:
        data = json.load(f)

    insights = []
    for version, key in [("v1", "v1_results"), ("v2", "v2_results"), ("v3", "v3_results")]:
        results = data.get(key, [])
        for case in results:
            insight = extract_insight_from_case(case, date)
            insight.axiom_id = f"{insight.axiom_id}_{version}"
            insights.append(insight)

    return insights


def load_history(log_path: str) -> list[BattleInsight]:
    """从历史日志文件加载所有洞察"""
    insights = []
    if not Path(log_path).exists():
        return insights
    with open(log_path) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                if "insight" in entry:
                    insights.append(BattleInsight(**entry["insight"]))
            except (json.JSONDecodeError, TypeError):
                continue
    return insights


def save_insight(insight: BattleInsight, log_path: str):
    """追加单条洞察到历史日志"""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps({"insight": insight.to_dict()}, ensure_ascii=False) + "\n")
