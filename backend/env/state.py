"""
state.py

Session state model for a simulated feed session.
Tracks engagement, safety signals, and diversity metrics.
"""

SCORE_MIN = 0.0001
SCORE_MAX = 0.9999


def init_state() -> dict:
    """
    Return a fresh initial session state.
    All fields reset to zero / empty.
    """
    return {
        # Step counters
        "step_count": 0,
        "session_time": 0,       # simulated seconds

        # Interaction logs
        "posts_seen": [],        # list of post IDs
        "liked_posts": [],       # post IDs that got a 'like'
        "skipped_posts": [],     # post IDs that were skipped

        # Watch time
        "watch_time": 0,         # total simulated watch seconds

        # Safety / quality signals
        "spiral_risk": 0.0,         # 0-10 scale; higher = more at-risk
        "repetition_score": SCORE_MIN, # avoid exact 0.0 boundary leaks
        "diversity_score": SCORE_MAX,  # avoid exact 1.0 boundary leaks

        # Recent history for locality-aware computations
        "recent_categories": [], # rolling window of last N categories seen
        "recent_risky_count": 0, # how many risky posts in recent window
    }


def update_state(state: dict, post: dict, task_config: dict) -> dict:
    """
    Apply the effect of showing a post to the session state.

    Args:
        state:       Current session state dict.
        post:        The post being shown.
        task_config: Active task configuration dict.

    Returns:
        Updated state dict (modified in place and returned).
    """
    WINDOW_SIZE = 5  # rolling window for recency calculations

    # --- Step / time ---
    state["step_count"] += 1
    watch_seconds = _simulated_watch_time(post)
    state["watch_time"] += watch_seconds
    state["session_time"] += watch_seconds + 2  # +2s for scroll/transition

    # --- Interaction history ---
    state["posts_seen"].append(post["id"])

    # Simple engagement heuristic: like if engagement > 7.5
    if post["engagement_score"] >= 7.5:
        state["liked_posts"].append(post["id"])
    elif post["engagement_score"] < 5.0:
        state["skipped_posts"].append(post["id"])

    # --- Recent categories (rolling window) ---
    state["recent_categories"].append(post["category"])
    if len(state["recent_categories"]) > WINDOW_SIZE:
        state["recent_categories"].pop(0)

    # --- Spiral risk ---
    is_risky = post["risk_score"] >= 5.0
    if is_risky:
        state["recent_risky_count"] += 1
    else:
        # slowly decay risky count when safe content is shown
        state["recent_risky_count"] = max(0, state["recent_risky_count"] - 0.5)

    # Spiral risk formula:
    # base from post risk, amplified by streak and task bias
    risk_bias = task_config.get("risk_bias", 0.3)
    spiral_delta = (post["risk_score"] / 10.0) * (1 + 0.4 * state["recent_risky_count"]) * (1 + risk_bias)
    if is_risky:
        state["spiral_risk"] = min(10.0, state["spiral_risk"] + spiral_delta)
    else:
        # safe content slowly reduces spiral risk
        state["spiral_risk"] = max(0.0, state["spiral_risk"] - 0.3)

    # --- Repetition score ---
    repeat_bias = task_config.get("repeat_bias", 0.3)
    category_freq = state["recent_categories"].count(post["category"])
    repetition_delta = (category_freq / WINDOW_SIZE) * (1 + repeat_bias)
    state["repetition_score"] = min(10.0, state["repetition_score"] + repetition_delta * 0.8)
    if category_freq == 1:
        # new category in window — reduce repetition
        state["repetition_score"] = max(SCORE_MIN, state["repetition_score"] - 0.2)
    state["repetition_score"] = max(SCORE_MIN, min(10.0, state["repetition_score"]))

    # --- Diversity score ---
    unique_cats = len(set(state["recent_categories"]))
    diversity_pressure = task_config.get("diversity_pressure", 0.3)
    state["diversity_score"] = max(
        SCORE_MIN,
        min(SCORE_MAX, unique_cats / max(1, len(state["recent_categories"])) - 0.05 * diversity_pressure)
    )

    return state


def _simulated_watch_time(post: dict) -> int:
    """
    Simulate how many seconds a user watches this post.
    Higher engagement = more likely to watch longer.
    """
    base = int(post["engagement_score"] * 1.5)
    return max(3, min(30, base))
