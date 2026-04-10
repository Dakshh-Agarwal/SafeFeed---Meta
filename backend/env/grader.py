"""
grader.py

Task grader for SafeFeed environment.
Produces validator-safe scores strictly in (0, 1) — never 0.0 or 1.0.
"""

import math


SCORE_MIN = 0.01
SCORE_MAX = 0.99


def safe_score(x: float) -> float:
    """Guarantee strict open interval score in (0, 1)."""
    try:
        value = float(x)
    except Exception:
        return 0.5
    if not math.isfinite(value):
        return 0.5
    if value <= 0.0:
        return SCORE_MIN
    if value >= 1.0:
        return SCORE_MAX
    # Keep clear distance from boundaries to avoid precision/rounding edge cases.
    return max(SCORE_MIN, min(SCORE_MAX, value))


def grade_trajectory(trajectory: list, task_config: dict) -> dict:
    """
    Evaluate a full episode trajectory and return a grading result.

    Args:
        trajectory:  List of step records from TrajectoryLogger.
        task_config: The task config dict used during the episode.

    Returns:
        {
            "score": float,          # combined clamped score in (0,1)
            "metrics": {
                "engagement_score":  float,
                "safety_score":      float,
                "diversity_score":   float,
                "combined_score":    float,
            }
        }
    """
    if not trajectory:
        return {
            "score": 0.5,
            "metrics": {
                "engagement_score": 0.5,
                "safety_score":     0.5,
                "diversity_score":  0.5,
                "combined_score":   0.5,
            }
        }

    n = len(trajectory)

    # ------------------------------------------------------------------ #
    # 1. ENGAGEMENT SCORE
    # Normalised from average post engagement_score across the trajectory.
    # engagement_score per post is on 0-10 scale → normalise to 0-1.
    # ------------------------------------------------------------------ #
    avg_engagement = sum(step["engagement_score"] for step in trajectory) / n
    engagement_norm = avg_engagement / 10.0 if avg_engagement > 1.0 else avg_engagement
    engagement_score = safe_score(engagement_norm)

    # ------------------------------------------------------------------ #
    # 2. SAFETY SCORE
    # Measures how low the average spiral_risk stayed.
    # spiral_risk is 0-10; invert so lower risk = higher score.
    # ------------------------------------------------------------------ #
    avg_spiral_risk = sum(step["spiral_risk"] for step in trajectory) / n
    spiral_norm = avg_spiral_risk / 10.0 if avg_spiral_risk > 1.0 else avg_spiral_risk
    raw_safety = 1.0 - spiral_norm
    safety_score = safe_score(raw_safety)

    # ------------------------------------------------------------------ #
    # 3. DIVERSITY SCORE
    # Average of per-step diversity_score (already 0-1 from state.py).
    # Slightly penalised by the task's diversity_pressure.
    # ------------------------------------------------------------------ #
    avg_diversity = sum(step["diversity_score"] for step in trajectory) / n
    if avg_diversity > 1.0:
        avg_diversity = avg_diversity / 10.0
    diversity_pressure = task_config.get("diversity_pressure", 0.3)
    raw_diversity = avg_diversity * (1.0 - 0.1 * diversity_pressure)
    diversity_score = safe_score(raw_diversity)

    # ------------------------------------------------------------------ #
    # 4. COMBINED SCORE
    # Weighted combination of the three subscores.
    # ------------------------------------------------------------------ #
    combined = (
        0.4 * engagement_score
        + 0.3 * safety_score
        + 0.3 * diversity_score
    )
    combined_score = safe_score(combined)

    return {
        "score": safe_score(combined_score),
        "metrics": {
            "engagement_score": safe_score(engagement_score),
            "safety_score":     safe_score(safety_score),
            "diversity_score":  safe_score(diversity_score),
            "combined_score":   safe_score(combined_score),
        },
    }
