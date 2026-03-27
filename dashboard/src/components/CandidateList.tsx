import { CandidateResult, SkillVerdict } from "../types";

interface Props { results: CandidateResult[]; selected: number; onSelect: (i: number) => void; }

const VERDICT_COLOR: Record<SkillVerdict, string> = {
  PASS: "#6b7280", WATCH: "#f59e0b", SCOUT: "#84cc16", ENGAGE: "#22c55e",
};

export default function CandidateList({ results, selected, onSelect }: Props) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      {results.map((r, i) => (
        <div
          key={r.candidate.mint}
          onClick={() => onSelect(i)}
          style={{
            background: selected === i ? "#0d1f00" : "#060a01",
            border: `1px solid ${selected === i ? "#3f6212" : "#1a2100"}`,
            borderRadius: 8, padding: "8px 12px", cursor: "pointer",
            display: "flex", justifyContent: "space-between", alignItems: "center",
          }}
        >
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#d9f99d" }}>${r.candidate.symbol}</div>
            <div style={{ fontSize: 10, color: "#4b5563", marginTop: 2 }}>
              {r.candidate.age_minutes.toFixed(0)}m · {r.candidate.bonding_progress_pct.toFixed(0)}% bonding
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 16, fontWeight: 800, color: VERDICT_COLOR[r.verdict] }}>
              {r.score.toFixed(0)}
            </div>
            <div style={{ fontSize: 10, color: VERDICT_COLOR[r.verdict], fontWeight: 600 }}>
              {r.verdict}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
