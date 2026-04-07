export default function StatePanel({ state, grade, summary }) {
  if (!state && !grade) {
    return (
      <div className="glass p-6 text-center text-slate-500 text-sm animate-fade-in">
        Run an agent to see session metrics.
      </div>
    )
  }

  const metrics = [
    { label: 'Steps',           value: state?.step_count ?? summary?.steps ?? '—',         icon: '📊' },
    { label: 'Watch Time',      value: `${state?.watch_time ?? summary?.total_watch_time ?? 0}s`, icon: '⏱' },
    { label: 'Spiral Risk',     value: (state?.spiral_risk ?? summary?.final_spiral_risk ?? 0).toFixed(2), icon: '🌀', color: riskBarColor(state?.spiral_risk ?? summary?.final_spiral_risk ?? 0) },
    { label: 'Repetition',     value: (state?.repetition_score ?? summary?.final_repetition ?? 0).toFixed(2), icon: '🔁' },
    { label: 'Diversity',       value: (state?.diversity_score ?? summary?.final_diversity ?? 0).toFixed(2), icon: '🎨' },
    { label: 'Posts Seen',      value: state?.posts_seen?.length ?? summary?.steps ?? '—',  icon: '📰' },
  ]

  const gradeMetrics = grade ? [
    { label: 'Combined Score',  value: grade.score?.toFixed(4),                            icon: '🏆', highlight: true },
    { label: 'Engagement',      value: grade.metrics?.engagement_score?.toFixed(4),        icon: '⚡' },
    { label: 'Safety',          value: grade.metrics?.safety_score?.toFixed(4),            icon: '🛡' },
    { label: 'Diversity',       value: grade.metrics?.diversity_score?.toFixed(4),         icon: '🎯' },
  ] : []

  return (
    <div className="glass p-6 animate-fade-in">
      <p className="section-title">Session State</p>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-5">
        {metrics.map((m) => (
          <div key={m.label} className="bg-surface-700/50 rounded-xl p-3">
            <div className="flex items-center gap-1.5 mb-1">
              <span className="text-sm">{m.icon}</span>
              <span className="text-[0.65rem] font-semibold text-slate-400 uppercase tracking-wider">{m.label}</span>
            </div>
            <span className="text-white font-bold text-lg">{m.value}</span>
            {m.color && (
              <div className="progress-bar mt-1.5">
                <div className="progress-fill" style={{ width: `${Math.min(100, (parseFloat(m.value) / 10) * 100)}%`, background: m.color }} />
              </div>
            )}
          </div>
        ))}
      </div>

      {gradeMetrics.length > 0 && (
        <>
          <p className="section-title">Grade (OpenEnv)</p>
          <div className="grid grid-cols-2 gap-3">
            {gradeMetrics.map((m) => (
              <div key={m.label} className={`rounded-xl p-3 ${m.highlight ? 'bg-gradient-to-br from-brand-500/20 to-purple-600/20 border border-brand-500/20' : 'bg-surface-700/50'}`}>
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="text-sm">{m.icon}</span>
                  <span className="text-[0.65rem] font-semibold text-slate-400 uppercase tracking-wider">{m.label}</span>
                </div>
                <span className={`font-bold text-lg font-mono ${m.highlight ? 'gradient-text' : 'text-white'}`}>{m.value}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function riskBarColor(risk) {
  if (risk >= 6) return '#ef4444'
  if (risk >= 3) return '#f59e0b'
  return '#10b981'
}
