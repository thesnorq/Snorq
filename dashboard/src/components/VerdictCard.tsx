import { CandidateResult, SkillVerdict } from "../types";

interface Props { result: CandidateResult; }

const VERDICT_COLOR: Record<SkillVerdict, string> = {
  PASS:   "#6b7280",
  WATCH:  "#f59e0b",
  SCOUT:  "#84cc16",
  ENGAGE: "#22c55e",
};

const VERDICT_ICON: Record<SkillVerdict, string> = {
  PASS: "—", WATCH: "👁", SCOUT: "🔍", ENGAGE: "⚡",
};

export default function VerdictCard({ result }: Props) {
  const color = VERDICT_COLOR[result.verdict];
  return (
    <div style={{ background: "#060a01", border: `1px solid ${color}44`, borderRadius: 12, padding: 20 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 20, fontWeight: 800, color: "#d9f99d" }}>${result.candidate.symbol}</div>
          <div style={{ fontSize: 10, color: "#4b5563", marginTop: 2, fontFamily: "monospace" }}>
            {result.candidate.mint.slice(0, 12)}...
          </div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 28, fontWeight: 800, color, lineHeight: 1 }}>
            {result.score.toFixed(0)}
          </div>
          <div style={{
            display: "inline-block", marginTop: 6,
            padding: "2px 12px", borderRadius: 20,
            background: `${color}22`, border: `1px solid ${color}`,
            color, fontSize: 11, fontWeight: 700,
          }}>
            {VERDICT_ICON[result.verdict]} {result.verdict}
          </div>
        </div>
      </div>

      {/* Score bar */}
      <div style={{ background: "#0a1200", borderRadius: 4, height: 5, marginBottom: 12 }}>
        <div style={{
          width: `${result.score}%`, height: "100%", borderRadius: 4,
          background: `linear-gradient(90deg, #1a2e00, ${color})`,
          transition: "width 0.5s ease",
        }} />
      </div>

      {/* Stats grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 12 }}>
        {[
          ["Age", `${result.candidate.age_minutes.toFixed(0)}m`],
          ["Bonding", `${result.candidate.bonding_progress_pct.toFixed(0)}%`],
          ["Holders", `${result.candidate.holder_count}`],
        ].map(([k, v]) => (
          <div key={k} style={{ background: "#0a1200", borderRadius: 6, padding: "6px 10px" }}>
            <div style={{ fontSize: 9, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1 }}>{k}</div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "#84cc16", marginTop: 2 }}>{v}</div>
          </div>
        ))}
      </div>

      {/* Position */}
      {result.verdict === "ENGAGE" && (
        <div style={{ background: "#052105", border: "1px solid #166534", borderRadius: 8, padding: "8px 12px", fontSize: 12 }}>
          <span style={{ color: "#4ade80", fontWeight: 700 }}>Position: </span>
          <span style={{ color: "#86efac" }}>{result.position_size_sol.toFixed(4)} SOL</span>
        </div>
      )}

      <div style={{ fontSize: 11, color: "#6b7280", marginTop: 10, lineHeight: 1.5 }}>
        {result.reasoning}
      </div>
    </div>
  );
}
