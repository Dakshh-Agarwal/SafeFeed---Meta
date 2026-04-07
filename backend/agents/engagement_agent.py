"""
engagement_agent.py

Baseline agent that always picks the post with the highest engagement score.
Deterministic, simple, and used as the control in comparisons.
"""

from env.content_pool import get_all_posts


class EngagementAgent:
    """
    Greedy engagement-maximising baseline agent.
    Ignores risk, repetition, and diversity entirely.
    """

    def select_action(self, state: dict, content_pool: list) -> int:
        """
        Choose the post with the highest engagement_score.

        Args:
            state:        Current session state (unused by this agent).
            content_pool: List of candidate post dicts.

        Returns:
            post ID (int) of the selected post.
        """
        if not content_pool:
            return get_all_posts()[0]["id"]

        best_post = max(content_pool, key=lambda p: p["engagement_score"])
        return best_post["id"]
