"""
axiom_battle 单元测试

测试覆盖：
1. axiom_base: Severity加权、evaluate()判决逻辑
2. axioms: 各公理attack()返回格式、注册表完整性
3. causal_arbitrator: 冲突检测与仲裁
4. axiom_arena: 记录与排名
5. run_battle: 端到端battle运行
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiom_battle.axioms import (
    AXIOM_REGISTRY, AXIOM_REGISTRY_V2, AXIOM_REGISTRY_V3,
    GrowthAxiom, LightAxiom, ColorAxiom,
    LayoutAxiom, NarrativeAxiom, BoundaryAxiom, FreedomAxiom,
    CausalAxiom,
)
from axiom_battle.axioms.axiom_base import Severity, Axiom, Attack, AxiomCase
from axiom_battle.causal_arbitrator import (
    ConflictResolver, AxiomClaim, ConflictType, AXIOM_PRIORITY
)
from axiom_battle.axiom_arena import AxiomArena
import tempfile, json, os


# ── axiom_base 测试 ─────────────────────────────────────────────────────────

class TestSeverity:
    def test_severity_order(self):
        assert Severity.LOW.value < Severity.MEDIUM.value < Severity.HIGH.value < Severity.CRITICAL.value
        print("  ✓ Severity 顺序正确")

    def test_attack_dataclass(self):
        a = Attack(
            type="reverse",
            description="测试攻击",
            severity=Severity.HIGH,
            evidence="证据",
            expected_impact="影响",
        )
        d = a.to_dict()
        assert d["severity"] == "HIGH"
        assert d["type"] == "reverse"
        assert d["evidence"] == "证据"
        print("  ✓ Attack dataclass 序列化正确")


class TestEvaluate:
    """测试 evaluate() 判决逻辑"""

    def _make_case(self, axiom_name, attacks: list[Attack]) -> AxiomCase:
        class T(Axiom):
            name = axiom_name
            statement = "测试公理"
            def attack(self): return attacks
        return T().run()

    def test_no_attacks_alive(self):
        case = self._make_case("test", [])
        assert case.verdict == "ALIVE"
        assert case.survival_pressure == 1.0
        print("  ✓ 无攻击 → ALIVE")

    def test_single_critical_modify(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.CRITICAL, "E", "I")
        ])
        assert case.verdict == "MODIFIED"
        print("  ✓ 1个CRITICAL无HIGH → MODIFIED")

    def test_two_critical_dead(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.CRITICAL, "E", "I"),
            Attack("cross_domain", "CD", Severity.CRITICAL, "E", "I"),
        ])
        assert case.verdict == "DEAD"
        print("  ✓ 2个CRITICAL → DEAD")

    def test_one_critical_no_high_modify(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.CRITICAL, "E", "I"),
        ])
        assert case.verdict == "MODIFIED"
        print("  ✓ 1个CRITICAL无HIGH → MODIFIED")

    def test_one_critical_plus_two_high_dead(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.CRITICAL, "E", "I"),
            Attack("cross_domain", "CD", Severity.HIGH, "E", "I"),
            Attack("counterfactual", "CF", Severity.HIGH, "E", "I"),
        ])
        assert case.verdict == "DEAD"
        print("  ✓ 1个CRITICAL+2个HIGH → DEAD")

    def test_two_high_strengthened(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.HIGH, "E", "I"),
            Attack("cross_domain", "CD", Severity.HIGH, "E", "I"),
        ])
        assert case.verdict == "STRENGTHENED"
        print("  ✓ 2个HIGH无CRITICAL → STRENGTHENED")

    def test_one_high_two_medium_modify(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.HIGH, "E", "I"),
            Attack("cross_domain", "CD", Severity.MEDIUM, "E", "I"),
            Attack("counterfactual", "CF", Severity.MEDIUM, "E", "I"),
        ])
        assert case.verdict == "MODIFIED"
        print("  ✓ 1个HIGH+2个MEDIUM → MODIFIED")

    def test_survival_below_05_suspended(self):
        # MEDIUM×4 = score=8, survival=0.2 → SUSPENDED
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.MEDIUM, "E", "I"),
            Attack("cross_domain", "CD", Severity.MEDIUM, "E", "I"),
            Attack("counterfactual", "CF", Severity.MEDIUM, "E", "I"),
            Attack("reverse", "R2", Severity.MEDIUM, "E", "I"),
        ])
        assert case.verdict == "SUSPENDED"
        print("  ✓ 4个MEDIUM(survival=0.2) → SUSPENDED")

    def test_all_low_alive(self):
        case = self._make_case("test", [
            Attack("reverse", "R", Severity.LOW, "E", "I"),
            Attack("cross_domain", "CD", Severity.LOW, "E", "I"),
        ])
        assert case.verdict == "ALIVE"
        print("  ✓ 2个LOW(survival=0.8) → ALIVE")


# ── axioms 注册表测试 ─────────────────────────────────────────────────────────

class TestRegistry:
    def test_v1_complete(self):
        assert len(AXIOM_REGISTRY) == 8
        names = list(AXIOM_REGISTRY.keys())
        expected = [f"axiom{i}_{n}" for i, n in enumerate(
            ["growth","light","color","layout","narrative","boundary","freedom","causal"], 1)]
        for e in expected:
            assert e in names, f"缺少 {e}"
        print(f"  ✓ v1注册表完整: 8公理")

    def test_v2_complete(self):
        assert len(AXIOM_REGISTRY_V2) == 8
        for name in AXIOM_REGISTRY_V2:
            assert name.endswith("_v2")
        print(f"  ✓ v2注册表完整: 8公理")

    def test_v3_count(self):
        assert len(AXIOM_REGISTRY_V3) == 3
        for name in AXIOM_REGISTRY_V3:
            assert name.endswith("_v3")
        print(f"  ✓ v3注册表: 3公理")

    def test_all_axioms_run(self):
        """每个注册的公理都能正常运行run()"""
        for registry in [AXIOM_REGISTRY, AXIOM_REGISTRY_V2, AXIOM_REGISTRY_V3]:
            for name, cls in registry.items():
                case = cls().run()
                assert isinstance(case, AxiomCase)
                assert case.axiom_name == name
                assert case.verdict in ("ALIVE","STRENGTHENED","MODIFIED","DEAD","SUSPENDED")
        print("  ✓ 所有注册公理均可运行")


# ── causal_arbitrator 测试 ────────────────────────────────────────────────────

class TestCausalArbitrator:
    def test_opposite_pair_detection(self):
        resolver = ConflictResolver()
        claims = [
            AxiomClaim(5, "concentrate", "peak", 0.95),
            AxiomClaim(7, "free", "max", 0.88),
        ]
        conflicts = resolver.detect_conflict(claims)
        assert len(conflicts) == 1
        assert conflicts[0].conflict_type == ConflictType.OPPOSITE
        print("  ✓ OPPOSITE冲突检测正确")

    def test_non_conflict(self):
        resolver = ConflictResolver()
        claims = [
            AxiomClaim(1, "grow", "value", 0.8),
            AxiomClaim(3, "warm_up", "value", 0.9),
        ]
        conflicts = resolver.detect_conflict(claims)
        assert len(conflicts) == 0
        print("  ✓ 非冲突claim正确识别")

    def test_priority_arbitration(self):
        resolver = ConflictResolver()
        claims = [
            AxiomClaim(5, "concentrate", "peak", 0.95),  # 叙事，优先级4
            AxiomClaim(7, "free", "max", 0.88),           # 自由，优先级7
        ]
        conflicts = resolver.detect_conflict(claims)
        final = resolver.arbitrate(conflicts)
        assert final[7] == 0.3  # 自由被压制 ×0.3
        assert final[5] == 1.0  # 叙事不变
        print("  ✓ 优先级仲裁：低优先级被压制×0.3")

    def test_resolve_one_shot(self):
        resolver = ConflictResolver()
        claims = [
            AxiomClaim(3, "constrain", "value", 0.80),   # 色彩，优先级6
            AxiomClaim(7, "free", "max", 0.88),            # 自由，优先级7
        ]
        final = resolver.resolve(claims)
        assert 7 in final and 3 in final
        print("  ✓ resolve()一键仲裁正常")


# ── axiom_arena 测试 ───────────────────────────────────────────────────────────

class TestArena:
    def test_record_and_ranking(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            arena = AxiomArena(path)
            arena.record("axiom1_growth", "alive", 0.8, "通过")
            arena.record("axiom1_growth", "alive", 0.6, "通过")
            arena.record("axiom2_light", "death", 0.0, "被击穿")

            summary = arena.summary()
            assert summary["total_axioms"] == 2
            assert summary["survived"] == 1
            assert summary["has_died"] == 1

            r = arena.ranking()
            # axiom1_growth avg=0.7, axiom2_light avg=0.0 → axiom1排前
            assert r[0][0] == "axiom1_growth"
            print("  ✓ Arena记录与排名正确")
        finally:
            os.unlink(path)

    def test_top_bottom(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            arena = AxiomArena(path)
            arena.record("a1", "alive", 0.9, "")
            arena.record("a2", "alive", 0.5, "")
            arena.record("a3", "death", 0.0, "")

            assert arena.top(2) == ["a1", "a2"]
            assert arena.bottom(1) == ["a3"]
            print("  ✓ top/bottom 正确")
        finally:
            os.unlink(path)


# ── run_battle 集成测试 ────────────────────────────────────────────────────────

class TestRunBattle:
    def test_run_all_regsitries(self):
        """端到端：三个注册表都能跑完"""
        import subprocess
        result = subprocess.run(
            ["python3", "run_battle.py"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=True, text=True, timeout=120
        )
        assert result.returncode == 0, f"run_battle.py 失败: {result.stderr[-500:]}"
        assert "ALIVE" in result.stdout
        assert "DEAD" in result.stdout
        print("  ✓ run_battle.py 端到端运行成功")


# ── 运行 ─────────────────────────────────────────────────────────────────────

def run_all():
    print("\n" + "="*60)
    print("  axiom-battle 单元测试")
    print("="*60)

    suites = [
        ("Severity & Attack", TestSeverity()),
        ("evaluate() 判决逻辑", TestEvaluate()),
        ("注册表完整性", TestRegistry()),
        ("causal_arbitrator", TestCausalArbitrator()),
        ("axiom_arena", TestArena()),
        ("端到端 run_battle", TestRunBattle()),
    ]

    passed = 0
    failed = 0
    for name, suite in suites:
        print(f"\n  【{name}】")
        methods = [m for m in dir(suite) if m.startswith("test_")]
        for method_name in methods:
            try:
                getattr(suite, method_name)()
                passed += 1
            except AssertionError as e:
                print(f"    ✗ {method_name}: {e}")
                failed += 1
            except Exception as e:
                print(f"    ✗ {method_name}: {type(e).__name__}: {e}")
                failed += 1

    print(f"\n{'='*60}")
    print(f"  结果: {passed} 通过, {failed} 失败")
    print("="*60)
    return failed == 0


if __name__ == "__main__":
    ok = run_all()
    exit(0 if ok else 1)
