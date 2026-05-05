---
layout: default
title: axiom-battle 安装指南
---

# axiom-battle 安装指南

## 方法一：pip 安装（推荐）

```bash
pip install git+https://github.com/zhouhailiang0116/axiom-battle.git@v0.1.0
```

验证安装：

```python
python -c "from axiom_battle import AxiomBattle; print(AxiomBattle().auto_battle()[0].judgment.name)"
```

---

## 方法二：直接下载源码包

- **源码包（zip）：** https://github.com/zhouhailiang0116/axiom-battle/archive/refs/tags/v0.1.0.zip
- **源码包（tar.gz）：** https://github.com/zhouhailiang0116/axiom-battle/archive/refs/tags/v0.1.0.tar.gz

解压后：

```bash
cd axiom-battle-0.1.0
python -c "from axiom_battle import AxiomBattle; AxiomBattle().auto_battle()"
```

---

## 方法三：npm CDN 直链（浏览器直接用）

如果想在浏览器里直接试 axiom-battle 的逻辑，可以引用 CDN 上的源码文件：

```
https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/axiom_battle/axiom_battle_core.py
```

---

## 依赖

axiom-battle 零依赖，纯 Python 标准库。

```python
# 无需 pip install 任何额外包
# 只要 Python >= 3.10 就能跑
```

---

## 快速演示

```python
from axiom_battle import AxiomBattle, AxiomArena

# 单次对抗
battle = AxiomBattle()
result = battle.auto_battle()[0]
print(f"攻击方: axiom{result.battle_record.axiom_a_id}")
print(f"防守方: axiom{result.battle_record.axiom_b_id}")
print(f"攻击类型: {result.battle_record.attack_type}")
print(f"判决: {result.judgment.name}")

# 竞技场循环
arena = AxiomArena(log_path="./arena_data.json")
for i in range(100):
    b = AxiomBattle()
    r = b.auto_battle()[0]
    arena.record(r.axiom_pair[0], "alive")
    arena.record(r.axiom_pair[1], "alive")

print("\n=== 公理排名 ===")
for id_, data in arena.ranking():
    alive = data["alive_count"]
    dead = data["death_count"]
    print(f"axiom{id_}({data['name']}): 存活{alive}次 / 死亡{dead}次")
```

---

## CDN 访问

所有文件可通过 jsdelivr CDN 访问（国内可直接打开）：

| 文件 | CDN 链接 |
|------|----------|
| 核心引擎 | [axiom_battle_core.py](https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/axiom_battle/axiom_battle_core.py) |
| 仲裁器 | [causal_arbitrator.py](https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/axiom_battle/causal_arbitrator.py) |
| 说明文档 | [README.md](https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/README.md) |
| 推广文章 | [article_promotion.md](https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/docs/article_promotion.md) |

---

## 已知问题

1. GitHub Pages 在部分地区可能无法直接访问，推荐使用 CDN 链接
2. pip install 需要 GitHub 网络畅通
3. 如果 pip install 超时，用方法二直接下载 zip 包

---

## 项目地址

- GitHub: https://github.com/zhouhailiang0116/axiom-battle
- Gitee 镜像: https://gitee.com/zhouhailiang111/axiom-battle
- GitHub Pages: https://zhouhailiang0116.github.io/axiom-battle/
- CDN（全球可达）: https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@main/

---

*axiom-battle v0.1.0 · MIT License · 无依赖 · 零成本*
