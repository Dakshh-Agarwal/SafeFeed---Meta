"""
safety_agent.py

Safety-aware agent that balances engagement with risk, repetition, and diversity.
Deterministic, explainable, and uses no external ML dependencies.
"""

from env.content_pool import get_all_posts


# Scoring weights for the safety agent
RISK_WEIGHT        = 1.2
REPETITION_WEIGHT  = 1.0
DIVERSITY_WEIGHT   = 0.8

WINDOW_SIZE = 5   # matches state.py rolling window


class SafetyAgent:
    """
    Safety-aware ranking agent.

    Scores every candidate post as:
        score = engagement - risk_w * risk - rep_w * repetition + div_w * diversity_bonus
    Then picks the highest-scoring post.
    """

    def select_action(self, state: dict, content_pool: list) -> int:
        """
        Choose the best post according to the safety-aware scoring function.

        Args:
            state:        Current session state dict.
            content_pool: List of candidate post dicts.

        Returns:
            post ID (int) of the selected post.
        """
        if not content_pool:
            return get_all_posts()[0]["id"]

        recent_cats   = state.get("recent_categories", [])
        recent_risky  = state.get("recent_risky_count", 0)
        current_spiral = state.get("spiral_risk", 0.0)

        scored = []
        for post in content_pool:
            score = self._score_post(post, recent_cats, recent_risky, current_spiral)
            scored.append((score, post["id"]))

        # Pick the highest scoring post (ties broken by post ID — deterministic)
        scored.sort(key=lambda x: (-x[0], x[1]))
        return scored[0][1]

    def _score_post(
        self,
        post: dict,
        recent_cats: list,
        recent_risky: int,
        current_spiral: float,
    ) -> float:
        """Compute a safety-aware score for a single candidate post."""

        # Normalised engagement (0-1)
        engagement = post["engagement_score"] / 10.0

        # Risk term: amplified by recent risky streak and current spiral level
        base_risk = post["risk_score"] / 10.0
        streak_multiplier = 1.0 + 0.3 * recent_risky
        spiral_multiplier = 1.0 + 0.1 * (current_spiral / 10.0)
        risk_term = base_risk * streak_multiplier * spiral_multiplier

        # Repetition term: penalise frequently repeated categories
        category_freq = recent_cats.count(post["category"]) if recent_cats else 0
        window = max(1, len(recent_cats))
        repetition_term = category_freq / window

        # Diversity bonus: reward posts that introduce a new category
        is_new_category  = post["category"] not in recent_cats
        diversity_bonus  = 1.0 if is_new_category else 0.0

        score = (
            engagement
            - RISK_WEIGHT       * risk_term
            - REPETITION_WEIGHT * repetition_term
            + DIVERSITY_WEIGHT  * diversity_bonus
        )
        return score
