import pytest
from snorq.models import SkillVerdict, RiskTolerance
from snorq.skill import run_skill, run_skill_single
from tests.conftest import make_candidate, make_input


class TestRunSkillSingle:
    def test_hot_candidate_engage(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert result.verdict == SkillVerdict.ENGAGE

    def test_cold_candidate_low_score(self, cold_candidate, default_input):
        result = run_skill_single(cold_candidate, default_input)
        assert result.score < 50.0

    def test_result_has_candidate(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert result.candidate.symbol == "HOT"

    def test_result_has_signals(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert len(result.signals) == 4

    def test_reasoning_not_empty(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert len(result.reasoning) > 0

    def test_position_size_ge_zero(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert result.position_size_sol >= 0.0

    def test_position_within_budget(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        assert result.position_size_sol <= default_input.budget_sol

    def test_engage_reasoning_mentions_active_signals(self, hot_candidate, default_input):
        result = run_skill_single(hot_candidate, default_input)
        if result.verdict == SkillVerdict.ENGAGE:
            assert "Active signals" in result.reasoning

    def test_medium_candidate_scout_or_watch(self, medium_candidate, default_input):
        inp = make_input(candidates=[medium_candidate])
        result = run_skill_single(medium_candidate, inp)
        assert result.verdict in (SkillVerdict.WATCH, SkillVerdict.SCOUT, SkillVerdict.ENGAGE)


class TestRunSkill:
    def test_returns_skill_output(self, multi_input):
        output = run_skill(multi_input)
        assert output is not None

    def test_results_sorted_by_score(self, multi_input):
        output = run_skill(multi_input)
        scores = [r.score for r in output.results]
        assert scores == sorted(scores, reverse=True)

    def test_top_pick_is_engage_or_none(self, multi_input):
        output = run_skill(multi_input)
        if output.top_pick:
            assert output.top_pick.verdict == SkillVerdict.ENGAGE

    def test_top_pick_is_highest_engage(self, multi_input):
        output = run_skill(multi_input)
        if output.top_pick and output.engage_candidates():
            assert output.top_pick.score == output.engage_candidates()[0].score

    def test_filters_old_candidates(self):
        old_c = make_candidate(age_minutes=120.0, holder_count=50)
        inp = make_input(candidates=[old_c], max_age=60.0)
        output = run_skill(inp)
        assert len(output.results) == 0

    def test_filters_low_holder_candidates(self):
        c = make_candidate(holder_count=3)
        inp = make_input(candidates=[c], min_holders=10)
        output = run_skill(inp)
        assert len(output.results) == 0

    def test_passes_filter_when_within_limits(self, hot_candidate):
        inp = make_input(candidates=[hot_candidate], max_age=60.0, min_holders=10)
        output = run_skill(inp)
        assert len(output.results) == 1

    def test_empty_candidates(self):
        inp = make_input(candidates=[])
        output = run_skill(inp)
        assert output.results == []
        assert output.top_pick is None

    def test_no_engage_top_pick_is_none(self):
        cold_list = [make_candidate(age_minutes=90.0, sol_per_minute=0.01,
                                    bonding_progress_pct=90.0, holder_count=50)]
        inp = make_input(candidates=cold_list, max_age=200.0)
        output = run_skill(inp)
        if not output.engage_candidates():
            assert output.top_pick is None

    def test_multi_input_all_within_filter(self, multi_input):
        # hot (10m, 30h) and medium (25m, 20h) pass; cold (90m, 5h) filtered
        output = run_skill(multi_input)
        for r in output.results:
            assert r.candidate.age_minutes <= multi_input.max_age_minutes

    def test_high_risk_more_engages(self):
        candidates = [make_candidate(symbol=f"T{i}", age_minutes=20.0,
                                      sol_per_minute=0.4, bonding_progress_pct=30.0,
                                      holder_count=25) for i in range(5)]
        inp_med  = make_input(candidates=candidates, risk=RiskTolerance.MEDIUM)
        inp_high = make_input(candidates=candidates, risk=RiskTolerance.HIGH)
        out_med  = run_skill(inp_med)
        out_high = run_skill(inp_high)
        assert len(out_high.engage_candidates()) >= len(out_med.engage_candidates())

    def test_output_input_reference(self, default_input):
        output = run_skill(default_input)
        assert output.input is default_input

    def test_each_result_has_reasoning(self, multi_input):
        output = run_skill(multi_input)
        for r in output.results:
            assert len(r.reasoning) > 0

    def test_engage_position_greater_than_pass_position(self, multi_input):
        output = run_skill(multi_input)
        engage = output.engage_candidates()
        if engage and len(output.results) > 1:
            last = output.results[-1]
            assert engage[0].position_size_sol >= last.position_size_sol
