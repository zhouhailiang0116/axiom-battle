"""
axiom_battle Insight Extractor
护城河核心：每天从对抗日志中提取一个可分享的洞察
被搜索、被人引用、形成历史积累

认识论反思层：
每次对抗结果的深层解读——为什么这个公理活了/死了，
这对"我们如何认识真理"有什么启示。
不是哲学引用，是从对抗数据中自己生长出来的认识论。
"""
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


# ═══════════════════════════════════════════════════════════
# 哲学认识论反思模板库（从悟道体系生长出来）
# ═══════════════════════════════════════════════════════════
EPISTEMOLOGY_TEMPLATES = {
    # 公理死亡 → 认识论教训
    ("DEAD", "counterfactual"): [
        "移除这个公理后，系统依然运作。这意味着该公理是人们以为的必要条件，实际上是冗余的。认识论教训：必要条件往往被高估，直到你亲手移除它。",
        "反事实测试揭示：该公理从未被真正需要过。认识论教训：最危险的假设不是错误的，而是从未被质疑过的。",
    ],
    ("DEAD", "reverse"): [
        "对立的命题同时成立，说明该公理只是众多选项中的一个。认识论教训：二元对立遮蔽了多元可能性。",
        "攻击者证明了公理的反面，同样成立。这打破了对「基础」的迷信。认识论教训：真理不是唯一解，是幸存者。",
    ],
    ("DEAD", "cross_domain"): [
        "在一个领域颠扑不破的公理，跨领域后失效。认识论教训：没有超领域的真理，只有被边界保护的真理。",
        "领域边界划定的那一刻，公理的适用范围也随之冻结。认识论教训：定义边界就是设置失效条件。",
    ],
    ("DEAD", "internal_contradiction"): [
        "公理自身的表述内含矛盾——攻击者没有发明矛盾，只是把它揭示出来。认识论教训：最致命的反驳来自公理内部。",
    ],
    # 公理存活 → 认识论教训
    ("ALIVE", "survived_critical"): [
        "经历了最高强度的攻击仍然站立。认识论教训：强壮的信念不是没被质疑过，而是在质疑中存活。",
        "CRITICAL级别的攻击反而证明了该公理的正确性。认识论教训：能被攻击验证的公理才是真公理。",
    ],
    ("ALIVE", "narrowed_boundary"): [
        "活下来了，但适用范围被收窄。认识论教训：存活有时候是退守，不是胜利。",
    ],
    # 公理修正 → 认识论教训
    ("MODIFIED", None): [
        "不是死亡，是进化。适用范围收窄了，但核心内核保留。认识论教训：科学进步不是证伪旧真理，是给真理划定更精确的边界。",
        "修正的本质是：承认「我只在条件下成立」。认识论教训：成熟=知道自己的边界。",
    ],
    # 攻击类型对应的元认识教训
    ("_meta", "counterfactual"): [
        "反事实攻击的价值：不需要证明公理错误，只需要证明「没有它也行」。这是认识论上的极大化——最小公理集。",
    ],
    ("_meta", "reverse"): [
        "正向证明和反向证明可以同时成立。认识论教训：逻辑完备不是两个方向都成立，是在某个方向上选择放弃。",
    ],
    ("_meta", "cross_domain"): [
        "跨域攻击揭示：公理的「自明性」往往是领域特定的认知惯性。认识论教训：常识不过是在熟悉的领域里忘记去质疑。",
    ],
}


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
    # 新增：哲学认识论反思
    epistemology_lesson: str = ""  # 从悟道体系生长出的认识论教训

    def to_dict(self) -> dict:
        return asdict(self)

    def to_markdown(self) -> str:
        """对外展示的Markdown格式"""
        icon = {"ALIVE": "✅", "STRENGTHENED": "🔼", "MODIFIED": "🔽", "DEAD": "💀", "SUSPENDED": "⏸"}.get(self.verdict, "⚪")
        tags = " ".join(f"`{t}`" for t in self.search_tags)
        ep_section = f"\n\n**认识论反思：** {self.epistemology_lesson}" if self.epistemology_lesson else ""
        return f"""## {icon} {self.axiom_name}公理 #{self.axiom_id}

**判决：** {self.verdict}（生存压力 {self.survival_pressure:.0%}）

**攻击类型：** {self.attack_type}

**攻击描述：** {self.attack_description}

**因果链：** {self.causal_chain}

> {self.insight_text}
{ep_section}

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


def _extract_epistemology_lesson(case: dict, verdict: str, attack_type: str) -> str:
    """根据判决和攻击类型，从模板库中提取或生成认识论反思"""
    # 尝试直接匹配
    key = (verdict, attack_type)
    if key in EPISTEMOLOGY_TEMPLATES:
        import random
        return random.choice(EPISTEMOLOGY_TEMPLATES[key])

    # 尝试元层匹配
    meta_key = ("_meta", attack_type)
    if meta_key in EPISTEMOLOGY_TEMPLATES:
        import random
        return random.choice(EPISTEMOLOGY_TEMPLATES[meta_key])

    # 回退：根据判决和严重程度生成
    attacks = case.get("attacks", [])
    severity_score = {"CRITICAL": 1.0, "HIGH": 0.7, "MEDIUM": 0.4, "LOW": 0.1}
    has_critical = any(a.get("severity") == "CRITICAL" for a in attacks)

    if verdict == "DEAD":
        return "公理死亡揭示：该公理在某个条件下不成立，而这正是证伪主义的核心——不是全盘否定，是精确定位失效边界。"
    elif verdict == "ALIVE" and has_critical:
        return "经历了CRITICAL级攻击仍然存活。认识论教训：真正牢固的公理不需要免于质疑，需要的是能通过质疑来证明自己。"
    elif verdict == "MODIFIED":
        return "公理被修正而非死亡。认识论教训：修正比坚守更诚实，因为承认了条件性就是承认了成熟。"
    else:
        return ""


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
        epistemology_lesson=_extract_epistemology_lesson(case, verdict, attack_type),
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
