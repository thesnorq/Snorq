import pytest
from snorq.signals import (
    age_signal, momentum_signal, progress_signal, holder_signal,
    evaluate_candidate,
    AGE_FRESH_MINUTES, MOMENTUM_THRESHOLD, PROGRESS_EARLY_PCT, HOLDER_MIN,
    AGE_WEIGHT, MOMENTUM_WEIGHT, PROGRESS_WEIGHT, HOLDER_WEIGHT,
)
from tests.conftest import make_candidate, make_input


class TestAgeSignal:
    def test_very_fresh_max_score(self):
        c = make_candidate(age_minutes=2.0)
        r = age_signal(c)
        assert r.score == 100.0

    def test_fresh_high_score(self):
        c = make_candidate(age_minutes=10.0)
        r = age_signal(c)
        assert r.score == 85.0

    def test_fresh_triggered(self):
        c = make_candidate(age_minutes=10.0)
        r = age_signal(c)
        assert r.triggered is True

    def test_30min_not_triggered(self):
        c = make_candidate(age_minutes=30.0)
        r = age_signal(c)
        assert r.triggered is False

    def test_old_low_score(self):
        c = make_candidate(age_minutes=90.0)
        r = age_signal(c)
        assert r.score == 10.0

    def test_score_decreases_with_age(self):
        fresh = age_signal(make_candidate(age_minutes=5.0))
        old   = age_signal(make_candidate(age_minutes=60.0))
        assert fresh.score > old.score

    def test_name(self):
        r = age_signal(make_candidate())
        assert r.name == "age"

    def test_weight(self):
        r = age_signal(make_candidate())
        assert r.weight == AGE_WEIGHT

    def test_detail_contains_minutes(self):
        c = make_candidate(age_minutes=12.5)
        r = age_signal(c)
        assert "12.5" in r.detail

    def test_boundary_exactly_15(self):
        c = make_candidate(age_minutes=15.0)
        r = age_signal(c)
        assert r.triggered is False  # < 15, not <=

    def test_boundary_14_triggered(self):
        c = make_candidate(age_minutes=14.9)
        r = age_signal(c)
        assert r.triggered is True


class TestMomentumSignal:
    def test_fast_triggered(self):
        c = make_candidate(sol_per_minute=1.0)
        r = momentum_signal(c)
        assert r.triggered is True

    def test_slow_not_triggered(self):
        c = make_candidate(sol_per_minute=0.1)
        r = momentum_signal(c)
        assert r.triggered is False

    def test_score_scales_with_velocity(self):
        slow = momentum_signal(make_candidate(sol_per_minute=0.1))
        fast = momentum_signal(make_candidate(sol_per_minute=0.9))
        assert fast.score > slow.score

    def test_capped_at_100(self):
        c = make_candidate(sol_per_minute=5.0)
        r = momentum_signal(c)
        assert r.score == 100.0

    def test_zero_velocity_zero_score(self):
        c = make_candidate(sol_per_minute=0.0)
        r = momentum_signal(c)
        assert r.score == 0.0
        assert r.triggered is False

    def test_name(self):
        r = momentum_signal(make_candidate())
        assert r.name == "momentum"

    def test_weight(self):
        r = momentum_signal(make_candidate())
        assert r.weight == MOMENTUM_WEIGHT

    def test_exactly_threshold_triggered(self):
        c = make_candidate(sol_per_minute=MOMENTUM_THRESHOLD)
        r = momentum_signal(c)
        assert r.triggered is True

    def test_detail_contains_sol_per_min(self):
        c = make_candidate(sol_per_minute=0.75)
        r = momentum_signal(c)
        assert "SOL/min" in r.detail


class TestProgressSignal:
    def test_early_bonding_triggered(self):
        c = make_candidate(bonding_progress_pct=20.0)
        r = progress_signal(c)
        assert r.triggered is True

    def test_late_bonding_not_triggered(self):
        c = make_candidate(bonding_progress_pct=60.0)
        r = progress_signal(c)
        assert r.triggered is False

    def test_zero_progress_max_score(self):
        c = make_candidate(bonding_progress_pct=0.0)
        r = progress_signal(c)
        assert r.score == 100.0

    def test_100_progress_zero_score(self):
        c = make_candidate(bonding_progress_pct=100.0)
        r = progress_signal(c)
        assert r.score == 0.0

    def test_score_decreases_with_progress(self):
        early = progress_signal(make_candidate(bonding_progress_pct=10.0))
        late  = progress_signal(make_candidate(bonding_progress_pct=80.0))
        assert early.score > late.score

    def test_name(self):
        r = progress_signal(make_candidate())
        assert r.name == "progress"

    def test_weight(self):
        r = progress_signal(make_candidate())
        assert r.weight == PROGRESS_WEIGHT

    def test_boundary_exactly_40(self):
        c = make_candidate(bonding_progress_pct=40.0)
        r = progress_signal(c)
        assert r.triggered is False  # < 40, not <=


class TestHolderSignal:
    def test_enough_holders_triggered(self):
        c = make_candidate(holder_count=30)
        r = holder_signal(c)
        assert r.triggered is True

    def test_too_few_not_triggered(self):
        c = make_candidate(holder_count=5)
        r = holder_signal(c)
        assert r.triggered is False

    def test_score_scales_with_count(self):
        few  = holder_signal(make_candidate(holder_count=10))
        many = holder_signal(make_candidate(holder_count=80))
        assert many.score > few.score

    def test_capped_at_100(self):
        c = make_candidate(holder_count=1000)
        r = holder_signal(c)
        assert r.score == 100.0

    def test_zero_holders_zero_score(self):
        c = make_candidate(holder_count=0)
        r = holder_signal(c)
        assert r.score == 0.0

    def test_name(self):
        r = holder_signal(make_candidate())
        assert r.name == "holders"

    def test_weight(self):
        r = holder_signal(make_candidate())
        assert r.weight == HOLDER_WEIGHT


class TestEvaluateCandidate:
    def test_returns_four_signals(self, hot_candidate, default_input):
        signals = evaluate_candidate(hot_candidate, default_input)
        assert len(signals) == 4

    def test_signal_names(self, hot_candidate, default_input):
        signals = evaluate_candidate(hot_candidate, default_input)
        names = [s.name for s in signals]
        assert "age" in names
        assert "momentum" in names
        assert "progress" in names
        assert "holders" in names

    def test_weights_sum_to_one(self, hot_candidate, default_input):
        signals = evaluate_candidate(hot_candidate, default_input)
        total = sum(s.weight for s in signals)
        assert abs(total - 1.0) < 0.001

    def test_hot_candidate_all_triggered(self, hot_candidate, default_input):
        signals = evaluate_candidate(hot_candidate, default_input)
        triggered = [s for s in signals if s.triggered]
        assert len(triggered) >= 3
