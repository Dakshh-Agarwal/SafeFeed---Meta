"""
helpers.py

Miscellaneous utility functions for SafeFeed backend.
"""

import random

SCORE_MIN = 0.0001
SCORE_MAX = 0.9999


def pick_candidate_posts(content_pool: list, n: int = 10, seed: int = None) -> list:
    """
    Return a random sample of n posts from the content pool.
    If n >= len(pool), return the full pool.

    Args:
        content_pool: Full list of post dicts.
        n:            Number of candidates to sample.
        seed:         Optional random seed for reproducibility.

    Returns:
        List of post dicts.
    """
    if seed is not None:
        random.seed(seed)
    if n >= len(content_pool):
        return list(content_pool)
    return random.sample(content_pool, n)


def normalise(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    """
    Linearly normalise a value from [lo, hi] to [0, 1].
    Clamps to [0, 1] if out of range.
    """
    if hi == lo:
        return 0.5
    return max(SCORE_MIN, min(SCORE_MAX, (value - lo) / (hi - lo)))


def summarise_trajectory(trajectory: list) -> dict:
    """
    Compute summary statistics over a full trajectory.

    Returns:
        Dict of averages and totals.
    """
    if not trajectory:
        return {}

    n = len(trajectory)
    avg_engagement = sum(s["engagement_score"] for s in trajectory) / n
    avg_risk = sum(s["risk_score"] for s in trajectory) / n
    avg_reward = sum(s["reward"] for s in trajectory) / n

    avg_engagement = avg_engagement / 10.0 if avg_engagement > 1.0 else avg_engagement
    avg_risk = avg_risk / 10.0 if avg_risk > 1.0 else avg_risk
    avg_reward = avg_reward / 10.0 if avg_reward > 1.0 else avg_reward

    final_spiral = trajectory[-1]["spiral_risk"]
    final_spiral = final_spiral / 10.0 if final_spiral > 1.0 else final_spiral

    return {
        "steps":               n,
        "total_watch_time":    trajectory[-1]["watch_time"] if trajectory else 0,
        "avg_engagement":      max(SCORE_MIN, min(SCORE_MAX, avg_engagement)),
        "avg_risk":            max(SCORE_MIN, min(SCORE_MAX, avg_risk)),
        "avg_reward":          max(SCORE_MIN, min(SCORE_MAX, avg_reward)),
        "final_spiral_risk":   max(SCORE_MIN, min(SCORE_MAX, final_spiral)),
        "final_repetition":    max(SCORE_MIN, min(SCORE_MAX, trajectory[-1]["repetition_score"])),
        "final_diversity":     max(SCORE_MIN, min(SCORE_MAX, trajectory[-1]["diversity_score"])),
        "categories_seen":     list({s["category"] for s in trajectory}),
        "risky_posts_shown":   sum(1 for s in trajectory if s["risk_score"] >= 0.5),
    }
