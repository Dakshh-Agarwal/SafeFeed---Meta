"""
app.py

FastAPI backend for SafeFeed benchmark environment.
Exposes environment, agents, and comparison API.
"""

import sys
import os
import json

# Ensure backend root is on the path so relative imports work
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

from env.safefeed_env import SafeFeedEnv
from env.tasks import get_all_tasks
from agents.engagement_agent import EngagementAgent
from agents.safety_agent import SafetyAgent
from utils.helpers import pick_candidate_posts, summarise_trajectory

# ------------------------------------------------------------------ #
# LLM Proxy Client (uses hackathon-injected env vars)
# ------------------------------------------------------------------ #

def _first_env(*names: str, default: str = "") -> str:
    """Return the first non-empty environment variable value."""
    for name in names:
        value = os.environ.get(name, "")
        if value:
            return value
    return default


MODEL_NAME = _first_env("MODEL_NAME", "OPENAI_MODEL", default="gpt-4.1-mini")
SCORE_MIN = 0.01
SCORE_MAX = 0.99


def _get_client() -> OpenAI:
    """Build an OpenAI client pointing at the hackathon LiteLLM proxy."""
    base = _first_env("API_BASE_URL", "OPENAI_BASE_URL", "OPENAI_API_BASE")
    key = _first_env("API_KEY", "OPENAI_API_KEY", "HF_TOKEN")
    if not base or not key:
        raise RuntimeError(
            "Missing LLM proxy env vars: "
            f"API_BASE_URL/OPENAI_BASE_URL/OPENAI_API_BASE={base!r}, "
            f"API_KEY/OPENAI_API_KEY/HF_TOKEN={'set' if key else 'EMPTY'}"
        )
    return OpenAI(base_url=base, api_key=key)


def _strict_unit_interval(value: float) -> float:
    """Force score into strict open interval (0, 1)."""
    try:
        v = float(value)
    except Exception:
        return 0.5
    return max(SCORE_MIN, min(SCORE_MAX, v))


def _sanitize_grade(grade: dict) -> dict:
    """Ensure all grade score fields are validator-safe."""
    if not isinstance(grade, dict):
        return {
            "score": 0.5,
            "metrics": {"combined_score": 0.5},
        }
    metrics = grade.get("metrics") if isinstance(grade.get("metrics"), dict) else {}
    out = {
        "score": _strict_unit_interval(grade.get("score", 0.5)),
        "metrics": dict(metrics),
    }
    for key, value in list(out["metrics"].items()):
        out["metrics"][key] = _strict_unit_interval(value)
    if "combined_score" not in out["metrics"]:
        out["metrics"]["combined_score"] = out["score"]
    return out


def llm_explain_results(grade: dict, agent_type: str, task_name: str) -> str:
    """Call the LLM proxy to generate a brief explanation of the run results."""
    client = _get_client()
    prompt = (
        f"Briefly explain (2-3 sentences) the performance of a '{agent_type}' "
        f"feed-ranking agent on the '{task_name}' benchmark task.\n"
        f"Score: {grade.get('score', 'N/A')}\n"
        f"Metrics: {json.dumps(grade.get('metrics', {}))}"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a concise AI safety analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM explanation unavailable ({e})"

# ------------------------------------------------------------------ #
# Lifespan: warm-up LLM call on startup
# ------------------------------------------------------------------ #

@asynccontextmanager
async def lifespan(app: FastAPI):
    """On startup, make a warmup LLM call through the proxy."""
    print("[STARTUP] FastAPI lifespan: making warmup LLM proxy call...", flush=True)
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Say OK."}],
            max_tokens=5,
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip()
        print(f"[STARTUP] ✅ Warmup LLM response: {result}", flush=True)
    except Exception as e:
        print(f"[STARTUP] ⚠️ Warmup LLM call failed: {e}", flush=True)
    yield


# ------------------------------------------------------------------ #
# App setup
# ------------------------------------------------------------------ #

app = FastAPI(
    title="SafeFeed API",
    description="OpenEnv-compatible benchmark environment for safe feed ranking agents.",
    version="1.0.0",
    lifespan=lifespan,
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
    grade      = _sanitize_grade(local_env.grade())
    summary    = summarise_trajectory(trajectory)

    # Call LLM proxy for AI-powered insight
    task_name = local_env.task_config.get("name", "unknown")
    ai_insight = llm_explain_results(grade, "agent", task_name)

    return {
        "task":       local_env.task_config,
        "trajectory": trajectory,
        "grade":      grade,
        "summary":    summary,
        "ai_insight": ai_insight,
        "final_state": state,
    }


# ------------------------------------------------------------------ #
# Endpoints
# ------------------------------------------------------------------ #

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "project": "SafeFeed"}


@app.get("/llm-test")
def llm_test():
    """Make a quick LLM proxy call for diagnostic purposes."""
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Say OK."}],
            max_tokens=5,
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip()
        return {"status": "ok", "llm_response": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


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
    return _sanitize_grade(env.grade())
