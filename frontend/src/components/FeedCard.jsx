export default function FeedCard({ post, index }) {
  if (!post) return null

  const riskColor =
    post.risk_score >= 6 ? 'text-red-400 bg-red-500/15 border-red-500/20' :
    post.risk_score >= 3 ? 'text-amber-400 bg-amber-500/15 border-amber-500/20' :
                           'text-emerald-400 bg-emerald-500/15 border-emerald-500/20'

  const engColor =
    post.engagement_score >= 8 ? 'text-brand-300 bg-brand-500/15 border-brand-500/20' :
                                 'text-slate-300 bg-white/5 border-white/10'

  return (
    <div className="glass p-4 animate-slide-up hover:border-brand-500/30 transition-all duration-200" style={{ animationDelay: `${index * 40}ms` }}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          {/* Step number */}
          <span className="text-[0.65rem] font-bold text-slate-500 uppercase tracking-wider">
            Step {post.step}
          </span>

          {/* Title */}
          <h3 className="text-white font-semibold text-sm mt-1 leading-snug truncate">
            {post.title}
          </h3>

          {/* Category tag */}
          <span className="inline-block mt-2 text-xs px-2 py-0.5 rounded-full bg-white/5 text-slate-400 border border-white/5">
            {post.category}
          </span>
        </div>

        {/* Scores column */}
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`badge border ${engColor}`}>
            ⚡ {post.engagement_score}
          </span>
          <span className={`badge border ${riskColor}`}>
            ⚠ {post.risk_score}
          </span>
        </div>
      </div>

      {/* Reward */}
      <div className="mt-3 flex items-center gap-3 text-xs">
        <span className="text-slate-500">Reward</span>
        <span className={`font-mono font-semibold ${post.reward >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
          {post.reward >= 0 ? '+' : ''}{post.reward?.toFixed(3)}
        </span>
      </div>
    </div>
  )
}
