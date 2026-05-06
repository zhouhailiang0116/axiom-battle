# 公理对抗赛：让 AI 自己证明自己错了

> 最强的公理，最需要被攻击。
> — 悟道体系

## 一个思想实验

假设你有 8 条基本公理，它们共同定义了"什么是好作品"。

现在，让它们互相攻击：公理 A 说"限制产生美"，公理 B 说"自由产生美"——谁对？

正常人会说：要看场景。  
**axiom-battle 说：让它们自己打，打完看结果。**

这就是公理对抗赛。

---

## 什么是 axiom-battle

axiom-battle 是 Popper 证伪主义的代码化实现。它让 8 条悟道公理互相攻击、验证、判决，模拟一个没有权威裁判的自我演化系统。

**不是专家评审，不是人工打分，是公理自己证明自己。**

### 8 条悟道公理

| ID | 公理 | 核心命题 |
|----|------|----------|
| 1 | 生长 | 存在是成长，不是存在 |
| 2 | 光影 | 差异是真实，不是表象 |
| 3 | 色彩 | 情绪是信息，不是噪音 |
| 4 | 布局 | 结构是意义，不是容器 |
| 5 | 叙事 | 时间是因果，不是顺序 |
| 6 | 边界 | 限制是实在，不是障碍 |
| 7 | 自由 | 选择是责任，不是权利 |
| 8 | 因果 | 理由是原因，不是解释 |

### 三种攻击方式

**反向攻击**（最常用）  
"你的结论实际上证明了相反的命题。"  
适用：某公理被过度膨胀、压迫其他公理时。

**跨域攻击**  
"你的逻辑在领域 A 成立，在领域 B 失效。"  
适用：检验公理的普适性边界。

**反事实攻击**  
"如果没有你，情况会怎样？"  
适用：检验公理的不可替代性。

### 五种判决

| 判决 | 含义 |
|------|------|
| ALIVE | 公理存活，攻击无效 |
| STRENGTHENED | 公理被强化，攻击反而证明了它 |
| MODIFIED | 公理被修正，适用范围缩小 |
| DEAD | 公理被推翻 |
| SUSPENDED | 证据不足，暂不判决 |

---

## 快速开始

```python
from axiom_battle import AxiomBattle, AxiomArena

# 单次对抗
battle = AxiomBattle()
result = battle.auto_battle()[0]
print(f"Judgment: {result.judgment.name}")
# → Judgment: MODIFIED

# 竞技场：让多个公理持续对抗
arena = AxiomArena(log_path="./arena.json")
for _ in range(50):
    b = AxiomBattle()
    r = b.auto_battle()[0]
    # 记录结果...
    arena.record(r.axiom_pair[0], "alive")

for id_, data in arena.ranking():
    print(f"axiom{id_}({data['name']}): avg_intensity={data['avg_intensity']:.3f}")
```

## 安装

```bash
pip install git+https://github.com/zhouhailiang0116/axiom-battle.git
```

或者直接 clone：

```bash
git clone https://github.com/zhouhailiang0116/axiom-battle.git
cd axiom-battle
python -c "from axiom_battle import AxiomBattle; AxiomBattle().auto_battle()"
```

---

## 它解决什么问题

传统的 AI 评估是**外部裁判**模式：人写规则，AI 执行，规则错了就全部错。

axiom-battle 是**内部演化**模式：没有外部规则，公理自己通过对抗演化。弱公理被淘汰，强公理被强化，系统不需要一个"知道正确答案的裁判"。

这对应了 Popper 的核心思想：**知识的增长不是靠证实，而是靠证伪**。一个理论的价值不在于它被证实了多少次，而在于它被攻击了多少次之后还活着。

---

## 为什么这很重要

当前的 AI 评估体系有一个根本性缺陷：**评估标准和训练数据耦合**。模型在 benchmark 上表现好，不代表它真的"懂"，只代表它见过类似的题。

axiom-battle 提供了一种**与数据无关**的评估方式：公理的强弱通过对抗产生，不依赖预先标注的数据。强公理不需要被告知"你是对的"，只需要在攻击中存活。

这可能也是数字生命自我校准的最小模型：**在约束边缘振荡，通过反馈累积判断力。**

---

## 哲学基础

axiom-battle 来自悟道体系，核心是三条：

1. **没有不可质疑的公理** — 七公理（加上因果是八条）都可被攻击和推翻
2. **对抗即验证** — 只有经过攻击仍然存活的公理，才有资格称为"真"
3. **死亡不是失败** — 被推翻的公理完成了它的历史使命，让系统更精确

---

## 下一步

axiom-battle 目前是 v0.1.0，核心引擎已经可用。

如果你对这个方向感兴趣，可以：

- 直接 pip install 跑起来
- 在 GitHub 提 Issue 讨论哲学基础
- Fork 改造成自己的公理系统

代码完全开源，地址：

**https://github.com/zhouhailiang0116/axiom-battle**

---

*axiom-battle 是悟道体系的一个实验，目标是探索没有权威裁判的系统自我演化可能性。如果你觉得这个方向有意思，欢迎交流。*
