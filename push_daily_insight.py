#!/usr/bin/env python3
"""
每日 axiom_battle 洞察推送到 GitHub
.run_battle() → 提取洞察 → 写 insight.jsonl → GitHub API push
"""
import json
import sys
import subprocess
from pathlib import Path
from datetime import date

# ── 路径配置 ───────────────────────────────────────────────
REPO = Path(__file__).parent
BATTLE_REPORT = "/tmp/axiom-battle/axiom_battle_v3_report.json"
INSIGHT_LOG = REPO / "insights" / "daily_insights.jsonl"
INDEX_FILE = REPO / "insights" / "index.json"
PUBLIC_INSIGHT_FILE = REPO / "docs" / "daily_insight.md"

sys.path.insert(0, str(REPO))
from axiom_battle.insight_extractor import (
    extract_insight_from_case,
    extract_from_v3_report,
    save_insight,
    load_history,
)

import os
TOKEN = os.environ.get("GITHUB_PAT", "")
if not TOKEN:
    # Fallback for local development only — do NOT commit real token
    TOKEN = ""
GITHUB_API = "https://api.github.com/repos/zhouhailiang0116/axiom-battle"


def run_battle():
    """运行 axiom_battle，返回报告路径"""
    import os
    os.makedirs("/tmp/axiom-battle", exist_ok=True)
    # 确保 axiom_battle 可导入
    sys.path.insert(0, str(REPO))
    from axiom_battle.axioms import AXIOM_REGISTRY, AXIOM_REGISTRY_V2, AXIOM_REGISTRY_V3
    from axiom_battle.axiom_arena import AxiomArena

    arena_path = str(REPO / "arena_log.jsonl")
    arena = AxiomArena(arena_path)

    all_results = {}
    for label, registry in [("v1", AXIOM_REGISTRY), ("v2", AXIOM_REGISTRY_V2), ("v3", AXIOM_REGISTRY_V3)]:
        results = []
        for name, cls in registry.items():
            case = cls().run()
            results.append(case.to_dict())
            arena.record(
                axiom_id=name,
                event={"ALIVE": "alive", "STRENGTHENED": "strengthen", "MODIFIED": "modify", "DEAD": "death"}.get(case.verdict, "alive"),
                survival_pressure=case.survival_pressure,
                reason=case.verdict_reason,
                attack_summary=f"{label}: {len(case.attacks)} attacks",
            )
        all_results[f"{label}_results"] = results

    output = {
        **all_results,
        "arena_summary": arena.summary(),
        "generated_at": str(date.today()),
    }
    with open(BATTLE_REPORT, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    return BATTLE_REPORT


def pick_top_insight(insights) -> dict:
    """选择最有价值的洞察（DEAD > MODIFIED > STRENGTHENED > ALIVE）"""
    priority = {"DEAD": 0, "MODIFIED": 1, "STRENGTHENED": 2, "ALIVE": 3, "SUSPENDED": 4}
    # 优先选死亡公理（最有新闻价值）
    dead = [i for i in insights if i.verdict == "DEAD"]
    if dead:
        return max(dead, key=lambda i: i.survival_pressure)
    modified = [i for i in insights if i.verdict == "MODIFIED"]
    if modified:
        return max(modified, key=lambda i: i.survival_pressure)
    return insights[0]


def update_public_file(insight, insights: list, date_str: str):
    """生成 docs/daily_insight.md（GitHub Pages 可访问）"""
    content = f"""# axiom-battle 每日洞察

**{date_str}**

---

## 今日最重要的公理对抗结果

{insight.to_markdown()}

---

## 历史洞察（最近10条）

"""
    for i in sorted(insights[-10:], key=lambda x: x.date, reverse=True):
        content += f"**{i.date}** | {i.axiom_name} | {i.verdict} | {i.insight_text[:80]}...\n"

    content += f"""

---

## 完整洞察日志

[查看所有洞察](insights/daily_insights.jsonl)

**数据来源：** axiom-battle 每日自动对抗  
**更新频率：** 每天一次  
**关于 axiom-battle：** https://github.com/zhouhailiang0116/axiom-battle
"""
    with open(PUBLIC_INSIGHT_FILE, "w") as f:
        f.write(content)


def update_index(insights: list):
    """生成 SEO index（JSON 格式，方便爬虫）"""
    index_data = [i.to_search_index_entry() for i in insights]
    with open(INDEX_FILE, "w") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)


def push_to_github(filepath: str, message: str, branch: str = "gh-pages"):
    """通过 GitHub API 推送文件"""
    import base64

    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    # 获取当前 SHA
    import subprocess
    path_in_repo = filepath if "docs/" in filepath else f"docs/{Path(filepath).name}"
    r = subprocess.run(
        ["curl", "-s", "-H", f"Authorization: token {TOKEN}",
         f"{GITHUB_API}/contents/{path_in_repo}"],
        capture_output=True, text=True, timeout=15
    )
    existing = json.loads(r.stdout)
    sha = existing.get("sha")

    # 上传
    data = json.dumps({
        "message": message,
        "content": encoded,
        "sha": sha,
        "branch": branch,
    })
    r2 = subprocess.run(
        ["curl", "-s", "-X", "PUT", "-H", f"Authorization: token {TOKEN}",
         "-H", "Content-Type: application/json", "-d", data,
         f"{GITHUB_API}/contents/{path_in_repo}"],
        capture_output=True, text=True, timeout=20
    )
    resp = json.loads(r2.stdout)
    ok = "commit" in resp
    print(f"{'✅' if ok else '❌'} GitHub API push: {resp.get('commit', {}).get('message', resp.get('message', ''))[:80]}")
    return ok


if __name__ == "__main__":
    today = str(date.today())
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
    insights = extract_from_v3_report(BATTLE_REPORT, today)
    print(f"  提取到 {len(insights)} 条洞察")

    top = pick_top_insight(insights)
    print(f"  头条洞察: [{top.verdict}] {top.axiom_name} - {top.insight_text[:60]}...")

    # 3. 保存到本地历史
    INSIGHT_LOG.parent.mkdir(parents=True, exist_ok=True)
    save_insight(top, str(INSIGHT_LOG))
    print(f"  ✅ 追加到 {INSIGHT_LOG}")

    # 4. 生成公开文件
    all_history = load_history(str(INSIGHT_LOG))
    update_public_file(top, all_history, today)
    update_index(all_history)
    print(f"  ✅ 生成 {PUBLIC_INSIGHT_FILE}")

    # 5. 推送到 GitHub gh-pages
    print("▶ 推送到 GitHub...")
    for fp, msg in [
        (str(PUBLIC_INSIGHT_FILE), f"docs: daily insight {today}"),
        (str(INDEX_FILE), f"insights: update index with {today} insight"),
    ]:
        if Path(fp).exists():
            push_to_github(fp, msg)

    print(f"\n✅ [{today}] 洞察推送完成")
    print(f"   头条: {top.verdict} {top.axiom_name} - {top.survival_pressure:.0%} survival pressure")
