import { useState } from 'react'
import Controls from '../components/Controls.jsx'
import FeedCard from '../components/FeedCard.jsx'
import StatePanel from '../components/StatePanel.jsx'
import MetricsChart from '../components/MetricsChart.jsx'
import ComparisonView from '../components/ComparisonView.jsx'

export default function Dashboard() {
  const [agentResult, setAgentResult] = useState(null)
  const [compareData, setCompareData] = useState(null)
  const [view, setView] = useState('single') // 'single' | 'compare'

  const handleResult = (data) => {
    setAgentResult(data)
    setCompareData(null)
    setView('single')
  }

  const handleCompare = (data) => {
    setCompareData(data)
    setAgentResult(null)
    setView('compare')
  }

  const handleReset = () => {
    setAgentResult(null)
    setCompareData(null)
    setView('single')
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <Controls onResult={handleResult} onCompare={handleCompare} onReset={handleReset} />

      {/* ── Compare view ──────────────────────────────────────── */}
      {view === 'compare' && (
        <ComparisonView compareData={compareData} />
      )}

      {/* ── Single agent view ─────────────────────────────────── */}
      {view === 'single' && agentResult && (
        <>
          {/* Agent banner */}
          <div className="glass p-4 flex items-center gap-3 animate-slide-up">
            <span className={`w-3 h-3 rounded-full ${agentResult.agent_type === 'safety' ? 'bg-brand-500' : 'bg-amber-500'}`} />
            <h2 className="text-white font-semibold capitalize">{agentResult.agent_type} Agent</h2>
            <span className="badge bg-white/5 text-slate-400 border border-white/10 ml-auto">
              Task: {agentResult.task?.name?.replace(/_/g, ' ')}
            </span>
          </div>

          {/* Grid: state panel + chart */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <StatePanel
              state={agentResult.final_state}
              grade={agentResult.grade}
              summary={agentResult.summary}
            />
            <MetricsChart
              trajectory={agentResult.trajectory}
              title={`${agentResult.agent_type} Agent — Metrics`}
            />
          </div>

          {/* Trajectory feed */}
          <div className="glass p-6 animate-fade-in">
            <p className="section-title">Feed Trajectory ({agentResult.trajectory?.length} steps)</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 max-h-[600px] overflow-y-auto pr-1">
              {agentResult.trajectory?.map((step, i) => (
                <FeedCard key={step.step} post={step} index={i} />
              ))}
            </div>
          </div>
        </>
      )}

      {/* Empty state */}
      {view === 'single' && !agentResult && !compareData && (
        <div className="glass p-12 text-center animate-fade-in">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-brand-500/20 to-purple-600/20 flex items-center justify-center">
            <span className="text-3xl">🔬</span>
          </div>
          <h2 className="text-white font-semibold text-lg mb-2">Ready to Benchmark</h2>
          <p className="text-slate-400 text-sm max-w-md mx-auto">
            Select a task scenario, then run an agent or click <strong>Compare Both</strong> to
            evaluate the engagement-only baseline vs. the safety-aware agent across all tasks.
          </p>
        </div>
      )}
    </div>
  )
}
