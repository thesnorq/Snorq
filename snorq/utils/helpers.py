from __future__ import annotations

import time
from ..models import SkillVerdict, RiskTolerance


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def format_sol(sol: float) -> str:
    return f"{sol:.4f} SOL"


def format_score(score: float) -> str:
    return f"{score:.1f}"


def format_age(minutes: float) -> str:
    if minutes < 60:
        return f"{minutes:.0f}m"
    return f"{minutes / 60:.1f}h"


def format_pct(value: float) -> str:
    return f"{value:.1f}%"


def ts_to_str(ts: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def verdict_color(verdict: SkillVerdict) -> str:
    return {
        SkillVerdict.PASS:   "#6b7280",
        SkillVerdict.WATCH:  "#f59e0b",
        SkillVerdict.SCOUT:  "#84cc16",
        SkillVerdict.ENGAGE: "#22c55e",
    }.get(verdict, "#6b7280")


def verdict_emoji(verdict: SkillVerdict) -> str:
    return {
        SkillVerdict.PASS:   "—",
        SkillVerdict.WATCH:  "👁",
        SkillVerdict.SCOUT:  "🔍",
        SkillVerdict.ENGAGE: "⚡",
    }.get(verdict, "?")


def risk_label(risk: RiskTolerance) -> str:
    return {
        RiskTolerance.LOW:    "Conservative",
        RiskTolerance.MEDIUM: "Balanced",
        RiskTolerance.HIGH:   "Aggressive",
    }.get(risk, "Unknown")


def score_bar(score: float, width: int = 20) -> str:
    filled = round((score / 100.0) * width)
    return "[" + "█" * filled + "░" * (width - filled) + f"] {score:.0f}"
