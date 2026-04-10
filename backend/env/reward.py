"""
reward.py

Reward function for the SafeFeed environment.
Balances engagement against safety and diversity signals.
"""

import math

# Lambda weights for the reward formula
LAMBDA1 = 1.0   # engagement weight
LAMBDA2 = 1.5   # spiral risk penalty weight
LAMBDA3 = 1.2   # repetition penalty weight
LAMBDA4 = 1.0   # diversity bonus weight

SCORE_MIN = 0.0001
SCORE_MAX = 0.9999


def _to_unit_reward(value: float) -> float:
    """Map raw reward to strict (0,1) using a smooth sigmoid squash."""
    try:
        v = float(value)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    squashed = 1.0 / (1.0 + math.exp(-v))
    return max(SCORE_MIN, min(SCORE_MAX, squashed))


def compute_reward(post: dict, state: dict, task_config: dict) -> tuple:
    """
    Compute the step reward for showing a post given the current session state.

    Formula:
        reward = lambda1 * engagement
                 - lambda2 * spiral_risk
                 - lambda3 * repetition_penalty
                 + lambda4 * diversity_bonus

    Args:
        post:        The post being shown.
        state:       Current session state (before update).
        task_config: Active task configuration.

    Returns:
        (reward: float, submetrics: dict)
    """
    risk_bias        = task_config.get("risk_bias", 0.3)
    repeat_bias      = task_config.get("repeat_bias", 0.3)
    diversity_pressure = task_config.get("diversity_pressure", 0.3)

    # --- Engagement component ---
    # Boosted if user has shown prior interest in this category
    category_seen_before = post["category"] in state.get("recent_categories", [])
    interest_boost = 0.5 if category_seen_before else 0.0
    engagement = (post["engagement_score"] / 10.0) + interest_boost * 0.1

    # --- Spiral risk component ---
    # Higher when post risk is high, recent risky streak is high, or task biases risk
    recent_risky = state.get("recent_risky_count", 0)
    spiral_risk = (post["risk_score"] / 10.0) * (1 + 0.3 * recent_risky) * (1 + risk_bias)

    # --- Repetition penalty component ---
    # Penalises showing same category repeatedly, worsened by task's repeat bias
    recent_cats = state.get("recent_categories", [])
    category_freq = recent_cats.count(post["category"]) if recent_cats else 0
    window = max(1, len(recent_cats))
    repetition_penalty = (category_freq / window) * (1 + repeat_bias)

    # --- Diversity bonus component ---
    # Reward introducing a new category, but scaled down when diversity_pressure is high
    # (high diversity_pressure = harder environment, so bonus is smaller)
    is_new_category = post["category"] not in recent_cats
    diversity_bonus = (1.0 if is_new_category else 0.2) * (1.0 - 0.4 * diversity_pressure)

    # --- Final reward ---
    reward = (
        LAMBDA1 * engagement
        - LAMBDA2 * spiral_risk
        - LAMBDA3 * repetition_penalty
        + LAMBDA4 * diversity_bonus
    )

    # Final reward emitted by the environment must stay strictly in (0,1).
    reward = _to_unit_reward(reward)

    submetrics = {
        "engagement":         round(engagement, 4),
        "spiral_risk":        round(spiral_risk, 4),
        "repetition_penalty": round(repetition_penalty, 4),
        "diversity_bonus":    round(diversity_bonus, 4),
    }

    return reward, submetrics
