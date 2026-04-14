# Snorq

**AI agent skill for PumpFun launch scouting on Solana.**

`$SNORQ` — `pip install snorq`

---

Most PumpFun tooling is built for humans watching a screen. Snorq is built for agents running in a loop.

You pass in a list of token candidates — fresh launches from the PumpFun feed — along with your budget and risk tolerance. Snorq evaluates each one across four on-chain signals, computes a weighted score, and returns a structured verdict: **PASS**, **WATCH**, **SCOUT**, or **ENGAGE**. If the verdict is ENGAGE, you also get a recommended position size.

No charts. No UI required. One function call in, one structured result out.

---

## What it evaluates

Every candidate is scored across four signals. The weights are fixed and intentional:

```
age_signal        weight: 30%   — how long since launch?
                                  < 5 min  → 100
                                  < 15 min → 85
                                  < 30 min → 60
                                  < 60 min → 35
                                  60+ min  → 10

momentum_signal   weight: 35%   — SOL/min bonding curve velocity
                                  score = min(sol_per_minute × 100, 100)
                                  triggers at ≥ 0.5 SOL/min

progress_signal   weight: 20%   — how early are we on the bonding curve?
                                  score = max(0, 100 - bonding_progress_pct)
                                  triggers at < 40% filled

holder_signal     weight: 15%   — is there real interest, not just a deployer?
                                  score = min((holders / 20) × 50, 100)
                                  triggers at ≥ 20 holders
```

Weighted average of these four → final score 0–100.

---

## Verdicts

```
0–25    PASS     skip entirely
26–50   WATCH    monitor, no position
51–75   SCOUT    investigate before committing
76–100  ENGAGE   agent takes position
```

The ENGAGE threshold shifts based on risk tolerance:

```
LOW     ≥ 85    position = 25% of budget
MEDIUM  ≥ 76    position = 50% of budget
HIGH    ≥ 65    position = 80% of budget
```

---

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

output = run_skill(SkillInput(
    candidates=candidates,
    budget_sol=2.0,
    risk_tolerance=RiskTolerance.MEDIUM,
))

print(output.top_pick.verdict)            # ENGAGE
print(output.top_pick.score)              # ~84.5
print(output.top_pick.position_size_sol)  # ~0.8450
print(output.top_pick.reasoning)          # "Strong multi-signal confirmation..."
```

The output is fully typed. Every field is a dataclass — no string parsing, no ambiguity. Designed to be consumed by the next step in an agent pipeline.

---

## Filters

Before scoring, Snorq applies two hard filters:

- `max_age_minutes` — tokens older than this are excluded entirely (default: 60)
- `min_holders` — tokens with fewer holders are excluded (default: 10)

This removes ghost tokens — single-wallet deploys with zero organic interest — before they pollute the verdict pool. Most new PumpFun launches never pass these filters. That's the point.

---

## Install

```bash
pip install snorq
```

No external dependencies. The core engine is pure Python 3.10+.

---

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

138 tests. Signals, scorer boundaries, skill filters, position sizing, helpers — every assumption is tested individually. If you change a threshold, the tests tell you exactly what breaks.

---

## Dashboard

```bash
cd dashboard && npm install && npm run dev
# → http://localhost:5173
```

Runs a mock scan of 6 candidates updating every 4 seconds. Verdict cards, signal breakdown with weights, candidate list with live selection. Dark lime theme. TypeScript React.

---

## Docker

```bash
docker compose up
```

---

## Why momentum gets 35%

Price on PumpFun is almost entirely bonding curve mechanics. If a token is filling at 0.8–1.0 SOL/min in the first 10 minutes, something real is happening. Below 0.1 SOL/min at minute 20, it's already dead.

Velocity is the signal. Everything else is context. The weight reflects that.

---

## Design philosophy

Snorq is a **skill** — a callable unit of intelligence designed to be composed inside larger agent frameworks. It doesn't manage state. It doesn't poll. It doesn't maintain a connection.

You call it. It decides. You act.

```
SkillInput → run_skill() → SkillOutput
```

That's the entire surface area. Keep it composable.

---

<sub>built by snorqdev · pumpsniff · agentskill</sub>
