"""
app.py

FastAPI backend for SafeFeed benchmark environment.
Exposes environment, agents, and comparison API.
"""

import sys
import os

# Ensure backend root is on the path so relative imports work
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from env.safefeed_env import SafeFeedEnv
from env.tasks import get_all_tasks
from agents.engagement_agent import EngagementAgent
from agents.safety_agent import SafetyAgent
from utils.helpers import pick_candidate_posts, summarise_trajectory

# ------------------------------------------------------------------ #
# App setup
# ------------------------------------------------------------------ #

app = FastAPI(
    title="SafeFeed API",
    description="OpenEnv-compatible benchmark environment for safe feed ranking agents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared environment instance (stateful; each reset() clears it)
env = SafeFeedEnv(max_steps=20)
engagement_agent = EngagementAgent()
safety_agent = SafetyAgent()


# ------------------------------------------------------------------ #
# Request / Response models
# ------------------------------------------------------------------ #

class ResetRequest(BaseModel):
    task_id: int = 0


class StepRequest(BaseModel):
    action: int = 0  # post ID


class RunAgentRequest(BaseModel):
    agent_type: str = "safety"   # "safety" or "engagement"
    task_id: int = 0
    steps: int = 20


# ------------------------------------------------------------------ #
# Helper
# ------------------------------------------------------------------ #

def _run_agent(agent, task_id: int, steps: int) -> dict:
    """Run a full episode with the given agent and return results."""
    local_env = SafeFeedEnv(max_steps=steps)
    state = local_env.reset(task_id=task_id)

    done = False
    while not done:
        candidates = pick_candidate_posts(local_env.content_pool, n=10)
        action = agent.select_action(state, candidates)
        state, reward, done, info = local_env.step(action)

    trajectory = local_env.get_trajectory()
    grade      = local_env.grade()
    summary    = summarise_trajectory(trajectory)

    return {
        "task":       local_env.task_config,
        "trajectory": trajectory,
        "grade":      grade,
        "summary":    summary,
        "final_state": state,
    }


# ------------------------------------------------------------------ #
# Endpoints
# ------------------------------------------------------------------ #

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "project": "SafeFeed"}


@app.get("/tasks")
def list_tasks():
    """Return all benchmark tasks (OpenEnv validation endpoint)."""
    return {"tasks": get_all_tasks()}


@app.post("/reset")
def reset_env(req: Optional[ResetRequest] = None):
    """
    Reset the shared environment to a fresh episode.
    Returns the initial state and selected task info.
    """
    req = req or ResetRequest()
    
    try:
        state = env.reset(task_id=req.task_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "state": state,
        "task":  env.task_config,
    }


@app.post("/step")
def step_env(req: Optional[StepRequest] = None):
    """
    Advance the shared environment by one step with the given post ID as action.
    """
    req = req or StepRequest()
    
    try:
        new_state, reward, done, info = env.step(req.action)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "state":  new_state,
        "reward": reward,
        "done":   done,
        "info":   info,
    }


@app.post("/run-agent")
def run_agent(req: Optional[RunAgentRequest] = None):
    """
    Run a full episode with either the engagement or safety agent.
    Returns trajectory, grade, and summary.
    """
    req = req or RunAgentRequest()
    
    if req.agent_type not in ("engagement", "safety"):
        raise HTTPException(
            status_code=400,
            detail="agent_type must be 'engagement' or 'safety'",
        )

    agent = safety_agent if req.agent_type == "safety" else engagement_agent

    try:
        result = _run_agent(agent, task_id=req.task_id, steps=req.steps)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "agent_type": req.agent_type,
        **result,
    }


@app.get("/compare")
def compare_agents():
    """
    Run both agents across all 3 tasks and return side-by-side comparison.
    This is the core benchmark comparison endpoint.
    """
    tasks = get_all_tasks()
    results = []

    for task in tasks:
        task_id = task["id"]

        eng_result  = _run_agent(engagement_agent, task_id=task_id, steps=20)
        safe_result = _run_agent(safety_agent,     task_id=task_id, steps=20)

        results.append({
            "task":             task,
            "engagement_agent": {
                "trajectory": eng_result["trajectory"],
                "grade":      eng_result["grade"],
                "summary":    eng_result["summary"],
            },
            "safety_agent": {
                "trajectory": safe_result["trajectory"],
                "grade":      safe_result["grade"],
                "summary":    safe_result["summary"],
            },
        })

    return {"tasks": results}


@app.get("/grade")
def grade_current():
    """Grade the current shared environment's trajectory."""
    trajectory = env.get_trajectory()
    if not trajectory:
        raise HTTPException(status_code=400, detail="No trajectory yet. Call /reset and /step first.")
    return env.grade()
