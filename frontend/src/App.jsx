import { useState } from 'react'
import Dashboard from './pages/Dashboard.jsx'

export default function App() {
  return (
    <div className="min-h-screen bg-surface-900">
      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="border-b border-white/5 bg-surface-800/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Logo mark */}
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 to-purple-600 flex items-center justify-center shadow-lg shadow-brand-500/30">
              <span className="text-white font-bold text-sm">SF</span>
            </div>
            <div>
              <h1 className="text-white font-bold text-lg leading-none">SafeFeed</h1>
              <p className="text-brand-400 text-xs leading-none mt-0.5">Feed Ranking Benchmark</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="badge bg-purple-500/15 text-purple-300 border border-purple-500/20">
              OpenEnv Compatible
            </span>
            <span className="badge bg-brand-500/15 text-brand-300 border border-brand-500/20">
              Meta × Scaler Hackathon
            </span>
          </div>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────────────────── */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Dashboard />
      </main>

      {/* ── Footer ─────────────────────────────────────────────── */}
      <footer className="border-t border-white/5 mt-12 py-6 text-center text-xs text-slate-500">
        SafeFeed · OpenEnv Benchmark · Meta PyTorch Hackathon x Scaler School of Technology
      </footer>
    </div>
  )
}
