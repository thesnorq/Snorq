import { SkillSignal } from "../types";

interface Props { signals: SkillSignal[]; }

const LABELS: Record<string, string> = {
  age:      "Launch Age",
  momentum: "Momentum",
  progress: "Bonding Stage",
  holders:  "Holder Count",
};

export default function SignalGrid({ signals }: Props) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {signals.map(s => (
        <div key={s.name} style={{
          background: "#060a01",
          border: `1px solid ${s.triggered ? "#3f6212" : "#1f2937"}`,
          borderRadius: 8, padding: "8px 12px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
            <span style={{ fontSize: 11, fontWeight: 600, color: s.triggered ? "#84cc16" : "#6b7280" }}>
              {s.triggered ? "▶" : "○"} {LABELS[s.name] ?? s.name}
            </span>
            <span style={{ fontSize: 11, fontWeight: 700, color: s.triggered ? "#65a30d" : "#374151" }}>
              {s.score.toFixed(0)} <span style={{ fontSize: 9, color: "#4b5563" }}>w:{(s.weight*100).toFixed(0)}%</span>
            </span>
          </div>
          <div style={{ background: "#0a1200", borderRadius: 3, height: 4, marginBottom: 4 }}>
            <div style={{
              width: `${s.score}%`, height: "100%", borderRadius: 3,
              background: s.triggered ? "#84cc16" : "#374151",
            }} />
          </div>
          <div style={{ fontSize: 10, color: "#4b5563" }}>{s.detail}</div>
        </div>
      ))}
    </div>
  );
}
