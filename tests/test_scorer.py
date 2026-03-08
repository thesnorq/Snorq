import pytest
from snorq.models import SkillSignal, SkillVerdict, RiskTolerance
from snorq.scorer import compute_score, classify_verdict, compute_position, triggered_count


def sig(name, score, triggered=True, weight=0.25):
    return SkillSignal(name=name, score=score, triggered=triggered, detail="", weight=weight)


class TestComputeScore:
    def test_all_zero(self):
        signals = [sig(f"s{i}", 0.0, False) for i in range(4)]
        assert compute_score(signals) == pytest.approx(0.0)

    def test_all_100(self):
        signals = [sig(f"s{i}", 100.0) for i in range(4)]
        assert compute_score(signals) == pytest.approx(100.0)

    def test_weighted_average(self):
        signals = [
            sig("age",      85.0, weight=0.30),
            sig("momentum", 100.0, weight=0.35),
            sig("progress", 80.0, weight=0.20),
            sig("holders",  50.0, weight=0.15),
        ]
        expected = 85*0.30 + 100*0.35 + 80*0.20 + 50*0.15
        assert compute_score(signals) == pytest.approx(expected, abs=0.01)

    def test_empty_signals(self):
        assert compute_score([]) == 0.0

    def test_single_signal(self):
        signals = [sig("only", 60.0, weight=1.0)]
        assert compute_score(signals) == pytest.approx(60.0)

    def test_result_in_range(self, hot_candidate, default_input):
        from snorq.signals import evaluate_candidate
        signals = evaluate_candidate(hot_candidate, default_input)
        score = compute_score(signals)
        assert 0.0 <= score <= 100.0

    def test_hot_higher_than_cold(self, hot_candidate, cold_candidate, default_input):
        from snorq.signals import evaluate_candidate
        from tests.conftest import make_input
        inp = make_input(candidates=[hot_candidate])
        score_hot  = compute_score(evaluate_candidate(hot_candidate, inp))
        score_cold = compute_score(evaluate_candidate(cold_candidate, inp))
        assert score_hot > score_cold


class TestClassifyVerdict:
    def test_low_score_pass(self):
        assert classify_verdict(10.0) == SkillVerdict.PASS

    def test_25_still_pass(self):
        assert classify_verdict(25.0) == SkillVerdict.PASS

    def test_26_watch(self):
        assert classify_verdict(26.0) == SkillVerdict.WATCH

    def test_50_watch(self):
        assert classify_verdict(50.0) == SkillVerdict.WATCH

    def test_51_scout(self):
        assert classify_verdict(51.0) == SkillVerdict.SCOUT

    def test_75_scout(self):
        assert classify_verdict(75.0) == SkillVerdict.SCOUT

    def test_76_engage_medium(self):
        assert classify_verdict(76.0, RiskTolerance.MEDIUM) == SkillVerdict.ENGAGE

    def test_high_risk_lower_engage_threshold(self):
        assert classify_verdict(65.0, RiskTolerance.HIGH) == SkillVerdict.ENGAGE

    def test_low_risk_higher_engage_threshold(self):
        assert classify_verdict(76.0, RiskTolerance.LOW) == SkillVerdict.SCOUT

    def test_100_always_engage(self):
        for risk in RiskTolerance:
            assert classify_verdict(100.0, risk) == SkillVerdict.ENGAGE


class TestComputePosition:
    def test_zero_score_zero_position(self):
        pos = compute_position(0.0, 1.0, RiskTolerance.MEDIUM)
        assert pos == 0.0

    def test_position_within_budget(self):
        pos = compute_position(100.0, 1.0, RiskTolerance.HIGH)
        assert pos <= 1.0

    def test_high_risk_larger_position(self):
        pos_med  = compute_position(80.0, 1.0, RiskTolerance.MEDIUM)
        pos_high = compute_position(80.0, 1.0, RiskTolerance.HIGH)
        assert pos_high > pos_med

    def test_low_risk_smaller_position(self):
        pos_low = compute_position(80.0, 1.0, RiskTolerance.LOW)
        pos_med = compute_position(80.0, 1.0, RiskTolerance.MEDIUM)
        assert pos_low < pos_med

    def test_larger_budget_larger_position(self):
        pos_small = compute_position(80.0, 1.0, RiskTolerance.MEDIUM)
        pos_large = compute_position(80.0, 5.0, RiskTolerance.MEDIUM)
        assert pos_large > pos_small


class TestTriggeredCount:
    def test_all_triggered(self):
        signals = [sig(f"s{i}", 80.0, True) for i in range(4)]
        assert triggered_count(signals) == 4

    def test_none_triggered(self):
        signals = [sig(f"s{i}", 10.0, False) for i in range(4)]
        assert triggered_count(signals) == 0

    def test_mixed(self):
        signals = [
            sig("a", 80.0, True),
            sig("b", 10.0, False),
            sig("c", 70.0, True),
            sig("d", 5.0, False),
        ]
        assert triggered_count(signals) == 2

    def test_empty(self):
        assert triggered_count([]) == 0
