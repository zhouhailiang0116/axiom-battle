import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from axiom_battle import AxiomBattle, AxiomArena

def test_auto_battle():
    battle = AxiomBattle(seed=42)
    result = battle.auto_battle(verbose=False)
    assert result.judgment.name in ["ALIVE", "STRENGTHENED", "MODIFIED", "DEAD", "SUSPENDED"]
    assert 1 <= result.attacker_id <= 8
    assert 1 <= result.defender_id <= 8
    assert result.attacker_id != result.defender_id
    print(f"Test passed: {result.attacker_label} → {result.defender_label} = {result.judgment.name}")

def test_arena_report():
    arena = AxiomArena(seed=42)
    arena.battles = [AxiomBattle(seed=i).auto_battle() for i in range(10)]
    report = arena.generate_report()
    assert "top3" in report
    assert "bottom3" in report
    assert len(report["top3"]) == 3
    assert len(report["bottom3"]) == 3
    print(f"Arena report: {len(arena.battles)} battles, top={report['top3'][0]['axiom_label']}({report['top3'][0]['strength']:.2f})")

if __name__ == "__main__":
    test_auto_battle()
    test_arena_report()
