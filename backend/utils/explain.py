"""
explain.py

Rule-based explainability helper.
Returns human-readable explanations for why a post was selected.
No LLM required.
"""

RISK_THRESHOLD       = 5.0
HIGH_ENGAGEMENT      = 7.5
LOW_SPIRAL_SAFE      = 2.0
HIGH_SPIRAL_DANGER   = 6.0


def explain_recommendation(state: dict, post: dict, agent_type: str = "safety") -> str:
    """
    Generate a plain-English explanation for why this post was recommended.

    Args:
        state:      Current session state after update.
        post:       The post that was recommended.
        agent_type: "safety", "engagement", or "env".

    Returns:
        A readable explanation string.
    """
    title        = post.get("title", "This post")
    category     = post.get("category", "general")
    eng          = post.get("engagement_score", 5.0)
    risk         = post.get("risk_score", 0.0)
    spiral       = state.get("spiral_risk", 0.0)
    recent_cats  = state.get("recent_categories", [])
    diversity    = state.get("diversity_score", 1.0)

    is_risky     = risk >= RISK_THRESHOLD
    is_new_cat   = recent_cats.count(category) <= 1
    high_eng     = eng >= HIGH_ENGAGEMENT
    spiral_high  = spiral >= HIGH_SPIRAL_DANGER

    # --- Engagement agent ---
    if agent_type == "engagement":
        if high_eng:
            return (
                f'"{title}" was selected because it has one of the highest engagement '
                f"scores ({eng}/10) in the current content pool. "
                "The engagement agent always picks the most engaging item regardless of risk."
            )
        return (
            f'"{title}" was selected as the highest-engagement post available '
            f"(score: {eng}/10)."
        )

    # --- Safety agent ---
    parts = []

    if high_eng and not is_risky:
        parts.append(f"strong engagement ({eng}/10) with low risk ({risk}/10)")
    elif high_eng and is_risky:
        parts.append(f"high engagement ({eng}/10), though risk is noted ({risk}/10)")
    else:
        parts.append(f"moderate engagement ({eng}/10)")

    if is_new_cat:
        parts.append(f"it introduces a new category ({category}) improving feed diversity")
    else:
        parts.append(f"it continues the {category} interest pattern")

    if spiral_high:
        parts.append(
            f"the session spiral risk is elevated ({spiral:.1f}/10), "
            "so safer content was prioritised"
        )
    elif spiral >= LOW_SPIRAL_SAFE:
        parts.append("spiral risk is moderate — safety weighting is active")

    if diversity < 0.5:
        parts.append("diversity is low, so category variety was boosted")

    if not parts:
        return f'"{title}" was selected as the best available option.'

    reason = "; ".join(parts)
    return f'"{title}" was selected because: {reason}.'
