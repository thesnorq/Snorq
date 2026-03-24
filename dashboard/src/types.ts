export type SkillVerdict  = "PASS" | "WATCH" | "SCOUT" | "ENGAGE";
export type RiskTolerance = "LOW" | "MEDIUM" | "HIGH";

export interface SkillSignal {
  name:      string;
  score:     number;
  triggered: boolean;
  detail:    string;
  weight:    number;
}

export interface TokenCandidate {
  mint:                 string;
  symbol:               string;
  age_minutes:          number;
  bonding_progress_pct: number;
  sol_per_minute:       number;
  holder_count:         number;
  entry_cost_sol:       number;
}

export interface CandidateResult {
  candidate:         TokenCandidate;
  verdict:           SkillVerdict;
  score:             number;
  signals:           SkillSignal[];
  reasoning:         string;
  position_size_sol: number;
}

export interface SkillOutput {
  results:  CandidateResult[];
  top_pick: CandidateResult | null;
}
