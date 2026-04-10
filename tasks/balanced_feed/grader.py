"""
Grader for the balanced_feed task (easy difficulty).

OpenEnv-compatible grader function. The platform calls grade()
after an episode completes and expects a float score in (0, 1).
"""

import sys
import os
import math

# Ensure backend modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

SCORE_MIN = 0.01
SCORE_MAX = 0.99
TASK_ID = 0


def _clamp(v):
    """Force a numeric value into strict (0, 1) open interval."""
    try:
        v = float(v)
    except Exception:
        return 0.5
    if not math.isfinite(v):
        return 0.5
    if v <= 0.0:
        return SCORE_MIN
    if v >= 1.0:
        return SCORE_MAX
    return round(max(SCORE_MIN, min(SCORE_MAX, v)), 6)


def grade(*args, **kwargs):
    """
    OpenEnv grader entry point.

    Accepts flexible arguments — the platform may pass:
      - grade(state)
      - grade(trajectory)
      - grade(state, trajectory)
      - grade(submission)  (dict with various fields)

    Returns a float score strictly in (0, 1).
    """
    try:
        from backend.env.grader import grade_trajectory, safe_score
        from backend.env.tasks import get_task_by_id

        task_config = get_task_by_id(TASK_ID)

        # Try to extract trajectory from various argument formats
        trajectory = _extract_trajectory(args, kwargs)

        if trajectory and len(trajectory) > 0:
            result = grade_trajectory(trajectory, task_config)
            return _clamp(result.get("score", 0.5))

        # If no trajectory available, run the environment ourselves
        return _run_and_grade(task_config)

    except Exception as e:
        print(f"[GRADER] balanced_feed grade error: {e}", file=sys.stderr)
        return 0.5


def _extract_trajectory(args, kwargs):
    """Try to extract a trajectory list from various argument formats."""
    # Check kwargs
    for key in ("trajectory", "history", "steps", "episodes"):
        if key in kwargs and isinstance(kwargs[key], list):
            return kwargs[key]

    # Check if first arg is a list (trajectory)
    if args and isinstance(args[0], list):
        return args[0]

    # Check if first arg is a dict with trajectory inside
    if args and isinstance(args[0], dict):
        obj = args[0]
        for key in ("trajectory", "history", "steps"):
            if key in obj and isinstance(obj[key], list):
                return obj[key]

    return None


def _run_and_grade(task_config):
    """Fallback: run the environment and grade the result."""
    try:
        from backend.env.safefeed_env import SafeFeedEnv
        from backend.agents.safety_agent import SafetyAgent

        env = SafeFeedEnv(max_steps=20)
        env.reset(task_id=TASK_ID)
        agent = SafetyAgent()

        done = False
        while not done:
            action = agent.select_action(env.state, env.content_pool)
            _, _, done, _ = env.step(action)

        result = env.grade()
        return _clamp(result.get("score", 0.5))
    except Exception as e:
        print(f"[GRADER] balanced_feed fallback error: {e}", file=sys.stderr)
        return 0.5
