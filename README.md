<div align="center">

<img src="https://capsule-render.vercel.app/api?type=slice&color=0:030501,50:1a2e00,100:84cc16&height=180&text=Snorq&fontSize=64&fontColor=d9f99d&fontAlignY=55&desc=AI%20Agent%20Skill%20for%20PumpFun%20Launch%20Scouting&descAlignY=75&descSize=15" width="100%"/>

### `$SNRQ`

[![Tests](https://github.com/snorqdevs/Snorq/actions/workflows/test.yml/badge.svg)](https://github.com/snorqdevs/Snorq/actions)
[![Python](https://img.shields.io/badge/Python-3.10%2B-84cc16?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-d9f99d?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-374151?style=flat-square)](LICENSE)
[![138 Tests](https://img.shields.io/badge/tests-138%20passed-22c55e?style=flat-square)]()

</div>

---

Snorq is an AI agent skill layer for PumpFun on Solana. It wraps new token launch evaluation into a structured skill API that AI agents can call autonomously. Pass in a list of token candidates with your budget and risk tolerance — Snorq scores each one across four signals and returns a verdict: **PASS / WATCH / SCOUT / ENGAGE**, with a recommended position size.

It's not a bot. It's a **skill** — a callable unit of intelligence designed to be composed inside larger agent frameworks.

---

## Skill Architecture

```
SkillInput
  ├─ candidates[]     → TokenCandidate list from PumpFun feed
  ├─ budget_sol       → agent's available capital
  ├─ risk_tolerance   → LOW / MEDIUM / HIGH
  ├─ max_age_minutes  → filter stale launches
  └─ min_holders      → filter ghost tokens
        │
        ▼
  evaluate_candidate()
    ├─ age_signal       → launch freshness  < 15 min   [weight: 30%]
    ├─ momentum_signal  → SOL/min velocity  ≥ 0.5      [weight: 35%]
    ├─ progress_signal  → bonding stage     < 40%      [weight: 20%]
    └─ holder_signal    → real interest     ≥ 20       [weight: 15%]
        │
        ▼
  compute_score() → 0–100
        │
        ▼
  classify_verdict() → PASS / WATCH / SCOUT / ENGAGE
        │
        ▼
  SkillOutput → top_pick + position_size_sol + reasoning
```

## Verdict Table

| Score | Verdict | Action |
|---|---|---|
| 0–25 | `PASS` | Skip entirely |
| 26–50 | `WATCH` | Monitor, no position |
| 51–75 | `SCOUT` | Investigate before committing |
| 76–100 | `ENGAGE` | AI agent takes position |

ENGAGE threshold adjusts with risk tolerance: HIGH=65+, MEDIUM=76+, LOW=85+.

## Install

```bash
pip install snorq
```

## Usage

```python
from snorq import run_skill, SkillInput, TokenCandidate, RiskTolerance

candidates = [
    TokenCandidate(
        mint="SnrqXyz...pump",
        symbol="SNRQ",
        age_minutes=8.0,
        bonding_progress_pct=18.0,
        sol_per_minute=0.9,
        holder_count=42,
        entry_cost_sol=0.04,
        total_supply=1_000_000_000,
    ),
]

skill_input = SkillInput(
    candidates=candidates,
    budget_sol=2.0,
    risk_tolerance=RiskTolerance.MEDIUM,
)

output = run_skill(skill_input)

print(output.top_pick.verdict)           # ENGAGE
print(output.top_pick.score)             # ~84.5
print(output.top_pick.position_size_sol) # ~0.8450
print(output.top_pick.reasoning)         # "Strong multi-signal..."
```

## Run Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
# 138 tests — signals, scorer, skill, models, helpers
```

## Dashboard

```bash
cd dashboard
npm install
npm run dev
# → http://localhost:5173
```

Live dashboard scanning 6 mock candidates. Shows verdict card, signal breakdown, candidate list — updates every 4 seconds.

## Docker

```bash
docker compose up
```

---

<div align="center">
<sub>built by snorqdev · pumpsniff · agentskill</sub>
</div>
