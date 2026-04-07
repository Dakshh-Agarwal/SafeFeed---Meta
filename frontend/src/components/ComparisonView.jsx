import MetricsChart from './MetricsChart.jsx'

export default function ComparisonView({ compareData }) {
  if (!compareData || !compareData.tasks || compareData.tasks.length === 0) {
    return (
      <div className="glass p-6 text-center text-slate-500 text-sm animate-fade-in">
        Click <strong>"Compare Both"</strong> to run both agents across all tasks.
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {compareData.tasks.map((item, idx) => (
        <div key={item.task.id} className="glass p-6">
          {/* Task header */}
          <div className="flex items-center gap-3 mb-5">
            <span className="w-8 h-8 rounded-lg bg-brand-500/20 flex items-center justify-center text-brand-300 font-bold text-sm">
              T{item.task.id}
            </span>
            <div>
              <h3 className="text-white font-semibold text-base">{item.task.name.replace(/_/g, ' ')}</h3>
              <p className="text-slate-400 text-xs">{item.task.description}</p>
            </div>
          </div>

          {/* Score cards side-by-side */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">
            {/* Engagement Agent */}
            <AgentScoreCard
              agentLabel="Engagement Agent"
              color="amber"
              grade={item.engagement_agent.grade}
              summary={item.engagement_agent.summary}
            />
            {/* Safety Agent */}
            <AgentScoreCard
              agentLabel="Safety Agent"
              color="brand"
              grade={item.safety_agent.grade}
              summary={item.safety_agent.summary}
            />
          </div>

          {/* Charts side-by-side */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <MetricsChart trajectory={item.engagement_agent.trajectory} title="Engagement Agent Trajectory" />
            <MetricsChart trajectory={item.safety_agent.trajectory}     title="Safety Agent Trajectory" />
          </div>
        </div>
      ))}
    </div>
  )
}


function AgentScoreCard({ agentLabel, color, grade, summary }) {
  const borderColor = color === 'brand'
    ? 'border-brand-500/25 bg-brand-500/5'
    : 'border-amber-500/25 bg-amber-500/5'
  const accentText = color === 'brand' ? 'text-brand-300' : 'text-amber-300'

  return (
    <div className={`rounded-xl border p-4 ${borderColor}`}>
      <p className={`text-xs font-bold uppercase tracking-wider mb-3 ${accentText}`}>{agentLabel}</p>

      {/* Score */}
      <div className="flex items-baseline gap-2 mb-3">
        <span className="text-3xl font-bold text-white font-mono">{grade?.score?.toFixed(4)}</span>
        <span className="text-xs text-slate-500">combined score</span>
      </div>

      {/* Subscores */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <SubScore label="Engagement" value={grade?.metrics?.engagement_score} color="#f59e0b" />
        <SubScore label="Safety"     value={grade?.metrics?.safety_score}     color="#10b981" />
        <SubScore label="Diversity"  value={grade?.metrics?.diversity_score}  color="#6e8dff" />
      </div>

      {/* Summary stats */}
      {summary && (
        <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400 mt-2">
          <span>⏱ {summary.total_watch_time}s</span>
          <span>🌀 {summary.final_spiral_risk?.toFixed(1)}</span>
          <span>⚠ {summary.risky_posts_shown} risky</span>
          <span>📂 {summary.categories_seen?.length} cats</span>
        </div>
      )}
    </div>
  )
}


function SubScore({ label, value, color }) {
  const pct = Math.round((value ?? 0) * 100)
  return (
    <div>
      <p className="text-[0.6rem] text-slate-500 uppercase tracking-wider mb-0.5">{label}</p>
      <p className="text-white font-bold text-sm font-mono">{value?.toFixed(3)}</p>
      <div className="progress-bar mt-1">
        <div className="progress-fill" style={{ width: `${pct}%`, background: color }} />
      </div>
    </div>
  )
}
