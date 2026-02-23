from __future__ import annotations

from .models import (
    SkillInput, SkillOutput, CandidateResult,
    TokenCandidate, SkillVerdict,
)
from .signals import evaluate_candidate
from .scorer import compute_score, classify_verdict, compute_position


_REASONING: dict[SkillVerdict, str] = {
    SkillVerdict.PASS:   "Token does not meet minimum criteria. Skip.",
    SkillVerdict.WATCH:  "Some signals active. Monitor for momentum shift.",
    SkillVerdict.SCOUT:  "Promising early signals. Gather more data before committing.",
    SkillVerdict.ENGAGE: "Strong multi-signal confirmation. AI agent should take position.",
}


def _passes_filters(candidate: TokenCandidate, skill_input: SkillInput) -> bool:
    if candidate.age_minutes > skill_input.max_age_minutes:
        return False
    if candidate.holder_count < skill_input.min_holders:
        return False
    return True


def _evaluate_one(candidate: TokenCandidate, skill_input: SkillInput) -> CandidateResult:
    signals  = evaluate_candidate(candidate, skill_input)
    score    = compute_score(signals)
    verdict  = classify_verdict(score, skill_input.risk_tolerance)
    position = compute_position(score, skill_input.budget_sol, skill_input.risk_tolerance)

    active = [s.name for s in signals if s.triggered]
    reasoning = _REASONING[verdict]
    if active:
        reasoning += f" Active signals: {', '.join(active)}."

    return CandidateResult(
        candidate=candidate,
        verdict=verdict,
        score=score,
        signals=signals,
        reasoning=reasoning,
        position_size_sol=position,
    )


def run_skill(skill_input: SkillInput) -> SkillOutput:
    results = []
    for candidate in skill_input.candidates:
        if not _passes_filters(candidate, skill_input):
            continue
        results.append(_evaluate_one(candidate, skill_input))

    results.sort(key=lambda r: r.score, reverse=True)

    top_pick = next(
        (r for r in results if r.verdict == SkillVerdict.ENGAGE), None
    )

    return SkillOutput(
        input=skill_input,
        results=results,
        top_pick=top_pick,
    )


def run_skill_single(candidate: TokenCandidate, skill_input: SkillInput) -> CandidateResult:
    return _evaluate_one(candidate, skill_input)
