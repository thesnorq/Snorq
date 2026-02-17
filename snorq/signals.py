from __future__ import annotations

from .models import TokenCandidate, SkillInput, SkillSignal

# --- Thresholds ---
AGE_FRESH_MINUTES    = 15.0   # < 15 min since launch = freshest opportunity
MOMENTUM_THRESHOLD   = 0.5    # >= 0.5 SOL/min bonding velocity = active
PROGRESS_EARLY_PCT   = 40.0   # bonding progress < 40% = still early
HOLDER_MIN           = 20     # >= 20 holders = real interest

# --- Weights (sum = 1.0) ---
AGE_WEIGHT       = 0.30
MOMENTUM_WEIGHT  = 0.35
PROGRESS_WEIGHT  = 0.20
HOLDER_WEIGHT    = 0.15


def age_signal(candidate: TokenCandidate) -> SkillSignal:
    """Fresher launch = higher opportunity score."""
    age = candidate.age_minutes
    if age < 5:
        score = 100.0
    elif age < 15:
        score = 85.0
    elif age < 30:
        score = 60.0
    elif age < 60:
        score = 35.0
    else:
        score = 10.0
    triggered = age < AGE_FRESH_MINUTES
    return SkillSignal(
        name="age",
        score=score,
        triggered=triggered,
        detail=f"Token launched {age:.1f} min ago (threshold <{AGE_FRESH_MINUTES} min)",
        weight=AGE_WEIGHT,
    )


def momentum_signal(candidate: TokenCandidate) -> SkillSignal:
    """Bonding curve fill rate — fast fill = active market."""
    spm = candidate.sol_per_minute
    score = min(spm * 100.0, 100.0)
    triggered = spm >= MOMENTUM_THRESHOLD
    return SkillSignal(
        name="momentum",
        score=score,
        triggered=triggered,
        detail=f"Bonding curve filling at {spm:.3f} SOL/min (threshold={MOMENTUM_THRESHOLD})",
        weight=MOMENTUM_WEIGHT,
    )


def progress_signal(candidate: TokenCandidate) -> SkillSignal:
    """Early bonding curve position = more upside before graduation."""
    pct = candidate.bonding_progress_pct
    # Score decreases as bonding fills: 0% progress → 100, 100% → 0
    score = max(0.0, 100.0 - pct)
    triggered = pct < PROGRESS_EARLY_PCT
    return SkillSignal(
        name="progress",
        score=score,
        triggered=triggered,
        detail=f"Bonding curve at {pct:.1f}% (threshold <{PROGRESS_EARLY_PCT}% = early)",
        weight=PROGRESS_WEIGHT,
    )


def holder_signal(candidate: TokenCandidate) -> SkillSignal:
    """Enough holders = real interest, not just deployer."""
    h = candidate.holder_count
    score = min((h / HOLDER_MIN) * 50.0, 100.0)
    triggered = h >= HOLDER_MIN
    return SkillSignal(
        name="holders",
        score=score,
        triggered=triggered,
        detail=f"{h} holders (threshold >= {HOLDER_MIN})",
        weight=HOLDER_WEIGHT,
    )


def evaluate_candidate(candidate: TokenCandidate, skill_input: SkillInput) -> list[SkillSignal]:
    return [
        age_signal(candidate),
        momentum_signal(candidate),
        progress_signal(candidate),
        holder_signal(candidate),
    ]
