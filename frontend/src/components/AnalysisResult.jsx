function ScoreRing({ score }) {
  const color = score >= 75 ? "#22c55e" : score >= 50 ? "#eab308" : "#ef4444";
  return (
    <div className="score-ring" style={{ borderColor: color }}>
      <span style={{ color }}>{score}</span>
      <small>ATS Score</small>
    </div>
  );
}

function ListSection({ title, items, tone }) {
  if (!items || items.length === 0) return null;
  return (
    <div className={`list-section ${tone}`}>
      <h4>{title}</h4>
      <ul>
        {items.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default function AnalysisResult({ analysis }) {
  if (!analysis) return null;

  if (analysis.status === "failed") {
    return (
      <div className="analysis-card error">
        <h3>Analysis failed</h3>
        <p>{analysis.error_message}</p>
      </div>
    );
  }

  return (
    <div className="analysis-card">
      <div className="analysis-header">
        <ScoreRing score={analysis.ats_score ?? 0} />
        <p className="summary">{analysis.summary}</p>
      </div>

      <div className="analysis-grid">
        <ListSection title="Strengths" items={analysis.strengths} tone="positive" />
        <ListSection title="Weaknesses" items={analysis.weaknesses} tone="negative" />
        <ListSection title="Missing Skills" items={analysis.missing_skills} tone="neutral" />
        <ListSection title="Suggestions" items={analysis.suggestions} tone="info" />
      </div>
    </div>
  );
}
