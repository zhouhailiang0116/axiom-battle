"""
axiom4_layout 物理锚点实验 v3
==============================
关键修复：
1. 环境生成：保证连通性（用BFS验证起点到终点可达）
2. 探索Agent：对比BFS展开（真正的系统性探索）vs 随机基线

BFS展开 = "差异感知"的精确物理实现
- BFS frontier = 已探测区域与未探测区域的边界
- axiom4_layout说"差异结构化即论证" → BFS frontier就是差异结构的精确定义
"""

import random
from dataclasses import dataclass, field
from typing import Optional
from collections import deque


# ============================================================
# 环境（保证连通性）
# ============================================================

@dataclass
class GridWorld:
    width: int = 20
    height: int = 20
    obstacles: set[tuple[int, int]] = field(default_factory=set)

    def __post_init__(self):
        # 先生成障碍，再验证连通性，不通就重建
        for _ in range(100):  # 最多100次重试
            self.obstacles.clear()
            for x in range(self.width):
                for y in range(self.height):
                    if (x, y) not in [(1, 1), (18, 18)] and random.random() < 0.15:
                        self.obstacles.add((x, y))
            if self._is_connected((1, 1), (18, 18)):
                return
        # 最后一次尝试：清空所有障碍保证连通
        self.obstacles.clear()

    def _is_connected(self, start: tuple[int, int], goal: tuple[int, int]) -> bool:
        """BFS验证起点到终点是否连通"""
        visited = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                return True
            for nx, ny in self.neighbors(x, y):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return False

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.obstacles

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(nx, ny) for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                if self.is_valid(nx, ny)]

    @property
    def free_cells(self) -> int:
        return self.width * self.height - len(self.obstacles)


# ============================================================
# 任务
# ============================================================

@dataclass
class NavigationTask:
    start: tuple[int, int] = (1, 1)
    goal: tuple[int, int] = (18, 18)
    max_steps: int = 500

    def reset(self) -> tuple[int, int]:
        return self.start

    def step(self, pos: tuple[int, int]) -> tuple[float, bool]:
        return (1.0, True) if pos == self.goal else (0.0, False)


@dataclass
class ExplorationTask:
    start: tuple[int, int] = (1, 1)
    max_steps: int = 300

    def reset(self) -> tuple[int, int]:
        return self.start


# ============================================================
# Agent基类
# ============================================================

class Agent:
    def __init__(self, env: GridWorld, task):
        self.env = env
        self.task = task
        self.pos: Optional[tuple[int, int]] = None
        self.steps: int = 0
        self.visited: set[tuple[int, int]] = set()

    def reset(self) -> tuple[int, int]:
        self.pos = self.task.start
        self.steps = 0
        self.visited = {self.pos}
        return self.pos

    def step(self, action: tuple[int, int]) -> tuple[tuple[int, int], float, bool]:
        if self.env.is_valid(*action):
            self.pos = action
        self.visited.add(self.pos)
        self.steps += 1
        done = self.steps >= self.task.max_steps
        return self.pos, 0.0, done


# ============================================================
# 控制组：纯随机游走
# ============================================================

class RandomAgent(Agent):
    def choose_action(self) -> tuple[int, int]:
        options = self.env.neighbors(*self.pos)
        return random.choice(options) if options else self.pos


# ============================================================
# 控制组：贪心朝向终点
# ============================================================

class GreedyNavAgent(Agent):
    def choose_action(self) -> tuple[int, int]:
        x, y = self.pos
        gx, gy = self.task.goal
        options = self.env.neighbors(x, y)
        if not options:
            return self.pos
        # 贪心选曼哈顿距离减少最多的
        best = min(options, key=lambda p: abs(p[0]-gx) + abs(p[1]-gy))
        return best


# ============================================================
# 实验组：BFS展开探索Agent
# axiom4_layout的精确物理实现：
# "差异关系结构化" = BFS frontier（已探测区域与未探测区域的边界）
# ============================================================

class BFSFrontierAgent(Agent):
    """
    axiom4_layout核心实现：
    - 已探测区域：self.visited
    - 未探测区域：所有其他可达格子
    - 差异边界：BFS frontier = reachable unvisited cells at minimum distance from visited set
    - 策略：每次朝BFS frontier移动，同时朝向目标（加权组合）
    """

    def __init__(self, env: GridWorld, task):
        super().__init__(env, task)
        self.frontier: set[tuple[int, int]] = set()

    def reset(self) -> tuple[int, int]:
        pos = super().reset()
        self._update_frontier()
        return pos

    def _update_frontier(self):
        """计算BFS frontier: 已访问区域周围的第一层未访问可达格子"""
        self.frontier.clear()
        boundary = deque(self.visited)
        explored = set(self.visited)
        steps = 0
        while boundary and steps < 1000:  # 展开到最多1000个frontier格子
            for _ in range(len(boundary)):
                x, y = boundary.popleft()
                for nx, ny in self.env.neighbors(x, y):
                    if (nx, ny) not in explored:
                        explored.add((nx, ny))
                        self.frontier.add((nx, ny))
                        boundary.append((nx, ny))
            steps += 1

    def step(self, action: tuple[int, int]) -> tuple[tuple[int, int], float, bool]:
        result = super().step(action)
        self._update_frontier()
        return result

    def choose_action(self) -> tuple[int, int]:
        options = self.env.neighbors(*self.pos)
        if not options:
            return self.pos

        # 检查是否有goal属性（NavigationTask有，ExplorationTask没有）
        has_goal = hasattr(self.task, 'goal')

        scored = []
        for ox, oy in options:
            if has_goal:
                gx, gy = self.task.goal
                goal_score = -(abs(ox - gx) + abs(oy - gy))
            else:
                goal_score = 0
            # 探索得分：在frontier里 +1，在visited里 -1
            if (ox, oy) in self.frontier:
                explore_score = 1.0
            elif (ox, oy) not in self.visited:
                explore_score = 0.5
            else:
                explore_score = -1.0
            # 有目标时：70%目标 + 30%探索；无目标时：纯frontier
            if has_goal:
                total = 0.7 * goal_score + 0.3 * explore_score * 100
            else:
                total = explore_score * 100
            scored.append((ox, oy, total))

        scored.sort(key=lambda t: t[2], reverse=True)
        return (scored[0][0], scored[0][1])


# ============================================================
# 实验组：BFS到frontier（纯探索，无目标）
# ============================================================

class PureExplorationAgent(Agent):
    """
    纯frontier探索：完全不考虑目标，只管最大化覆盖率
    对比用：看"朝向目标"是否帮了还是害了探索
    """

    def __init__(self, env: GridWorld, task):
        super().__init__(env, task)
        self.frontier: set[tuple[int, int]] = set()

    def reset(self) -> tuple[int, int]:
        pos = super().reset()
        self._update_frontier()
        return pos

    def _update_frontier(self):
        self.frontier.clear()
        boundary = deque(self.visited)
        explored = set(self.visited)
        steps = 0
        while boundary and steps < 1000:
            for _ in range(len(boundary)):
                x, y = boundary.popleft()
                for nx, ny in self.env.neighbors(x, y):
                    if (nx, ny) not in explored:
                        explored.add((nx, ny))
                        self.frontier.add((nx, ny))
                        boundary.append((nx, ny))
            steps += 1

    def step(self, action: tuple[int, int]) -> tuple[tuple[int, int], float, bool]:
        result = super().step(action)
        self._update_frontier()
        return result

    def choose_action(self) -> tuple[int, int]:
        options = self.env.neighbors(*self.pos)
        if not options:
            return self.pos
        # 优先选frontier格子，次选未访问格子
        scored = []
        for ox, oy in options:
            if (ox, oy) in self.frontier:
                score = 2.0
            elif (ox, oy) not in self.visited:
                score = 1.0
            else:
                score = 0.0
            scored.append((ox, oy, score))
        scored.sort(key=lambda t: t[2], reverse=True)
        return (scored[0][0], scored[0][1])


# ============================================================
# 实验运行
# ============================================================

def run_navigation(agent_class, seed: int) -> dict:
    random.seed(seed)
    env = GridWorld()
    task = NavigationTask()
    agent = agent_class(env, task)
    agent.reset()
    for _ in range(task.max_steps):
        if agent.pos == task.goal:
            return {"reached": True, "steps": agent.steps}
        agent.step(agent.choose_action())
    return {"reached": False, "steps": agent.steps}


def run_exploration(agent_class, seed: int) -> dict:
    random.seed(seed)
    env = GridWorld()
    task = ExplorationTask()
    agent = agent_class(env, task)
    agent.reset()
    for _ in range(task.max_steps):
        agent.step(agent.choose_action())
    return {
        "coverage": len(agent.visited) / agent.env.free_cells,
        "n_visited": len(agent.visited),
        "total": agent.env.free_cells,
    }


def run_all(n: int = 200) -> dict:
    nav_results = {"Random": [], "Greedy": []}
    exp_results = {"Random": [], "PureFrontier": [], "BFSFrontier": []}

    for seed in range(n):
        nav_results["Random"].append(run_navigation(RandomAgent, seed))
        nav_results["Greedy"].append(run_navigation(GreedyNavAgent, seed))
        exp_results["Random"].append(run_exploration(RandomAgent, seed))
        exp_results["PureFrontier"].append(run_exploration(PureExplorationAgent, seed))
        exp_results["BFSFrontier"].append(run_exploration(BFSFrontierAgent, seed))

    def avg(lst, key):
        vals = [x[key] for x in lst if x.get(key) is not None]
        return sum(vals) / len(vals) if vals else 0

    def sr(lst):
        return sum(1 for x in lst if x["reached"]) / len(lst)

    return {
        "n": n,
        "nav": {
            "Random": {"sr": sr(nav_results["Random"]), "avg_steps": avg([x for x in nav_results["Random"] if x["reached"]], "steps")},
            "Greedy": {"sr": sr(nav_results["Greedy"]), "avg_steps": avg([x for x in nav_results["Greedy"] if x["reached"]], "steps")},
        },
        "exp": {
            "Random": {"cov": avg(exp_results["Random"], "coverage")},
            "PureFrontier": {"cov": avg(exp_results["PureFrontier"], "coverage")},
            "BFSFrontier": {"cov": avg(exp_results["BFSFrontier"], "coverage")},
        },
    }


def print_report(r: dict):
    n = r["n"]
    print("=" * 65)
    print("axiom4_layout 物理锚点实验 v3")
    print("=" * 65)
    print(f"实验次数: {n}")
    print()

    print("【任务A：导航】固定起点→终点")
    print(f"  RandomAgent:   成功率 {r['nav']['Random']['sr']:.1%}")
    print(f"  GreedyNavAgent: 成功率 {r['nav']['Greedy']['sr']:.1%}")
    nav_diff = r['nav']['Greedy']['sr'] - r['nav']['Random']['sr']
    print(f"  贪心 vs 随机: {nav_diff:+.1%}")
    print()

    print("【任务B：探索】300步内最大化覆盖率")
    rand_cov = r['exp']['Random']['cov']
    pure_cov = r['exp']['PureFrontier']['cov']
    bfs_cov = r['exp']['BFSFrontier']['cov']
    print(f"  RandomAgent:       覆盖率 {rand_cov:.1%}")
    print(f"  PureFrontierAgent: 覆盖率 {pure_cov:.1%}  ← axiom4_layout核心实现")
    print(f"  BFSFrontierAgent:  覆盖率 {bfs_cov:.1%}  ← axiom4_layout+目标导航")
    print()
    print(f"  PureFrontier vs Random: {pure_cov - rand_cov:+.1%}")
    print(f"  BFSFrontier  vs Random: {bfs_cov - rand_cov:+.1%}")

    # 95% CI
    def ci(p, n):
        return 1.96 * ((p * (1 - p) / n) ** 0.5)
    print(f"  95%置信区间: ±{ci(bfs_cov, n):.1%}")
    print()

    if bfs_cov - rand_cov > 0.08:
        print("结论: 公理有物理效力 — BFS frontier探索显著优于随机")
    elif pure_cov - rand_cov < 0.02 and bfs_cov - rand_cov < 0.02:
        print("结论: 公理无效 — frontier策略无显著优势（随机基线已够好）")
    else:
        print("结论: 效果有限 — frontier有优势但不大")
    print("=" * 65)


if __name__ == "__main__":
    print("启动 axiom4_layout 物理锚点实验 v3...")
    print()
    results = run_all(n=200)
    print_report(results)