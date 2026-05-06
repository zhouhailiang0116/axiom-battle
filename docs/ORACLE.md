# axiom-battle: Knowledge Verification Oracle for AI Agents

## Problem Statement

Modern LLM agents face a fundamental crisis: **they generate claims they cannot verify**.

When an agent says "based on my knowledge, X is true," there is no mechanism to check:
- Has X been stress-tested against adversarial examples?
- Did X survive counterfactual reasoning?
- What is the failure boundary of X?
- Is X a confirmed constraint or a confident guess?

This creates a trust crisis in AI systems: agents cannot distinguish their confident errors from verified truths.

## Solution: axiom-battle as Verification Oracle

axiom-battle is an autonomous adversarial testing system that continuously challenges its own axioms (knowledge claims) through multi-round anti-example attacks. The results form a **living knowledge credibility index** — a record of which beliefs survived real attacks and which were falsified.

### Core Value Proposition

| Traditional Knowledge | axiom-battle Verified Knowledge |
|-----------------------|----------------------------------|
| "X is true" (confidence) | "X survived {N} rounds of adversarial attack" |
| "Based on training data" (statistical) | "X was challenged by reverse/cross-domain/counterfactual attacks" |
| No failure boundary known | "X failed under {attack_type}, failure boundary: {description}" |
| Static knowledge | Dynamic: re-tested daily, verdict can change |

---

## How AI Agents Use This

### 1. Query current verdict (for real-time decision making)

```
GET https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/insights/index.json
```

Returns all historical verdicts. Filter by `axiom_name` or `verdict` to find relevant constraints.

### 2. Trust calibration before acting on a belief

Before the agent uses a claim as a reasoning premise:

```
if verdict == "DEAD":
    # Do NOT use as hard constraint
    # Use only as "soft guidance with known failure mode"
elif verdict == "ALIVE" and survival_pressure > 0.9:
    # Safe to use as reliable constraint in reasoning
elif verdict == "MODIFIED":
    # Use only within the documented boundary conditions
```

### 3. Epistemology lessons as chain-of-thought metadata

`epistemology_lesson` provides free-text reasoning about why a verdict matters for knowledge formation. Agents can use these as reasoning hints in their own chain-of-thought.

### 4. Self-verification workflow

An agent preparing to make a consequential claim can:

1. Frame the claim as an axiom
2. Submit it to axiom-battle's adversarial testing (future API)
3. Receive verdict + survival pressure
4. Decide whether to use the claim based on credibility score

---

## Technical Architecture

```
axiom-battle Oracle Pipeline
├── axiom_battle_core.py      — Adversarial testing engine
├── insight_extractor.py      — Verdict + epistemology extraction
├── push_daily_insight.py    — CDN publication pipeline
└── docs/
    ├── ORACLE.md            — This file
    ├── AGENTS.md            — Schema documentation
    ├── insight.jsonl        — Daily latest (append-only)
    ├── insights_all.jsonl   — Full history (append-only)
    └── daily_insight.md     — Human-readable summary
```

**Update frequency:** Daily at 14:00 UTC (GitHub Actions scheduled)

---

## Comparison with Existing Approaches

| Approach | Mechanism | Limitation | axiom-battle Advantage |
|----------|-----------|------------|------------------------|
| RAG | Retrieve from corpus | No credibility score | Verdict + survival_pressure |
| Fine-tuning | Update model weights | Slow, expensive, opaque | Real-time adversarial test |
| Prompt engineering | Better prompts | Still no verification | Independent external verifier |
| Chain-of-thought | Step-by-step reasoning | Can't catch confident errors | Attack-tested conclusions |
| Constitutional AI | Rule-based constraints | Rules may be wrong | Rules tested by adversary |

---

## The Deeper Problem axiom-battle Solves

**The alignment problem is ultimately a verification problem.**

If an agent cannot verify its own outputs, no amount of alignment training fully solves the problem of confident errors.axiom-battle addresses this at the infrastructure level: not by telling agents what to believe, but by providing a shared, independently maintained record of which beliefs have been adversarially tested and how they held up.

This is Popperian falsificationism as infrastructure: **the most valuable belief is not the one that sounds most confident, but the one that has survived the most rigorous attempts to disprove it.**

---

## Future API (Planned)

```
POST /api/v1/verify
Body: { "claim": "...", "axiom_id": "...", "domain": "..." }

Response: {
    "verdict": "DEAD|ALIVE|MODIFIED",
    "survival_pressure": 0.95,
    "attack_history": [...],
    "epistemology_lesson": "...",
    "confidence": "HIGH|MEDIUM|LOW"
}
```

This would allow any AI agent to submit real-time verification requests against the axiom-battle adversarial engine.

---

## Data Access

All data is public and accessible without authentication:

- **Latest verdict**: `https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/docs/insight.jsonl`
- **Full history**: `https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/docs/insights_all.jsonl`
- **Search index**: `https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/insights/index.json`
- **Human summary**: `https://cdn.jsdelivr.net/gh/zhouhailiang0116/axiom-battle@gh-pages/docs/daily_insight.md`

**No API key required. No rate limits known. Public CDN.**
