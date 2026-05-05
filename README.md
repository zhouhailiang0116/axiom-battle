# axiom-battle：公理对抗赛引擎

> "最强的公理，最需要被攻击。"
> — 悟道体系·公理哲学

## 什么是公理对抗赛？

axiom-battle 是 Popper 证伪主义的代码化实现。让悟道公理互相攻击、验证、判决，模拟一个没有权威裁判的自我演化系统。

**核心思路：** 给定公理 A，系统生成三种攻击——反向/跨域/反事实——看 A 能否存活。

### 公理体系

| ID | 公理 | 说明 |
|----|------|------|
| 1 | 生长 | 向边界生长 |
| 2 | 光影 | 对比定义形态 |
| 3 | 色彩 | 约束中涌现和谐 |
| 4 | 布局 | 空间即论证 |
| 5 | 叙事 | 序列即因果 |
| 6 | 边界 | 局限赋予意义 |
| 7 | 自由 | 自主需要约束 |
| 8 | 因果 | 因果链不可还原 |

## 三种攻击方式

- **反向攻击**：A 为真时，什么必定为假？
- **跨域攻击**：领域假设变化时 A 还成立吗？
- **反事实攻击**：因果链断裂时会发生什么？

## 五种判决

`ALIVE` / `STRENGTHENED` / `MODIFIED` / `DEAD` / `SUSPENDED`

## 快速开始

```python
# 运行全部公理对抗
from axiom_battle.axioms import AXIOM_REGISTRY
from axiom_battle.axioms.axiom_base import AxiomCase

for name, cls in AXIOM_REGISTRY.items():
    case: AxiomCase = cls().run()
    print(f"{name}: {case.verdict} ({case.survival_pressure:.0%})")
    for atk in case.attacks:
        print(f"  [{atk.severity.name}] {atk.type}: {atk.description[:40]}")
```

输出示例：
```
axiom1_growth: DEAD (0%)
  [HIGH] reverse: ...
  [CRITICAL] counterfactual: ...
axiom2_light: ALIVE (50%)
  [MEDIUM] reverse: ...
```

## 添加新公理

```python
from axiom_battle.axioms.axiom_base import Axiom, Attack, Severity

class MyAxiom(Axiom):
    name = "axiom9_entropy"
    statement = "孤立系统的熵永不减少"
    depends_on = []  # 公理依赖图

    def attack(self) -> list[Attack]:
        return [
            Attack(
                type="reverse",
                description="麦克斯韦妖：隔着边界分类分子，熵减少了",
                severity=Severity.CRITICAL,
                evidence="热力学第二定律在开放系统中可被局部违反",
                expected_impact="熵增公理需要边界条件限定",
            ),
            Attack(
                type="cross_domain",
                description="信息论：信息熵与热力学熵等价吗？",
                severity=Severity.MEDIUM,
                evidence="香农熵是抽象的信息度量，不同于物理熵",
                expected_impact="跨域后熵增定律的形式是否保持？",
            ),
        ]

# 注册（需修改 axioms/__init__.py）
# AXIOM_REGISTRY["axiom9_entropy"] = MyAxiom

case = MyAxiom().run()
print(case.verdict, case.verdict_reason)
```

## 自定义判决策略

```python
from axiom_battle.axioms.axiom_base import Axiom, Attack, Severity, JudgmentPolicy

# 方式1：全局替换
def strict_policy(attacks):
    for a in attacks:
        if a.severity >= Severity.HIGH:
            return "DEAD", "高危攻击存在，拒绝通过", 0.0
    return "ALIVE", "无高危攻击", 1.0

Axiom.default_policy = type("StrictPolicy", (), {
    "evaluate": staticmethod(strict_policy)
})

# 方式2：子类替换
class StrictAxiom(Axiom):
    default_policy = type("StrictPolicy", (), {
        "evaluate": staticmethod(strict_policy)
    })
```

## 公理依赖图

```python
from axiom_battle.axioms import AXIOM_REGISTRY
from axiom_battle.axioms.axiom_base import build_dependency_graph, topological_sort

# 构建依赖图
graph = build_dependency_graph(AXIOM_REGISTRY)
# graph["axiom4_layout"] = ["axiom5_narrative"]
print(graph)

# 拓扑排序（先验证依赖，再验证被依赖者）
order = topological_sort(AXIOM_REGISTRY)
print("验证顺序:", order)
```

## 运行完整对抗报告

```bash
cd axiom-battle
python3 run_battle.py
```

生成 `axiom_battle_v3_report.json` 和 Arena 历史记录 `/tmp/axiom_arena_log.jsonl`。

## 运行测试

```bash
cd axiom-battle
python3 tests/test_battle.py
```

## 目录结构

```
axiom_battle/
├── axiom_base.py          # 公理基类（Axiom/Attack/Severity/JudgmentPolicy）
├── axioms/
│   ├── axiom1_growth.py   # v1 公理
│   ├── axiom_v2_*.py      # v2 精化版
│   └── axiom_v3_*.py      # v3 再精化版
├── axiom_arena.py         # 历史记录与排名追踪
├── axiom_battle_core.py   # 对抗引擎（生成对抗样本/反事实测试）
└── causal_arbitrator.py   # 公理冲突仲裁器
```

## 哲学基础

axiom-battle 来自悟道体系，核心是：没有不可质疑的公理，对抗即验证，死亡不是失败。

## License

MIT
