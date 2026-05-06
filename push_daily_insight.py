#!/usr/bin/env python3
"""
每日 axiom_battle 洞察推送到 GitHub Pages (gh-pages branch)
.run_battle() → 提取洞察 → 生成文件 → GitHub API push
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

import requests

# ── 路径配置 ───────────────────────────────────────────────
REPO = Path(__file__).parent
BATTLE_REPORT = "/tmp/axiom-battle/axiom_battle_v3_report.json"
INSIGHT_LOG = REPO / "insights" / "daily_insights.jsonl"
INDEX_FILE = REPO / "insights" / "index.json"
PUBLIC_INSIGHT_FILE = REPO / "docs" / "daily_insight.md"

GITHUB_API = "https://api.github.com/repos/zhouhailiang0116/axiom-battle"


def get_token():
    """从环境变量获取GitHub token，CI环境用secrets.GITHUB_TOKEN，本地开发用GITHUB_TOKEN环境变量"""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("❌ 未找到GitHub token，设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)
    return token


def run_battle():
    """运行 axiom_battle，返回报告路径"""
    from axiom_battle.arena_log import ArenaLogger

    os.makedirs("/tmp/axiom-battle", exist_ok=True)

    # axiom_battle 已通过 pip install -e . 安装，直接 import
    from axiom_battle.axioms import AXIOM_REGISTRY_V3
    from axiom_battle.axiom_arena import AxiomArena

    arena_path = str(REPO / "arena_log.jsonl")
    arena = AxiomArena(arena_path)

    results = []
    for name, cls in AXIOM_REGISTRY_V3.items():
        case = cls().run()
        results.append(case.to_dict())
        arena.record(
            axiom_id=name,
            event={
                "ALIVE": "alive",
                "STRENGTHENED": "strengthen",
                "MODIFIED": "modify",
                "DEAD": "death",
            }.get(case.verdict, "alive"),
            survival_pressure=case.survival_pressure,
            reason=case.verdict_reason,
            attack_summary=f"v3: {len(case.attacks)} attacks",
        )

    output = {
        "v3_results": results,
        "arena_summary": arena.summary(),
        "generated_at": str(date.today()),
    }

    with open(BATTLE_REPORT, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    return BATTLE_REPORT


def extract_insights_from_report(report_path: str, today: str):
    """从报告提取洞察（简化版，不依赖 insight_extractor）"""
    with open(report_path) as f:
        report = json.load(f)

    insights = []
    for r in report.get("v3_results", []):
        attacks = r.get("attacks", [])
        if not attacks:
            continue
        top_attack = max(attacks, key=lambda a: a.get("pressure", 0))
        insights.append({
            "date": today,
            "axiom_id": r.get("axiom_id"),
            "axiom_name": r.get("axiom_name"),
            "verdict": r.get("verdict"),
            "survival_pressure": r.get("survival_pressure"),
            "attack_type": top_attack.get("type"),
            "attack_description": top_attack.get("description"),
            "causal_chain": top_attack.get("causal_chain", ""),
            "insight_text": top_attack.get("insight", ""),
            "axiom_statement": r.get("axiom_statement"),
        })

    # 优先 DEAD > MODIFIED > STRENGTHENED > ALIVE
    priority = {"DEAD": 0, "MODIFIED": 1, "STRENGTHENED": 2, "ALIVE": 3}
    insights.sort(key=lambda i: priority.get(i["verdict"], 99))
    return insights


def generate_public_file(top_insight: dict, all_insights: list, date_str: str):
    """生成 docs/daily_insight.md"""
    ep_block = f"\n\n> **认识论反思：** {top_insight.get('causal_chain', '')}"

    md = f"""# axiom-battle 每日洞察

**{date_str}**

---

## 今日头条

**{top_insight['axiom_name']}公理 #{top_insight['axiom_id']}** | {top_insight['verdict']} | 生存压力 {top_insight['survival_pressure']:.0%}

- **攻击类型：** {top_insight['attack_type']}
- **攻击描述：** {top_insight['attack_description']}
- **洞察：** {top_insight['insight_text']}{ep_block}

---

## 历史洞察（最近10条）

"""
    for i in all_insights[-10:]:
        md += f"**{i['date']}** | {i['axiom_name']} | {i['verdict']} | {i['insight_text'][:60]}...\n"

    md += f"""
**数据格式：** `insights/daily_insights.jsonl`（机器可读，JSONL每行一条）
**索引：** `insights/index.json`
**更新：** 每天 14:00 UTC
**来源：** axiom-battle 自动对抗系统
"""
    with open(PUBLIC_INSIGHT_FILE, "w") as f:
        f.write(md)


def generate_jsonl_files(top_insight: dict, all_insights: list):
    """生成 docs/insight.jsonl 和 docs/insights_all.jsonl"""
    AGENT_JSONL = REPO / "docs" / "insight.jsonl"
    ALL_AGENT_JSONL = REPO / "docs" / "insights_all.jsonl"

    # 追加单条到 insight.jsonl
    with open(AGENT_JSONL, "a") as f:
        f.write(json.dumps(top_insight, ensure_ascii=False) + "\n")

    # 重写完整历史
    with open(ALL_AGENT_JSONL, "w") as f:
        for i in all_insights:
            f.write(json.dumps(i, ensure_ascii=False) + "\n")


def update_index(all_insights: list):
    """生成 insights/index.json"""
    index = [
        {
            "date": i["date"],
            "axiom_id": i["axiom_id"],
            "verdict": i["verdict"],
            "insight": i["insight_text"][:100],
        }
        for i in all_insights
    ]
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def push_to_github(filepath: str, message: str, branch: str = "gh-pages", token: str = None):
    """通过 GitHub Contents API 推送文件到指定分支"""
    token = token or get_token()
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    # 转换本地路径为仓库内的路径
    if str(filepath).startswith(str(REPO)):
        path_in_repo = str(filepath)[len(str(REPO)) + 1:]
    elif "docs/" in filepath:
        path_in_repo = filepath if filepath.startswith("docs/") else f"docs/{Path(filepath).name}"
    elif "insights/" in filepath:
        path_in_repo = filepath if filepath.startswith("insights/") else f"insights/{Path(filepath).name}"
    else:
        path_in_repo = Path(filepath).name

    # 获取当前 SHA（如果文件已存在）
    sha = None
    url = f"{GITHUB_API}/contents/{path_in_repo}"
    params = {"ref": branch}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    if r.status_code == 200:
        sha = r.json().get("sha")

    # 上传文件
    with open(filepath, "rb") as f:
        encoded = __import__("base64").b64encode(f.read()).decode()

    payload = {
        "message": message,
        "content": encoded,
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    r2 = requests.put(url, headers=headers, json=payload, timeout=20)
    resp = r2.json()
    if "commit" in resp:
        print(f"✅ {path_in_repo}: {resp['commit']['message'][:60]}")
        return True
    else:
        print(f"❌ {path_in_repo}: {resp.get('message', str(resp)[:80])}")
        return False


if __name__ == "__main__":
    today = str(date.today())
    token = get_token()
    print(f"[{today}] axiom-battle 每日洞察生成器")

    # 1. 运行 battle
    print("▶ 运行对抗...")
    try:
        run_battle()
        print("  ✅ battle 完成")
    except Exception as e:
        print(f"  ⚠️ battle 失败: {e}，使用已有报告")
        if not Path(BATTLE_REPORT).exists():
            print("  ❌ 没有可用报告，退出")
            sys.exit(1)

    # 2. 提取洞察
    print("▶ 提取洞察...")
    insights = extract_insights_from_report(BATTLE_REPORT, today)
    print(f"  提取到 {len(insights)} 条洞察")

    if not insights:
        print("  ❌ 没有洞察，退出")
        sys.exit(1)

    top = insights[0]
    print(f"  头条洞察: [{top['verdict']}] {top['axiom_name']} - {top['insight_text'][:60]}...")

    # 3. 生成公开文件
    all_history = insights  # 简化：只用当天的
    generate_public_file(top, all_history, today)
    generate_jsonl_files(top, all_history)
    update_index(all_history)
    print(f"  ✅ 生成文件完成")

    # 4. 推送到 GitHub gh-pages
    print("▶ 推送到 GitHub gh-pages...")
    files_to_push = [
        (str(PUBLIC_INSIGHT_FILE), f"docs: daily insight {today}"),
        (str(INDEX_FILE), f"insights: update index {today}"),
        (str(REPO / "docs" / "insight.jsonl"), f"docs: daily insight.jsonl {today}"),
        (str(REPO / "docs" / "insights_all.jsonl"), f"docs: insights_all.jsonl {today}"),
    ]
    for fp, msg in files_to_push:
        if Path(fp).exists():
            push_to_github(fp, msg, token=token)

    print(f"\n✅ [{today}] 洞察推送完成")
    print(f"   头条: {top['verdict']} {top['axiom_name']} - survival pressure {top['survival_pressure']:.0%}")
