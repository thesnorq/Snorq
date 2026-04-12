# Snorq — Claude Context

## What this is
AI agent skill layer for PumpFun on Solana. Wraps PumpFun token evaluation into a structured skill API that AI agents call to scout, score, and decide on new launches.

## Core skill flow
```
SkillInput (candidates + budget + risk) → run_skill() → SkillOutput
```

## Signals (weights sum to 1.0)
- `age_signal` — freshness of launch (weight: 30%)
- `momentum_signal` — SOL/min bonding velocity (weight: 35%)
- `progress_signal` — early on bonding curve (weight: 20%)
- `holder_signal` — holder count threshold (weight: 15%)

## Verdicts
- PASS (0–25): skip
- WATCH (26–50): monitor
- SCOUT (51–75): investigate
- ENGAGE (76–100): take position

## Engage threshold by risk
- LOW: 85+
- MEDIUM: 76+
- HIGH: 65+

## Entry point
```python
from snorq import run_skill, SkillInput, TokenCandidate
output = run_skill(skill_input)
print(output.top_pick.verdict)  # ENGAGE
```

## Tests
```bash
pytest tests/ -v  # 138 tests
```
