"""
logger.py

Trajectory logger for the SafeFeed environment.
Records every step for debugging, charting, and grading.
"""

SCORE_MIN = 0.0001
SCORE_MAX = 0.9999


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
        def _avoid_unit_edges(value: float) -> float:
            """
            Keep values away from exact 0.0/1.0 while preserving scale.
            This avoids strict validator edge-case rejections.
            """
            try:
                v = float(value)
            except Exception:
                return 0.5
            if v > 1.0:
                # Score-like signals are natively 0-10 in parts of the env.
                v = v / 10.0
            return max(SCORE_MIN, min(SCORE_MAX, v))

        # Ensure all required fields have defaults if caller missed any
        record = {
            "step":              data.get("step", len(self._trajectory) + 1),
            "post_id":           data.get("post_id"),
            "title":             data.get("title", ""),
            "category":          data.get("category", ""),
            "engagement_score":  _avoid_unit_edges(float(data.get("engagement_score", 0.0)) / 10.0),
            "risk_score":        _avoid_unit_edges(data.get("risk_score", 0.0)),
            "reward":            _avoid_unit_edges(data.get("reward", 0.5)),
            "watch_time":        data.get("watch_time", 0),
            "spiral_risk":       _avoid_unit_edges(data.get("spiral_risk", 0.5)),
            "repetition_score":  _avoid_unit_edges(data.get("repetition_score", 0.0)),
            "diversity_score":   _avoid_unit_edges(data.get("diversity_score", 0.9999)),
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
