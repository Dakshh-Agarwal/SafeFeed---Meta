import os
import json
from typing import Dict, Any, List

from openai import OpenAI

from backend.env.safefeed_env import SafeFeedEnv
from backend.agents.engagement_agent import EngagementAgent
from backend.agents.safety_agent import SafetyAgent


# =========================================================
# REQUIRED ENV VARIABLES (as per checklist)
# =========================================================

# Allowed defaults
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

# No default for token
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional for docker image workflows
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")


# =========================================================
# OPTIONAL OpenAI-compatible client
# (only used if you later plug LLM explainability)
# =========================================================

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else "EMPTY_KEY_FOR_LOCAL_DEV"
)


# =========================================================
# CORE HELPERS
# =========================================================

def get_tasks() -> List[Dict[str, Any]]:
    """
    Return all available benchmark tasks.
    """
    env = SafeFeedEnv()
    return env.get_tasks()


def get_agent(agent_type: str):
    """
    Return the correct agent instance.
    """
    if agent_type == "engagement":
        return EngagementAgent()
    return SafetyAgent()


def run_single_task(task_id: int = 0, agent_type: str = "safety", steps: int = 20) -> Dict[str, Any]:
    """
    Run one task with one agent and return structured results.
    """
    env = SafeFeedEnv(max_steps=steps)
    state = env.reset(task_id=task_id)
    agent = get_agent(agent_type)

    task_name = env.task_config["name"]

    print(f"START: task={task_name} | agent={agent_type} | max_steps={steps}")

    done = False
    step_count = 0

    while not done:
        action = agent.select_action(env.state, env.content_pool)
        new_state, reward, done, info = env.step(action)

        step_count += 1

        post = info.get("selected_post", {})
        post_id = post.get("id", "NA")
        category = post.get("category", "NA")

        print(
            f"STEP: task={task_name} | step={step_count} | "
            f"post_id={post_id} | category={category} | reward={reward:.4f}"
        )

    grade = env.grade()

    print(
        f"END: task={task_name} | agent={agent_type} | "
        f"score={grade['score']:.4f}"
    )

    return {
        "task_id": task_id,
        "task_name": task_name,
        "agent_type": agent_type,
        "trajectory": env.get_trajectory(),
        "grade": grade
    }


def run_all_tasks(agent_type: str = "safety", steps: int = 20) -> List[Dict[str, Any]]:
    """
    Run all tasks for a given agent.
    """
    tasks = get_tasks()
    results = []

    for task in tasks:
        result = run_single_task(
            task_id=task["id"],
            agent_type=agent_type,
            steps=steps
        )
        results.append(result)

    return results


def compare_agents(steps: int = 20) -> Dict[str, Any]:
    """
    Compare engagement and safety agents across all tasks.
    """
    tasks = get_tasks()
    comparison = []

    for task in tasks:
        task_id = task["id"]

        engagement_result = run_single_task(
            task_id=task_id,
            agent_type="engagement",
            steps=steps
        )

        safety_result = run_single_task(
            task_id=task_id,
            agent_type="safety",
            steps=steps
        )

        comparison.append({
            "task": task,
            "engagement_agent": {
                "score": engagement_result["grade"]["score"],
                "metrics": engagement_result["grade"]["metrics"]
            },
            "safety_agent": {
                "score": safety_result["grade"]["score"],
                "metrics": safety_result["grade"]["metrics"]
            }
        })

    return {"tasks": comparison}


# =========================================================
# ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    print("START: SafeFeed inference validation run")

    tasks = get_tasks()
    print(f"STEP: total_tasks={len(tasks)}")

    results = run_all_tasks(agent_type="safety", steps=20)

    print("STEP: completed safety-agent run across all tasks")

    for r in results:
        print(
            f"STEP: task={r['task_name']} | score={r['grade']['score']:.4f}"
        )

    print("END: SafeFeed inference completed")
