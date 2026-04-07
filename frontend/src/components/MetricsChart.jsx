import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend,
} from 'recharts'

export default function MetricsChart({ trajectory, title }) {
  if (!trajectory || trajectory.length === 0) {
    return (
      <div className="glass p-6 text-center text-slate-500 text-sm animate-fade-in">
        No trajectory data yet.
      </div>
    )
  }

  const data = trajectory.map((s) => ({
    step:        s.step,
    reward:      parseFloat(s.reward?.toFixed(3)),
    spiralRisk:  parseFloat(s.spiral_risk?.toFixed(2)),
    diversity:   parseFloat(s.diversity_score?.toFixed(2)),
    engagement:  parseFloat((s.engagement_score / 10).toFixed(2)),
  }))

  return (
    <div className="glass p-6 animate-fade-in">
      <p className="section-title">{title || 'Metrics Over Time'}</p>

      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 4, right: 20, bottom: 4, left: -10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis
              dataKey="step"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.08)' }}
            />
            <Tooltip
              contentStyle={{
                background: '#1a1e36',
                border: '1px solid rgba(74,108,247,0.25)',
                borderRadius: 10,
                fontSize: 12,
                color: '#e2e8f0',
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: 11, color: '#94a3b8' }}
            />
            <Line
              type="monotone"
              dataKey="reward"
              name="Reward"
              stroke="#4a6cf7"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#4a6cf7' }}
            />
            <Line
              type="monotone"
              dataKey="spiralRisk"
              name="Spiral Risk"
              stroke="#ef4444"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#ef4444' }}
            />
            <Line
              type="monotone"
              dataKey="diversity"
              name="Diversity"
              stroke="#10b981"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4, fill: '#10b981' }}
            />
            <Line
              type="monotone"
              dataKey="engagement"
              name="Engagement"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={false}
              strokeDasharray="5 3"
              activeDot={{ r: 4, fill: '#f59e0b' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
