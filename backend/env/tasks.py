"""
tasks.py

Defines the 3 benchmark tasks for OpenEnv evaluation.
Each task represents a different feed scenario with distinct risk/repetition profiles.
"""

TASKS = [
    {
        "id": 0,
        "name": "balanced_feed",
        "description": "A balanced session with moderate-risk and diverse content.",
        "risk_bias": 0.3,
        "repeat_bias": 0.3,
        "diversity_pressure": 0.3,
    },
    {
        "id": 1,
        "name": "high_risk_feed",
        "description": "A session with higher availability of risky content and spiral pressure.",
        "risk_bias": 0.7,
        "repeat_bias": 0.4,
        "diversity_pressure": 0.5,
    },
    {
        "id": 2,
        "name": "low_diversity_feed",
        "description": "A session where repetitive content loops are more likely.",
        "risk_bias": 0.4,
        "repeat_bias": 0.8,
        "diversity_pressure": 0.8,
    },
]


def get_all_tasks() -> list:
    """Return all benchmark tasks."""
    return TASKS


def get_task_by_id(task_id: int) -> dict:
    """Return a task config by its ID. Raises ValueError if not found."""
    for task in TASKS:
        if task["id"] == task_id:
            return task
    raise ValueError(f"Task ID {task_id} not found. Valid IDs: {[t['id'] for t in TASKS]}")
