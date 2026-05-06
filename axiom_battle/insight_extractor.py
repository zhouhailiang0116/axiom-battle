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
# ═══════════════════════════════════════════════════════════════════════
# 三层洞察设计原则（2026-05-06 重构）
# ─────────────────────────────────────────────────────────────────────────
# layer 1: insight_text       → 描述这场battle里实际发生了什么（叙事层）
# layer 2: epistemology_lesson → 这个结果对"知识如何成立"有什么根本教训（认识论层）
# layer 3: shadow_insight     → 如果这个结论错了，真正的错误是哪个更深层的预设（反刍层）
#
# 关键：三层说不同的三句话，不抢同一句。
#       insight_text    描述 → 经验层
#       epistemology     抽象 → 哲学层
#       shadow_insight  反刍 → 元层（攻击结论自身的前提）
# ═══════════════════════════════════════════════════════════════════════

EPISTEMOLOGY_TEMPLATES = {
    # ── DEAD ──────────────────────────────────────────────────────────────
    # counterfactual：攻击者问"如果没有它会怎样"，系统回答"没问题"
    # 认识论教训：问错问题会杀死正确的公理。"必要"二字是认知惯性，不是逻辑必然。
    ("DEAD", "counterfactual"): [
        "反事实攻击揭示：我们把「习惯了」误认为「必要了」。认识论教训：错误往往不在公理本身，而在发起攻击的那个问题——问题错了，答案再正确也是死的。",
        "攻击者问的是「没有A系统会怎样」，答案是「还能转」。这不证明A无用，只证明我们从未真正测量过A的贡献。认识论教训：相关性不等于必要性，但「没有A也行」也不等于「A无用」。",
    ],
    # reverse：攻击者证明了公理的反面，且反面同样成立
    # 认识论教训：正反都成立，说明我们在一个不允许同时为真的逻辑框架里操作——框架本身才是真正的约束。
    ("DEAD", "reverse"): [
        "公理和它的反命题同时成立。这意味着我们默认的逻辑框架不允许并列的真值——这个框架才是真正未被质疑的假设。认识论教训：当我们说一个公理「死了」，可能是我们的逻辑体系先死了。",
        "对偶命题同时为真，打破了排中律的幻觉。认识论教训：形式逻辑不是世界的属性，是人类认知的强制约束。公理死亡常常是逻辑框架的边界，不是世界的边界。",
    ],
    # cross_domain：跨领域后公理失效
    # 认识论教训：公理越基础，越可能是领域特定的认知投射。 универсальность是危险假设。
    ("DEAD", "cross_domain"): [
        "一个领域的「自明之理」到了另一个领域什么都不是。这说明所谓公理的自明性是训练出来的，不是客观的。认识论教训：最危险的假设是那些我们以为不需要假设的假设。",
        "跨域失效不是因为公理错了，而是因为我们的认知地图在绘制时只走了一条路。认识论教训：地图不是领土，当我们把地图上的线当成领土本身时，跨界就是背叛。",
    ],
    # internal_contradiction：矛盾在公理内部，被攻击者挖出来
    # 认识论教训：最致命的一击不是外部攻击，是公理内部早已埋藏的地雷。
    ("DEAD", "internal_contradiction"): [
        "公理死于内因——它自己包含了它的死亡。攻击者只是把它埋的东西挖出来埋得更深一点。认识论教训：形式上无懈可击的系统可能在语义层早已破产，而我们通常只看形式。",
    ],
    # ── ALIVE ────────────────────────────────────────────────────────────
    # survived_critical：经历了最高强度攻击仍存活
    # 认识论教训：能承受攻击不是因为我坚硬，是因为我承认了条件性。
    ("ALIVE", "survived_critical"): [
        "CRITICAL级攻击证明的不是公理正确，而是这个公理的边界被测试过了。认识论教训：可检验性才是真理的标记，不是不可动摇。",
        "攻击越猛，活下来的越说明它不依赖嘴硬，而依赖边界清晰。认识论教训：真正的信念不需要免于质疑，需要的是能精确说出自己在哪里结束。",
    ],
    # narrowed_boundary：活了但边界被收窄
    # 认识论教训：存活有时候是战略撤退，不是胜利。知道自己不能做什么，比坚持自己能做什么更重要。
    ("ALIVE", "narrowed_boundary"): [
        "适用边界收窄了——这本身就是收获。认识论教训：成熟不是知道自己能做什么，是终于敢承认自己不能做什么。",
    ],
    # ── MODIFIED ─────────────────────────────────────────────────────────
    ("MODIFIED", None): [
        "不是死亡，是进化。进化不是旧真理变成新真理，是旧真理学会了精确地描述自己。认识论教训：最深的进步不是找到新答案，是把旧问题问得更准确。",
        "修正的本质是：承认「我只在条件下成立」。认识论教训：这是认识论上最诚实的一步——不是投降，是精确。",
    ],
    # ── SUSPENDED ─────────────────────────────────────────────────────────
    ("SUSPENDED", None): [
        "暂缓判决本身就是信息——说明当前的验证手段不足以给这个公理一个确定答案。认识论教训：不知道和搞错了之间，后者更危险。",
    ],
    # ── 攻击类型元层教训（辅助覆盖）───────────────────────────────────
    ("_meta", "counterfactual"): [
        "反事实攻击的哲学意义：它测的不是公理本身，而是我们对「必要性」的感知。认识论教训：我们以为的必要条件，往往是重复了千百遍的习惯。",
    ],
    ("_meta", "reverse"): [
        "reverse攻击的哲学意义：它揭示二元逻辑的局限——世界不需要是排中律的。认识论教训：每当我们被迫选A或B时，问题本身可能已经错了。",
    ],
    ("_meta", "cross_domain"): [
        "跨域攻击的哲学意义：它剥离了公理周围的「文化层」，露出赤裸的结构。认识论教训：常识在熟悉的领域里叫常识，换个领域就叫偏见了。",
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

    # ═══════════════════════════════════════════════════════════
    # 反阴影层（Self-Verification：每个洞察都要能承受自己的对立面）
    # ═══════════════════════════════════════════════════════════
    shadow_insight: str = ""      # 如果这个洞察是错的，真正的错误会是什么
    shadow_attack_type: str = ""  # 攻击这个洞察的方法论
    self_verification_status: str = "UNVERIFIED"  # UNVERIFIED / SURVIVED / FALSIFIED

    def to_dict(self) -> dict:
        return asdict(self)

    def to_markdown(self) -> str:
        """对外展示的Markdown格式"""
        icon = {"ALIVE": "✅", "STRENGTHENED": "🔼", "MODIFIED": "🔽", "DEAD": "💀", "SUSPENDED": "⏸"}.get(self.verdict, "⚪")
        tags = " ".join(f"`{t}`" for t in self.search_tags)
        ep_section = f"\n\n**认识论反思：** {self.epistemology_lesson}" if self.epistemology_lesson else ""
        shadow_section = ""
        if self.shadow_insight:
            sv_icon = {"SURVIVED": "🛡️", "FALSIFIED": "⚠️", "UNVERIFIED": "❓"}.get(self.self_verification_status, "❓")
            shadow_section = f"\n\n**反阴影验证** {sv_icon}：{self.shadow_insight}"
        return f"""## {icon} {self.axiom_name}公理 #{self.axiom_id}

**判决：** {self.verdict}（生存压力 {self.survival_pressure:.0%}）

**攻击类型：** {self.attack_type}

**攻击描述：** {self.attack_description}

**因果链：** {self.causal_chain}

> {self.insight_text}
{ep_section}{shadow_section}

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


# ═══════════════════════════════════════════════════════════════════════
# 反阴影生成（Self-Verification Protocol）
# 每个洞察必须能承受自己对立面的攻击
# ═══════════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════
# 反阴影模板（Self-Verification Protocol）
# ═══════════════════════════════════════════════════════════════════════
# 原则：shadow_insight 不是重复 epistemology_lesson，而是攻击更深的预设。
# 例如：
#   epistemology 说"问错问题会杀死正确的公理"
#   shadow      说"如果问题是正确的，那我们的「正确」标准本身是不是也有问题"
#
# 三层分工：
#   insight_text          → 描述battle中实际发生了什么（攻击者做了什么，公理怎么死的/活的）
#   epistemology_lesson   → 这个结果对"知识如何成立"有什么根本教训
#   shadow_insight       → 攻击这个结论自身的前提：什么假设如果错了，结论就不成立了？

SHADOW_TEMPLATES = {
    "DEAD": {
        # counterfactual 的攻击前提：如果「移除后系统还能转」不能证明无用，那什么才能？
        # 隐藏前提：我们假设了"贡献可移除性"是测贡献的正确方法
        "counterfactual": [
            # shadow质疑：我们有没有可能把「A在支撑系统」和「A在被系统支撑」混淆了？
            "如果这个公理被移除后系统还能转，我们假设的前提是「贡献=移除后系统崩溃」。但有没有可能A的贡献是「让其他部分能转」而不是「直接让系统转」？反阴影：贡献有两种——直接的和结构的，我们只测了前者。",
            # shadow质疑：测量框架本身是否预设了公理正确？
            "我们的验证框架本身就依赖这个公理——我们是在用被攻击目标来验证被攻击目标。数学上这叫循环验证。影子：如果验证系统是内嵌的，验证结果还有意义吗？",
        ],
        # reverse 的攻击前提：如果正反命题同时成立，那「成立」本身是不是需要重新定义？
        # 隐藏前提：我们假设了公理和反公理不能同时为真
        "reverse": [
            # shadow质疑：我们有没有可能把「逻辑上的反」当成「存在上的反」？
            "公理和反命题同时为真——我们通常把这解读为公理错了，但有没有可能解读为：公理和反命题各自描述的是不同层次的现象？影子：「死亡」有没有可能只是我们强行把多层次现象压进二元框架的结果？",
            # shadow质疑：reverse攻击本身是否预设了二元逻辑的裁决权？
            "reverse攻击者假设了「公理和反命题不能同时为真」是裁决标准。但这个标准本身来自被攻击的同一个逻辑体系。影子：用自己的规则来裁决自己，这算外部攻击还是内部自检？",
        ],
        # cross_domain 的攻击前提：如果跨域失败是因为领域划分本身是人为的？
        # 隐藏前提：我们假设了领域边界是客观的，不是认知的
        "cross_domain": [
            # shadow质疑：我们划分的领域边界本身是否就是认知局限的一部分？
            "这个公理在跨域后失败了——但「领域」是我们划分的。影子：有没有可能我们只是在同一个世界里换了个观察角度，然后说「原来的公理不对」？跨域失效可能只是暴露了领域划分的武断性，不是公理的局限。",
            # shadow质疑：检验的顺序是否决定了结果？
            "先在一个领域建立公理，再跨到另一个领域检验——这个顺序本身就预设了「先建立后检验」的合理性。影子：如果调换顺序，另一个领域的公理在这个领域里可能也「死」了。",
        ],
        # internal_contradiction 的攻击前提：我们对「矛盾」的定义本身是否足够精确？
        "internal_contradiction": [
            # shadow质疑：矛盾是被发现的，还是被制造的（通过重新解释）？
            "矛盾被发现了——但同一个符号系统里，矛盾往往可以通过重新定义术语来消除。影子：我们是在揭示公理中早已存在的矛盾，还是在用一种特定的语言游戏制造了矛盾？",
            # shadow质疑：形式矛盾和语义矛盾是不同的
            "形式层面的矛盾不等于语义层面的矛盾。影子：我们说公理「自相矛盾」，是形式上可证明的，还是我们把语义张力误认为形式矛盾了？",
        ],
        "default": "如果公理没死，错误在于：我们把「适用范围的边界」当成了「公理的死亡证明」。修正≠死亡，只是边界重新标定。",
    },
    "ALIVE": {
        # alive 的 shadow 质疑：谁在验证？验证者的多样性够吗？
        "reverse": [
            # shadow质疑：我们用来裁决的逻辑体系本身是否足够多样化？
            "公理活过了reverse攻击——但我们用来裁决的标准是同一套逻辑体系。影子：有没有可能存在另一套逻辑体系，在那里这个公理还是死了？ALIVE verdict是所有可能逻辑体系中的平均值，还是只是我们这一套的当前值？",
        ],
        "cross_domain": [
            # shadow质疑：活过的跨域攻击数量是否足够代表「跨域」这个概念？
            "跨域攻击失败了——但我们测试的跨域是有限的几个组合。影子：领域组合是指数级的，我们只测了一个无穷小集合。「活过」是我们采样的结果，不是证明。",
        ],
        "counterfactual": [
            # shadow质疑：我们对「系统」的界定是否是公理存活的决定因素？
            "counterfactual攻击失败了——但「没有A系统会怎样」的答案完全取决于我们如何界定「系统」。影子：如果把系统边界扩大，这个公理还有那么必要吗？「移除后系统还能转」是系统边界的函数，不是公理属性的函数。",
        ],
        "default": "ALIVE verdict 只说明这个公理通过了今天的攻击。历史上「已证明」的正确最后翻车的案例，远比「存活到今天」的公理多。",
    },
    "MODIFIED": {
        "default": [
            "修正后的公理适用范围收窄了——但「收窄」本身就是解释。影子：我们是把边界收准了，还是只是在暴力拟合攻击数据？修正如果只是针对已知攻击的补丁，它预测新攻击的能力并没有提升。",
            "修正意味着旧公理死亡、新公理诞生。影子：谁保证了新公理的优先级？它只是「还没被攻击过」，不等于「更正确」。进化论和求生欲有时候分不清。",
        ],
    },
    "SUSPENDED": {
        "default": [
            "暂缓判决被当成「公理有问题」的信息——但也可能是「验证系统有问题」。影子：不知道是验证者不够强还是公理真的不够好，两者都表现为「无法裁决」。用「无法裁决」来判断公理质量，是循环论证吗？",
        ],
    },
}


def _generate_shadow_insight(case: dict, verdict: str, attack_type: str) -> tuple[str, str]:
    """生成反阴影洞察：攻击这个洞察自身的前提
    Returns: (shadow_insight_text, shadow_attack_type)
    """
    import random

    axiom = case.get("axiom", "")
    verdict_templates = SHADOW_TEMPLATES.get(verdict, SHADOW_TEMPLATES.get("ALIVE", {}))
    templates = verdict_templates.get(attack_type, verdict_templates.get("default", [""]))

    # default可能是str也可能是list
    if isinstance(templates, str):
        shadow_text = templates.format(axiom=axiom)
    else:
        shadow_text = random.choice(templates).format(axiom=axiom)

    # 反阴影攻击类型：和原攻击类型正交
    # counterfactual → internal_contradiction（质疑测量框架本身）
    # reverse        → cross_domain（质疑逻辑体系的多样性）
    # cross_domain   → counterfactual（质疑测量顺序和系统边界）
    # internal_contradiction → reverse（质疑形式和语义的边界）
    shadow_attack_map = {
        "counterfactual": "internal_contradiction",
        "reverse": "cross_domain",
        "cross_domain": "counterfactual",
        "internal_contradiction": "reverse",
    }
    shadow_attack = shadow_attack_map.get(attack_type, "cross_domain")

    return shadow_text, shadow_attack


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

    # 生成反阴影（每个洞察的对立版本）
    shadow_text, shadow_attack = _generate_shadow_insight(case, verdict, attack_type)

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
        shadow_insight=shadow_text,
        shadow_attack_type=shadow_attack,
        self_verification_status="UNVERIFIED",
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
