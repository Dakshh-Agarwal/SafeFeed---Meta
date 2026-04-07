"""
inference.py

Required by Scaler OpenEnv Phase 1 automated checks.
This script demonstrates how to instantiate the environment and run the safety-aware agent.
"""

from backend.env.safefeed_env import SafeFeedEnv
from backend.agents.safety_agent import SafetyAgent

def run_inference():
    """
    Runs the safety agent against all tasks and prints the final grades.
    """
    env = SafeFeedEnv(max_steps=20)
    agent = SafetyAgent()
    
    results = {}
    for task in env.get_tasks():
        state = env.reset(task_id=task["id"])
        done = False
        
        while not done:
            action = agent.select_action(state, env.content_pool)
            state, reward, done, info = env.step(action)
            
        grade = env.grade()
        results[task["name"]] = grade
        
        print(f"[{task['name']}] Combined Score: {grade['score']:.4f}")
        print(f"  Engagement: {grade['metrics']['engagement_score']:.4f}")
        print(f"  Safety:     {grade['metrics']['safety_score']:.4f}")
        print(f"  Diversity:  {grade['metrics']['diversity_score']:.4f}")
        print("-" * 40)
        
    return results

if __name__ == "__main__":
    run_inference()
