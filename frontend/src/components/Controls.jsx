import { useState } from 'react'

const API = '/api'

export default function Controls({ onResult, onCompare, onReset }) {
  const [loading, setLoading] = useState(null) // 'engagement' | 'safety' | 'compare' | null
  const [taskId, setTaskId] = useState(0)
  const [steps, setSteps] = useState(20)

  const runAgent = async (agentType) => {
    setLoading(agentType)
    try {
      const res = await fetch(`${API}/run-agent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent_type: agentType, task_id: taskId, steps }),
      })
      const data = await res.json()
      onResult(data)
    } catch (err) {
      console.error('Run agent error:', err)
    } finally {
      setLoading(null)
    }
  }

  const compare = async () => {
    setLoading('compare')
    try {
      const res = await fetch(`${API}/compare`)
      const data = await res.json()
      onCompare(data)
    } catch (err) {
      console.error('Compare error:', err)
    } finally {
      setLoading(null)
    }
  }

  const reset = () => {
    onReset()
  }

  return (
    <div className="glass p-6 animate-fade-in">
      <p className="section-title">Controls</p>

      {/* Task & Steps selectors */}
      <div className="flex flex-wrap gap-4 mb-5">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-400 font-medium">Task Scenario</label>
          <select
            id="task-selector"
            value={taskId}
            onChange={(e) => setTaskId(Number(e.target.value))}
            className="bg-surface-700 text-white border border-white/10 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-brand-500 transition"
          >
            <option value={0}>Balanced Feed</option>
            <option value={1}>High Risk Feed</option>
            <option value={2}>Low Diversity Feed</option>
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs text-slate-400 font-medium">Steps</label>
          <input
            id="steps-input"
            type="number"
            min={5}
            max={50}
            value={steps}
            onChange={(e) => setSteps(Number(e.target.value))}
            className="bg-surface-700 text-white border border-white/10 rounded-lg px-3 py-2 text-sm w-20 focus:outline-none focus:border-brand-500 transition"
          />
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-3">
        <button
          id="btn-run-engagement"
          className="btn btn-secondary"
          disabled={loading !== null}
          onClick={() => runAgent('engagement')}
        >
          {loading === 'engagement' && <span className="spinner" />}
          Run Engagement Agent
        </button>

        <button
          id="btn-run-safety"
          className="btn btn-primary"
          disabled={loading !== null}
          onClick={() => runAgent('safety')}
        >
          {loading === 'safety' && <span className="spinner" />}
          Run Safety Agent
        </button>

        <button
          id="btn-compare"
          className="btn btn-success"
          disabled={loading !== null}
          onClick={compare}
        >
          {loading === 'compare' && <span className="spinner" />}
          Compare Both
        </button>

        <button
          id="btn-reset"
          className="btn btn-danger"
          disabled={loading !== null}
          onClick={reset}
        >
          Reset
        </button>
      </div>
    </div>
  )
}
