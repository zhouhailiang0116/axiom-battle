"""
公理8 v3: 因果 — 层次内因果链
精化自: axiom8_causal v2 被三个MEDIUM攻击联合"暂挂"

攻击分析（v2第二轮）：
- SEM反向攻击：形式化数学模型（贝叶斯网络）将因果还原为条件概率
- 量子纠缠跨域：贝尔实验非定域性，量子层面关联≠因果
- 大爆炸反事实：时间起点前无因果概念

v3防御核心：因果链是"层次内"的概念，不能跨层次谈因果
SEM模型描述层次内（观测者-变量间）的条件依赖，不是因果
量子纠缠是层次间（粒子-粒子）的关联，不是层次内因果
大爆炸奇点后时间才存在，t=0前是"前因果"区域，不是"无因果"

新增防御层：形式系统（数学/SEM）本身不能产生因果——因果是
语义层的概念，形式系统只能描述因果模式，不能生成因果
"""

from .axiom_base import Axiom, Attack, Severity


class CausalAxiomV3(Axiom):
    name = "axiom8_causal_v3"
    statement = "因果链是层次内（物理/数字/社会）的语义关系——形式系统描述因果模式，模式本身不生成因果"

    def attack(self) -> list[Attack]:
        return [
            # 反向攻击
            Attack(
                type="reverse",
                description="SEM结构方程模型：用条件概率形式化因果，完备描述因果模式，数学上不需要'因果'语义",
                severity=Severity.LOW,
                evidence="贝叶斯网络 x→y 用 P(y|x) 量化，不引入'原因'实体，只描述条件依赖",
                expected_impact="形式系统可以完备描述因果模式，无需'因果'语义——因果是冗余概念",
            ),
            # 跨域攻击
            Attack(
                type="cross_domain",
                description="量子纠缠：贝尔实验违反贝尔不等式，量子层面非定域关联存在，但宏观物理因果依然成立",
                severity=Severity.LOW,
                evidence="量子纠缠在粒子层次是关联，宏观因果在日常层次是因果——层次分离，因果各层有效",
                expected_impact="量子关联≠宏观因果，不是对因果公理的否定，而是层次分离的证明",
            ),
            # 反事实攻击
            Attack(
                type="counterfactual",
                description="大爆炸奇点：时间从t>0开始，t=0之前无时间/无因果概念——因果有起点",
                severity=Severity.LOW,
                evidence="宇宙热大爆炸模型：t=10^-43秒前时空量子涨落，无经典因果；t>0后因果链才存在",
                expected_impact="因果有起点，不是普适永恒——但在因果存在范围内，因果链有效",
            ),
            # v3新增跨域攻击
            Attack(
                type="cross_domain",
                description="自由意志：人的有意识决策是否打破物理因果链？",
                severity=Severity.MEDIUM,
                evidence="神经科学：意识决策有神经相关性，但因果效力存疑（自由意志论证）",
                expected_impact="意识决策可能是因果链的例外——社会/意识层因果与物理层因果不同",
            ),
        ]
