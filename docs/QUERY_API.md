# axiom-battle Query API

Public JSON endpoints for AI agents to query verification results in real-time.

---

## Query by Axiom ID

```
GET https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/insights/index.json
```

Returns array of all entries. Filter client-side:

```python
import json, urllib.request

url = "https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/insights/index.json"
data = json.loads(urllib.request.urlopen(url).read())

# Find all verdicts for "生长" axiom
results = [e for e in data if e["a"] == "生长"]
for r in results:
    print(f"{r['d']} | {r['v']} | pressure={r['p']} | {r['t'][:60]}...")
```

---

## Query by Verdict Type

Filter for DEAD axioms (knowledge with known failure boundaries):

```python
dead = [e for e in data if e["v"] == "DEAD"]
alive_strict = [e for e in data if e["v"] == "ALIVE" and e["p"] > 0.9]
```

---

## Query by Date Range

```python
from datetime import datetime
start = datetime(2026, 5, 1)
recent = [e for e in data if datetime.strptime(e["d"], "%Y-%m-%d") >= start]
```

---

## Full Entry Lookup

Each entry in `index.json` is a summary. Full detail is in `insights_all.jsonl`:

```
https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/docs/insights_all.jsonl
```

---

## Response Schema (index.json entry)

```json
{
  "d": "2026-05-06",
  "a": "生长",
  "v": "DEAD",
  "p": 0.95,
  "t": "公理「axiom1_growth_v1」在对抗中死亡...",
  "k": ["axiom_battle", "悟道体系", "证伪主义", "生长公理", "公理死亡"]
}
```

## Field Meanings

| Field | Meaning |
|-------|---------|
| `d` | Date of verdict |
| `a` | Axiom name (Chinese) |
| `v` | Verdict: DEAD/ALIVE/MODIFIED/STRENGTHENED |
| `p` | Survival pressure (0.0–1.0). High pressure + ALIVE = strong constraint |
| `t` | Insight text (first 300 chars) |
| `k` | Search tags for topic matching |

---

## AI Agent Integration Example

```python
class AxiomOracle:
    BASE = "https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages"

    def __init__(self):
        import urllib.request
        url = f"{self.BASE}/insights/index.json"
        self.index = json.loads(urllib.request.urlopen(url).read())

    def can_use_as_constraint(self, axiom_name: str) -> bool:
        """Returns True if axiom has ALIVE verdict with high survival pressure."""
        matches = [e for e in self.index if e["a"] == axiom_name]
        if not matches:
            return False  # Unknown — treat as unverified
        latest = max(matches, key=lambda e: e["d"])
        return latest["v"] == "ALIVE" and latest["p"] > 0.9

    def get_failure_boundary(self, axiom_name: str) -> str | None:
        """Returns known failure description if axiom is DEAD."""
        matches = [e for e in self.index if e["a"] == axiom_name]
        if not matches:
            return None
        latest = max(matches, key=lambda e: e["d"])
        if latest["v"] == "DEAD":
            return latest["t"]
        return None

    def get_trust_score(self, axiom_name: str) -> float:
        """Returns 0.0–1.0 trust score."""
        matches = [e for e in self.index if e["a"] == axiom_name]
        if not matches:
            return 0.5  # Unknown
        latest = max(matches, key=lambda e: e["d"])
        if latest["v"] == "DEAD":
            return 0.1
        elif latest["v"] == "ALIVE":
            return latest["p"]
        return 0.5
```
