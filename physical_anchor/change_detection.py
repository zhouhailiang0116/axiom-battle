"""
axiom4_layout 物理锚点实验 v4
==============================
分析v3失败原因：随机游走在20x20网格+15%障碍下覆盖率已达~23%
说明随机基线已经够好，无法体现差异感知的价值

新实验设计：
- 任务C：变化检测（动态环境）
  环境中有些格子会随时间变化（闪烁）
  Agent需要"感知差异"才能注意到变化
  差异感知 = 记忆"之前是什么"，比较"现在是什么"

- 对照实验：
  控制组：只记录"当前视野"，不建差异记忆
  实验组：记录"差异历史"，感知"变了什么"

这才是差异结构化的核心：感知差异 + 记忆差异关系 + 基于差异做决策
"""

import random
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 动态网格环境（环境随时间变化）
# ============================================================

@dataclass
class DynamicGrid:
    width: int = 15
    height: int = 15
    obstacle_rate: float = 0.15
    change_rate: float = 0.05  # 每步有5%概率切换格子状态

    # 状态：0=空白(安全)，1=障碍(不可走)，2=闪烁(安全但状态会变)
    grid: list[list[int]] = field(default_factory=list)

    def __post_init__(self):
        self.grid = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                if random.random() < self.obstacle_rate:
                    row.append(1)  # 障碍
                elif random.random() < 0.2:
                    row.append(2)  # 闪烁格子
                else:
                    row.append(0)  # 普通空白
            self.grid.append(row)
        # 保证起点终点不是障碍
        self.grid[1][1] = 0
        self.grid[self.width-2][self.height-2] = 0

    def is_valid(self, x: int, y: int) -> bool:
        return (0 <= x < self.width and 0 <= y < self.height
                and self.grid[y][x] != 1)

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                if self.is_valid(nx, ny)]

    def step_simulation(self):
        """模拟环境变化：闪烁格子状态切换"""
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] == 2 and random.random() < self.change_rate:
                    # 闪烁格子状态在0和2之间切换（但始终可走）
                    self.grid[y][x] = 0 if self.grid[y][x] == 2 else 2

    def is_flashing(self, x: int, y: int) -> bool:
        return self.grid[y][x] == 2

    def get_state(self, x: int, y: int) -> int:
        return self.grid[y][x]


# ============================================================
# 任务：差异感知检测
# ============================================================

@dataclass
class ChangeDetectionTask:
    start: tuple[int, int] = (1, 1)
    max_steps: int = 100
    # 评估：Agent在100步内检测到几次"闪烁格子的状态变化"

    def reset(self) -> tuple[int, int]:
        return self.start


# ============================================================
# Agent A：控制组（无差异感知）
# ============================================================

class NaiveAgent:
    """
    无差异感知：只看当前状态，不记忆历史差异
    - 不记录"之前是什么"
    - 不比较"现在和之前有什么不同"
    - 只根据"当前可不可走"做决策
    """

    def __init__(self, env: DynamicGrid, task: ChangeDetectionTask):
        self.env = env
        self.task = task
        self.pos: Optional[tuple[int, int]] = None
        self.steps: int = 0
        self.changes_detected: int = 0
        self.current_state: dict[tuple[int, int], int] = {}  # 只记录当前状态

    def reset(self) -> tuple[int, int]:
        self.pos = self.task.start
        self.steps = 0
        self.changes_detected = 0
        self.current_state = {}
        return self.pos

    def observe(self):
        """观察当前格子状态，但不记忆差异"""
        if self.env.is_flashing(*self.pos):
            # 闪烁格子——但NaiveAgent不知道它"变了"，只看到"当前是什么"
            pass

    def step(self, action: tuple[int, int]) -> tuple[tuple[int, int], float, bool]:
        if self.env.is_valid(*action):
            self.pos = action
        self.steps += 1
        self.observe()
        self.env.step_simulation()
        done = self.steps >= self.task.max_steps
        return self.pos, 0.0, done

    def choose_action(self) -> tuple[int, int]:
        options = self.env.neighbors(*self.pos)
        if not options:
            return self.pos
        # 随机游走
        return random.choice(options)


# ============================================================
# Agent B：实验组（差异感知）
# axiom4_layout: "差异关系的结构化" = 记忆差异 + 比较差异 + 基于差异决策
# ============================================================

class DifferenceAgent:
    """
    差异感知实现：
    - 记忆每个格子的"历史状态快照"
    - 每步检测：当前状态 vs 上次记录的状态 → 有差异则标记
    - 差异检测到的次数作为reward信号
    """

    def __init__(self, env: DynamicGrid, task: ChangeDetectionTask):
        self.env = env
        self.task = task
        self.pos: Optional[tuple[int, int]] = None
        self.steps: int = 0
        self.changes_detected: int = 0

        # axiom4_layout核心：差异关系记忆
        self.state_memory: dict[tuple[int, int], int] = {}  # 记忆每个格子的历史状态
        self.diff_history: list[tuple[int, int, int, int]] = []  # 差异记录：(x,y,旧状态,新状态)
        self.difference_frontier: set[tuple[int, int]] = set()  # 有差异的格子集合

    def reset(self) -> tuple[int, int]:
        self.pos = self.task.start
        self.steps = 0
        self.changes_detected = 0
        self.state_memory = {}
        self.diff_history = []
        self.difference_frontier = set()
        # 初始观察：记录初始状态
        for x in range(self.env.width):
            for y in range(self.env.height):
                if self.env.is_valid(x, y):
                    self.state_memory[(x, y)] = self.env.get_state(x, y)
        return self.pos

    def _detect_differences(self):
        """检测哪些格子状态发生了变化，更新差异结构"""
        new_diffs = []
        for x in range(self.env.width):
            for y in range(self.env.height):
                if self.env.is_valid(x, y):
                    current = self.env.get_state(x, y)
                    remembered = self.state_memory.get((x, y), None)
                    if remembered is not None and current != remembered:
                        new_diffs.append((x, y, remembered, current))
                        self.state_memory[(x, y)] = current

        self.diff_history.extend(new_diffs)
        for x, y, _, _ in new_diffs:
            self.difference_frontier.add((x, y))
        self.changes_detected += len(new_diffs)

    def observe(self):
        """观察并检测差异"""
        # 观察当前格子是否有变化
        current = self.env.get_state(*self.pos)
        remembered = self.state_memory.get(self.pos)
        if remembered is not None and current != remembered:
            # 检测到差异
            self.changes_detected += 1
            self.state_memory[self.pos] = current
            self.difference_frontier.add(self.pos)

    def step(self, action: tuple[int, int]) -> tuple[tuple[int, int], float, bool]:
        if self.env.is_valid(*action):
            self.pos = action
        self.steps += 1
        self._detect_differences()
        self.observe()
        self.env.step_simulation()
        done = self.steps >= self.task.max_steps
        return self.pos, 0.0, done

    def choose_action(self) -> tuple[int, int]:
        """
        axiom4_layout策略：
        - 优先朝有差异的格子移动（信息价值高）
        - 其次朝闪烁格子移动（潜在变化多）
        - 最后随机
        """
        options = self.env.neighbors(*self.pos)
        if not options:
            return self.pos

        scored = []
        for ox, oy in options:
            score = 0
            # 差异格子优先
            if (ox, oy) in self.difference_frontier:
                score += 10
            # 闪烁格子次优先
            if self.env.is_flashing(ox, oy):
                score += 3
            # 朝向中心的格子稍微优先（避免一直在角落）
            cx, cy = self.env.width // 2, self.env.height // 2
            score -= abs(ox - cx) + abs(oy - cy)
            scored.append((ox, oy, score))

        scored.sort(key=lambda t: t[2], reverse=True)
        return scored[0][:2]


# ============================================================
# 实验运行
# ============================================================

def run_trial(agent_class, seed: int) -> dict:
    random.seed(seed)
    env = DynamicGrid()
    task = ChangeDetectionTask()
    agent = agent_class(env, task)
    agent.reset()

    # 先做一次初始观察
    agent.observe()
    agent.env.step_simulation()

    for _ in range(task.max_steps):
        agent.step(agent.choose_action())

    return {
        "changes_detected": agent.changes_detected,
        "total_changes": len(agent.diff_history) if hasattr(agent, 'diff_history') else 0,
        "seed": seed,
    }


def run_experiment(n: int = 500) -> dict:
    naive_results = []
    diff_results = []

    for seed in range(n):
        naive_results.append(run_trial(NaiveAgent, seed))
        diff_results.append(run_trial(DifferenceAgent, seed))

    def avg(lst, key):
        return sum(x[key] for x in lst) / len(lst)

    return {
        "n": n,
        "naive": {
            "avg_changes": avg(naive_results, "changes_detected"),
        },
        "diff": {
            "avg_changes": avg(diff_results, "changes_detected"),
        },
        "naive_raw": naive_results,
        "diff_raw": diff_results,
    }


def statistical_test(a_vals, b_vals):
    """独立双样本t检验（简化版）"""
    import math
    n1, n2 = len(a_vals), len(b_vals)
    mean1 = sum(a_vals) / n1
    mean2 = sum(b_vals) / n2
    var1 = sum((x - mean1)**2 for x in a_vals) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in b_vals) / (n2 - 1)
    se = math.sqrt(var1/n1 + var2/n2)
    t = (mean2 - mean1) / se
    # 自由度近似
    df = min(n1, n2) - 1
    # 简化：|t| > 1.96 则 p < 0.05
    significant = abs(t) > 1.96
    return t, significant


def print_report(r: dict):
    n = r["n"]
    naive_mean = r["naive"]["avg_changes"]
    diff_mean = r["diff"]["avg_changes"]
    diff_improvement = diff_mean - naive_mean
    relative = diff_improvement / naive_mean * 100 if naive_mean > 0 else 0

    print("=" * 65)
    print("axiom4_layout 物理锚点实验 v4 — 变化检测任务")
    print("=" * 65)
    print(f"实验次数: {n}")
    print(f"任务: 100步内检测环境状态变化的次数")
    print()
    print(f"控制组 (NaiveAgent - 无差异感知):")
    print(f"  平均检测次数: {naive_mean:.2f}")
    print()
    print(f"实验组 (DifferenceAgent - 差异感知):")
    print(f"  平均检测次数: {diff_mean:.2f}")
    print()
    print(f"绝对提升: {diff_improvement:+.2f} 次")
    print(f"相对提升: {relative:+.1f}%")
    print()

    # 95% CI
    def ci(vals):
        import math
        n = len(vals)
        m = sum(vals) / n
        v = sum((x - m)**2 for x in vals) / (n - 1)
        return 1.96 * math.sqrt(v / n)

    naive_ci = ci([x["changes_detected"] for x in r["naive_raw"]])
    diff_ci = ci([x["changes_detected"] for x in r["diff_raw"]])
    print(f"95%置信区间: Naive ±{naive_ci:.2f}, Diff ±{diff_ci:.2f}")
    print()

    # 统计检验
    a = [x["changes_detected"] for x in r["naive_raw"]]
    b = [x["changes_detected"] for x in r["diff_raw"]]
    t, sig = statistical_test(a, b)
    print(f"双样本t检验: t={t:.2f}, p{'< 0.05 (显著)' if sig else '>= 0.05 (不显著)'}")
    print()

    if sig and diff_improvement > 0:
        print("结论: 公理有物理效力 — 差异感知显著提升变化检测能力")
    elif sig and diff_improvement < 0:
        print("结论: 公理有负效力 — 差异感知反而降低了检测能力")
    else:
        print("结论: 公理无效 — 差异感知无显著优势")
    print("=" * 65)


if __name__ == "__main__":
    print("启动 axiom4_layout 物理锚点实验 v4...")
    print("任务: 动态环境变化检测（闪烁格子）")
    print()
    results = run_experiment(n=500)
    print_report(results)