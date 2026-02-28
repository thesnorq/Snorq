import pytest
from snorq.models import TokenCandidate, SkillInput, RiskTolerance


def make_candidate(
    mint="mint123",
    symbol="TEST",
    age_minutes=10.0,
    bonding_progress_pct=20.0,
    sol_per_minute=0.8,
    holder_count=30,
    entry_cost_sol=0.05,
    total_supply=1_000_000_000.0,
):
    return TokenCandidate(
        mint=mint,
        symbol=symbol,
        age_minutes=age_minutes,
        bonding_progress_pct=bonding_progress_pct,
        sol_per_minute=sol_per_minute,
        holder_count=holder_count,
        entry_cost_sol=entry_cost_sol,
        total_supply=total_supply,
    )


def make_input(candidates=None, budget_sol=1.0, risk=RiskTolerance.MEDIUM,
               max_age=60.0, min_holders=10):
    if candidates is None:
        candidates = [make_candidate()]
    return SkillInput(
        candidates=candidates,
        budget_sol=budget_sol,
        risk_tolerance=risk,
        max_age_minutes=max_age,
        min_holders=min_holders,
    )


@pytest.fixture
def hot_candidate():
    """Very fresh, fast-moving, early bonding — ENGAGE candidate."""
    return make_candidate(
        symbol="HOT",
        age_minutes=3.0,
        bonding_progress_pct=10.0,
        sol_per_minute=1.2,
        holder_count=45,
    )


@pytest.fixture
def cold_candidate():
    """Old, slow, nearly graduated — PASS candidate."""
    return make_candidate(
        symbol="COLD",
        age_minutes=90.0,
        bonding_progress_pct=85.0,
        sol_per_minute=0.05,
        holder_count=5,
    )


@pytest.fixture
def medium_candidate():
    """Mid-range signals — WATCH or SCOUT."""
    return make_candidate(
        symbol="MID",
        age_minutes=25.0,
        bonding_progress_pct=35.0,
        sol_per_minute=0.4,
        holder_count=20,
    )


@pytest.fixture
def default_input(hot_candidate):
    return make_input(candidates=[hot_candidate])


@pytest.fixture
def multi_input(hot_candidate, cold_candidate, medium_candidate):
    return make_input(candidates=[hot_candidate, cold_candidate, medium_candidate])
