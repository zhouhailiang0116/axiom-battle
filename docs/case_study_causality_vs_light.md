---
layout: default
title: axiom-battle实战案例：因果vs光影
---

# axiom-battle 实战案例：因果 vs 光影

## 运行结果

以下是一次真实的对抗结果（seed=42）：

**攻击方：axiom 8（因果）**
**防守方：axiom 2（光影）**
**攻击类型：反向攻击**
**判决：MODIFIED**

判决理由：反向攻击帧占比 90.9%，处于灰色地带。axiom 8 需要加约束条件（如 domain 或 threshold）。

---

## 20 次对抗后的公理排名

| 排名 | 公理 | 存活次数 | 死亡次数 | 平均强度 |
|------|------|---------|---------|---------|
| 1 | axiom 2（光影） | 20 | 0 | 0.091 |
| 2 | axiom 8（因果） | 20 | 0 | 0.909 |
| 3 | axiom 1（生长） | 0 | 0 | 1.000 |
| 4 | axiom 3（色彩） | 0 | 0 | 1.000 |
| 5 | axiom 4（布局） | 0 | 0 | 1.000 |
| 6 | axiom 5（叙事） | 0 | 0 | 1.000 |
| 7 | axiom 6（边界） | 0 | 0 | 1.000 |
| 8 | axiom 7（自由） | 0 | 0 | 1.000 |


---

## 这个案例说明了什么

### 因果公理（axiom 8）的局限

因果公理主张"理由是原因，不是解释"——它要求事件必须有可追溯的因果链。

但光影公理（axiom 2）主张"差异是真实，不是表象"——它关注的不是因果链，而是**感知差异本身**。

两者冲突时，因果公理被"修正"（MODIFIED）而非被"推翻"（DEAD），这说明：**光影公理不需要因果解释来支撑自己的有效性，感知差异本身就是证据。**

这是一个重要的哲学发现：**不是所有"真实"都需要因果链来背书。**

---

## 怎么跑自己的实验

```bash
pip install git+https://github.com/zhouhailiang0116/axiom-battle.git
```

然后：

```python
from axiom_battle import AxiomBattle, AxiomArena

# 单次对抗
result = AxiomBattle().auto_battle()[0]
print(f"判决: {result.judgment.name}")

# 竞技场循环
arena = AxiomArena(log_path="./my_arena.json")
for i in range(100):
    b = AxiomBattle()
    r = b.auto_battle()[0]
    arena.record(r.axiom_pair[0], "alive")
    arena.record(r.axiom_pair[1], "alive")

# 查看排名
for id_, data in arena.ranking():
    print(f"axiom{id_}({data['name']}): 存活{data['alive_count']}次")
```

---

## 核心发现

axiom-battle 的价值不在于给每个公理打分，而在于**发现公理之间的隐藏关系**。

上面的案例里，"因果"与"光影"的冲突揭示了一个反直觉的结论：感知差异的"真实性"不依赖因果链。

这是传统评估体系永远发现不了的——因为它需要公理之间真正碰撞。

---

*源码：https://github.com/zhouhailiang0116/axiom-battle*
