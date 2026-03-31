import { useState, useEffect } from "react";
import { SkillOutput, CandidateResult, SkillVerdict } from "./types";
import VerdictCard from "./components/VerdictCard";
import SignalGrid from "./components/SignalGrid";
import CandidateList from "./components/CandidateList";

const SYMBOLS = ["SNRQ", "PEPE2", "DOGE9", "MOONK", "KERO", "FLOP", "REKT", "WAGMI", "GWEI", "BONK2"];

function randomCandidate(symbol: string) {
  const age = Math.random() * 70;
  const bonding = Math.random() * 90;
  const spm = Math.random() * 1.5;
  const holders = Math.floor(Math.random() * 100) + 5;
  const ageScore = age < 5 ? 100 : age < 15 ? 85 : age < 30 ? 60 : age < 60 ? 35 : 10;
  const momScore = Math.min(spm * 100, 100);
  const progScore = Math.max(0, 100 - bonding);
  const holdScore = Math.min((holders / 20) * 50, 100);
  const score = ageScore * 0.30 + momScore * 0.35 + progScore * 0.20 + holdScore * 0.15;
  const verdict: SkillVerdict = score >= 76 ? "ENGAGE" : score >= 51 ? "SCOUT" : score >= 26 ? "WATCH" : "PASS";
  const active = [];
  if (age < 15) active.push("age");
  if (spm >= 0.5) active.push("momentum");
  if (bonding < 40) active.push("progress");
  if (holders >= 20) active.push("holders");

  const result: CandidateResult = {
    candidate: { mint: `${symbol}${Math.random().toString(36).slice(2, 8)}pump`, symbol, age_minutes: age, bonding_progress_pct: bonding, sol_per_minute: spm, holder_count: holders, entry_cost_sol: 0.05 },
    verdict, score,
    signals: [
      { name: "age",      score: ageScore,  triggered: age < 15,     detail: `Token launched ${age.toFixed(1)} min ago`, weight: 0.30 },
      { name: "momentum", score: momScore,  triggered: spm >= 0.5,   detail: `${spm.toFixed(3)} SOL/min velocity`,       weight: 0.35 },
      { name: "progress", score: progScore, triggered: bonding < 40, detail: `Bonding at ${bonding.toFixed(1)}%`,         weight: 0.20 },
      { name: "holders",  score: holdScore, triggered: holders >= 20, detail: `${holders} holders`,                      weight: 0.15 },
    ],
    reasoning: verdict === "ENGAGE"
      ? `Strong multi-signal confirmation. AI agent should take position. Active signals: ${active.join(", ")}.`
      : verdict === "SCOUT" ? "Promising early signals. Gather more data before committing."
      : verdict === "WATCH" ? "Some signals active. Monitor for momentum shift."
      : "Token does not meet minimum criteria. Skip.",
    position_size_sol: verdict === "ENGAGE" ? parseFloat((score / 100 * 0.5).toFixed(4)) : 0,
  };
  return result;
}

function mockOutput(): SkillOutput {
  const results = SYMBOLS.slice(0, 6)
    .map(s => randomCandidate(s))
    .sort((a, b) => b.score - a.score);
  const top_pick = results.find(r => r.verdict === "ENGAGE") ?? null;
  return { results, top_pick };
}

export default function App() {
  const [output, setOutput] = useState<SkillOutput>(mockOutput());
  const [selected, setSelected] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setOutput(mockOutput());
      setSelected(0);
    }, 4000);
    return () => clearInterval(id);
  }, []);

  const current = output.results[selected];

  return (
    <div style={{ minHeight: "100vh", background: "#030501", color: "#e2e8f0", fontFamily: "monospace", padding: "32px 24px" }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: 28, borderBottom: "1px solid #1a2100", paddingBottom: 18 }}>
          <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: "#84cc16", letterSpacing: 3 }}>SNORQ</h1>
          <div style={{ fontSize: 11, color: "#4b5563", marginTop: 4, letterSpacing: 1 }}>
            AI AGENT SKILL · PUMPFUN LAUNCH SCOUT · SOLANA
          </div>
          <div style={{ display: "flex", gap: 16, marginTop: 10, fontSize: 11 }}>
            <span style={{ color: "#84cc16" }}>● SCANNING</span>
            {output.top_pick && (
              <span style={{ color: "#22c55e" }}>⚡ TOP PICK: ${output.top_pick.candidate.symbol} ({output.top_pick.score.toFixed(0)})</span>
            )}
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 20 }}>
          {/* Left: candidate list */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={{ fontSize: 11, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1 }}>
              Candidates ({output.results.length})
            </div>
            <CandidateList results={output.results} selected={selected} onSelect={setSelected} />
          </div>

          {/* Right: detail */}
          {current && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <VerdictCard result={current} />
              <div style={{ background: "#060a01", border: "1px solid #1a2100", borderRadius: 12, padding: 18 }}>
                <div style={{ fontSize: 11, color: "#4b5563", textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
                  Signal Breakdown
                </div>
                <SignalGrid signals={current.signals} />
              </div>
            </div>
          )}
        </div>

        <div style={{ marginTop: 28, fontSize: 11, color: "#1f2937", textAlign: "center" }}>
          built by snorqdev · pumpsniff · agentskill
        </div>
      </div>
    </div>
  );
}
