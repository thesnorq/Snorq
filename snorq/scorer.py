from __future__ import annotations

from typing import List

from .models import SkillSignal, SkillVerdict, RiskTolerance

# Risk tolerance adjusts the ENGAGE threshold
_ENGAGE_THRESHOLD: dict[RiskTolerance, float] = {
    RiskTolerance.LOW:    85.0,
    RiskTolerance.MEDIUM: 76.0,
    RiskTolerance.HIGH:   65.0,
}


def compute_score(signals: List[SkillSignal]) -> float:
    """Weighted average of signal scores → 0–100."""
    total_weight = sum(s.weight for s in signals)
    if total_weight == 0:
        return 0.0
    return sum(s.score * s.weight for s in signals) / total_weight


def classify_verdict(score: float, risk_tolerance: RiskTolerance = RiskTolerance.MEDIUM) -> SkillVerdict:
    engage_threshold = _ENGAGE_THRESHOLD[risk_tolerance]
    if score >= engage_threshold:
        return SkillVerdict.ENGAGE
    if score >= 51.0:
        return SkillVerdict.SCOUT
    if score >= 26.0:
        return SkillVerdict.WATCH
    return SkillVerdict.PASS


def compute_position(
    score: float,
    budget_sol: float,
    risk_tolerance: RiskTolerance,
) -> float:
    """Position size scales with score and risk tolerance."""
    _multipliers = {
        RiskTolerance.LOW:    0.25,
        RiskTolerance.MEDIUM: 0.50,
        RiskTolerance.HIGH:   0.80,
    }
    base_pct = (score / 100.0) * _multipliers[risk_tolerance]
    return round(budget_sol * base_pct, 4)


def triggered_count(signals: List[SkillSignal]) -> int:
    return sum(1 for s in signals if s.triggered)
