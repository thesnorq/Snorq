import time
import pytest
from snorq.models import (
    TokenCandidate, SkillInput, SkillOutput, CandidateResult,
    SkillSignal, SkillVerdict, RiskTolerance,
)
from tests.conftest import make_candidate, make_input


class TestSkillVerdict:
    def test_all_verdicts_exist(self):
        assert SkillVerdict.PASS
        assert SkillVerdict.WATCH
        assert SkillVerdict.SCOUT
        assert SkillVerdict.ENGAGE

    def test_verdict_values(self):
        assert SkillVerdict.ENGAGE.value == "ENGAGE"
        assert SkillVerdict.PASS.value == "PASS"


class TestRiskTolerance:
    def test_all_levels(self):
        assert RiskTolerance.LOW
        assert RiskTolerance.MEDIUM
        assert RiskTolerance.HIGH

    def test_values(self):
        assert RiskTolerance.HIGH.value == "HIGH"


class TestTokenCandidate:
    def test_basic_creation(self):
        c = make_candidate(symbol="SNRQ", age_minutes=5.0)
        assert c.symbol == "SNRQ"
        assert c.age_minutes == 5.0

    def test_default_fields(self):
        c = make_candidate()
        assert c.total_supply == 1_000_000_000.0
        assert c.holder_count == 30

    def test_zero_age(self):
        c = make_candidate(age_minutes=0.0)
        assert c.age_minutes == 0.0

    def test_bonding_progress_100(self):
        c = make_candidate(bonding_progress_pct=100.0)
        assert c.bonding_progress_pct == 100.0

    def test_mint_field(self):
        c = make_candidate(mint="So111abc")
        assert c.mint == "So111abc"


class TestSkillInput:
    def test_default_budget(self):
        inp = make_input()
        assert inp.budget_sol == 1.0

    def test_custom_budget(self):
        inp = make_input(budget_sol=5.0)
        assert inp.budget_sol == 5.0

    def test_default_risk(self):
        inp = make_input()
        assert inp.risk_tolerance == RiskTolerance.MEDIUM

    def test_high_risk(self):
        inp = make_input(risk=RiskTolerance.HIGH)
        assert inp.risk_tolerance == RiskTolerance.HIGH

    def test_candidates_list(self):
        candidates = [make_candidate(symbol=f"T{i}") for i in range(3)]
        inp = make_input(candidates=candidates)
        assert len(inp.candidates) == 3


class TestSkillSignal:
    def test_creation(self):
        s = SkillSignal(name="age", score=85.0, triggered=True, detail="fresh", weight=0.30)
        assert s.name == "age"
        assert s.triggered is True
        assert s.weight == 0.30

    def test_not_triggered(self):
        s = SkillSignal(name="momentum", score=10.0, triggered=False, detail="slow", weight=0.35)
        assert s.triggered is False


class TestCandidateResult:
    def test_timestamp_auto(self, hot_candidate, default_input):
        from snorq.skill import run_skill_single
        before = time.time()
        result = run_skill_single(hot_candidate, default_input)
        after = time.time()
        assert before <= result.timestamp <= after

    def test_has_four_signals(self, hot_candidate, default_input):
        from snorq.skill import run_skill_single
        result = run_skill_single(hot_candidate, default_input)
        assert len(result.signals) == 4


class TestSkillOutput:
    def test_engage_candidates_filter(self, multi_input):
        from snorq.skill import run_skill
        output = run_skill(multi_input)
        engage = output.engage_candidates()
        assert all(r.verdict == SkillVerdict.ENGAGE for r in engage)

    def test_watch_candidates_filter(self, multi_input):
        from snorq.skill import run_skill
        output = run_skill(multi_input)
        watch = output.watch_candidates()
        assert all(r.verdict == SkillVerdict.WATCH for r in watch)

    def test_scout_candidates_filter(self, multi_input):
        from snorq.skill import run_skill
        output = run_skill(multi_input)
        scout = output.scout_candidates()
        assert all(r.verdict == SkillVerdict.SCOUT for r in scout)

    def test_timestamp_auto(self, default_input):
        from snorq.skill import run_skill
        before = time.time()
        output = run_skill(default_input)
        after = time.time()
        assert before <= output.timestamp <= after
