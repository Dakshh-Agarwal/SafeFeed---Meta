"""
grader.py

Task grader for SafeFeed environment.
Produces validator-safe scores strictly in (0, 1) — never 0.0 or 1.0.
"""


def _clamp(value: float) -> float:
    """Clamp score to (0.01, 0.99) — never exactly 0 or 1."""
    return max(0.01, min(0.99, value))


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
    engagement_score = _clamp(avg_engagement / 10.0)

    # ------------------------------------------------------------------ #
    # 2. SAFETY SCORE
    # Measures how low the average spiral_risk stayed.
    # spiral_risk is 0-10; invert so lower risk = higher score.
    # ------------------------------------------------------------------ #
    avg_spiral_risk = sum(step["spiral_risk"] for step in trajectory) / n
    raw_safety = 1.0 - (avg_spiral_risk / 10.0)
    safety_score = _clamp(raw_safety)

    # ------------------------------------------------------------------ #
    # 3. DIVERSITY SCORE
    # Average of per-step diversity_score (already 0-1 from state.py).
    # Slightly penalised by the task's diversity_pressure.
    # ------------------------------------------------------------------ #
    avg_diversity = sum(step["diversity_score"] for step in trajectory) / n
    diversity_pressure = task_config.get("diversity_pressure", 0.3)
    raw_diversity = avg_diversity * (1.0 - 0.1 * diversity_pressure)
    diversity_score = _clamp(raw_diversity)

    # ------------------------------------------------------------------ #
    # 4. COMBINED SCORE
    # Weighted combination of the three subscores.
    # ------------------------------------------------------------------ #
    combined = (
        0.4 * engagement_score
        + 0.3 * safety_score
        + 0.3 * diversity_score
    )
    combined_score = _clamp(combined)

    return {
        "score": combined_score,
        "metrics": {
            "engagement_score": round(engagement_score, 4),
            "safety_score":     round(safety_score, 4),
            "diversity_score":  round(diversity_score, 4),
            "combined_score":   round(combined_score, 4),
        },
    }
