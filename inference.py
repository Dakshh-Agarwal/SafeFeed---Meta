import random
from backend.env.safefeed_env import SafeFeedEnv
from backend.agents.engagement_agent import EngagementAgent
from backend.agents.safety_agent import SafetyAgent


def get_tasks():
    """
    Return all available tasks for the benchmark.
    """
    env = SafeFeedEnv()
    return env.get_tasks()


def run_task(task_id=0, agent_type="safety", steps=20):
    """
    Run a specific agent on a given task and return trajectory + grade.
    """
    env = SafeFeedEnv(max_steps=steps)
    env.reset(task_id=task_id)

    if agent_type == "engagement":
        agent = EngagementAgent()
    else:
        agent = SafetyAgent()

    done = False
    while not done:
        action = agent.select_action(env.state, env.content_pool)
        _, _, done, _ = env.step(action)

    result = env.grade()
    return {
        "task_id": task_id,
        "agent_type": agent_type,
        "trajectory": env.logger.get_trajectory(),
        "grade": result
    }


def validate_all_tasks(agent_type="safety", steps=20):
    """
    Run the selected agent across all tasks.
    Useful for quick validation before submission.
    """
    env = SafeFeedEnv()
    tasks = env.get_tasks()

    results = []

    for task in tasks:
        result = run_task(task_id=task["id"], agent_type=agent_type, steps=steps)
        results.append({
            "task": task,
            "score": result["grade"]["score"],
            "metrics": result["grade"]["metrics"]
        })

    return results


if __name__ == "__main__":
    print("=== SafeFeed Inference Check ===")
    tasks = get_tasks()
    print(f"Found {len(tasks)} tasks")

    results = validate_all_tasks(agent_type="safety", steps=20)
    for r in results:
        print(f"{r['task']['name']} -> Score: {r['score']:.4f}")
