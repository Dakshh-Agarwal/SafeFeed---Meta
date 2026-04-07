"""
logger.py

Trajectory logger for the SafeFeed environment.
Records every step for debugging, charting, and grading.
"""


class TrajectoryLogger:
    """Logs each step of a feed session as a structured dict."""

    def __init__(self):
        self._trajectory: list = []

    def log_step(self, data: dict) -> None:
        """
        Append a step record to the trajectory.

        Expected keys in data:
            step, post_id, title, category,
            engagement_score, risk_score, reward,
            watch_time, spiral_risk, repetition_score, diversity_score
        """
        # Ensure all required fields have defaults if caller missed any
        record = {
            "step":              data.get("step", len(self._trajectory) + 1),
            "post_id":           data.get("post_id"),
            "title":             data.get("title", ""),
            "category":          data.get("category", ""),
            "engagement_score":  round(float(data.get("engagement_score", 0.0)), 4),
            "risk_score":        round(float(data.get("risk_score", 0.0)), 4),
            "reward":            round(float(data.get("reward", 0.0)), 4),
            "watch_time":        data.get("watch_time", 0),
            "spiral_risk":       round(float(data.get("spiral_risk", 0.0)), 4),
            "repetition_score":  round(float(data.get("repetition_score", 0.0)), 4),
            "diversity_score":   round(float(data.get("diversity_score", 1.0)), 4),
            # Optional: reward submetrics from reward.py
            "reward_breakdown":  data.get("reward_breakdown", {}),
        }
        self._trajectory.append(record)

    def get_trajectory(self) -> list:
        """Return the full trajectory list."""
        return list(self._trajectory)

    def reset(self) -> None:
        """Clear the trajectory for a fresh episode."""
        self._trajectory = []

    def __len__(self) -> int:
        return len(self._trajectory)
