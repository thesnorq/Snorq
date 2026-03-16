import pytest
from snorq.models import SkillVerdict, RiskTolerance
from snorq.utils.helpers import (
    clamp, format_sol, format_score, format_age, format_pct,
    ts_to_str, verdict_color, verdict_emoji, risk_label, score_bar,
)


class TestClamp:
    def test_within_range(self):
        assert clamp(50.0, 0.0, 100.0) == 50.0

    def test_below_min(self):
        assert clamp(-5.0, 0.0, 100.0) == 0.0

    def test_above_max(self):
        assert clamp(120.0, 0.0, 100.0) == 100.0

    def test_at_boundaries(self):
        assert clamp(0.0, 0.0, 100.0) == 0.0
        assert clamp(100.0, 0.0, 100.0) == 100.0


class TestFormatSol:
    def test_basic(self):
        assert format_sol(1.5) == "1.5000 SOL"

    def test_zero(self):
        assert format_sol(0.0) == "0.0000 SOL"

    def test_small(self):
        assert format_sol(0.0001) == "0.0001 SOL"


class TestFormatScore:
    def test_basic(self):
        assert format_score(85.3) == "85.3"

    def test_zero(self):
        assert format_score(0.0) == "0.0"


class TestFormatAge:
    def test_minutes(self):
        assert format_age(30.0) == "30m"

    def test_hours(self):
        assert format_age(120.0) == "2.0h"

    def test_exactly_60(self):
        assert "h" in format_age(60.0)


class TestFormatPct:
    def test_basic(self):
        assert format_pct(42.5) == "42.5%"

    def test_zero(self):
        assert format_pct(0.0) == "0.0%"


class TestTsToStr:
    def test_returns_string(self):
        import time
        result = ts_to_str(time.time())
        assert isinstance(result, str)
        assert len(result) > 0


class TestVerdictColor:
    def test_pass_gray(self):
        assert verdict_color(SkillVerdict.PASS) == "#6b7280"

    def test_engage_green(self):
        assert verdict_color(SkillVerdict.ENGAGE) == "#22c55e"

    def test_watch_amber(self):
        assert verdict_color(SkillVerdict.WATCH) == "#f59e0b"

    def test_scout_lime(self):
        assert verdict_color(SkillVerdict.SCOUT) == "#84cc16"


class TestVerdictEmoji:
    def test_pass_dash(self):
        assert verdict_emoji(SkillVerdict.PASS) == "—"

    def test_engage_lightning(self):
        assert verdict_emoji(SkillVerdict.ENGAGE) == "⚡"


class TestRiskLabel:
    def test_low(self):
        assert risk_label(RiskTolerance.LOW) == "Conservative"

    def test_medium(self):
        assert risk_label(RiskTolerance.MEDIUM) == "Balanced"

    def test_high(self):
        assert risk_label(RiskTolerance.HIGH) == "Aggressive"


class TestScoreBar:
    def test_contains_score(self):
        bar = score_bar(75.0)
        assert "75" in bar

    def test_brackets(self):
        bar = score_bar(50.0)
        assert "[" in bar and "]" in bar

    def test_zero(self):
        bar = score_bar(0.0, width=10)
        assert "0" in bar

    def test_100(self):
        bar = score_bar(100.0, width=10)
        assert "100" in bar
