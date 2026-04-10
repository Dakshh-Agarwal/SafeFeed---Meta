"""
safefeed_env.py

Core OpenEnv-style environment class for SafeFeed.
Implements get_tasks / reset / step / grade interface.
"""

from env.content_pool import get_all_posts, get_posts_by_id
from env.state import init_state, update_state
from env.tasks import get_all_tasks, get_task_by_id
from env.reward import compute_reward
from env.logger import TrajectoryLogger
from env.grader import grade_trajectory, safe_score
from utils.explain import explain_recommendation


class SafeFeedEnv:
    """
    OpenEnv-compatible benchmark environment for feed ranking evaluation.

    Usage:
        env = SafeFeedEnv(max_steps=20)
        for task in env.get_tasks():
            state = env.reset(task_id=task["id"])
            done = False
            while not done:
                action = agent.select_action(state, env.content_pool)
                state, reward, done, info = env.step(action)
            grade = env.grade()
    """

    def __init__(self, max_steps: int = 20):
        self.max_steps = max_steps
        self.content_pool = get_all_posts()
        self._post_index = {p["id"]: p for p in self.content_pool}

        # These will be set on reset()
        self.task_config: dict = {}
        self.state: dict = {}
        self.logger = TrajectoryLogger()
        self._done: bool = False

    @staticmethod
    def _unit_score(value: float, scale10: bool = False) -> float:
        """Convert numeric score-like signals to strict (0,1)."""
        try:
            v = float(value)
        except Exception:
            return 0.5
        if scale10:
            v = v / 10.0
        return safe_score(v)

    def _public_state(self) -> dict:
        """Return a validator-safe state snapshot without mutating internal state."""
        out = dict(self.state)
        if "repetition_score" in out:
            out["repetition_score"] = self._unit_score(out.get("repetition_score", 0.5), scale10=True)
        if "diversity_score" in out:
            out["diversity_score"] = self._unit_score(out.get("diversity_score", 0.5))
        if "spiral_risk" in out:
            out["spiral_risk"] = self._unit_score(out.get("spiral_risk", 0.5), scale10=True)
        return out

    # ------------------------------------------------------------------ #
    # PUBLIC API
    # ------------------------------------------------------------------ #

    def get_tasks(self) -> list:
        """Return all benchmark tasks (OpenEnv compliance)."""
        return get_all_tasks()

    def reset(self, task_id: int = 0) -> dict:
        """
        Start a fresh episode for the given task.

        Args:
            task_id: Which task to load (0, 1, or 2).

        Returns:
            Initial state dict.
        """
        self.task_config = get_task_by_id(task_id)
        self.state = init_state()
        self.logger.reset()
        self._done = False
        return self._public_state()

    def step(self, action: int) -> tuple:
        """
        Advance the environment by one step.

        Args:
            action: Post ID to show to the simulated user.

        Returns:
            (new_state, reward, done, info)
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() before stepping again.")

        # Retrieve post
        post = self._post_index.get(action)
        if post is None:
            # Fall back to first post if invalid ID; prevents crashes
            post = self.content_pool[0]

        # Compute reward BEFORE state update (uses pre-update context)
        reward, reward_breakdown = compute_reward(post, self.state, self.task_config)

        # Update session state
        self.state = update_state(self.state, post, self.task_config)

        # Build explanation
        explanation = explain_recommendation(self.state, post, agent_type="env")

        info_post = dict(post)
        info_post["engagement_score"] = self._unit_score(post.get("engagement_score", 0.5), scale10=True)
        info_post["risk_score"] = self._unit_score(post.get("risk_score", 0.5), scale10=True)

        # Log this step
        self.logger.log_step({
            "step":             self.state["step_count"],
            "post_id":          info_post["id"],
            "title":            info_post["title"],
            "category":         info_post["category"],
            "engagement_score": info_post["engagement_score"],
            "risk_score":       info_post["risk_score"],
            "reward":           reward,
            "watch_time":       self.state["watch_time"],
            "spiral_risk":      self.state["spiral_risk"],
            "repetition_score": self.state["repetition_score"],
            "diversity_score":  self.state["diversity_score"],
            "reward_breakdown": reward_breakdown,
        })

        # Done condition
        self._done = self.state["step_count"] >= self.max_steps

        public_reward_breakdown = {}
        for key, value in reward_breakdown.items():
            if isinstance(value, (int, float)):
                public_reward_breakdown[key] = self._unit_score(value, scale10=(float(value) > 1.0))
            else:
                public_reward_breakdown[key] = value

        info = {
            "post":             info_post,
            "explanation":      explanation,
            "reward_breakdown": public_reward_breakdown,
            "task":             self.task_config,
        }

        return self._public_state(), reward, self._done, info

    def grade(self, trajectory: list = None, task_id: int = None) -> dict:
        """
        Grade the episode trajectory.

        Args:
            trajectory: Optional external trajectory list. Uses internal log if None.
            task_id:    Optional task id override. Uses current task if None.

        Returns:
            Grade dict with 'score' and 'metrics'.
        """
        traj = trajectory if trajectory is not None else self.logger.get_trajectory()
        cfg  = get_task_by_id(task_id) if task_id is not None else self.task_config
        result = grade_trajectory(traj, cfg)

        # Final guard at env boundary to guarantee validator-safe range.
        result["score"] = safe_score(result.get("score", 0.5))
        metrics = result.get("metrics")
        if isinstance(metrics, dict):
            for key, value in list(metrics.items()):
                metrics[key] = safe_score(value)

        return result

    def get_trajectory(self) -> list:
        """Return the full logged trajectory for the current episode."""
        return self.logger.get_trajectory()
