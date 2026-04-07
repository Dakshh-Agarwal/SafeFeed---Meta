"""
helpers.py

Miscellaneous utility functions for SafeFeed backend.
"""

import random


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
        return 0.0
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def summarise_trajectory(trajectory: list) -> dict:
    """
    Compute summary statistics over a full trajectory.

    Returns:
        Dict of averages and totals.
    """
    if not trajectory:
        return {}

    n = len(trajectory)
    return {
        "steps":               n,
        "total_watch_time":    trajectory[-1]["watch_time"] if trajectory else 0,
        "avg_engagement":      round(sum(s["engagement_score"] for s in trajectory) / n, 3),
        "avg_risk":            round(sum(s["risk_score"]       for s in trajectory) / n, 3),
        "avg_reward":          round(sum(s["reward"]           for s in trajectory) / n, 3),
        "final_spiral_risk":   round(trajectory[-1]["spiral_risk"],    3),
        "final_repetition":    round(trajectory[-1]["repetition_score"], 3),
        "final_diversity":     round(trajectory[-1]["diversity_score"],  3),
        "categories_seen":     list({s["category"] for s in trajectory}),
        "risky_posts_shown":   sum(1 for s in trajectory if s["risk_score"] >= 5.0),
    }
