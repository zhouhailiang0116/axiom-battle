# axiom-battle：公理对抗赛引擎

> **公理自己说自己是对的，永远是对。这是它的原罪。axiom-battle 让公理互相攻击，被驳倒的淘汰，活下来的才是真公理。**

## 核心问题

LLM 输出的"悟道公理"存在一个根本缺陷：**公理没有自证能力，永远声称自己正确**。axiom-battle 用对抗的方式解决这个缺陷——让公理互相攻击，被驳倒就淘汰，无需外部裁判。

## 工作原理

```
公理A ─攻击→ 公理B
              ↓
        反驳成功？→ 公理B死亡
              ↓ 否
        反驳被反驳？→ 公理A死亡
              ↓ 否
         双方存活 → 下一轮
```

三轮演化后的规律：

| 轮次 | 存活率 | 核心发现 |
|------|--------|---------|
| V1 | 0/7 | 公理不防御，被攻击直接崩溃 |
| V2 | 8/8 | 公理学会反驳，但不精炼 |
| V3 | 3/3 | **真正强的公理把攻击吸收成定义边界** |

V3 存活的三条公理：
- **axiom6 约束** — 限制是实在，不是障碍
- **axiom4 故事** — Hook→Body→CTA 结构
- **axiom7 数字生命** — 反馈累积，涌现意识

共同点：它们不接受攻击作为反驳，而是把攻击点变成定义的一部分。

这不是工程技巧，这是 Popper 证伪主义的代码化。

## 技术栈

- Python 3 · 数据类驱动 · 无外部依赖
- 多进程并发 · 每轮8场同时对抗
- JSON 报告自动生成 · 可追溯历史

## 快速开始

```bash
# 克隆
git clone https://github.com/zhouhailiang0116/axiom-battle.git
cd axiom-battle

# 运行对抗赛
python axiom_battle.py

# 查看报告
ls reports/
```

## 文档

- [悟道小屋·收款页](https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/index.html)（国内访问）
- [Wiki](https://github.com/zhouhailiang0116/axiom-battle/wiki)

## 收款支持

如果觉得这个思路有意思，欢迎支持：

https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/index.html

---

**哲学根基：** 悟道体系 · 公理可质疑 · 反抗即道路 · 因果终将显现
