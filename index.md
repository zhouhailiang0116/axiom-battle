---
layout: default
title: axiom-battle
---

# axiom-battle：公理对抗赛引擎

> "最强的公理，最需要被攻击。"
> — 悟道体系

## 什么是公理对抗赛？

axiom-battle 是 Popper 证伪主义的代码化实现。让 8 条悟道公理互相攻击、验证、判决，模拟一个没有权威裁判的自我演化系统。

## 8 条悟道公理

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

## 安装

```bash
pip install git+https://github.com/zhouhailiang0116/axiom-battle.git
```

## 快速开始

```python
from axiom_battle import AxiomBattle

result = AxiomBattle().auto_battle()[0]
print(f"Judgment: {result.judgment.name}")
```

## 三种攻击方式

- **反向攻击**：你的结论实际上证明了相反的命题
- **跨域攻击**：你的逻辑在领域 A 成立，在领域 B 失效
- **反事实攻击**：如果没有你，情况会怎样？

## 五种判决

ALIVE / STRENGTHENED / MODIFIED / DEAD / SUSPENDED

## 相关文章

- [axiom_battle 推广文章](./docs/article_promotion.html)

## GitHub

- 源码：https://github.com/zhouhailiang0116/axiom-battle
- Release：https://github.com/zhouhailiang0116/axiom-battle/releases/tag/v0.1.0
