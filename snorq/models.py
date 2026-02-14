from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class SkillVerdict(str, Enum):
    PASS   = "PASS"    # 0–25: skip entirely
    WATCH  = "WATCH"   # 26–50: monitor, no position
    SCOUT  = "SCOUT"   # 51–75: investigate further
    ENGAGE = "ENGAGE"  # 76–100: AI agent takes position


class RiskTolerance(str, Enum):
    LOW    = "LOW"
    MEDIUM = "MEDIUM"
    HIGH   = "HIGH"


@dataclass
class TokenCandidate:
    mint:                 str
    symbol:               str
    age_minutes:          float   # minutes since PumpFun launch
    bonding_progress_pct: float   # 0–100% toward 85 SOL graduation
    sol_per_minute:       float   # bonding curve fill velocity
    holder_count:         int
    entry_cost_sol:       float   # SOL to buy 1% of remaining curve supply
    total_supply:         float   # token total supply


@dataclass
class SkillInput:
    candidates:      List[TokenCandidate]
    budget_sol:      float         = 1.0
    risk_tolerance:  RiskTolerance = RiskTolerance.MEDIUM
    max_age_minutes: float         = 60.0
    min_holders:     int           = 10


@dataclass
class SkillSignal:
    name:      str
    score:     float   # 0–100
    triggered: bool
    detail:    str
    weight:    float


@dataclass
class CandidateResult:
    candidate:         TokenCandidate
    verdict:           SkillVerdict
    score:             float
    signals:           List[SkillSignal]
    reasoning:         str
    position_size_sol: float
    timestamp:         float = field(default_factory=time.time)


@dataclass
class SkillOutput:
    input:    SkillInput
    results:  List[CandidateResult]
    top_pick: Optional[CandidateResult]
    timestamp: float = field(default_factory=time.time)

    def engage_candidates(self) -> List[CandidateResult]:
        return [r for r in self.results if r.verdict == SkillVerdict.ENGAGE]

    def watch_candidates(self) -> List[CandidateResult]:
        return [r for r in self.results if r.verdict == SkillVerdict.WATCH]

    def scout_candidates(self) -> List[CandidateResult]:
        return [r for r in self.results if r.verdict == SkillVerdict.SCOUT]
